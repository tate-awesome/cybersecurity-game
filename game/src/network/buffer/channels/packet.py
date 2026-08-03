

from collections import deque
from multiprocessing import Lock
from ...meta_packet import MetaPacket

class PacketBuffer:
    def __init__(self, context, max_size=5000):
        self.max_size = max_size
        self.context = context

        self.last_displayed = 0
        self.buffer = deque(maxlen=self.max_size)
        self.lock = Lock()

        self.numbers = {}
        for key in ["absolute", "nmap", "arp", "sniff", "dos", "mitm", "pcap"]:
            self.numbers[key] = 1

    
    def get_new_packets(self, filter: callable) -> list[MetaPacket]:
        with self.lock:
            snapshot = list(self.buffer)

        new_packets = [
            meta_packet for meta_packet in snapshot
            if meta_packet.absolute_number > self.console_buffers["packets"]["last_displayed"]
            and filter(meta_packet)
        ]

        if new_packets:
            self.console_buffers["packets"]["last_displayed"] = max(
                packet.absolute_number for packet in new_packets
            )

        return new_packets

    def reset_packet_cursor(self):
        with self.console_buffers["packets"]["lock"]:
            self.console_buffers["packets"]["last_displayed"] = 0
    
