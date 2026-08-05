from collections import deque
from multiprocessing import Lock
import time
from ..meta_packet import MetaPacket
from scapy.all import Packet

class PacketBuffer:
    def __init__(self, max_size=5000):
        self.max_size = max_size
        self.buffer = deque(maxlen=self.max_size)
        self.lock = Lock()
        self.numbers = {}
        for key in ["absolute", "nmap", "arp", "sniff", "dos", "mitm", "pcap"]:
            self.numbers[key] = 1
        self.last_displayed = 0
        self.first_packet_time = None

    def put(self, mpkt: MetaPacket):
        with self.lock:
            self.buffer.append(mpkt)
        self.numbers[mpkt.hack] += 1
        self.numbers["absolute"] += 1

    def get_new_packets(self, filter_func, max_return: int = 1000) -> list:
        new_packets = []
        
        with self.lock:
            # Scan backward starting from the newest packets (right side of deque)
            for meta_packet in reversed(self.buffer):
                if meta_packet.absolute_number > self.last_displayed:
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
            self.last_displayed = max(p.absolute_number for p in new_packets)

        return new_packets

    def reset_packet_cursor(self):
        with self.lock:
            self.last_displayed = 0

    def get_first_packet_time(self, pkt: Packet) -> float:
        if self.first_packet_time is None:
            self.first_packet_time = pkt.time
        return self.first_packet_time
    
