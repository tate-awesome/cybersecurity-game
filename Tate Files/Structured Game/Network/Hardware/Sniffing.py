from scapy.all import TCP, AsyncSniffer
import Modbus as mb

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
    

def start(packet_handler):
    print("Starting sniffer...")
    global sniffer
    sniffer = AsyncSniffer(
        filter="tcp port 502",
        prn=packet_handler,
        store=False
    )

    sniffer.start()
    print("Started sniffer")


def stop():
    global sniffer
    if not sniffer == None:
        sniffer.stop()
        sniffer = None
        print("Stopped sniffer")
    else:
        print("Sniffer is not running")