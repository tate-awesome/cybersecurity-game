import platform

from .arp_spoofing import ArpSpoofer
from .dos import Denier
from .nmap1 import NMapper
from .sniffing import Sniffer
from .wifi import Wifi
from .ap_poller import APPoller

if platform.system() == "Windows":
    from .nfq_windows import NetFilterQueue
else:
    from .nfq_linux import NetFilterQueue
