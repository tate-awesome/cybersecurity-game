from scapy.all import Packet, IP, TCP, UDP, ARP, DNS, DNSQR, Raw, Ether, conf
from scapy.arch import get_if_addr, get_if_hwaddr
from scapy.contrib import modbus
import json, socket, uuid
from scapy.contrib.modbus import *


class MetaPacket:
    def __init__(  self, pkt: Packet, first_packet_time: float, absolute_number: int, hack_number: int,
    hack: str, src="None", purpose: str = "None"):

        # Essential info
        self.pkt = pkt
        self.time = pkt.time - first_packet_time
        self.time_word = f"{self.time:.4f}"
        self.absolute_number = absolute_number
        self.hack_number = hack_number
        self.length = str(len(self.pkt))

        # External info
        self.hack = hack
        self.src = src
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
        elif self.src == "recv":
            self.direction = "in"
            self.direction_verbose = "Received"
        elif self.src == "send":
            self.direction = "out"
            self.direction_verbose = "Sent"
        else:
            self.direction = "other"   # 👈 important for promiscuous mode
            self.direction_verbose = "Observed"

        # Modbus info
        self.variables, self.values, self.command, self.is_modbus = self.get_modbus_command()

        # Summary fields
        self.summary = self.get_info()
        if self.hack == "nfq":
            if self.src == "send":
                self.observer = "postrouting nfq"
            elif self.src == "recv":
                self.observer = "prerouting nfq"
            else:
                self.observer = self.hack
        else:
            self.observer = self.hack
        self.mac_word = f"{self.mac_src} → {self.mac_dst}" if pkt.haslayer(Ether) else "-"
        self.ip_word = f"{self.ip_src} → {self.ip_dst}" if pkt.haslayer(IP) else "-"
        self.transaction_word = f"{self.direction_verbose}\n{self.mac_word}\n{self.ip_word}"
        # modbus_associations = []
        # for i, variable in enumerate(self.variables):

        #     modbus_associations.append(f"{str(self.variables[i])} = {self.values[i]:.2f}")
        # if len(modbus_associations) == 0:
        #     self.modbus_word = "-"
        # else:
        #     self.modbus_word = " , ".join(modbus_associations)
        self.set_modbus_word()

    def get_column_value(self, column_name: str):
        match column_name:
            case "time":
                return self.time_word
            case "number":
                return self.absolute_number
            case "length":
                return self.length
            case "observer":
                return self.observer
            case "transaction_word":
                return self.direction_verbose
            case "transaction_ip":
                return self.ip_word
            case "transaction_mac":
                return self.mac_word
            case "layers":
                return self.proto_str
            case "purpose":
                return self.purpose
            case "summary":
                return self.summary
            case "modbus":
                return self.modbus_word
            case _:
                return "-"

    def matches(self, requirement: str):
        '''
        Returns whether the given requirement is true given a primary key string found in presets.json - "packet_filter_columns".
        '''
        
        match requirement:
            case "nmap":
                return self.hack == "nmap"
            case "arp":
                return self.hack == "arp"
            case "dos":
                return self.hack == "dos"
            case "sniff":
                return self.hack == "sniff"
            case "nfq":
                return self.hack == "nfq"
            case "pcap":
                return self.hack == "pcap"

            case "TCP":
                return "TCP" in self.protocols
            case "ARP":
                return "ARP" in self.protocols
            case "UDP":
                return "UDP" in self.protocols
            case "DNS":
                return "DNS" in self.protocols
            case "MODBUSADU":
                return "MODBUSADU" in self.protocols
            case "WRITE SINGLE REGISTER":
                return "WRITE SINGLE REGISTER" in self.protocols
            case "READ HOLDING REGISTERS RESPONSE":
                return "READ HOLDING REGISTERS RESPONSE" in self.protocols

            case "out":
                return self.direction == "out"
            case "in":
                return self.direction == "in"
            case "other":
                return self.direction == "other"
            case _:
                return True

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
    
    def get_modbus_command(self) -> tuple[list[str], list[float], str]:
            # return variables, values, command string
            # Return command
            # 2 of 18 instructions implemented lol
            p = self.pkt
            variables = []
            values = []
            command = ""
            m = None
            is_modbus = False
            
            if m := p.getlayer(ModbusPDU03ReadHoldingRegistersRequest):
                for i in range(m.startAddr, m.startAddr + m.quantity):
                    variables.append(f"register_{i}")
            elif m := p.getlayer(ModbusPDU03ReadHoldingRegistersResponse):
                for value in p.payload.registerVal:
                    values.append(value)

            elif m := p.getlayer(ModbusPDU06WriteSingleRegisterRequest):
                variables.append(f"register_{p.payload.registerAddr}")
                values.append(p.payload.registerValue)
            elif m := p.getlayer(ModbusPDU06WriteSingleRegisterResponse):
                variables.append(f"register_{p.payload.registerAddr}")
                values.append(p.payload.registerValue)

            if m is not None:
                command = m.name
                is_modbus = True

            return variables, values, command, is_modbus

    def set_modbus_word(self) -> None:
        if self.is_modbus:
            values_strings = []
            for num in self.values:
                values_strings.append(f"{num:.2f}")
            self.modbus_word = f"{", ".join(self.variables)} = {", ".join(values_strings)}"
        else:
            self.modbus_word = "-"

    def old_extract_modbus(self, source: str, pkt: Packet) -> tuple[list[str], list[float]]:
            '''
            Returns the modbus variables and values in the packet.
            If there's no modbus, return empty lists
            '''
            # Extract variables
            if pkt.haslayer("Read Holding Registers Response"):
                variables = ["speed"]
                mbl = pkt.getlayer(ModbusADUResponse)
                values = [self.convert["speed"](mbl.payload.registerVal[0])]
    
                if len(mbl.payload.registerVal) > 1:
                    variables.append("rudder")
                    values.append(self.convert["rudder"](mbl.payload.registerVal[1]))
    
            elif pkt.haslayer("Write Single Register"):
                mbl = pkt.getlayer(ModbusADURequest)
                if mbl.payload.registerAddr == 10: # X address
                    var = "x"
                elif mbl.payload.registerAddr == 11: # Y address
                    var = "y"
                else: # Theta address
                    var = "theta"
    
                z = mbl.payload.registerValue
    
                variables = [var]
                values = [self.convert[var](z)]
            
            else:
                variables = []
                values = []
    
            return variables, values