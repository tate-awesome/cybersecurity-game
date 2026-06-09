from .hardware import arp_spoofing, sniffing, net_filter_queue, nmap, dos
from .virtual import master, slave
from .saved import loader
from . import packet_buffer, mod_table, data_buffer

class NetworkController:

    def __init__(self):
        self.data_buffer = data_buffer.DataBuffer()
        self.table = mod_table.ModTable()

        self.loader = loader.Loader(self.data_buffer)

    def abort_all(self):
        self.data_buffer.reset_packet_cursor()
        self.data_buffer.reset_status_cursor()
        self.table.reset_table()

class HardwareController(NetworkController):
    def __init__(self):
        super().__init__()
        self.nmap = nmap.NMapper(self.data_buffer)
        self.sniffer = sniffing.Sniffer(self.data_buffer)

    def do_nmap(self):
        self.nmap.do_nmap()

    def start_sniff(self):
        self.sniffer.start()
    
    def sniff_is_running(self):
        return self.sniffer.is_running()

    def stop_sniff(self):
        self.sniffer.stop()
    
    def abort_all(self):
        super().abort_all()
        self.stop_sniff()
    
class HardwareAttacker(HardwareController):
    def __init__(self):
        super().__init__()
        self.arp_spoofer = arp_spoofing.ArpSpoofer(self.data_buffer)
        self.mitm = net_filter_queue.NetFilterQueue(self.data_buffer, self.table)
        self.dos = dos.Denier(self.data_buffer)
    
    def abort_all(self):
        super().abort_all()
        self.stop_arp()
        self.stop_mitm()
        self.stop_dos()

    def start_arp(self, target_ip, host_ip):
        # target_ip='192.168.8.137', host_ip='192.168.8.243'
        self.arp_spoofer.start(target_ip, host_ip)
    
    def arp_is_running(self):
        return self.arp_spoofer.running

    def stop_arp(self):
        self.arp_spoofer.stop()

    def start_mitm(self):
        self.mitm.start()

    def mitm_is_running(self):
        return self.mitm.is_running()
    
    def stop_mitm(self):
        self.mitm.stop()

    def start_dos(self, target_1, target_2):
        self.dos.start([target_1, target_2])
    
    def dos_is_running(self):
        self.dos.is_running()
    
    def stop_dos(self):
        self.dos.stop()

class HardwareDefender(HardwareController):
    def __init__(self):
        super().__init__()