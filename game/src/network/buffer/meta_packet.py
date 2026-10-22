from scapy.all import Packet, IP, IPv6
from scapy.arch import get_if_hwaddr, get_working_if
import uuid
from scapy.contrib.modbus import *
from typing import Any

from . import describe, link as links


def _resolve_local_mac() -> str:
    '''
    The MAC address of the network interface actually used for outbound
    traffic - used below to tell "packets addressed to us" apart from any
    other traffic a sniffer/nfq happens to see.

    uuid.getnode() is unreliable for this on any machine with more than one
    MAC-bearing adapter, which is the common case on Windows (Wi-Fi +
    Ethernet + Bluetooth + VPN/virtual adapters, etc.) but rare on a typical
    single-NIC Linux box - it has no notion of "the active one" and can
    return an unrelated, even disconnected, adapter's MAC (observed: it
    picked a laptop's Bluetooth radio over its connected Wi-Fi adapter).
    When that happens, direction never resolves to "in"/"out" for sniffed
    packets, which silently breaks modbus transaction tracking (is_primary
    never gets set - see TransactionManager). get_working_if() resolves the
    adapter scapy would actually route traffic through instead.
    '''
    try:
        return get_if_hwaddr(get_working_if().name).lower()
    except Exception:
        node = uuid.getnode()
        return ':'.join(f'{(node >> ele) & 0xff:02x}' for ele in range(40, -8, -8)).lower()


class MetaPacket:

    KEYS = {
        "pkt",              # scapy packet
        "time",             # pkt.time float
        "number",           # buffer number
        "hack",             # hack source str: arp, sniff, dos, nfq, nmap
        "purpose",          # packet purpose str, from put()
        "mac_src",          # pkt.mac_src
        "mac_dst",          # pkt.mac_dst
        "ip_src",           # IPv4 or IPv6 source, or "-"
        "ip_dst",           # IPv4 or IPv6 destination, or "-"
        "direction",        # in or out
        "layers",           # pkt.layers list
        "protocol",         # the innermost layer that says what the packet is (see describe.protocol)
        "observer",         # hack observer: any hack, prerouting nfq, postrouting nfq
        "layers_word",      # pkt.layers joined by " / "
        "length",           # len(pkt)
        "time_word",        # pkt.time to 4 decimels
        "summary",          # one plain-English sentence about the packet (see describe.summary)
        "info",             # Wireshark-style Info text (see describe.info)
        "src",              # source IP, or MAC without an IP layer
        "dst",              # destination IP, or MAC without an IP layer
        "src_port",         # TCP/UDP source port, or "-"
        "dst_port",         # TCP/UDP destination port, or "-"
        "service",          # well-known port's service name: "ModBus", "DNS", ... or "-"
        "tcp_flags",        # "SYN, ACK", ... or "-"
        "ttl",              # IP time to live (IPv6 hop limit), or "-"
        "payload_length",   # bytes above TCP/UDP
        "time_delta",       # seconds since the previous packet in the buffer, to 4 decimals (set by PacketBuffer)
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

    # The fields set_described works out from the scapy packet
    DESCRIBED = {"src", "dst", "src_port", "dst_port", "service", "tcp_flags", "ttl", "payload_length", "info"}

    LOCAL_MAC = _resolve_local_mac()
    BROADCAST_MAC = "ff:ff:ff:ff:ff:ff"

    def __init__(  self, pkt: Packet, first_packet_time: float, number: int,
    hack: str, purpose: str, dir: str | None):

        self.data = dict()
        # Lazy-dissection fields, only used by ones rebuilt from a helper
        # payload (see from_payload) - the live-packet path below keeps the
        # scapy packet in self.data["pkt"] and never touches these.
        self._raw: bytes | None = None
        self._link: str = "ether"
        self._abs_time: float | None = None

        time = pkt.time - first_packet_time
        # Given information
        self.set("pkt", pkt)
        self.set("time", time)
        self.set("number", number)
        self.set("hack", hack)
        self.set("purpose", purpose)

        # Addressing information
        # Hardware addresses from whatever framed it - Ethernet II, 802.3, Wi-Fi... (see link)
        mac_src, mac_dst = links.hardware_addresses(pkt)
        self.set("mac_src", mac_src)
        self.set("mac_dst", mac_dst)
        ip = pkt[IP] if pkt.haslayer(IP) else pkt[IPv6] if pkt.haslayer(IPv6) else None
        self.set("ip_src", ip.src if ip is not None else "-")
        self.set("ip_dst", ip.dst if ip is not None else "-")

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
        self.set("protocol", describe.protocol(pkt))

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

        # Additional information
        self.set("layers_word", "/".join(self.get("layers")))
        self.set("length", str(len(pkt)))
        self.set("time_word", f"{time:.4f}")
        self.set_described(pkt)
        self.update_modbus_word() # updated from transaction manager
        self.set("mac_word", f"{mac_src} → {mac_dst}" if mac_src != "-" or mac_dst != "-" else "-")
        self.set("ip_word", f"{self.get("ip_src")} → {self.get("ip_dst")}" if ip is not None else "-")

    def set(self, key: str, value):
        if key not in self.KEYS:
            return
        self.data[key] = value

    def get(self, key: str) -> Any:
        if key not in self.KEYS:
            return None
        # Rebuilt-from-payload packets carry only raw bytes - dissect the
        # scapy packet the first time something actually asks for it (the
        # modbus transaction key, the file stream), never on the hot path
        # of filling the packet console's columns.
        if key == "pkt" and "pkt" not in self.data:
            self.data["pkt"] = self._dissect()
        return self.data.get(key)

    def _dissect(self) -> Packet | None:
        if self._raw is None:
            return None
        pkt = links.dissect(self._raw, self._link)
        if self._abs_time is not None:
            pkt.time = self._abs_time  # scapy stamps "now" otherwise - keep the capture time
        return pkt

    def to_payload(self, link: str | None = None) -> dict:
        '''
        A picklable snapshot for sending across the helper connection (see
        network/helper): every computed field, the raw bytes, and the
        absolute capture time - everything except the live scapy packet,
        which the receiving side dissects only on demand (see from_payload).
        link is how to dissect the raw bytes again (see link) - by default,
        what this packet was framed in.
        '''
        pkt = self.data.get("pkt")
        if link is None:
            link = self._link if self._raw is not None or pkt is None else links.link_of(pkt)
        raw = self._raw if self._raw is not None else (bytes(pkt) if pkt is not None else b"")
        abs_time = self._abs_time if self._abs_time is not None else (float(pkt.time) if pkt is not None else 0.0)
        data = {key: value for key, value in self.data.items() if key != "pkt"}
        return {"d": data, "raw": raw, "t": abs_time, "link": link}

    @classmethod
    def from_payload(cls, payload: dict, first_packet_time: float, number: int) -> "MetaPacket":
        '''
        Rebuilds a MetaPacket from a to_payload() snapshot without
        re-dissecting: the fields come straight across, the scapy packet
        stays lazy (see get), and "time" is recomputed relative to this
        buffer's own first packet so charts and rates line up.
        '''
        self = cls.__new__(cls)
        self.data = dict(payload["d"])
        self._raw = payload["raw"]
        self._link = payload.get("link", "ether")
        self._abs_time = float(payload["t"])
        relative = self._abs_time - (first_packet_time or 0.0)
        self.data["time"] = relative
        self.data["time_word"] = f"{relative:.4f}"
        self.data["number"] = number
        return self

    def get_column_value(self, column_name: str):
        output = self.get(column_name)
        if output is None and column_name in self.DESCRIBED and self.get("pkt") is not None:
            # From a recording made before these fields existed - describe it now, once
            self.set_described(self.get("pkt"))
            self.update_modbus_word()
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

    def set_described(self, pkt: Packet) -> None:
        '''
        The fields describe works out from the scapy packet - addresses,
        ports, flags, and the Info and Summary text. A packet describe
        can't make sense of still gets scapy's own summary rather than
        stopping the capture.
        '''
        try:
            src, dst = describe.endpoints(pkt)
            sport, dport = describe.ports(pkt)
            self.set("src", src)
            self.set("dst", dst)
            self.set("src_port", str(sport) if sport is not None else "-")
            self.set("dst_port", str(dport) if dport is not None else "-")
            self.set("service", describe.service(pkt))
            self.set("tcp_flags", describe.tcp_flags(pkt))
            self.set("ttl", describe.ttl(pkt))
            self.set("payload_length", str(describe.payload_length(pkt)))
            self.set("info", describe.info(pkt))
            self.set("summary", describe.summary(pkt))
        except Exception as error:
            print(f"Couldn't describe packet {pkt.summary()!r}: {error!r}")
            for key in ("src", "dst", "src_port", "dst_port", "service", "tcp_flags", "ttl", "payload_length"):
                self.data.setdefault(key, "-")
            self.set("info", pkt.summary())
            self.set("summary", pkt.summary())

    def update_modbus_word(self) -> None:
        '''
        modbus_word, and a ModBus packet's Info and Summary - again whenever
        the TransactionManager fills in a response's registers. Built from
        this packet's fields only, never the scapy packet, which a packet
        from the helper only dissects on demand (see get).
        '''
        if self.get("is_modbus"):
            values_strings = []
            for num in self.get("values"):
                values_strings.append(f"{num:.2f}")
            modbus_word = f"{", ".join(self.get("variables"))} = {", ".join(values_strings)}"
            fields = (self.get("command"), self.get("command_type"), self.get("variables"), self.get("values"))
            self.set("info", describe.modbus_info(*fields))
            self.set("summary", describe.modbus_summary(self.get("src") or "-", self.get("dst") or "-", *fields))
        else:
            modbus_word = "-"
        self.set("modbus_word", modbus_word)