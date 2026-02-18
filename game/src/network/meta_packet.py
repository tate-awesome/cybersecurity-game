from scapy.all import Packet, IP, TCP, UDP, ARP, DNS, DNSQR, Raw

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

    def wireshark_line(self, dump = False) -> list[str]:
        pkt = self.pkt

        number = str(self.number)
        time = f"{self.time:.6f}"
        length = str(len(pkt))
        direction = self.direction

        src = "?"
        dst = "?"
        proto = "?"
        info = ""

        # ---------------- ARP ----------------
        if pkt.haslayer(ARP):
            arp = pkt[ARP]
            proto = "ARP"
            src = arp.psrc
            dst = arp.pdst

            if arp.op == 1:
                info = f"Who has {arp.pdst}? Tell {arp.psrc}"
            elif arp.op == 2:
                info = f"{arp.psrc} is at {arp.hwsrc}"
            else:
                info = "ARP"

        # ---------------- IP ----------------
        elif pkt.haslayer(IP):
            ip = pkt[IP]
            src = ip.src
            dst = ip.dst

            # ---------- TCP ----------
            if pkt.haslayer(TCP):
                tcp = pkt[TCP]
                proto = "TCP"

                flags = tcp.flags

                flag_str = ""
                if flags.S:
                    flag_str += "SYN,"
                if flags.A:
                    flag_str += "ACK,"
                if flags.F:
                    flag_str += "FIN,"
                if flags.R:
                    flag_str += "RST,"
                if flags.P:
                    flag_str += "PSH,"

                flag_str = flag_str.rstrip(",")

                # Duplicate ACK heuristic
                if flags.A and not flags.S and tcp.len == 0:
                    flag_str += " (Dup ACK?)"

                info = f"{tcp.sport} → {tcp.dport} [{flag_str}] Seq={tcp.seq} Ack={tcp.ack}"

                # -------- HTTP detection --------
                if pkt.haslayer(Raw):
                    payload = pkt[Raw].load
                    try:
                        text = payload.decode(errors="ignore")

                        # HTTP Request
                        if text.startswith(("GET ", "POST ", "PUT ", "DELETE ", "HEAD ")):
                            first_line = text.split("\r\n")[0]
                            proto = "HTTP"
                            info = first_line

                        # HTTP Response
                        elif text.startswith("HTTP/"):
                            first_line = text.split("\r\n")[0]
                            proto = "HTTP"
                            info = first_line

                    except:
                        pass

            # ---------- UDP ----------
            elif pkt.haslayer(UDP):
                udp = pkt[UDP]
                proto = "UDP"
                info = f"{udp.sport} → {udp.dport}"

                # -------- DNS detection --------
                if pkt.haslayer(DNS):
                    dns = pkt[DNS]
                    proto = "DNS"

                    if dns.qr == 0 and dns.qd is not None:
                        query = dns.qd.qname.decode(errors="ignore")
                        info = f"Standard query: {query}"

                    elif dns.qr == 1:
                        info = "DNS response"

            # ---------- ICMP ----------
            elif ip.proto == 1:
                proto = "ICMP"
                info = "ICMP"

            else:
                proto = f"IP({ip.proto})"
                info = pkt.summary()

        else:
            proto = pkt.__class__.__name__
            info = pkt.summary()

        out = [
            number,
            time,
            src,
            dst,
            proto,
            length,
            direction,
            info
        ]

        if dump:
            print("\t".join(out))
        else:
            return out

    
