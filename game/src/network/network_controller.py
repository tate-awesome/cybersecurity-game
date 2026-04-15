from .hardware import arp_spoofing, sniffing, net_filter_queue, nmap, dos
from .virtual import master, slave
from .saved import loader
from . import packet_buffer, mod_table, data_buffer

class NetworkController:

    def __init__(self):
        self.buffer = packet_buffer.PacketBuffer()
        self.data_buffer = data_buffer.DataBuffer()
        self.table = mod_table.ModTable()
    
    def abort_all(self):
        pass
    
class Hardware(NetworkController):
    def __init__(self):
        super().__init__()
        self.arp_spoofer = arp_spoofing.ArpSpoofer(self.data_buffer)
        self.nmap = nmap.NMapper(self.data_buffer)
        self.nfq = net_filter_queue.NetFilterQueue(self.data_buffer, self.table)
        self.sniffer = sniffing.Sniffer(self.data_buffer)
        self.dos = dos.Denier(self.data_buffer)

    def do_nmap(self):
        self.nmap.do_nmap()

    def start_arp(self, target_ip, host_ip):
        # target_ip='192.168.8.137', host_ip='192.168.8.243'
        self.arp_spoofer.start(target_ip, host_ip)
    
    def arp_is_running(self):
        return self.arp_spoofer.running

    def stop_arp(self):
        self.arp_spoofer.stop()

    def start_nfq(self):
        self.nfq.start()

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

    def start_dos(self, target_1, target_2):
        self.dos.start([target_1, target_2])
    
    def dos_is_running(self):
        self.dos.is_running()
    
    def stop_dos(self):
        self.dos.stop()

    def abort_all(self):
        self.stop_arp()
        self.stop_nfq()
        self.stop_sniff()
        self.stop_dos()

class SavedNetwork(NetworkController):
    '''
    Fills up the buffer
    '''
    def __init__(self):
        super().__init__()

    def load_packets(self):
        # Becomes file picker "how to enter the network"
        self.file = loader.Loader(self.buffer, self.table)