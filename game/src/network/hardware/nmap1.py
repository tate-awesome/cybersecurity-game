'''
Module
'''
import scapy.all as scapy
from scapy.all import get_if_addr, get_working_if, get_if_hwaddr
import netifaces
from ..process import Process
import nmap, socket

class NMapper(Process):
    def __init__(self, buffer, context):
        super().__init__(buffer, context)

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
        # Initialize scanner
        nm = nmap.PortScanner()
        local_ip = self.get_local_ip()
        if local_ip is None:
            self.buffer.put("nmap", "Could not determine local IP address (no network connection?). Aborting scan.")
            return
        subnet = self.get_local_subnet(local_ip)

        self.buffer.put("nmap", f"Local IP Found: {local_ip}")
        self.buffer.put("nmap", f"Target Subnet Detected: {subnet}")
        self.buffer.put("nmap", "Scanning for active hosts (this may take a few seconds)...")

        try:
            # -sn: Ping scan (no port scan, host discovery only)
            # -PE: ICMP Echo Request
            nm.scan(hosts=subnet, arguments='-sn -PE')
        except Exception as e:
            self.buffer.put("nmap", f"NMap scan failed: {e}")
            return

        self.buffer.put("nmap", "--- Active Hosts Found ---")
        # Iterate through all discovered up hosts
        for host in nm.all_hosts():
            if nm[host].state() == 'up':
                hostname = nm[host].hostname()
                hostname_str = f"({hostname})" if hostname else "(No Hostname)"
                self.buffer.put("nmap", f"IP Address: {host:<15} State: {nm[host].state():<5} Hostname: {hostname_str}")

    def do_nmap(self):
        self.library_nmap()

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