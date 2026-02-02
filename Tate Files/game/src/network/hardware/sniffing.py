from scapy.all import TCP, AsyncSniffer
from . import modbus as mb
from . import buffer

sniffer = None

class handlers:

    def show(pkt):
        pkt.show()

    def show_modbus(pkt):
        if pkt.haslayer(TCP) and (pkt[TCP].sport == 502 or pkt[TCP].dport == 502):
            if mb.is_coord(pkt) or mb.is_commands(pkt):
                pkt.show()

    def print_scannable(pkt):
        if pkt.haslayer(TCP) and (pkt[TCP].sport == 502 or pkt[TCP].dport == 502):
            if mb.is_coord(pkt) or mb.is_commands(pkt):
                mb.print_scannable(pkt, convert=True)

    def put_modbus_in_buffer(pkt):
        if pkt.haslayer(TCP) and (pkt[TCP].sport == 502 or pkt[TCP].dport == 502):
            if mb.is_coord(pkt) or mb.is_commands(pkt):
                buffer.put(pkt, False)


class Sniffer:
    def __init__(self):
        self.sniffer = None
    

    def start(self, packet_handler):
        if self.sniffer is not None:
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