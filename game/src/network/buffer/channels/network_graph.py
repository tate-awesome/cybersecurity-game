from ..meta_packet import MetaPacket
from collections import deque
from multiprocessing import Lock
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
        self.hosts = set()
        self.arrows_this_tick = {}

    def put(self, mpkt: MetaPacket):
        macs_involved = list((mpkt.get("mac_src"), mpkt.get("mac_dst")))
        with self.lock:
            for mac in macs_involved:
                self.add_host(mac)
            self.add_arrow(mpkt, macs_involved)

    def add_host(self, mac_addr: str):
        self.hosts.add(mac_addr)

    def add_arrow(self, mpkt: MetaPacket, macs: list[str]):
        self.arrows_this_tick[mpkt] = macs

    def get_arrows_this_tick(self):
        with self.lock:
            output = self.arrows_this_tick.copy()
            self.arrows_this_tick.clear()
            return output