'''
Module
'''
import scapy.all as scapy
from scapy.all import Packet, ARP
import ipaddress, netifaces
from ..data_buffer import DataBuffer

class NMapper:
    def __init__(self, buffer: DataBuffer):
        self.buffer = buffer

    def do_nmap(self):
        # TODO nmap console command outputs
        # TODO Name these things correctly
        iface = str(self.get_interface())
        self.buffer.put("nmap", "Detected interface", ["Your network interface", iface])

        ip = self.get_ip(iface)
        self.buffer.put("nmap", "info", ["Your IP Address", ip])

        netmask = self.get_netmask(iface)
        self.buffer.put("nmap", "info", ["Network Mask", netmask])

        network = self.compute_network(ip, netmask)
        self.buffer.put("nmap", "info", ["Network Range", network])

        ping_packet, answered, unanswered = self.ping_hosts(network)
        self.buffer.put("nmap", "ARP Probe", ping_packet)

        responses = []
        
        for received in answered:
            self.buffer.put("nmap", "Answered ARP Request", received[0])
            self.buffer.put("nmap", "ARP Response", received[1])
            responses.append(received[1])

        hosts = self.compute_hosts(responses)
        for host in hosts:
            self.buffer.put("nmap", "info", ["Found host", host])





    def get_interface(self):
        interface = scapy.conf.iface
        return interface


    def get_ip(self, iface) -> str:
        info = netifaces.ifaddresses(iface)[netifaces.AF_INET][0]
        ip = info["addr"]
        return str(ip)

    def get_netmask(self, iface) -> str:
        info = netifaces.ifaddresses(iface)[netifaces.AF_INET][0]
        netmask = info["netmask"]
        return str(netmask)

    def compute_network(self, ip: str, netmask: str) -> str:
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
            infos.append(f"Host IP {pkt[ARP].psrc} is at MAC address {pkt[ARP].hwsrc}")
        return infos