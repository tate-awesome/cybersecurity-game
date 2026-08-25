from ..buffer import Buffer
from .net_filter_queue import NetFilterQueueBaseClass
from netfilterqueue import NetfilterQueue as NFQ

from scapy.all import IP, TCP, Packet, Ether, IPv6
import threading, os, select, subprocess
from .nmap1 import NMapper

class NetFilterQueue(NetFilterQueueBaseClass):
    '''
    Linux Version
    '''
    def __init__(self, buffer: Buffer, context):
        super().__init__(buffer, context)

    def start(self): 
        if self.is_running():
            self.buffer.put("nfq", "NFQ is already running")
            return
        self.running = True
        self.stop_event = threading.Event()
        self.buffer.put("nfq", "Starting NFQ")

        # Run appropriate packet prerouter
        self.thread = threading.Thread(target=self.start_thread, daemon=True)
        self.thread.start()

    def start_thread(self):
        # Captured locally so stop() clearing self.stop_event once the
        # worker has exited can't race with the loop's own check of it.
        stop_event = self.stop_event

        # Calculate iface
        nmapper = NMapper(self.buffer)
        active_iface = nmapper.get_active_iface()

        # IPTables rule
        
        rules = [
            [
                "sudo", "iptables",
                "-t", "mangle",
                "-A", "PREROUTING",
                "-i", active_iface,
                "-j", "NFQUEUE",
                "--queue-num", "1",
            ],
            [
                "sudo", "iptables",
                "-t", "mangle",
                "-A", "POSTROUTING",
                "-o", active_iface,
                "-j", "NFQUEUE",
                "--queue-num", "2",
            ]
        ]

        for cmd in rules:
            result = subprocess.run(cmd, capture_output=True, text=True)
            print(result.stdout)
            print(result.stderr)
        
        self.buffer.put("nfq", f"Adding iptables rule:")
        self.buffer.put("nfq", f"sudo iptables -t mangle -A PREROUTING -i {active_iface} -p TCP -j NFQUEUE --queue-num 1")
        # Part	Meaning
        # iptables	Configure Linux packet filtering rules
        # -t mangle	Use the mangle table (used for packet modification/inspection)
        # -A PREROUTING	Append rule to the PREROUTING chain
        # -i wlp5s0	Match packets arriving on interface wlp5s0
        # -p TCP	Match only TCP packets
        # -j NFQUEUE	Instead of normal processing, send packets to an NFQUEUE
        # --queue-num 1	Send them to queue number 1

        nfq_in = NFQ()
        nfq_out = NFQ()

        nfq_in.bind(1, self.prerouting_callback)
        nfq_out.bind(2, self.postrouting_callback)

        # Get readable file descriptor
        qfd_in = nfq_in.get_fd()
        qfd_out = nfq_out.get_fd()

        poller = select.poll()
        poller.register(qfd_in, select.POLLIN)
        poller.register(qfd_out, select.POLLIN)

        # Pipe for stop signaling
        stop_r, stop_w = os.pipe()
        poller.register(stop_r, select.POLLIN)
        self.buffer.put("nfq", "Starting NFQ")
        try:
            while not stop_event.is_set():
                events = poller.poll(500)

                for fd, _ in events:
                    if fd == qfd_in:
                        try:
                            nfq_in.run(False)
                        except Exception as e:
                            self.buffer.put("nfq", f"Error processing PREROUTING queue: {e}")

                    elif fd == qfd_out:
                        try:
                            nfq_out.run(False)
                        except Exception as e:
                            self.buffer.put("nfq", f"Error processing POSTROUTING queue: {e}")

                    elif fd == stop_r:
                        stop_event.set()
                    # Stop on error or stop event
        finally:
            nfq_in.unbind()
            nfq_out.unbind()
            os.close(stop_r)
            os.close(stop_w)

            rules = [
                [
                    "sudo", "iptables",
                    "-t", "mangle",
                    "-D", "PREROUTING",
                    "-i", active_iface,
                    "-j", "NFQUEUE",
                    "--queue-num", "1",
                ],
                [
                    "sudo", "iptables",
                    "-t", "mangle",
                    "-D", "POSTROUTING",
                    "-o", active_iface,
                    "-j", "NFQUEUE",
                    "--queue-num", "2",
                ]
            ]

            for cmd in rules:
                subprocess.run(cmd, capture_output=True, text=True)
            self.buffer.put("nfq", "Stopped net filter queue")

    def accept_only(self, pkt: Packet):
            pkt.accept()

    def prerouting_callback(self, pkt):
        spkt = self.get_spkt(pkt)
        if spkt is None:
            pkt.accept()
            return

        enriched_mpkt = self.buffer.put("nfq", "PREROUTING NFQ", spkt, "in")
        if enriched_mpkt is None:
            pkt.accept()
            return
        # TODO add logic and timeline flags if it really does get modded
        spkt, modified = self.modify_mpkt(enriched_mpkt)
        if modified:
            self.buffer.put("nfq", "MODIFIED NFQ", spkt, "in")
            pkt.set_payload(bytes(spkt))

        pkt.accept()

    def postrouting_callback(self, pkt):
        spkt = self.get_spkt(pkt)
        if spkt is None:
            pkt.accept()
            return

        self.buffer.put("nfq", "POSTROUTING NFQ", spkt, "out")

        pkt.accept()

    def get_spkt(self, pkt):
        spkt = None
        raw = pkt.get_payload()

        if len(raw) < 1:
            return spkt

        # IPv4
        if raw[0] >> 4 == 4:
            return IP(raw)

        # IPv6
        if raw[0] >> 4 == 6:
            return IPv6(raw)

        # Ethernet?
        if len(raw) >= 14:
            ethertype = int.from_bytes(raw[12:14], "big")

            if ethertype == 0x0800:
                return Ether(raw)
            elif ethertype == 0x0806:
                return Ether(raw)
            elif ethertype == 0x86DD:
                return Ether(raw)
        return spkt