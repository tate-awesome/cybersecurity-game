from ..meta_packet import MetaPacket
from .modbus import ModbusBuffer

class HouseBuffer:
    def __init__(self, context, modbuffer: ModbusBuffer, max_size=5000):
        self.context = context

    def put(self, mpkt: MetaPacket):
        ...