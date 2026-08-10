from .hardware import arp_spoofing, sniffing, nmap, dos
from .virtual import master, slave
from .saved import loader
from . import mod_table
from .buffer import Buffer

class NetworkController:

    def __init__(self, context):
        self.buffer = Buffer(context)
        self.table = mod_table.ModTable()
        self.loader = loader.Loader(self.buffer)

    def abort_all(self):
        self.buffer.reset()
        self.loader.abort()
        self.table.reset_table()

class HardwareController(NetworkController):
    def __init__(self, context):
        super().__init__(context)
        self.nmap = nmap.NMapper(self.buffer)
        self.sniffer = sniffing.Sniffer(self.buffer)

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
    def __init__(self, context):
        super().__init__(context)
        self.arp_spoofer = arp_spoofing.ArpSpoofer(self.buffer)
        if context.os_name == "Windows":
            from .hardware import  nfq_windows
            self.nfq = nfq_windows.NetFilterQueue(self.buffer, context)
        else:
            from .hardware import  nfq_linux
            self.nfq = nfq_linux.NetFilterQueue(self.buffer, context)
        self.dos = dos.Denier(self.buffer)
    
    def abort_all(self):
        super().abort_all()
        self.stop_arp()
        self.stop_nfq()
        self.stop_dos()

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

    def start_dos(self, target_1, target_2):
        self.dos.start([target_1, target_2])
    
    def dos_is_running(self):
        self.dos.is_running()
    
    def stop_dos(self):
        self.dos.stop()

class HardwareDefender(HardwareController):
    def __init__(self, context):
        super().__init__(context)