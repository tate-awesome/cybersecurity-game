

class PacketBuffer:
    def __init__(self, max_size=5000):
        self.max_size = max_size
            # Buffers for console use
        self.console_buffers = {}
        '''
        For the Console:
            "packets":
                "numbers": {
                    "absolute": n,
                    "this_hack": n
                }
                "buffer": deque[MetaPacket],
                "lock": Lock()
            "status":
                "number": n,
                "buffer": deque[MetaStatus],
                "lock": Lock()

        '''
        self.console_buffers["packets"] = {
                "numbers": {},
                "last_displayed": 0,
                "buffer": deque(maxlen=self.max_size),
                "lock": Lock()
            }
        for key in ["absolute", "nmap", "arp", "sniff", "dos", "mitm", "pcap"]:
            self.console_buffers["packets"]["numbers"][key] = 1
        self.console_buffers["status"] = {
            "number": 1,
            "last_displayed": 0,
            "buffer": deque(maxlen=self.max_size),
            "lock": Lock()
        }

    
    def get_new_packets(self, filter: callable) -> list[MetaPacket]:
        with self.console_buffers["packets"]["lock"]:
            snapshot = list(self.console_buffers["packets"]["buffer"])

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
    
