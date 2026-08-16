from .hardware import arp_spoofing, sniffing, nmap, dos, wifi
from .virtual import master, slave
from .saved import loader, replay
from .buffer import Buffer

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..app_core import Context

class NetworkController:

    def __init__(self, context: "Context"):
        self.buffer = Buffer(context)
        self.loader = loader.Loader(self.buffer, context)

    def abort_all(self):
        self.buffer.reset()
        self.loader.abort()

class HardwareController(NetworkController):
    def __init__(self, context):
        super().__init__(context)
        self.wifi = wifi.Wifi(self.buffer)
        self.nmap = nmap.NMapper(self.buffer)
        self.sniffer = sniffing.Sniffer(self.buffer)
        self.replay = replay.Replay(self.buffer, context)

    def start_wifi(self, match_name: str):
        self.wifi.start(match_name)

    def wifi_is_running(self):
        self.wifi.is_running()

    def stop_wifi(self):
        self.wifi.stop()

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
        self.replay.abort()
    
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
        self.stop_wifi()

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

    def abort_all(self):
        self.stop_wifi()
        super().abort_all()