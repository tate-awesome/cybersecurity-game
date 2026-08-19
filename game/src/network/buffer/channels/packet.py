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
        self.number = 1
        self.last_displayed = 0
        self.first_packet_time = None

        self.rate_history = deque(maxlen=300)
        self.selected_number = None

    def put(self, mpkt: MetaPacket):
        with self.lock:
            mpkt.set("number", self.number)
            self.number += 1
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

    def get_new_packets(self, filter_func, max_return: int = 1000) -> list:
        new_packets = []
        with self.lock:
            # Scan backward starting from the newest packets (right side of deque)
            for meta_packet in reversed(self.buffer):
                if meta_packet.get("number") > self.last_displayed:
                    # Apply the lambda filter function directly
                    if filter_func(meta_packet):
                        new_packets.append(meta_packet)
                        
                        # Stop scanning early if we hit our maximum GUI display threshold
                        if len(new_packets) >= max_return:
                            break
                else:
                    # Sequential order guarantee: Everything before this is already displayed.
                    break

        if new_packets:
            # Restore chronological order (oldest to newest)
            new_packets.reverse()
            # Update the cursor to track the absolute highest packet ID processed
            self.last_displayed = max(p.get("number") for p in new_packets)

        return new_packets

    def reset_packet_cursor(self):
        with self.lock:
            self.last_displayed = 0

    def reset_time(self):
        self.first_packet_time = None

    def get_first_packet_time(self, pkt: Packet) -> float:
        if self.first_packet_time is None:
            self.first_packet_time = pkt.time
        return self.first_packet_time