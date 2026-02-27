from scapy.all import Packet, IP, TCP, UDP, ARP, DNS, DNSQR, Raw, Ether
from scapy.arch import get_if_addr, get_if_hwaddr
from scapy.contrib import modbus
import json

class MetaPacket:
    def __init__(  self, pkt: Packet, current_time: float, number: int,
    hack: str, purpose: str = "None",
    variables: list[str] = [], values: list[str] = []):

        # Essential info
        self.pkt = pkt
        self.time = current_time
        self.number = number

        # Hack showcase info
        self.hack = hack
        self.purpose = purpose
        direction = "none"
        if pkt.haslayer(Ether):
            mac = get_if_hwaddr("wlp0s20f3")
            if pkt[Ether].src == mac:
                direction = "out"
            elif pkt[Ether].dst == mac:
                direction = "in"
        elif pkt.haslayer(IP):
            ip = get_if_addr("wlp0s20f3")
            if pkt[IP].src == ip:
                direction = "out"
            elif pkt[IP].dst == ip:
                direction = "in"
        self.direction = direction

        # Modbus info
        self.variables = variables
        self.values = values

    def __str__(self) -> str:
        s=" / "
        c=","
        if self.direction == "in":
            dir = "incoming"
        elif self.direction == "out":
            dir = "outgoing"
        else:
            dir = "unknown"

        hwsrc = ""
        hwdst = ""
        if self.pkt.haslayer(Ether):
            hwsrc = str(self.pkt[Ether].src)
            hwdst = str(self.pkt[Ether].dst)
        ipsrc = ""
        ipdst = ""
        if self.pkt.haslayer(IP):
            ipsrc = str(self.pkt[IP].src)
            ipdst = str(self.pkt[IP].dst)

        layers = s.join(layer.__name__ for layer in self.pkt.layers())
        length = str(len(self.pkt))

        lines = []
        lines.append(f"[ {layers} ]")
        lines.append(f"   | no: {self.number}\ttime: {self.time:.3f}\tlen: {length}\tfrom: {self.hack}")
        lines.append(f"   | hwsrc: {hwsrc}\thwdst: {hwdst}")
        lines.append(f"   | ipsrc: {ipsrc}\tipdst: {ipdst}")
        lines.append(f"   | dir: {dir}\tpurpose: {self.purpose}")
        lines.append(f"   | {self.get_info()}")
        lines.append("")
        return "\n".join(lines)


    def get_info(self) -> str:
        pkt = self.pkt
        info = ""
        proto = ""

        # ---------------- ARP ----------------
        if pkt.haslayer(ARP):
            arp = pkt[ARP]
            proto = "ARP"

            if arp.op == 1:
                info = f"Who has {arp.pdst}? Tell {arp.psrc}"
            elif arp.op == 2:
                info = f"{arp.psrc} is at {arp.hwsrc}"
            else:
                info = "ARP"

        # ---------------- IP ----------------
        elif pkt.haslayer(IP):
            ip = pkt[IP]

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
                if flags.A and not flags.S and len(tcp) == 0:
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
                
                # -------- ModBus detection --------
                if pkt.haslayer(modbus.ModbusADUResponse) or pkt.haslayer(modbus.ModbusADURequest):
                    func_meanings = {
                        1: "Read Coils",
                        2: "Read Discrete Inputs",
                        3: "Read Holding Registers",
                        4: "Read Input Registers",
                        5: "Write Single Coil",
                        6: "Write Single Register",
                        15: "Write Multiple Coils",
                        16: "Write Multiple Registers"
                    }
                    register_meanings = {
                        3: "Speed Feedback",    # 12-bit count Bytes = X*5/4095
                        4: "Rudder Feedback",   # 12-bit count Bytes = X*30/4095
                        10: "X Position",       # Bytes = meters*100
                        11: "Y Position",       # meters*100
                        12: "Theta (Heading)"   # milli-radians
                    }
                    if pkt.haslayer(modbus.ModbusADUResponse):
                        mbl = pkt.getlayer(modbus.ModbusADUResponse)
                        re = "Response"
                    elif pkt.haslayer(modbus.ModbusADURequest):
                        mbl = pkt.getlayer(modbus.ModbusADURequest)
                        re = "Request"
                    func_code = mbl.funcCode
                    name = mbl.getlayer(1).name
                    action = ""
                    if pkt.haslayer("Write Single Register") or pkt.haslayer("Read Holding Registers Response"):
                        action = f"{str(self.variables)} is {str(self.values)}"
                    proto = "Modbus"
                    info = f"({func_code}) {name} - {action}"
                    

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
            info = pkt.summary()

        return f"{proto}: {info}"

    
