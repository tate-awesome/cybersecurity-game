from .status import StatusBuffer
from .packet import PacketBuffer
from .modbus import ModbusBuffer
from .submarine_model import MapBuffer
from .hvac_model import HouseBuffer
from .network_graph import NetworkGraph
from .defender_modbus import DefenderModbusBuffer
from .defender_map import DefenderMapBuffer
from .defender_status import DefenderStatusBuffer

from typing import Protocol
from ..meta_packet import MetaPacket


class Channel(Protocol):
    '''
    The shape shared by PacketBuffer, ModbusBuffer, MapBuffer, HouseBuffer, and
    NetworkGraph - each is fed a MetaPacket by buffer_manager.distribute_packet()
    and cleared by Buffer.reset(). StatusBuffer intentionally doesn't conform
    (it takes plain source/purpose strings, not packets - see its own put()).
    '''
    def put(self, mpkt: MetaPacket) -> None: ...
    def reset(self) -> None: ...