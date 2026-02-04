from abc import ABC, abstractmethod
from .hardware import arp_spoofing, net_filter_queue, sniffing
from .virtual import master, slave
from .saved import 
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
    

class VirtualNetwork(Network):
    def __init__(self, virtual_slave):
        self.virtual_slave = virtual_slave


class SavedNetwork(Network):
    '''
    Fills up the buffer
    '''
    def __init__(self, saved_loader):
        self.saved_loader = saved_loader

    def start_arp(self):
        pass

    def stop_arp(self):
        pass

    def start_nfq(self):
        pass
    
    def stop_nfq(self):
        pass

    def start_sniff(self):
        pass

    def stop_sniff(self):
        pass