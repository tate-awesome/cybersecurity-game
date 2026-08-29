from scapy.all import Packet, IP, TCP, UDP, ARP, DNS, DNSQR, Raw, Ether, conf
from scapy.arch import get_if_addr, get_if_hwaddr
from scapy.contrib import modbus
import json, socket, uuid
from scapy.contrib.modbus import *
from typing import Any

class MetaPacket:

    KEYS = {
        "pkt",              # scapy packet
        "time",             # pkt.time float
        "number",           # buffer number
        "hack",             # hack source str: arp, sniff, dos, nfq, nmap
        "purpose",          # packet purpose str, from put()
        "mac_src",          # pkt.mac_src
        "mac_dst",          # pkt.mac_dst
        "ip_src",           # pkt.ip_src
        "ip_dst",           # pkt.ip_dst
        "direction",        # in or out
        "layers",           # pkt.layers list
        "protocol",         # pkt.layers[-1] str
        "observer",         # hack observer: any hack, prerouting nfq, postrouting nfq
        "layers_word",      # pkt.layers joined by " / "
        "length",           # len(pkt)
        "time_word",        # pkt.time to 4 decimels
        "summary",          # pkt.summary
        "direction_word",   # "Sent" or "Received"
        "mac_word",         # mac_src -> mac_dst
        "ip_word",          # ip_src -> ip_dst
        "variables",        # list of hreg str
        "values",           # list of ints
        "command",          # modbus layer name - "read holding registers response"
        "command_type",     # "Request" or "Response"
        "is_modbus",        # bool - includes modbus layer
        "is_useful",        # bool - changes register value
        "is_primary",       # bool - is the first request or response of this transaction
        "command_word",     # str - "Write Request" or "Read Response"
        "modbus_word"       # str - "variable list = value list"
    }

    LOCAL_MAC = ':'.join(f'{(uuid.getnode() >> ele) & 0xff:02x}' for ele in range(40, -8, -8)).lower()
    BROADCAST_MAC = "ff:ff:ff:ff:ff:ff"

    def __init__(  self, pkt: Packet, first_packet_time: float, number: int,
    hack: str, purpose: str, dir: str | None):

        self.data = dict()

        time = pkt.time - first_packet_time
        # Given information
        self.set("pkt", pkt)
        self.set("time", time)
        self.set("number", number)
        self.set("hack", hack)
        self.set("purpose", purpose)

        # Addressing information
        self.set("mac_src", pkt[Ether].src if pkt.haslayer(Ether) else "-")
        self.set("mac_dst", pkt[Ether].dst if pkt.haslayer(Ether) else "-")
        self.set("ip_src", pkt[IP].src if pkt.haslayer(IP) else "-")
        self.set("ip_dst", pkt[IP].dst if pkt.haslayer(IP) else "-")

        # Direction information
        if dir == "in":
            direction = "in"
            direction_verbose = "Received"
        elif dir == "out":
            direction = "out"
            direction_verbose = "Sent"
        elif self.get("mac_dst").lower() == self.LOCAL_MAC or self.get("mac_dst").lower() == self.BROADCAST_MAC:
            direction = "in"
            direction_verbose = "Received"
        elif self.get("mac_src").lower() == self.LOCAL_MAC:
            direction = "out"
            direction_verbose = "Sent"
        else:
            direction = "other"
            direction_verbose = "Observed"
        self.set("direction", direction)
        self.set("direction_word", direction_verbose)

        # Layer information
        layers = [class_name.__name__.upper() for class_name in pkt.layers()]
        self.set("layers", layers)
        self.set("protocol", layers[-1])

        # Observer information
        if hack == "nfq" and dir == "send":
            observer = "postrouting nfq"
        elif hack == "nfq" and dir == "recv":
            observer = "prerouting nfq"
        else:
            observer = hack
        self.set("observer", observer)

        # Modbus information - sometimes updated from the outside
        self.set_modbus_information()
        self.update_modbus_word() # updated from transaction manager

        # Additional information
        self.set("layers_word", "/".join(self.get("layers")))
        self.set("length", str(len(pkt)))
        self.set("time_word", f"{time:.4f}")
        self.set("summary", pkt.summary())
        self.set("mac_word", f"{self.get("mac_src")} → {self.get("mac_dst")}" if pkt.haslayer(Ether) else "-")
        self.set("ip_word", f"{self.get("ip_src")} → {self.get("ip_dst")}" if pkt.haslayer(IP) else "-")

    def set(self, key: str, value):
        if key not in self.KEYS:
            return
        self.data[key] = value

    def get(self, key: str) -> Any:
        if key not in self.KEYS:
            return None
        else:
            return self.data[key]

    def get_column_value(self, column_name: str):
        output = self.get(column_name)
        if output is None:
            return f"None of this {column_name}"
        return self.get(column_name)

    def matches(self, category: str, requirement: str):
        '''
        Returns whether the given requirement is true given a primary key string found in settings.json - "packet_filter_columns".
        '''
        return requirement in self.get(category)
    
    def set_modbus_information(self) -> None:
        # return variables, values, command string
        # Return command
        # 2 of 18 instructions implemented lol
        p = self.get("pkt")
        variables = []
        values = []
        command = ""
        command_type = ""
        m = None
        is_modbus = False
        is_useful_modbus = False
        
        if m := p.getlayer(ModbusPDU03ReadHoldingRegistersRequest):
            for i in range(m.startAddr, m.startAddr + m.quantity):
                variables.append(f"hreg_{i}")
        elif m := p.getlayer(ModbusPDU03ReadHoldingRegistersResponse):
            for value in p.payload.registerVal:
                values.append(value)
            is_useful_modbus = True

        elif m := p.getlayer(ModbusPDU06WriteSingleRegisterRequest):
            variables.append(f"hreg_{p.payload.registerAddr}")
            values.append(p.payload.registerValue)
            is_useful_modbus = True
        elif m := p.getlayer(ModbusPDU06WriteSingleRegisterResponse):
            variables.append(f"hreg_{p.payload.registerAddr}")
            values.append(p.payload.registerValue)

        if p.haslayer(ModbusADURequest):
            command_type = "Request"
        elif p.haslayer(ModbusADUResponse):
            command_type = "Response"

        if m is not None:
            command = m.name
            is_modbus = True
        self.set("variables", variables)
        self.set("values", values)
        self.set("command", command)
        self.set("command_type", command_type)
        command_word = f"{command.split(" ")[0]} {command_type}"
        self.set("command_word", command_word)
        self.set("is_modbus", is_modbus)
        self.set("is_useful", is_useful_modbus)
        self.set("is_primary", False)

    def update_modbus_word(self) -> None:
        if self.get("is_modbus"):
            values_strings = []
            for num in self.get("values"):
                values_strings.append(f"{num:.2f}")
            modbus_word = f"{", ".join(self.get("variables"))} = {", ".join(values_strings)}"
        else:
            modbus_word = "-"
        self.set("modbus_word", modbus_word)