'''
Words for one packet, for the packet console's columns (see MetaPacket):

  - info: what Wireshark's Info column says - short and technical, e.g.
    "Who has 10.0.0.5? Tell 10.0.0.1" or "51234 → 502 [SYN] Seq=0 Win=64240".
  - summary: one plain-English sentence about what the packet does, for
    students who don't read protocols yet, e.g. "10.0.0.2 asks to open a
    connection to 10.0.0.9 on port 502 (ModBus)."

Built from scapy's dissection rather than a library: nothing in Python
explains a single packet in plain words, and Wireshark's own Info text
(through tshark/pyshark) would need Wireshark installed and a tshark
process per capture. The ModBus words are built from MetaPacket's fields
alone (modbus_info/modbus_summary), since a response's registers are only
filled in later, by the TransactionManager, on packets that may not have a
scapy packet dissected at all (see MetaPacket.from_payload).
'''
from scapy.layers.dns import DNS
from scapy.layers.dhcp import BOOTP, DHCP
from scapy.layers.inet import ICMP, IP, TCP, UDP
from scapy.layers.inet6 import IPv6
from scapy.layers.l2 import ARP, Ether
from scapy.packet import Packet

# Destinations that mean every device on the network
BROADCASTS = {"ff:ff:ff:ff:ff:ff", "255.255.255.255"}

# Well-known ports: (short name for the Service column, name for a sentence)
SERVICES: dict[int, tuple[str, str]] = {
    20: ("FTP-DATA", "file transfer (FTP)"), 21: ("FTP", "file transfer (FTP)"), 22: ("SSH", "remote login (SSH)"),
    23: ("Telnet", "remote login (Telnet)"), 25: ("SMTP", "email (SMTP)"), 53: ("DNS", "name lookup (DNS)"),
    67: ("DHCP", "address assignment (DHCP)"), 68: ("DHCP", "address assignment (DHCP)"), 80: ("HTTP", "web (HTTP)"),
    102: ("S7comm", "Siemens PLC (S7)"), 110: ("POP3", "email (POP3)"), 123: ("NTP", "time sync (NTP)"),
    137: ("NetBIOS", "Windows naming (NetBIOS)"), 138: ("NetBIOS", "Windows naming (NetBIOS)"),
    139: ("NetBIOS", "Windows file sharing (NetBIOS)"), 143: ("IMAP", "email (IMAP)"),
    161: ("SNMP", "device management (SNMP)"), 443: ("HTTPS", "secure web (HTTPS)"),
    445: ("SMB", "Windows file sharing (SMB)"), 502: ("ModBus", "ModBus"), 1883: ("MQTT", "IoT messaging (MQTT)"),
    1900: ("SSDP", "device discovery (SSDP)"), 3389: ("RDP", "remote desktop (RDP)"),
    5353: ("mDNS", "local name lookup (mDNS)"), 8080: ("HTTP", "web (HTTP)"), 20000: ("DNP3", "DNP3"),
    44818: ("EtherNet/IP", "EtherNet/IP"), 47808: ("BACnet", "building control (BACnet)"),
}
# TCP flags in Wireshark's order, by scapy's letter
TCP_FLAGS = (("S", "SYN"), ("F", "FIN"), ("R", "RST"), ("P", "PSH"), ("A", "ACK"), ("U", "URG"), ("E", "ECE"), ("C", "CWR"))
ICMP_UNREACHABLE = {0: "network unreachable", 1: "host unreachable", 2: "protocol unreachable",
                    3: "port unreachable", 4: "fragmentation needed", 13: "administratively blocked"}
DNS_TYPES = {1: "A", 2: "NS", 5: "CNAME", 6: "SOA", 12: "PTR", 15: "MX", 16: "TXT", 28: "AAAA", 33: "SRV", 255: "ANY"}
DHCP_TYPES = {1: "Discover", 2: "Offer", 3: "Request", 4: "Decline", 5: "ACK", 6: "NAK", 7: "Release", 8: "Inform"}


# Fields
def endpoints(pkt: Packet) -> tuple[str, str]:
    '''Source and destination as Wireshark's columns show them: the IP addresses, or the MACs without an IP layer.'''
    for layer in (IP, IPv6):
        if pkt.haslayer(layer):
            return pkt[layer].src, pkt[layer].dst
    if pkt.haslayer(Ether):
        return pkt[Ether].src, pkt[Ether].dst
    return "-", "-"


def ports(pkt: Packet) -> tuple[int | None, int | None]:
    for layer in (TCP, UDP):
        if pkt.haslayer(layer):
            return pkt[layer].sport, pkt[layer].dport
    return None, None


def service_port(pkt: Packet) -> int | None:
    '''The well-known port of the conversation - whichever end has one, the lower if both do.'''
    known = [port for port in ports(pkt) if port in SERVICES]
    return min(known) if known else None


def service(pkt: Packet) -> str:
    port = service_port(pkt)
    return SERVICES[port][0] if port is not None else "-"


def tcp_flags(pkt: Packet) -> str:
    if not pkt.haslayer(TCP):
        return "-"
    flags = str(pkt[TCP].flags)
    return ", ".join(name for letter, name in TCP_FLAGS if letter in flags)


def ttl(pkt: Packet) -> str:
    if pkt.haslayer(IP):
        return str(pkt[IP].ttl)
    if pkt.haslayer(IPv6):
        return str(pkt[IPv6].hlim)
    return "-"


def payload_length(pkt: Packet) -> int:
    '''Bytes carried above TCP/UDP - the application's own data.'''
    for layer in (TCP, UDP):
        if pkt.haslayer(layer):
            return len(pkt[layer].payload)
    return 0


# Info (Wireshark-style)
def info(pkt: Packet) -> str:
    if pkt.haslayer(ARP):
        arp = pkt[ARP]
        if arp.op == 1:
            return f"Gratuitous ARP for {arp.psrc}" if arp.psrc == arp.pdst else f"Who has {arp.pdst}? Tell {arp.psrc}"
        return f"{arp.psrc} is at {arp.hwsrc}"
    if pkt.haslayer(ICMP):
        icmp = pkt[ICMP]
        if icmp.type in (0, 8):
            kind = "request" if icmp.type == 8 else "reply"
            return f"Echo (ping) {kind}  id=0x{icmp.id:04x}, seq={icmp.seq}, ttl={ttl(pkt)}"
        if icmp.type == 3:
            return f"Destination unreachable ({ICMP_UNREACHABLE.get(icmp.code, f'code {icmp.code}')})"
        if icmp.type == 11:
            return "Time-to-live exceeded in transit"
        return f"ICMP type {icmp.type}, code {icmp.code}"
    if pkt.haslayer(DHCP):
        return f"DHCP {dhcp_type(pkt)} - Transaction ID 0x{pkt[BOOTP].xid:08x}"
    if pkt.haslayer(DNS):
        dns = pkt[DNS]
        name, qtype = dns_question(dns)
        if not dns.qr:
            return f"Standard query 0x{dns.id:04x} {qtype} {name}"
        answers = dns_answers(dns)
        tail = f" {qtype} {', '.join(answers)}" if answers else (" No such name" if dns.rcode == 3 else "")
        return f"Standard query response 0x{dns.id:04x} {qtype} {name}{tail}"
    sport, dport = ports(pkt)
    if pkt.haslayer(TCP):
        tcp = pkt[TCP]
        text = f"{sport} → {dport} [{tcp_flags(pkt)}] Seq={tcp.seq}"
        if "A" in str(tcp.flags):
            text += f" Ack={tcp.ack}"
        return f"{text} Win={tcp.window} Len={payload_length(pkt)}"
    if pkt.haslayer(UDP):
        return f"{sport} → {dport} Len={payload_length(pkt)}"
    return frame_kind(pkt)


def dns_question(dns) -> tuple[str, str]:
    if not dns.qd:
        return "", ""
    question = dns.qd[0] if hasattr(dns.qd, "__getitem__") else dns.qd
    return question.qname.decode(errors="replace").rstrip("."), DNS_TYPES.get(question.qtype, str(question.qtype))


def dns_answers(dns) -> list[str]:
    '''The answers' data - addresses, names... Newer scapy keeps them in a list, older chains them as payloads.'''
    if isinstance(dns.an, list):
        records = dns.an
    else:
        records, record = [], dns.an
        while record is not None and hasattr(record, "rdata"):
            records.append(record)
            record = record.payload if record.payload else None
    answers = []
    for record in records:
        data = getattr(record, "rdata", None)
        if data is not None:
            answers.append(data.decode(errors="replace").rstrip(".") if isinstance(data, bytes) else str(data))
    return answers


def dhcp_type(pkt: Packet) -> str:
    for option in pkt[DHCP].options:
        if isinstance(option, tuple) and option[0] == "message-type":
            kind = option[1]
            if isinstance(kind, int):
                return DHCP_TYPES.get(kind, str(kind))
            return {"ack": "ACK", "nak": "NAK"}.get(str(kind).lower(), str(kind).capitalize())
    return "message"


def frame_kind(pkt: Packet) -> str:
    '''The innermost layer scapy knows - or, for a frame it can't read past Ethernet, its EtherType.'''
    layer = pkt.lastlayer()
    while layer.name in ("Raw", "Padding") and layer.underlayer is not None:
        layer = layer.underlayer
    if isinstance(layer, Ether):
        return f"EtherType 0x{layer.type:04x}"
    return layer.name


# Summary (plain English)
def name(address: str) -> str:
    return "everyone on the network" if address.lower() in BROADCASTS else address


def summary(pkt: Packet) -> str:
    src, dst = (name(address) for address in endpoints(pkt))
    if pkt.haslayer(ARP):
        arp = pkt[ARP]
        if arp.op == 1 and arp.psrc == arp.pdst:
            return f"{arp.psrc} announces to everyone that it's at hardware address {arp.hwsrc}."
        if arp.op == 1:
            return f"{arp.psrc} asks everyone on the network which device has the address {arp.pdst}."
        return f"{arp.psrc} tells {arp.pdst} that it's the device at hardware address {arp.hwsrc}."
    if pkt.haslayer(ICMP):
        icmp = pkt[ICMP]
        if icmp.type == 8:
            return f"{src} pings {dst} to see if it's there."
        if icmp.type == 0:
            return f"{src} answers {dst}'s ping - it's there."
        if icmp.type == 3:
            reason = ICMP_UNREACHABLE.get(icmp.code, "it couldn't be reached")
            return f"{src} tells {dst} that a packet couldn't be delivered: {reason}."
        if icmp.type == 11:
            return f"{src} tells {dst} that a packet passed through too many routers and was dropped."
        return f"{src} sends {dst} a network control message (ICMP)."
    if pkt.haslayer(DHCP):
        kind = dhcp_type(pkt)
        return {
            "Discover": f"{src} looks for a server to give it an IP address.",
            "Offer": f"{src} offers {pkt[BOOTP].yiaddr} as an IP address.",
            "Request": f"{src} asks to use the IP address it was offered.",
            "ACK": f"{src} confirms that {pkt[BOOTP].yiaddr} is now that device's IP address.",
        }.get(kind, f"{src} sends a DHCP {kind} message about IP addresses.")
    if pkt.haslayer(DNS):
        dns = pkt[DNS]
        question, _ = dns_question(dns)
        if not dns.qr:
            return f"{src} asks {dst} for the address of {question}."
        answers = dns_answers(dns)
        if answers:
            return f"{src} tells {dst} that {question} is at {', '.join(answers)}."
        return f"{src} tells {dst} that {question} doesn't exist." if dns.rcode == 3 else f"{src} answers {dst}'s lookup of {question}."
    sport, dport = ports(pkt)
    port = service_port(pkt)
    what = SERVICES[port][1] if port is not None else None
    if pkt.haslayer(TCP):
        flags = str(pkt[TCP].flags)
        on_port = f"port {dport}" + (f" ({SERVICES[dport][1]})" if dport in SERVICES else "")
        if "S" in flags and "A" not in flags:
            return f"{src} asks to open a connection to {dst} on {on_port}."
        if "S" in flags:
            return f"{src} agrees to open the connection {dst} asked for" + (f" ({what})." if what else ".")
        if "R" in flags:
            return f"{src} refuses or cuts off its connection with {dst}."
        if "F" in flags:
            return f"{src} closes its connection with {dst}."
        length = payload_length(pkt)
        if length:
            return f"{src} sends {dst} {length} bytes of {what or 'data'}" + ("." if what else f" on port {dport}.")
        return f"{src} confirms to {dst} that its data arrived."
    if pkt.haslayer(UDP):
        return f"{src} sends {dst} {payload_length(pkt)} bytes of {what or f'data on port {dport}'} (UDP)."
    protocol = frame_kind(pkt)
    if protocol.startswith("EtherType"):
        return f"{src} sends {dst} a kind of frame this game doesn't read ({protocol})."
    return f"{src} sends {dst} a {protocol} packet." if pkt.haslayer(IP) or pkt.haslayer(IPv6) else f"{src} sends {dst} a {protocol} frame."


# ModBus, from MetaPacket's own fields
def modbus_function(command: str) -> str:
    '''scapy's layer name without "Request"/"Response" - those come from command_type.'''
    for ending in (" Request", " Response", " request", " response"):
        if command.endswith(ending):
            return command[: -len(ending)]
    return command


def register_values(variables: list, values: list, joiner: str = " = ") -> str:
    if variables and len(variables) == len(values):
        return ", ".join(f"{variable}{joiner}{value}" for variable, value in zip(variables, values))
    return ", ".join(str(value) for value in values)


def modbus_info(command: str, command_type: str, variables: list, values: list) -> str:
    text = f"{modbus_function(command)} {command_type.lower()}".strip()
    if values:
        return f"{text}: {register_values(variables, values)}"
    if variables:
        span = variables[0] if len(variables) == 1 else f"{variables[0]}–{variables[-1]}"
        return f"{text}: {span}"
    return text


def modbus_summary(src: str, dst: str, command: str, command_type: str, variables: list, values: list) -> str:
    writing = "write" in command.lower()
    if command_type == "Request":
        if writing and values:
            return f"{src} tells {dst} to set {register_values(variables, values, ' to ')}."
        return f"{src} asks {dst} for the values of {', '.join(variables) or 'some registers'}."
    if command_type == "Response":
        if writing:
            return f"{src} confirms to {dst} that it set {register_values(variables, values, ' to ')}."
        return f"{src} answers {dst}: {register_values(variables, values) or 'no values'}."
    return f"{src} sends {dst} a ModBus {modbus_function(command) or 'message'}."
