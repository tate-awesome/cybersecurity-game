'''
NFQ module. Callbacks and persistent object
'''

from scapy.all import IP, TCP, Packet, Ether, IPv6
from scapy.contrib.modbus import *
from ..buffer import Buffer
from ..buffer.meta_packet import MetaPacket
import threading

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...app_core import Context

class NetFilterQueueBaseClass:

    def __init__(self, buffer: Buffer, context: "Context"):
        self.buffer = buffer
        self.context = context

        self.running = False
        # Only meaningfully set once start() is called - declared here so
        # their type is known throughout the class (see stop()).
        self.stop_event: threading.Event | None = None
        self.thread: threading.Thread | None = None

    def is_running(self):
        return self.running

    def stop(self):
        if not self.is_running():
            self.buffer.put("nfq", "NFQ is not running")
            return
        else:
            if self.stop_event is not None:
                self.stop_event.set()
            if self.thread is not None:
                self.thread.join(timeout=5)
                if self.thread.is_alive():
                    # Worker didn't exit in time - its iptables rules and NFQ
                    # bind may still be live. Leave state as running so
                    # is_running() stays truthful and a retry is possible,
                    # instead of silently reporting a clean stop.
                    self.buffer.put("nfq", "NFQ worker did not stop in time; iptables rules may still be active")
                    return
            self.stop_event = None
            self.thread = None
            self.running = False
            self.buffer.put("nfq", "Stopped NFQ")

    def modify_mpkt(self, mpkt: MetaPacket) -> tuple[Packet, bool]:
        modified_flag = False
        pkt = mpkt.get("pkt")

        if not mpkt.get("is_modbus") or len(mpkt.get("variables")) < 1:
            return mpkt.get("pkt"), modified_flag

        if not self.context.states.get("modbus_modify_enabled") == 1:
            return pkt, modified_flag

        for i, variable in enumerate(mpkt.get("variables")):

            factor_str = self.context.states.get_register(variable, "factor")
            mult_str = self.context.states.get_register(variable, "multiplier")
            offs_str = self.context.states.get_register(variable, "offset")
            fact = 1.0
            mult = 1.0
            offs = 0.0
            try: 
                fact = float(factor_str)
                mult = float(mult_str)
                offs = float(offs_str)
            except:
                continue

            modify = self.context.states.get_register(variable, "modify")
            if modify == 0 or modify == "0":
                continue

            if mult == 1.0 and offs == 0.0:
                continue

            offs = offs / fact

            if m := pkt.getlayer(ModbusPDU03ReadHoldingRegistersResponse):
                val = m.registerVal[i]
                val = int(val * mult + offs)
                val = max(0, min(65535, val))
                m.registerVal[i] = val
                modified_flag = True

            elif m := pkt.getlayer(ModbusPDU06WriteSingleRegisterRequest):
                address = m.registerAddr
                val = m.registerValue
                val = int(val * mult + offs)
                val = max(0, min(65535, val))
                m.registerValue = val
                modified_flag = True

        if modified_flag:
            del pkt[IP].len
            del pkt[TCP].chksum
            del pkt[IP].chksum
            # Rebuild len, chksum, chksum
            pkt = IP(bytes(pkt))
            mpkt.set("pkt", pkt)
        return pkt, modified_flag