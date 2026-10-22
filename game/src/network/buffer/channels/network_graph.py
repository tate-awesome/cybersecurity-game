from ..meta_packet import MetaPacket
from multiprocessing import Lock
import ipaddress
import math
from scapy.all import conf
from .packet import PacketBuffer

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ....app_core import Context

# The exercises' access point (see OpenAccessPointConfigInBrowser)
EXERCISE_AP_IP = "192.168.4.1"


def _default_gateway_ip() -> str | None:
    '''This machine's default gateway, as scapy's routing table has it when this runs.'''
    try:
        gateway = conf.route.route("0.0.0.0")[2]
    except Exception:
        return None
    return None if gateway in ("0.0.0.0", "") else gateway


def _is_global(ip_addr: str) -> bool:
    try:
        return ipaddress.ip_address(ip_addr).is_global
    except ValueError:
        return False


class NetworkGraph:
    '''
    The hosts (MACs) seen in the packet buffer, the IPs seen on each, and
    the packets between them this tick - for the network graph. The
    broadcast MAC isn't a host: a packet to it goes to every host.
    '''
    def __init__(self, context: "Context", packet_buffer: PacketBuffer, max_size: int):
        self.lock = Lock()
        self.reset()

    def reset(self):
        self.host_order = []
        self._host_set = set()
        # Every IP seen, in order, and the IPs seen on each MAC - a packet's
        # IP source/destination counts for its MAC source/destination
        self.ip_order = []
        self._ip_set = set()
        self.host_ips = {}
        self.arrows_this_tick = {}
        # Read again on every reset (Clear Data), as joining a network changes it
        self.gateway_ips = [ip for ip in (_default_gateway_ip(), EXERCISE_AP_IP) if ip]


    def put(self, mpkt: MetaPacket):
        hosts_involved = ((mpkt.get("mac_src"), mpkt.get("ip_src")), (mpkt.get("mac_dst"), mpkt.get("ip_dst")))
        macs_involved = [mac for mac, ip in hosts_involved]
        with self.lock:
            for mac, ip in hosts_involved:
                if mac != MetaPacket.BROADCAST_MAC:
                    self.add_host(mac, ip)
            self.add_arrow(mpkt, macs_involved)

    def add_host(self, mac_addr: str, ip_addr: str | None = None):
        if mac_addr not in self._host_set:
            self._host_set.add(mac_addr)
            self.host_order.append(mac_addr)
            self.host_ips[mac_addr] = []
        # MetaPacket uses "-" for a packet with no IP layer
        if not ip_addr or ip_addr == "-":
            return
        if ip_addr not in self._ip_set:
            self._ip_set.add(ip_addr)
            self.ip_order.append(ip_addr)
        if ip_addr not in self.host_ips[mac_addr]:
            self.host_ips[mac_addr].append(ip_addr)

    def get_hosts(self) -> tuple[list[str], list[str], dict[str, list[str]]]:
        '''Every MAC seen, every IP seen (both in the order first seen), and the IPs seen on each MAC.'''
        with self.lock:
            return list(self.host_order), list(self.ip_order), {mac: list(ips) for mac, ips in self.host_ips.items()}

    def get_access_point(self) -> str | None:
        '''
        The MAC that's most likely the access point: the first one seen with
        a gateway's IP (see gateway_ips), or else the one that carries the
        most internet IPs - only a router forwards those onto the local
        network. None if nothing points to one yet.
        '''
        with self.lock:
            for gateway in self.gateway_ips:
                for mac in self.host_order:
                    if gateway in self.host_ips[mac]:
                        return mac
            global_counts = {mac: sum(_is_global(ip) for ip in ips) for mac, ips in self.host_ips.items()}
        best = max(global_counts, key=global_counts.get, default=None)
        return best if best is not None and global_counts[best] > 0 else None

    def add_arrow(self, mpkt: MetaPacket, macs: list[str]):
        self.arrows_this_tick[mpkt] = macs

    def get_arrows_this_tick(self):
        with self.lock:
            output = self.arrows_this_tick.copy()
            self.arrows_this_tick.clear()
            return output

    def get_host_positions(self, hidden: set[str] = frozenset()) -> dict:
        '''
        Each shown MAC's spot on a circle - hidden ones are left out, and the
        rest spread to fill it. The access point (see get_access_point) goes
        in the middle, since every host talks through it.
        '''
        access_point = self.get_access_point()
        with self.lock:
            hosts = [mac for mac in self.host_order if mac not in hidden]

        positions = {}
        if access_point in hosts:
            hosts.remove(access_point)
            positions[access_point] = (0.0, 0.0)
        n = len(hosts)
        if n == 0:
            return positions
        # A lone host takes the middle, unless the access point already has it
        if n == 1 and not positions:
            positions[hosts[0]] = (0.0, 0.0)
            return positions

        for i, mac in enumerate(hosts):
            angle = 2 * math.pi * i / n
            positions[mac] = (math.cos(angle), math.sin(angle))
        return positions
