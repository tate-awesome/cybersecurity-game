from ..meta_packet import MetaPacket
from .modbus import ModbusBuffer

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ....app_core import Context

class HouseBuffer:
    '''
    Buffer specific to the HVAC model widget.

    Unlike MapBuffer (which derives submarine x/y path data the physics
    simulation needs beyond raw register values), HVAC's registers - things
    like temperature and heater state, configured generically in
    modbus_settings/hvac.json - don't need any model-specific derived
    computation. ModbusBuffer already tracks each register's history directly
    by key, so this class exists mainly as HVAC's counterpart to MapBuffer:
    something the pipeline and HVAC panels can depend on consistently, and the
    place that exposes the direction-generalized history lookup HVAC's strip
    charts use.
    '''
    def __init__(self, context: "Context", modbuffer: ModbusBuffer, max_size: int = 5000):
        self.context = context
        self.modbuffer = modbuffer

    def put(self, mpkt: MetaPacket):
        # No HVAC-specific derived data to build - ModbusBuffer (which receives
        # every packet independently via buffer_manager.distribute_packet)
        # already tracks every register's history directly.
        pass

    def reset(self):
        pass

    def get_all_histories_and_legends(self, variable: str) -> dict[str, list[tuple[float, float]]]:
        '''
        Returns every exchange-type bucket's history for one register
        (e.g. "hreg_10"), delegated directly to ModbusBuffer.
        '''
        return self.modbuffer.get_all_histories_and_legends(variable)