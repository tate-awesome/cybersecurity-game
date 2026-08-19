from ..meta_packet import MetaPacket
from collections import deque
from multiprocessing import Lock
import math
import time
from ..meta_packet import MetaPacket
from .packet import PacketBuffer
from scapy.all import Packet

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ....app_core import Context

class NetworkGraph:
    def __init__(self, context: "Context", packet_buffer: PacketBuffer, max_size: int):
        self.lock = Lock()
        self.host_order = []
        self._host_set = set()
        self.arrows_this_tick = {}

    def put(self, mpkt: MetaPacket):
        macs_involved = list((mpkt.get("mac_src"), mpkt.get("mac_dst")))
        with self.lock:
            for mac in macs_involved:
                self.add_host(mac)
            self.add_arrow(mpkt, macs_involved)

    def add_host(self, mac_addr: str):
        if mac_addr not in self._host_set:
            self._host_set.add(mac_addr)
            self.host_order.append(mac_addr)

    def add_arrow(self, mpkt: MetaPacket, macs: list[str]):
        self.arrows_this_tick[mpkt] = macs

    def get_arrows_this_tick(self):
        with self.lock:
            output = self.arrows_this_tick.copy()
            self.arrows_this_tick.clear()
            return output

    def get_host_positions(self) -> dict:
        with self.lock:
            hosts = list(self.host_order)

        positions = {}
        n = len(hosts)
        if n == 0:
            return positions
        if n == 1:
            positions[hosts[0]] = (0.0, 0.0)
            return positions

        for i, mac in enumerate(hosts):
            angle = 2 * math.pi * i / n
            positions[mac] = (math.cos(angle), math.sin(angle))
        return positions
