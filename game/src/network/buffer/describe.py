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

Beyond IP, it reads what a capture picks up from the link layer itself:
802.3 frames (spanning tree, CDP, other LLC traffic), LLDP, the Wi-Fi
WPA handshake (EAPOL), and 802.11 management frames from a card in
monitor mode - beacons, probes, joining, and deauthentication.
'''
from scapy.layers.dns import DNS
from scapy.layers.dhcp import BOOTP, DHCP
from scapy.layers.dot11 import (Dot11, Dot11AssoReq, Dot11AssoResp, Dot11Auth, Dot11Beacon, Dot11Deauth, Dot11Disas,
                                Dot11Elt, Dot11ProbeReq, Dot11ProbeResp, Dot11ReassoReq)
from scapy.layers.eap import EAPOL
from scapy.layers.inet import ICMP, IP, TCP, UDP
from scapy.layers.inet6 import IPv6
from scapy.layers.l2 import ARP, STP, Dot3, Ether
from scapy.packet import Packet

from .link import hardware_addresses

# Loaded for the layers they register (scapy leaves contrib protocols out
# unless asked), so LLDP and CDP frames dissect instead of staying Raw
try:
    from scapy.contrib.cdp import CDPMsgDeviceID, CDPv2_HDR
    from scapy.contrib.lldp import LLDPDU, LLDPDUSystemName
except ImportError:
    CDPMsgDeviceID = CDPv2_HDR = LLDPDU = LLDPDUSystemName = None

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
# Layers that never say what a packet is - its leftover bytes, and the
# list of tagged elements (SSID, rates...) on the end of an 802.11 frame
FILLER_LAYERS = ("Raw", "Padding", "NoPayload", "Dot11Elt")
# Why a device was told to leave a Wi-Fi network (802.11 reason codes, the common ones)
DOT11_REASONS = {1: "unspecified", 2: "its login is no longer valid", 3: "the sender is leaving",
                 4: "it was inactive", 6: "it wasn't authenticated yet", 7: "it wasn't associated yet",
                 8: "the sender is leaving", 15: "the handshake timed out"}


# Fields
def endpoints(pkt: Packet) -> tuple[str, str]:
    '''
    Source and destination as Wireshark's columns show them: the IP
    addresses, or without an IP layer the hardware addresses of whatever
    framed it (Ethernet II, 802.3, Wi-Fi... - see link.hardware_addresses).
    '''
    for layer in (IP, IPv6):
        if pkt.haslayer(layer):
            return pkt[layer].src, pkt[layer].dst
    return hardware_addresses(pkt)


def is_filler(layer: Packet) -> bool:
    return type(layer).__name__.startswith(FILLER_LAYERS)


def meaningful_layer(pkt: Packet) -> Packet:
    '''The innermost layer that says what the packet is - not its leftover bytes or 802.11 tagged elements.'''
    layer = pkt.lastlayer()
    while is_filler(layer) and layer.underlayer is not None:
        layer = layer.underlayer
    return layer


def protocol(pkt: Packet) -> str:
    '''The Protocol column: the meaningful layer's scapy class, upper-cased (as the packet filter's names are).'''
    if is_lldp(pkt):
        return "LLDP"  # its TLVs are each a layer of their own
    return type(meaningful_layer(pkt)).__name__.upper()


def is_lldp(pkt: Packet) -> bool:
    '''Whether pkt carries LLDP - its TLV layers subclass LLDPDU, which haslayer doesn't count.'''
    if LLDPDU is None:
        return False
    layer = pkt
    while layer is not None and not is_filler(layer):
        if isinstance(layer, LLDPDU):
            return True
        layer = layer.payload
    return False


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
    link = link_info(pkt)
    if link is not None:
        return link
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
    layer = meaningful_layer(pkt)
    if isinstance(layer, Ether):
        return f"EtherType 0x{layer.type:04x}"
    if isinstance(layer, Dot3):
        return "802.3"
    return layer.name


# Summary (plain English)
def name(address: str) -> str:
    return "everyone on the network" if address.lower() in BROADCASTS else address


def summary(pkt: Packet) -> str:
    src, dst = (name(address) for address in endpoints(pkt))
    link = link_summary(pkt, src, dst)
    if link is not None:
        return link
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
        on_port = f"port {dport}" + (f" for {SERVICES[dport][1]}" if dport in SERVICES else "")
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
            return f"{src} sends {dst} {length} bytes of {what} data." if what else f"{src} sends {dst} {length} bytes of data on port {dport}."
        return f"{src} confirms to {dst} that its data arrived."
    if pkt.haslayer(UDP):
        return f"{src} sends {dst} {payload_length(pkt)} bytes of {what or f'data on port {dport}'} (UDP)."
    protocol = frame_kind(pkt)
    if protocol.startswith("EtherType") or protocol == "802.3":
        return f"{src} sends {dst} a kind of frame this game doesn't read ({protocol})."
    return f"{src} sends {dst} a {protocol} packet." if pkt.haslayer(IP) or pkt.haslayer(IPv6) else f"{src} sends {dst} a {protocol} frame."


# Below IP: 802.3, LLDP, EAPOL, 802.11
def ssid(pkt: Packet) -> str | None:
    '''The network name in an 802.11 frame's tagged elements - "" for a hidden or wildcard one, None if it has none.'''
    element = pkt.getlayer(Dot11Elt)
    while isinstance(element, Dot11Elt):
        if element.ID == 0:
            return element.info.decode(errors="replace")
        element = element.payload
    return None


def handshake_message(pkt: Packet) -> int | None:
    '''Which of the WPA 4-way handshake's messages an EAPOL key frame is, from its key information bits.'''
    key = pkt[EAPOL].payload
    ack, mic = getattr(key, "key_ack", None), getattr(key, "has_key_mic", getattr(key, "key_mic", None))
    install, secure = getattr(key, "install", 0), getattr(key, "secure", 0)
    if ack is None or mic is None:
        return None
    if ack and not mic:
        return 1
    if ack and mic and install:
        return 3
    if not ack and mic:
        return 4 if secure else 2
    return None


def is_dot11_control(pkt: Packet) -> bool:
    '''An 802.11 frame that isn't carrying IP or ARP - management and control frames, described here.'''
    return pkt.haslayer(Dot11) and not (pkt.haslayer(IP) or pkt.haslayer(IPv6) or pkt.haslayer(ARP))


def link_info(pkt: Packet) -> str | None:
    '''info for a link-layer protocol - None for anything else (see info).'''
    if pkt.haslayer(EAPOL):
        message = handshake_message(pkt) if pkt[EAPOL].type == 3 else None
        return f"Key (Message {message} of 4)" if message else f"EAPOL {pkt[EAPOL].sprintf('%EAPOL.type%')}"
    if pkt.haslayer(STP):
        stp = pkt[STP]
        if stp.bpdutype == 0x80:
            return "Topology Change Notification"
        return f"Conf. Root = {stp.rootid}/0/{stp.rootmac}  Cost = {stp.pathcost}  Port = 0x{stp.portid:04x}"
    if is_lldp(pkt):
        system = pkt.getlayer(LLDPDUSystemName)
        return f"LLDP: {system.system_name.decode(errors='replace')}" if system is not None else "LLDP announcement"
    if CDPv2_HDR is not None and pkt.haslayer(CDPv2_HDR):
        device = pkt.getlayer(CDPMsgDeviceID)
        return f"Device ID: {device.val.decode(errors='replace')}" if device is not None else "Cisco Discovery Protocol"
    if is_dot11_control(pkt):
        dot11 = pkt[Dot11]
        network = ssid(pkt)
        named = f', SSID="{network}"' if network else (", SSID=Wildcard (Broadcast)" if network == "" else "")
        number = f"SN={dot11.SC >> 4}" if dot11.SC is not None else ""
        for layer, kind in ((Dot11Beacon, "Beacon frame"), (Dot11ProbeReq, "Probe Request"),
                            (Dot11ProbeResp, "Probe Response"), (Dot11AssoReq, "Association Request"),
                            (Dot11ReassoReq, "Reassociation Request"), (Dot11AssoResp, "Association Response"),
                            (Dot11Auth, "Authentication")):
            if pkt.haslayer(layer):
                return f"{kind}, {number}{named}"
        for layer, kind in ((Dot11Deauth, "Deauthentication"), (Dot11Disas, "Disassociate")):
            if pkt.haslayer(layer):
                return f"{kind}, {number}, Reason code {pkt[layer].reason}"
        return f"802.11 {meaningful_layer(pkt).name}"
    return None


def link_summary(pkt: Packet, src: str, dst: str) -> str | None:
    '''summary for a link-layer protocol - None for anything else (see summary).'''
    if pkt.haslayer(EAPOL):
        message = handshake_message(pkt) if pkt[EAPOL].type == 3 else None
        if message:
            return (f"{src} and {dst} trade keys to secure their Wi-Fi connection - message {message} of the 4-way "
                    "handshake. With all four, an attacker can try to guess the Wi-Fi password offline.")
        return f"{src} and {dst} work on logging in to a secured network (EAPOL)."
    if pkt.haslayer(STP):
        return f"{src}, a network switch, shares spanning tree information - how switches keep traffic from looping forever."
    if is_lldp(pkt):
        system = pkt.getlayer(LLDPDUSystemName)
        called = f" - it's {system.system_name.decode(errors='replace')}" if system is not None else ""
        return f"{src} tells the devices next to it what it is (LLDP){called}."
    if CDPv2_HDR is not None and pkt.haslayer(CDPv2_HDR):
        device = pkt.getlayer(CDPMsgDeviceID)
        called = f" - it's {device.val.decode(errors='replace')}" if device is not None else ""
        return f"{src}, a Cisco device, tells the devices next to it what it is (CDP){called}."
    if is_dot11_control(pkt):
        network = ssid(pkt)
        quoted = f'"{network}"' if network else "its network"
        if pkt.haslayer(Dot11Beacon):
            return f"{src} announces its Wi-Fi network {quoted}." if network else f"{src} announces a hidden Wi-Fi network."
        if pkt.haslayer(Dot11ProbeReq):
            return f'{src} looks for the Wi-Fi network "{network}".' if network else f"{src} looks for any Wi-Fi network nearby."
        if pkt.haslayer(Dot11ProbeResp):
            return f"{src} answers {dst}: its Wi-Fi network {quoted} is here."
        if pkt.haslayer(Dot11Auth):
            return f"{src} and {dst} take the first step toward connecting over Wi-Fi (authentication)."
        if pkt.haslayer(Dot11AssoReq) or pkt.haslayer(Dot11ReassoReq):
            return f"{src} asks {dst} to join its Wi-Fi network {quoted}."
        if pkt.haslayer(Dot11AssoResp):
            joined = pkt[Dot11AssoResp].status == 0
            return f"{src} lets {dst} join its Wi-Fi network." if joined else f"{src} refuses to let {dst} join its Wi-Fi network."
        for layer, verb in ((Dot11Deauth, "disconnect from"), (Dot11Disas, "leave")):
            if pkt.haslayer(layer):
                reason = DOT11_REASONS.get(pkt[layer].reason, f"reason {pkt[layer].reason}")
                return (f"{src} tells {dst} to {verb} the Wi-Fi network ({reason}). A flood of these is a common "
                        "attack to knock devices offline.")
        return f"{src} sends {dst} an 802.11 {meaningful_layer(pkt).name} frame."
    return None


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
