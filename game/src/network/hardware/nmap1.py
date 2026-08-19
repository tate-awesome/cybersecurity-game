'''
Module
'''
import scapy.all as scapy
from scapy.all import Packet, ARP, get_if_addr, get_working_if, get_if_hwaddr
import ipaddress, netifaces
from ..buffer import Buffer
import nmap, socket

class NMapper:
    def __init__(self, buffer: Buffer):
        self.buffer = buffer

    def get_local_ip(self) -> str:
        # Connect to an external IP briefly to discover the active local interface IP
        local_ip = None
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
        finally:
            s.close()
        return local_ip

    def get_local_subnet(self, local_ip: str) -> str:
        local_ip = self.get_local_ip()
        
        # Convert local IP (e.g., 192.168.1.15) to a /24 subnet string (192.168.1.0/24)
        ip_parts = local_ip.split('.')
        ip_parts[-1] = '0/24'
        return '.'.join(ip_parts)

    def library_nmap(self):
        # Initialize scanner
        nm = nmap.PortScanner()
        local_ip = self.get_local_ip()
        subnet = self.get_local_subnet(local_ip)

        self.buffer.put("nmap", f"Local IP Found: {local_ip}")
        self.buffer.put("nmap", f"Target Subnet Detected: {subnet}")
        self.buffer.put("nmap", "Scanning for active hosts (this may take a few seconds)...")

        # -sn: Ping scan (no port scan, host discovery only)
        # -PE: ICMP Echo Request
        nm.scan(hosts=subnet, arguments='-sn -PE')

        self.buffer.put("nmap", "--- Active Hosts Found ---")
        # Iterate through all discovered up hosts
        for host in nm.all_hosts():
            if nm[host].state() == 'up':
                hostname = nm[host].hostname()
                hostname_str = f"({hostname})" if hostname else "(No Hostname)"
                self.buffer.put("nmap", f"IP Address: {host:<15} State: {nm[host].state():<5} Hostname: {hostname_str}")

    def do_nmap(self):
        # self.manual_nmap()
        self.library_nmap()


#  OLD bad manual method

    def get_active_iface(self):
        active_iface = ""
        self.interface_manager = self.InterfaceManager()
        ifm = self.interface_manager
        for i, iface in enumerate(ifm.interfaces):
            if iface["is_active"]:
                active_iface = iface
        return active_iface["display_name"]

    def manual_nmap(self):
        self.interface_manager = self.InterfaceManager()
        ifm = self.interface_manager

        self.buffer.put("nmap", "Starting NMap...")

        active_iface = next(
            (
                iface for iface in ifm.interfaces
                if iface["is_active"]
                and iface["ip"]
                and iface["ip"] != "0.0.0.0"
            ),
            None
        )

        if active_iface is None:
            self.buffer.put("nmap", "Could not find an active IPv4 interface.")
            return

        iface_name = active_iface["scapy_name"]
        active_ip = active_iface["ip"]
        active_netmask = active_iface["netmask"]
        active_mac = active_iface["mac"]

        self.buffer.put("nmap", f"Interface: {active_iface['display_name']}")
        self.buffer.put("nmap", f"Scapy interface: {iface_name}")
        self.buffer.put("nmap", f"MAC: {active_mac}")
        self.buffer.put("nmap", f"IP: {active_ip}")
        self.buffer.put("nmap", f"Netmask: {active_netmask}")

        if not active_netmask:
            self.buffer.put("nmap", "Could not determine network mask.")
            return

        network = self.compute_network(active_ip, active_netmask)

        self.buffer.put("nmap", f"Network ping range: {network}")
        self.buffer.put("nmap", f"Sending ARP probes through {iface_name}...")

        ping_packet, answered, unanswered = self.ping_hosts(
            network,
            iface_name
        )

        self.buffer.put(
            "nmap",
            "ARP Probe",
            ping_packet,
            "send"
        )

        hosts = []

        for sent, received in answered:
            self.buffer.put(
                "nmap",
                "Answered ARP Request",
                sent,
                "recv"
            )

            self.buffer.put(
                "nmap",
                "ARP Response",
                received,
                "recv"
            )

            if scapy.ARP in received:
                ip = received[scapy.ARP].psrc
                mac = received[scapy.ARP].hwsrc

                hosts.append((ip, mac))

        for ip, mac in hosts:
            self.buffer.put(
                "nmap",
                f"Found host {ip} at {mac}"
            )

        self.buffer.put(
            "nmap",
            f"NMap complete. {len(hosts)} host(s) found."
        )


    def compute_network(self, ip: str, netmask: str) -> str:
        if not netmask:
            return "Invalid netmask"
        else:
            network = ipaddress.IPv4Network(f"{ip}/{netmask}", strict=False)
            return str(network)

    def ping_hosts(self, network: str, iface: str):
        packet = (
            scapy.Ether(dst="ff:ff:ff:ff:ff:ff") /
            scapy.ARP(pdst=network)
        )

        answered, unanswered = scapy.srp(
            packet,
            iface=iface,
            timeout=2,
            verbose=False
        )

        return packet, answered, unanswered
    
    def compute_hosts(self, responses: list[Packet]):
        infos = []
        for pkt in responses:
            infos.append(f"Host IP {pkt[ARP].psrc} at MAC address {pkt[ARP].hwsrc}")
        return infos

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