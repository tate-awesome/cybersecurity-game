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

    def is_running(self) -> bool:
        '''Whether the process is active (started and not stopped). Subclasses override.'''
        return False

    def is_starting(self) -> bool:
        '''
        Whether the process is between being asked to start and reaching its
        steady running state - e.g. resolving addresses, or waiting for a
        first response. Takes priority over is_running when a card decides how
        to show it (a yellow indicator), so it only has to be True during that
        window. Default False: a process with no startup delay never reports it.
        '''
        return False

    def is_stopping(self) -> bool:
        '''
        Whether the process is between being asked to stop and being fully
        stopped. Like is_starting, it only needs to be True during that
        window. Default False.
        '''
        return False

    def stop(self):
        pass
