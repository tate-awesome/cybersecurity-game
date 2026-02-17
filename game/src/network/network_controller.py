from abc import ABC, abstractmethod
from .hardware import arp_spoofing, sniffing, net_filter_queue, nmap
from .virtual import master, slave
from .saved import loader
from . import packet_buffer, mod_table

class Network(ABC):
    @abstractmethod
    def start_arp(self, target_ip, host_ip):...

    @abstractmethod
    def arp_is_running(self):...

    @abstractmethod
    def stop_arp(self):...

    @abstractmethod
    def start_nfq(self, callback: str):...

    @abstractmethod
    def nfq_is_running(self):...

    @abstractmethod
    def stop_nfq(self):...

    @abstractmethod
    def start_sniff(self):...

    @abstractmethod
    def sniff_is_running(self):...

    @abstractmethod
    def stop_sniff(self):...

    def abort_all(self):
        self.stop_arp()
        self.stop_nfq()
        self.stop_sniff()


class HardwareNetwork(Network):
    def __init__(self):
        self.arp_spoofer = arp_spoofing.ArpSpoofer()
        self.nmap = nmap
        self.buffer = packet_buffer.PacketBuffer()
        self.table = mod_table.ModTable()
        self.nfq = net_filter_queue.NetFilterQueue(self.buffer, self.table)
        self.sniffer = sniffing.Sniffer(self.buffer)

    def start_arp(self, target_ip, host_ip):
        # target_ip='192.168.8.137', host_ip='192.168.8.243'
        self.arp_spoofer.start(target_ip, host_ip)
    
    def arp_is_running(self):
        return self.arp_spoofer.running

    def stop_arp(self):
        self.arp_spoofer.stop()

    def start_nfq(self, callback: str):
        self.nfq.start(callback)

    def nfq_is_running(self):
        return self.nfq.is_running()
    
    def stop_nfq(self):
        self.nfq.stop()

    def start_sniff(self):
        self.sniffer.start()
    
    def sniff_is_running(self):
        return self.sniffer.is_running()

    def stop_sniff(self):
        self.sniffer.stop()
    

class VirtualNetwork(Network):
    def __init__(self, virtual_slave):
        self.virtual_slave = virtual_slave


class SavedNetwork(Network):
    '''
    Fills up the buffer
    '''
    def __init__(self):
        self.buffer = packet_buffer.PacketBuffer()
        self.table = mod_table.ModTable()

    def start_arp(self, target_ip, host_ip):
        # Becomes file picker "how to enter the network"
        self.file = loader.Loader(self.buffer, self.table)

    def stop_arp(self):
        pass

    def start_nfq(self):
        # Becomes file loader "how to obtain packets"
        self.file.open_pcap_file(self.file.buffer_and_accept)
    
    def stop_nfq(self):
        pass

    def start_sniff(self):
        pass

    def stop_sniff(self):
        pass