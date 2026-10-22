from collections import deque
from multiprocessing import Lock
import time
from ..meta_packet import MetaPacket
from scapy.all import Packet

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ....app_core import Context

class PacketBuffer:
    def __init__(self, context: "Context", max_size=5000):
        self.max_size = max_size
        self.buffer = deque(maxlen=self.max_size)
        self.context = context
        self.lock = Lock()
        self.window_type_pps = deque(maxlen=self.max_size)

        self.rate_history = deque(maxlen=300)
        self.selected_number = None
        self.reset()

    def reset(self):
        with self.lock:
            self.first_packet_time = None
            self.window_type_pps.clear()
            self.buffer.clear()
            self.number = 1

    def put(self, mpkt: MetaPacket):
        with self.lock:
            mpkt.set("number", self.number)
            self.number += 1
            previous = self.buffer[-1].get("time") if self.buffer else mpkt.get("time")
            mpkt.set("time_delta", f"{mpkt.get('time') - previous:.4f}")
            self.buffer.append(mpkt)

            bucket = float(int(mpkt.get("time")))
            if self.rate_history and self.rate_history[-1][0] == bucket:
                t, count = self.rate_history[-1]
                self.rate_history[-1] = (t, count + 1)
            else:
                self.rate_history.append((bucket, 1))

    def get_rate_history(self) -> list:
        with self.lock:
            return list(self.rate_history)

    def get_window_type_pps(self):
        # 1. Update
        with self.lock:
            reverse = reversed(self.buffer)
        now = self.get_relative_time()
        if now is None:
            return self.window_type_pps
        cutoff = now - 1.0
        count = 0
        for mpkt in reverse:
            if mpkt.get("time") > cutoff:
                count += 1
            else:
                break
        # 2. Put and return
        self.window_type_pps.append((now, count))
        return self.window_type_pps

    def select(self, number: int):
        self.selected_number = number

    def get_selected(self) -> MetaPacket | None:
        if self.selected_number is None:
            return None
        with self.lock:
            for mpkt in self.buffer:
                if mpkt.get("number") == self.selected_number:
                    return mpkt
        return None

    def read(self, filter_func, after: int, up_to: int | None = None, max_return: int = 1000) -> tuple[list, int]:
        '''
        The packets numbered after `after` (and up to `up_to`, if given) that
        pass filter_func, oldest first - the newest max_return of them - and
        the highest number it looked at, for the reader's next `after`. Each
        reader (a packet console) keeps its own place, so one console's
        filter or pause never moves another's.
        '''
        found = []
        looked_to = after
        with self.lock:
            # Newest first: everything at or before `after` has been read already
            for meta_packet in reversed(self.buffer):
                number = meta_packet.get("number")
                if number <= after:
                    break
                if up_to is not None and number > up_to:
                    continue
                looked_to = max(looked_to, number)
                if filter_func(meta_packet):
                    found.append(meta_packet)
                    if len(found) >= max_return:
                        break
        found.reverse()
        return found, looked_to

    def latest_number(self) -> int:
        '''The number of the newest packet so far - 0 with none.'''
        with self.lock:
            return self.number - 1

    def get_first_packet_time(self, pkt: Packet) -> float:
        if self.first_packet_time is None:
            self.first_packet_time = pkt.time
        return self.first_packet_time

    def note_first_time(self, abs_time: float) -> float:
        '''Like get_first_packet_time, but for a bare timestamp carried in a helper payload (see Buffer.put_payload).'''
        if self.first_packet_time is None:
            self.first_packet_time = abs_time
        return self.first_packet_time

    def get_relative_time(self):
        if self.first_packet_time:
            return time.time() - self.first_packet_time