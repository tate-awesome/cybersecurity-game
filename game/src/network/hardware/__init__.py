import platform

from .arp_spoofing import ArpSpoofer
from .dos import Denier
from .nmap import NMapper
from .sniffing import Sniffer
from .ap_poller import APPoller

if platform.system() == "Windows":
    from .nfq_windows import NetFilterQueue
    from .wifi_windows import Wifi
else:
    from .nfq_linux import NetFilterQueue
    from .wifi_linux import Wifi
