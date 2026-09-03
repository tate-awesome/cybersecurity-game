from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..app_core import Context
    from .buffer import Buffer

class Process:
    '''
    Base class for everything in network/hardware and network/saved: a
    thread or other long-running action that a widget starts and needs to
    be able to stop, including on the widget's behalf during cleanup (see
    ProcessManager.abort_all). Subclasses that run a persistent thread
    should override stop(); one-shot actions with nothing to interrupt can
    rely on this no-op default.
    '''
    def __init__(self, buffer: "Buffer", context: "Context"):
        self.buffer = buffer
        self.context = context

    def stop(self):
        pass
