'''
Module
'''
import scapy.all as scapy
from scapy.all import Packet, ARP, get_if_addr, get_working_if, get_if_hwaddr
import ipaddress, netifaces
from ..data_buffer import DataBuffer

class NMapper:
    def __init__(self, buffer: DataBuffer):
        self.buffer = buffer

    def get_active_iface(self):
        active_iface = ""
        self.interface_manager = self.InterfaceManager()
        ifm = self.interface_manager
        for i, iface in enumerate(ifm.interfaces):
            if iface["is_active"]:
                active_iface = iface
        return active_iface["display_name"]
        

    def do_nmap(self):
        self.interface_manager = self.InterfaceManager()
        ifm = self.interface_manager
        self.buffer.put("nmap", "Starting NMap...")


        # Post interfaces, find active interface
        active_iface = None
        self.buffer.put("nmap", "vvvv Your network interfaces vvvv")
        for i, iface in enumerate(ifm.interfaces):
            if iface["is_active"]:
                active = "[ACTIVE]" 
                active_iface = iface
            else:
                active = ""
            self.buffer.put("nmap", f"Interface {i}: {iface['display_name']} {active}")
            self.buffer.put("nmap", f"   Alt Name:   {iface['scapy_name']}")
            self.buffer.put("nmap", f"   MAC:     {iface['mac']}")
            self.buffer.put("nmap", f"   IP:      {iface['ip']}")
            self.buffer.put("nmap", f"   Netmask: {iface['netmask']}")
        active_ip = active_iface["ip"] if active_iface else "None"
        active_netmask = active_iface["netmask"] if active_iface else "None"
        active_mac = active_iface["mac"] if active_iface else "None"
        self.buffer.put("nmap", f"Your MAC address: {active_mac}")
        self.buffer.put("nmap", f"Your IP address: {active_ip}")
        self.buffer.put("nmap", f"Your netmask: {active_netmask}")

        network = self.compute_network(active_ip, active_netmask)
        self.buffer.put("nmap", f"Network ping range: {network}")

        ping_packet, answered, unanswered = self.ping_hosts(network)
        self.buffer.put("nmap", "ARP Probe", ping_packet)

        responses = []
        
        for received in answered:
            self.buffer.put("nmap", "Answered ARP Request", received[0])
            self.buffer.put("nmap", "ARP Response", received[1])
            responses.append(received[1])

        hosts = self.compute_hosts(responses)
        for host in hosts:
            self.buffer.put("nmap", f"Found {host}")

        self.buffer.put("nmap", "NMap complete.")


    def compute_network(self, ip: str, netmask: str) -> str:
        if not netmask:
            return "Invalid netmask"
        else:
            network = ipaddress.IPv4Network(f"{ip}/{netmask}", strict=False)
            return str(network)

    def ping_hosts(self, network: str) -> tuple[Packet, list, list]:
        '''
        May block for up to 2 seconds.
        '''
        network = str(network)
        ping_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") / scapy.ARP(pdst=network)
        answered, unanswered = scapy.srp(ping_packet, timeout=2.0, verbose=False)

        return ping_packet, answered, unanswered
    
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