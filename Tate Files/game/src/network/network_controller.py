from abc import ABC, abstractmethod
from .hardware import arp_spoofing, net_filter_queue, sniffing
from . import packet_buffer, mod_table

class Network(ABC):
    @abstractmethod
    def start_arp(self):...

    @abstractmethod
    def stop_arp(self):...

    @abstractmethod
    def start_nfq(self):...

    @abstractmethod
    def stop_nfq(self):...

    @abstractmethod
    def start_sniff(self):...

    @abstractmethod
    def stop_sniff(self):...


class HardwareNetwork(Network):
    def __init__(self):
        self.arp_spoofer = arp_spoofing.ArpSpoofer()
        self.buffer = packet_buffer.PacketBuffer()
        self.table = mod_table.ModTable()
        self.nfq = net_filter_queue.NetFilterQueue(self.buffer, self.table)
        self.sniffer = sniffing.Sniffer(self.buffer)

    def start_arp(self):
        self.arp_spoofer.start()

    def stop_arp(self):
        self.arp_spoofer.stop()

    def start_nfq(self):
        self.nfq.start(self.nfq.buffer_and_modify)
    
    def stop_nfq(self):
        self.nfq.stop()

    def start_sniff(self):
        self.sniffer.start(self.sniffer.put_modbus_in_buffer)

    def stop_sniff(self):
        self.sniffer.stop()
    