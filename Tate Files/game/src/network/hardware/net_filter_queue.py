'''
NFQ module. Callbacks and persistent object
'''

from scapy.all import IP, TCP
import threading, os, select
from netfilterqueue import NetfilterQueue as NFQ
from . import modbus as mb
from . import buffer as buffer


class callbacks:

    def accept_only(pkt):
        pkt.accept()

    def print_and_accept(pkt):
        spkt = IP(pkt.get_payload())
        mb.print_scannable(spkt)
        pkt.accept()

    def print_and_modify(pkt):
        spkt = IP(pkt.get_payload())
        mb.print_scannable(spkt)


        if mb.is_commands(spkt):
            spkt = mb.modify_commands(spkt)

        elif mb.is_coord(spkt):
            spkt = mb.modify_coord(spkt)

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

    def buffer_and_accept(pkt):
        spkt = IP(pkt.get_payload())
        buffer.put(spkt, False)
        pkt.accept()

    def buffer_and_modify(pkt):
        spkt = IP(pkt.get_payload())
        
        buffer.put(spkt, False)

        if mb.is_commands(spkt):
            spkt = mb.modify_commands(spkt)

        elif mb.is_coord(spkt):
            spkt = mb.modify_coord(spkt)

        else:
            pkt.accept()
            return

        buffer.put(spkt, True)

        # Recalculate checksums
        del spkt[TCP].chksum
        del spkt[IP].chksum
        del spkt[IP].len

        pkt.set_payload(bytes(spkt))
        pkt.accept()


class NetFilterQueue:

    def __init__(self):
        self.stop_event = None
        self.thread = None
        self.callback = None


    def start(self, _callback = callbacks.accept_only): 
        if self.stop_event is not None or self.thread is not None or self.callback is not None:
            print("NFQ already running")
            return
        self.callback = _callback
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
            print("Stopped net filter queue")