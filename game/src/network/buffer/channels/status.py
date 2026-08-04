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
        new_statuses = []
        
        with self.lock:
            # Scan backward from the newest items (right side of deque)
            for meta_status in reversed(self.buffer):
                if meta_status.number > self.last_displayed:
                    new_statuses.append(meta_status)
                else:
                    # Because it's ordered, everything before this is older. Stop scanning!
                    break
                    
        if new_statuses:
            # Reverse back to normal chronological order (oldest to newest)
            new_statuses.reverse()
            self.last_displayed = new_statuses[-1].number

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
    