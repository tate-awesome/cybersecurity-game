'''
Module
'''
import threading
import scapy.all as scapy
from scapy.all import get_if_addr, get_working_if, get_if_hwaddr
import netifaces
from ..process import Process
from ..buffer.channels.network_graph import MAX_NICKNAME_LENGTH
from ..buffer.notice import Report
import nmap, re, socket, subprocess, sys

# An IP, then a MAC later on its line - in /proc/net/arp, "arp -a" (Windows,
# with dashes) and "arp -an" (macOS, which drops each byte's leading zero)
ARP_ENTRY = re.compile(r"(\d+\.\d+\.\d+\.\d+)\D.*?\b([0-9a-f]{1,2}(?:[:-][0-9a-f]{1,2}){5})\b", re.IGNORECASE)

class NMapper(Process):
    def __init__(self, buffer, context):
        super().__init__(buffer, context)
        self._running = False

    def is_running(self) -> bool:
        return self._running

    def start(self):
        '''
        Runs the scan on a background thread so it can complete (or fail) on
        its own without blocking the UI - is_running() flips back to False
        when the thread finishes either way, which is what lets the process
        button's poll notice completion and reset itself.
        '''
        if self._running:
            self.buffer.put("nmap", "NMap scan is already running")
            return

        self._running = True

        def job():
            try:
                self.library_nmap()
            except Exception as e:
                self.buffer.put_error("nmap", f"NMap scan failed: {e}", "nmap_scan_failed")
            finally:
                self._running = False

        threading.Thread(target=job, daemon=True).start()

    def get_local_ip(self) -> str | None:
        # Connect to an external IP briefly to discover the active local interface IP
        local_ip = None
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
        except OSError:
            pass
        finally:
            s.close()
        return local_ip

    def get_local_subnet(self, local_ip: str) -> str:
        # Convert local IP (e.g., 192.168.1.15) to a /24 subnet string (192.168.1.0/24)
        ip_parts = local_ip.split('.')
        ip_parts[-1] = '0/24'
        return '.'.join(ip_parts)

    def library_nmap(self):
        # Initialize scanner - python-nmap only wraps the nmap program, so it
        # fails here when nmap itself isn't installed (or isn't on PATH)
        try:
            nm = nmap.PortScanner()
        except nmap.PortScannerError as e:
            if "not found" not in str(e):
                raise
            self.buffer.put_error("nmap", f"NMap scan failed: the nmap program was not found. "
                                          f"Please install nmap ({self.nmap_install_hint()}), then restart the game.",
                                  "nmap_not_installed")
            return
        local_ip = self.get_local_ip()
        if local_ip is None:
            self.buffer.put_error("nmap", "Could not determine local IP address (no network connection?). Aborting scan.",
                                  "no_network_connection")
            return
        subnet = self.get_local_subnet(local_ip)

        self.buffer.put("nmap", f"Scanning {subnet} for active hosts (this may take a few seconds)...")

        try:
            # -sn: Ping scan (no port scan, host discovery only)
            # -PE: ICMP Echo Request
            nm.scan(hosts=subnet, arguments='-sn -PE')
        except Exception as e:
            self.buffer.put_error("nmap", f"NMap scan failed: {e}", "nmap_scan_failed")
            return

        # The whole scan as one report - shown as one toast, not a line per host
        hosts = []
        for host in nm.all_hosts():
            if nm[host].state() == 'up':
                hosts.append([host, nm[host].state(), nm[host].hostname() or "(No Hostname)"])
        macs = self.host_macs(nm)
        for host, mac in macs.items():
            self.context.buffer.network.put_host(mac, host)
        nicknamed = self.apply_nicknames(nm, macs)

        report = Report("NMap Scan")
        report.facts({"Local IP": local_ip, "Target subnet": subnet})
        report.heading(f"Active hosts ({len(hosts)})")
        report.table(["IP Address", "State", "Hostname"], hosts, empty="No active hosts found.")
        if nicknamed:
            report.heading("Nicknamed hosts")
            report.table(["MAC", "IP Address", "Nickname"], nicknamed)
        found = f"{len(hosts)} active host" + ("" if len(hosts) == 1 else "s")
        self.buffer.put_report("nmap", f"Finished NMap scan: found {found}.", report)

    def nmap_install_hint(self) -> str:
        if sys.platform == "win32":
            return "download it from https://nmap.org/download.html"
        if sys.platform == "darwin":
            return "brew install nmap"
        return "e.g. sudo apt install nmap"

    def host_macs(self, nm) -> dict[str, str]:
        '''
        The MAC of each host the scan found up, by IP. It comes from the scan
        when nmap could see it (a privileged scan on the same network), or
        else from the OS's ARP cache - reaching a host on the same network
        fills it in, even unprivileged - or else from the IPs the network
        graph has seen on each MAC. A host with none of these is left out.
        '''
        arp_macs = self.arp_cache()
        _, host_ips = self.context.buffer.network.get_hosts()
        seen_macs = {}
        for mac, ips in host_ips.items():
            for ip in ips:
                seen_macs.setdefault(ip, mac)

        macs = {}
        for host in nm.all_hosts():
            if nm[host].state() != 'up':
                continue
            mac = nm[host].get('addresses', {}).get('mac')
            mac = mac.lower() if mac else arp_macs.get(host) or seen_macs.get(host)
            if mac:
                macs[host] = mac
        return macs

    def arp_cache(self) -> dict[str, str]:
        '''The OS's ARP cache - each IP's MAC, lowercase and colon-separated. Empty if it can't be read.'''
        try:
            if sys.platform.startswith("linux"):
                with open("/proc/net/arp") as f:
                    text = f.read()
            else:
                flags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
                text = subprocess.run(["arp", "-a" if sys.platform == "win32" else "-an"],
                                      capture_output=True, text=True, timeout=5, creationflags=flags).stdout
        except (OSError, subprocess.SubprocessError):
            return {}
        cache = {}
        for ip, mac in ARP_ENTRY.findall(text):
            mac = ":".join(byte.zfill(2) for byte in re.split("[:-]", mac.lower()))
            # Incomplete entries read as all zeros
            if mac not in ("00:00:00:00:00:00", "ff:ff:ff:ff:ff:ff"):
                cache.setdefault(ip, mac)
        return cache

    def apply_nicknames(self, nm, macs: dict[str, str]) -> list[list[str]]:
        '''
        Nicknames each host found (in network_hosts, by MAC - see the network
        graph's Configure Hosts, and host_macs for where its MAC comes from)
        after its hostname, or else the maker nmap reads from its MAC. Hosts
        already nicknamed keep theirs. Returns each one it nicknamed -
        [mac, ip, nickname] - for the scan's report.
        '''
        preferences = self.context.preferences
        nicknamed = []
        for host, mac in macs.items():
            scan_mac = nm[host].get('addresses', {}).get('mac')
            vendor = nm[host].get('vendor', {}).get(scan_mac, "") if scan_mac else ""
            name = nm[host].hostname() or vendor
            if not name:
                continue
            if preferences.host_nickname(mac):
                continue
            # Cut to fit a chip - "Raspberry Pi Trading" reads as "Raspberry Pi"
            name = name[:MAX_NICKNAME_LENGTH].strip()
            preferences.set_host_nickname(mac, name)
            nicknamed.append([mac, host, name])
        return nicknamed

    def get_active_iface(self):
        active_iface = ""
        self.interface_manager = self.InterfaceManager()
        ifm = self.interface_manager
        for i, iface in enumerate(ifm.interfaces):
            if iface["is_active"]:
                active_iface = iface
        return active_iface["display_name"]

    class InterfaceManager:
        def __init__(self):
            self.interfaces = []
            self.active_iface = None
            self.load_interfaces()

        def load_interfaces(self):
            self.interfaces.clear()

            try:
                working = get_working_if()
                self.active_iface = working.name
            except Exception:
                self.active_iface = None

            for iface in scapy.IFACES.data.values():
                scapy_name = iface.name
                display_name = iface.description

                # Get IP (Scapy works great here)
                try:
                    ip = get_if_addr(scapy_name)
                except Exception:
                    ip = None

                # Get netmask (fallback method)
                netmask = self.get_netmask(scapy_name)

                try:
                    mac = get_if_hwaddr(scapy_name)
                except Exception:
                    mac = None

                self.interfaces.append({
                    "scapy_name": scapy_name,
                    "display_name": display_name,
                    "ip": ip,
                    "netmask": netmask,
                    "mac": mac,
                    "is_active": scapy_name == self.active_iface
                })

        def get_netmask(self, iface):
            try:
                addrs = netifaces.ifaddresses(iface)
                inet = addrs.get(netifaces.AF_INET)

                if not inet:
                    return None

                for entry in inet:
                    if "netmask" in entry:
                        return entry["netmask"]
                    if "mask" in entry:
                        return entry["mask"]

            except Exception:
                pass

            return None

        def get_interface(self, index):
            return self.interfaces[index]["scapy_name"]