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
            self.buffer.put("nfq", "NFQ is not running")
            return
        else:
            self.stop_event.set()
            self.thread.join(timeout=2)
            self.stop_event = None
            self.thread = None
            self.running = False

    def modify_mpkt(self, mpkt: MetaPacket) -> tuple[Packet, bool]:
        slots = self.context.states[self.slot_name]
        modified_flag = False

        if not mpkt.is_modbus or len(mpkt.variables) < 1:
            return mpkt.pkt, modified_flag

        if not self.context.states["modbus_modify_enabled"] == 1:
            return mpkt.pkt, modified_flag

        for i, variable in enumerate(mpkt.variables):
            slot = slots[variable]

            factor_str = self.context.states["modbus_variables"][variable]["factor"]
            mult_str = self.context.states["modbus_variables"][variable]["multiplier"]
            offs_str = self.context.states["modbus_variables"][variable]["offset"]
            fact = 1.0
            mult = 1.0
            offs = 0.0
            try: 
                fact = float(factor_str)
                mult = float(mult_str)
                offs = float(offs_str)
            except:
                continue


            if slot["modify"] == 0 or slot["modify"] == "0":
                continue

            if mult == 1.0 and offs == 0.0:
                continue

            offs = offs / fact

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