'''
NFQ module. Callbacks and persistent object
'''

from scapy.all import IP, TCP, Packet
import threading, os, select
from netfilterqueue import NetfilterQueue as NFQ
from .. import modbus_util as mb
from ..mod_table import ModTable
from ..packet_buffer import PacketBuffer


class NetFilterQueue:

    def __init__(self, buffer: PacketBuffer, mod_table: ModTable):
        self.stop_event = None
        self.thread = None
        self.callback = None
        self.buffer = buffer
        self.table = mod_table

    def is_running(self):
        return self.stop_event is not None or self.thread is not None or self.callback is not None


    def start(self): 
        if self.is_running():
            print("NFQ already running")
            return
        callback_dict = {
            "none_accept": self.accept_only,
            "print_accept": self.print_and_accept,
            "show_accept": self.show_and_accept,
            "buffer_accept": self.buffer_and_accept,
            
            "none_modify": None,
            "print_modify": self.print_and_modify,
            "buffer_modify": self.buffer_and_modify
        }
        self.callback = self.print_and_modify
        self.stop_event = threading.Event()

        self.thread = threading.Thread(target=self._start, daemon=True)
        self.thread.start()


    def _start(self):

        # IPTables rule
        os.system("iptables -t mangle -A PREROUTING -i wlp0s20f3 -p TCP -j NFQUEUE --queue-num 1")

        # Create and bind NFQ callback
        nfq = NFQ()
        nfq.bind(1, self.callback)

        # Get readable file descriptor
        qfd = nfq.get_fd()
        poller = select.poll()
        poller.register(qfd, select.POLLIN)

        # Pipe for stop signaling
        stop_r, stop_w = os.pipe()
        poller.register(stop_r, select.POLLIN)
        print("Starting NFQ")
        try:
            while not self.stop_event.is_set():
                events = poller.poll(500)
                for fd, _ in events:
                    if fd == qfd:
                        nfq.run(False)   # process packets without blocking
                    elif fd == stop_r:
                        self.stop_event.set()
        # Stop on error or stop event
        finally:
            nfq.unbind()
            os.close(stop_r)
            os.close(stop_w)
            os.system("iptables -t mangle -D PREROUTING -i wlp0s20f3 -p TCP -j NFQUEUE --queue-num 1")


    def stop(self):
        if self.stop_event == None and self.thread == None:
            print("Net filter queue is not running")
            return
        else:
            print("Stopping net filter queue...")
            self.stop_event.set()
            self.thread.join()
            self.stop_event = None
            self.thread = None
            self.callback = None
            print("Stopped net filter queue")

    # Callbacks
    def accept_only(self, pkt: Packet):
        pkt.accept()

    def print_and_accept(self, pkt: Packet):
        spkt = IP(pkt.get_payload())
        mb.print_scannable(spkt)
        pkt.accept()

    def show_and_accept(self, pkt: Packet):
        spkt = IP(pkt.get_payload())
        spkt.show()
        pkt.accept()

    def print_and_modify(self, pkt: Packet):
        spkt = IP(pkt.get_payload())
        mb.print_scannable(spkt)


        if mb.is_commands(spkt):
            spkt = mb.modify_commands(spkt, self.table)

        elif mb.is_coord(spkt):
            spkt = mb.modify_coord(spkt, self.table)

        else:
            pkt.accept()
            return
    
        mb.print_scannable(spkt)

        # Recalculate checksums
        del spkt[TCP].chksum
        del spkt[IP].chksum
        del spkt[IP].len

        pkt.set_payload(bytes(spkt))
        pkt.accept()

    def buffer_and_accept(self, pkt: Packet):
        spkt = IP(pkt.get_payload())
        self.buffer.put(spkt, "in")
        pkt.accept()

    def buffer_print_accept(self, pkt: Packet):
        spkt = IP(pkt.get_payload())
        self.buffer.put(spkt, "in")
        mb.print_scannable(spkt)
        pkt.accept()

    def buffer_and_modify(self, pkt: Packet):
        spkt = IP(pkt.get_payload())
        
        self.buffer.put(spkt, "in")

        if mb.is_commands(spkt):
            spkt = mb.modify_commands(spkt, self.table)

        elif mb.is_coord(spkt):
            spkt = mb.modify_coord(spkt, self.table)

        else:
            pkt.accept()
            return

        self.buffer.put(spkt, "out")

        # Recalculate checksums
        del spkt[TCP].chksum
        del spkt[IP].chksum
        del spkt[IP].len

        pkt.set_payload(bytes(spkt))
        pkt.accept()