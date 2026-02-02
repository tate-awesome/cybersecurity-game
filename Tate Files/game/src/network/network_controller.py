from abc import ABC, abstractmethod
from hardware import arp_spoofing, sniffing

class NetworkMode(ABC):
    @abstractmethod
    def start_arp(self):...
    @abstractmethod
    def stop_arp(self):...

class HardwareNetworkMode(NetworkMode):
    def __init__(self):
        # arp_spoofing access
        self.arp_spoofing = arp_spoofing
        self.arp_spoofer = arp_spoofing.ArpSpoofer()