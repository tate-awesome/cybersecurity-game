'''
The status buffer makes status messages available to the status toasts
(see widgets/frame_widgets/toasts.py).
It receives data from the worker's Put method - a plain line of text, or a
Notice (an error or a report - see notice.py).

'''
from collections import deque
from threading import Lock
import time
from ..meta_status import MetaStatus
from ..notice import Notice

class StatusBuffer:
    def __init__(self, max_size: int = 5000):
        self.max_size = max_size
        self.buffer = deque(maxlen=self.max_size)
        self.lock = Lock()
        self.number = 1

    def put(self, source: str, purpose: "str | Notice"):
        current_time = time.time()
        with self.lock:
            self.buffer.append(MetaStatus(source, purpose, current_time, self.number))
            self.number += 1

    def statuses_after(self, number: int) -> list[MetaStatus]:
        '''
        Every status numbered past number, oldest first - each reader keeps
        its own place (the last number it read), so reading takes nothing
        from anyone else.
        '''
        new_statuses = []
        with self.lock:
            # Scan backward from the newest items (right side of deque)
            for meta_status in reversed(self.buffer):
                if meta_status.number <= number:
                    # Because it's ordered, everything before this is older. Stop scanning!
                    break
                new_statuses.append(meta_status)
        new_statuses.reverse()
        return new_statuses

    def clear(self):
        '''Forgets every status so far - new ones keep numbering on from here.'''
        with self.lock:
            self.buffer.clear()
