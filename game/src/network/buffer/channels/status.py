'''
The map buffer makes status messages available to the status console.
It receives data from the worker's Put method

'''
from collections import deque
from threading import Lock
import time
from ..meta_status import MetaStatus

class StatusBuffer:
    def __init__(self, max_size: int = 5000):
        self.max_size = max_size
        self.buffer = deque(maxlen=self.max_size)
        self.lock = Lock()
        self.number = 1
        self.last_displayed = 0

    def put(self, source: str, purpose: str):
        current_time = time.time()
        meta_status = MetaStatus(source, purpose, current_time, self.number)
        with self.lock:
            self.buffer.append(meta_status)
        self.number += 1

    def get_new_statuses(self) -> list[MetaStatus]:
        with self.lock:
            snapshot = list(self.buffer)

        new_statuses = [
            meta_status for meta_status in snapshot
            if meta_status.number > self.last_displayed
        ]

        if new_statuses:
            self.last_displayed = max(
                status.number for status in new_statuses
            )

        return new_statuses

    def get_new_lines(self) -> str:
        statuses = self.get_new_statuses()
        if len(statuses) == 0:
            return ""
        status_strings = [str(status) for status in statuses]
        text_block = "\n\n".join(status_strings) + "\n\n"
        return text_block

    def reset_cursor(self):
        with self.lock:
            self.last_displayed = 0
    