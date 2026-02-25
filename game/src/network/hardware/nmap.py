'''
Module
'''
import scapy.all as scapy
from scapy.all import Packet
import ipaddress, netifaces
from ..data_buffer import DataBuffer

class NMapper:
    def __init__(self, buffer: DataBuffer):
        self.buffer = buffer

    def do_nmap(self):
        # TODO Name these things correctly
        ip = self.get_ip()
        self.buffer.put("nmap", "info", ["Your IP Address", ip])

        netmask = self.get_netmask()
        self.buffer.put("nmap", "info", ["Network Mask", netmask])

        network = self.compute_network(ip, netmask)
        self.buffer.put("nmap", "info", ["Network Range", network])

        ping_packet, answered, unanswered = self.ping_hosts(network)
        self.buffer.put("nmap", "ARP Probe", ping_packet)
        
        for received in answered:
            self.buffer.put("nmap", "Answered ARP Request", received[0])
            self.buffer.put("nmap", "ARP Response", received[1])



    def get_ip(self) -> str:
        iface = "wlp0s20f3"
        info = netifaces.ifaddresses(iface)[netifaces.AF_INET][0]
        ip = info["addr"]
        return str(ip)

    def get_netmask(self, ) -> str:
        iface = "wlp0s20f3"
        info = netifaces.ifaddresses(iface)[netifaces.AF_INET][0]
        netmask = info["netmask"]
        return str(netmask)

    def compute_network(self, ip: str, netmask: str) -> str:
        network = ipaddress.IPv4Network(f"{ip}/{netmask}", strict=False)
        return str(network)

    def ping_hosts(self, network: str, iface="wlp0s20f3") -> tuple[Packet, list, list]:
        '''
        May block for up to 2 seconds.
        '''
        network = str(network)
        ping_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") / scapy.ARP(pdst=network)
        answered, unanswered = scapy.srp(ping_packet, timeout=2, verbose=False)

        return ping_packet, answered, unanswered