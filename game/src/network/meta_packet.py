from scapy.all import Packet

class MetaPacket:
    def __init__(self, pkt: Packet, current_time: float, number: int, direction: str = "in", variable: str = "None", value: str = "None"):
        self.pkt = pkt
        self.time = current_time
        self.number = number
        self.variable = variable
        self.value = value
        self.direction = direction

    def show(self):
        self.pkt.show()

    def wireshark_line(self, dump=False):
        pkt = self.pkt

        # Defaults
        src = "?"
        dst = "?"
        proto = "?"
        length = str(len(pkt))
        info = pkt.summary()

        # IP layer
        if pkt.haslayer("IP"):
            ip = pkt["IP"]
            src = ip.src
            dst = ip.dst
            proto = ip.proto

        # TCP layer
        if pkt.haslayer("TCP"):
            tcp = pkt["TCP"]
            proto = "TCP"
            info = f"{tcp.sport} → {tcp.dport} Seq={tcp.seq}"

        # UDP layer
        elif pkt.haslayer("UDP"):
            udp = pkt["UDP"]
            proto = "UDP"
            info = f"{udp.sport} → {udp.dport}"

        # ICMP layer
        elif pkt.haslayer("ICMP"):
            proto = "ICMP"

        out = [
            str(self.number),
            f"{self.time:.6f}",
            src,
            dst,
            str(proto),
            length,
            info
        ]

        if dump:
            print("\t".join(out))
        else:
            return out

    
