'''
The map buffer makes status messages available to the status console.
It receives data from the worker's Put method

'''
import deque
from threading import Lock

class StatusBuffer:
    def __init__(self, max_size: int = 5000):
        self.max_size = max_size

        # Buffers for the status console
        self.console_buffers = {}
        '''
        Console elements:
        "status":
            "buffer": deque of MetaStatus objects,
            "lock": Lock(),
            "number": int,
            "last_displayed": int
        '''
        self.console_buffers["status"] = {
            "buffer": deque(maxlen=self.max_size),
            "lock": Lock(),
            "number": 0,
            "last_displayed": 0
        }
    def put(self, source: str, purpose: str):
        ...
    def get_new_statuses(self) -> list[MetaStatus]:
        with self.console_buffers["status"]["lock"]:
            snapshot = list(self.console_buffers["status"]["buffer"])

        new_statuses = [
            meta_status for meta_status in snapshot
            if meta_status.number > self.console_buffers["status"]["last_displayed"]
        ]

        if new_statuses:
            self.console_buffers["status"]["last_displayed"] = max(
                status.number for status in new_statuses
            )

        return new_statuses

    def reset_status_cursor(self):
        with self.console_buffers["status"]["lock"]:
            self.console_buffers["status"]["last_displayed"] = 0
    