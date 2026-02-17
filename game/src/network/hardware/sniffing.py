from scapy.all import TCP, AsyncSniffer
from .. import modbus_util as mb
from ..packet_buffer import PacketBuffer


class Sniffer:
    def __init__(self, buffer: PacketBuffer):
        self.sniffer = None
        self.buffer = buffer

    
    def is_running(self):
        return self.sniffer is not None
    

    def start(self, packet_handler):
        if self.is_running():
            print("Sniffer is already running")
            return

        print("Starting sniffer...")
        self.sniffer = AsyncSniffer(
            filter="tcp port 502",
            prn=packet_handler,
            store=False
        )
        self.sniffer.start()
        print("Started sniffer")


    def stop(self):
        if self.sniffer is not None:
            self.sniffer.stop()
            self.sniffer = None
            print("Stopped sniffer")
        else:
            print("Sniffer is not running")

    def show(self, pkt):
        pkt.show()

    def show_modbus(self, pkt):
        if pkt.haslayer(TCP) and (pkt[TCP].sport == 502 or pkt[TCP].dport == 502):
            if mb.is_coord(pkt) or mb.is_commands(pkt):
                pkt.show()

    def print_scannable(self, pkt):
        if pkt.haslayer(TCP) and (pkt[TCP].sport == 502 or pkt[TCP].dport == 502):
            if mb.is_coord(pkt) or mb.is_commands(pkt):
                mb.print_scannable(pkt, convert=True)

    def put_modbus_in_buffer(self, pkt):
        if pkt.haslayer(TCP) and (pkt[TCP].sport == 502 or pkt[TCP].dport == 502):
            if mb.is_coord(pkt) or mb.is_commands(pkt):
                self.buffer.put(pkt, "in")