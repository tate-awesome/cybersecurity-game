
from typing import TYPE_CHECKING
from .process import Process
if TYPE_CHECKING:
    from ..app_core import Context

PROCESS_TAGS = [
    "stop_last",
]

class ProcessManager:
    '''
    Container for processes (threads/long-running actions) that must
    survive a page refresh. Widgets are recreated on every refresh, so each
    one retrieves its process back out of here by name (get_process)
    instead of losing track of it - creating and registering it (add_process)
    only on first visit. Does not own the Buffer; that belongs to the
    context.
    '''
    def __init__(self, context: "Context"):
        self.context = context
        self.processes: dict[str, Process] = {}
        self.process_tags: dict[str, list[str]] = {}

    def add_process(self, name: str, process: Process, tags: list[str] | None = None):
        if name in self.processes:
            raise ValueError(f"Process with name '{name}' already exists.")
        self.processes[name] = process
        if tags:
            self.process_tags[name] = tags

    def get_process(self, name: str) -> Process | None:
        return self.processes.get(name)

    def _safe_stop(self, stop_func):
        '''
        Calls a single abort_all() step in isolation, so one failing step
        (e.g. a hardware module that's already in a bad state) can't prevent
        the rest of cleanup from running.
        '''
        try:
            stop_func()
        except Exception as e:
            print(f"Error during {stop_func.__qualname__}: {e}")

    def abort_all(self):
        stop_last = []
        for key, process in self.processes.items():
            if key in self.process_tags and "stop_last" in self.process_tags[key]:
                stop_last.append(process)
            else:
                self._safe_stop(process.stop)
        for process in stop_last:
            self._safe_stop(process.stop)