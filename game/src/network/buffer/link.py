'''
A packet's link layer - what it was framed in on the wire - so a packet
can travel as raw bytes (to and from the privileged helper, into and out
of a recording) and come back as the same scapy packet, and so its
hardware addresses can be read whatever the framing.

  - "ether": Ethernet II, and IEEE 802.3 frames (a length where Ethernet
    II has its EtherType - STP, CDP and other LLC traffic). Ether()
    dissects both: scapy hands an 802.3 frame to Dot3 by itself.
  - "ip": a bare IP packet, as the packet interceptor (NFQ) sees one
  - "radiotap" / "dot11": 802.11 Wi-Fi, from a card in monitor mode -
    with or without the radiotap header the driver adds
  - "sll" / "sll2": Linux "cooked" captures (capturing on "any")
  - "loopback": BSD loopback / Windows Npcap loopback
'''
from scapy.layers.dot11 import Dot11, RadioTap
from scapy.layers.inet import IP
from scapy.layers.inet6 import IPv6
from scapy.layers.l2 import CookedLinux, CookedLinuxV2, Dot3, Ether, Loopback
from scapy.packet import Packet, Raw

# Outermost layer class -> link name, checked in order (a subclass before its base)
LINK_LAYERS: list[tuple[type, str]] = [
    (Ether, "ether"), (Dot3, "ether"), (IP, "ip"), (IPv6, "ip"), (RadioTap, "radiotap"), (Dot11, "dot11"),
    (CookedLinuxV2, "sll2"), (CookedLinux, "sll"), (Loopback, "loopback"),
]
# Link name -> the class that dissects its raw bytes ("ip" picks IP or IPv6 by version)
DISSECTORS: dict[str, type] = {
    "ether": Ether, "radiotap": RadioTap, "dot11": Dot11, "sll": CookedLinux, "sll2": CookedLinuxV2,
    "loopback": Loopback,
}


def link_of(pkt: Packet) -> str:
    '''The link name for pkt's outermost layer - "ether" for anything unrecognised, as it always was.'''
    for layer, name in LINK_LAYERS:
        if isinstance(pkt, layer):
            return name
    return "ether"


def dissect(raw: bytes, link: str) -> Packet:
    '''raw (the bytes of a packet with this link name) as a scapy packet again.'''
    if not raw:
        return Raw(raw)
    if link == "ip":
        return (IPv6 if raw[0] >> 4 == 6 else IP)(raw)
    return DISSECTORS.get(link, Ether)(raw)


def hardware_addresses(pkt: Packet) -> tuple[str, str]:
    '''
    The frame's source and destination hardware (MAC) addresses, from
    whichever link layer it has - or "-" for one it doesn't carry (a bare
    IP packet has none; a cooked capture records only the sender's).
    For Wi-Fi, the transmitter and receiver (addr2, addr1).
    '''
    for layer in (Ether, Dot3):
        if pkt.haslayer(layer):
            # None on a frame built by hand and never sent, which scapy fills in only once built
            return pkt[layer].src or "-", pkt[layer].dst or "-"
    if pkt.haslayer(Dot11):
        dot11 = pkt[Dot11]
        return dot11.addr2 or "-", dot11.addr1 or "-"
    for layer in (CookedLinuxV2, CookedLinux):
        if pkt.haslayer(layer):
            cooked = pkt[layer]
            length = getattr(cooked, "lladdrlen", 6) or 6
            source = bytes(cooked.src)[:length]
            return (":".join(f"{byte:02x}" for byte in source) if source.strip(b"\0") else "-"), "-"
    return "-", "-"
