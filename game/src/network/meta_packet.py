from scapy.all import Packet, IP, TCP, UDP, ARP, DNS, DNSQR, Raw, Ether, conf
from scapy.arch import get_if_addr, get_if_hwaddr
from scapy.contrib import modbus
import json, socket, uuid

class MetaStatus:
    def __init__(self, hack: str, status: str, time: float, number: int):
        self.hack = hack
        self.status = status
        self.time = time
        self.number = number
    
    def get_line(self, max_length=80) -> str:
        from datetime import datetime

        # --- format time ---
        dt = datetime.fromtimestamp(self.time)
        time_str = dt.strftime("%S.%f")[:-3]  # HH:MM:SS.SSS

        # --- prefix ---
        prefix = f"{self.number} {time_str} [{self.hack}] "
        return f"{prefix}{self.status}"

class MetaPacket:
    def __init__(  self, pkt: Packet, first_packet_time: float, absolute_number: int, hack_number: int,
    hack: str, purpose: str = "None",
    variables: list[str] = [], values: list[str] = []):

        # Essential info
        self.pkt = pkt
        self.time = pkt.time - first_packet_time
        self.time_word = f"{self.time:.4f}"
        self.absolute_number = absolute_number
        self.hack_number = hack_number
        self.length = str(len(self.pkt))

        # External info
        self.hack = hack
        self.purpose = purpose

        # MAC
        self.mac_src = pkt[Ether].src if pkt.haslayer(Ether) else "-"
        self.mac_dst = pkt[Ether].dst if pkt.haslayer(Ether) else "-"

        # IP
        self.ip_src = pkt[IP].src if pkt.haslayer(IP) else "-"
        self.ip_dst = pkt[IP].dst if pkt.haslayer(IP) else "-"

        # Protocols
        layers = []
        current = pkt
        while current:
            layers.append(current.name.upper())
            current = current.payload if current.payload else None
            if current == b'':
                break
        self.protocols = layers
        self.proto_str = "/".join(self.protocols)

        # Direction
        def get_local_ip():
            try:
                return socket.gethostbyname(socket.gethostname())
            except:
                return None
            
        def get_local_mac():
            mac = uuid.getnode()
            return ':'.join(f'{(mac >> ele) & 0xff:02x}' for ele in range(40, -8, -8))

        LOCAL_IP = get_local_ip()
        LOCAL_MAC = get_local_mac()
        BROADCAST_MAC = "ff:ff:ff:ff:ff:ff"

        if self.ip_src == LOCAL_IP or self.mac_src.lower() == LOCAL_MAC.lower():
            self.direction = "out"
            self.direction_verbose = "Sent"

        elif (
            self.ip_dst == LOCAL_IP
            or self.mac_dst.lower() == LOCAL_MAC.lower()
            or self.mac_dst.lower() == BROADCAST_MAC
        ):
            self.direction = "in"
            self.direction_verbose = "Received"

        else:
            self.direction = "other"   # 👈 important for promiscuous mode
            self.direction_verbose = "Observed"

        # Modbus info
        self.variables = variables
        self.values = values

        # Summary fields
        self.summary = self.get_info()
        self.hack_word = f"{self.hack} {self.hack_number}".strip()
        self.mac_word = f"{self.mac_src} → {self.mac_dst}" if pkt.haslayer(Ether) else "-"
        self.ip_word = f"{self.ip_src} → {self.ip_dst}" if pkt.haslayer(IP) else "-"
        self.transaction_word = f"{self.direction_verbose}\n{self.mac_word}\n{self.ip_word}"
        self.modbus_word = f"{self.variables} = {self.values}"

    def __str__(self) -> str:
        lines = []
        lines.append(f"[ {self.proto_str} ]")
        lines.append(f"   | no: {self.absolute_number}\ttime: {self.time:.3f}\tlen: {self.length}\tfrom: {self.hack}\t{self.hack_number}")
        lines.append(f"   | hwsrc: {self.mac_src}\thwdst: {self.mac_dst}")
        lines.append(f"   | ipsrc: {self.ip_src}\tipdst: {self.ip_dst}")
        lines.append(f"   | dir: {self.direction_verbose}\tpurpose: {self.purpose}")
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

    
