'''
The house buffer builds structures that can be easily displayed on the canvas.
It receives data from ModbusBuffer.
in temp
out temp
in heater
out heater

'''

from threading import Lock
from collections import deque
from math import hypot
from ..meta_packet import MetaPacket
from .modbus import ModbusBuffer

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ....app_core import Context

class HouseBuffer:
    '''
    Buffer specific to the hvac model widget.
    Uses ModBusBuffer to get single values
    '''
    def __init__(self, context: "Context", modbuffer: ModbusBuffer, max_size: int = 5000):
        self.max_size = max_size
        self.context = context
        self.modbuffer = modbuffer
        self.reset()


    def put(self, mpkt: MetaPacket):
        # No HVAC-specific derived data to build - ModbusBuffer (which receives
        # every packet independently via buffer_manager.distribute_packet)
        # already tracks every register's history directly.
        pass

    def reset(self):
        pass

        self.variables = {
            "heater": "hreg_6",
            "temperature": "hreg_10"
        }

        self.registers = {value: key for key, value in self.variables.items()}

        self.factors = {
            "heater": 0.01,
            "temperature": 0.01
        }

    def convert(self, variable: str, raw: int):
        output = raw
        if variable in self.factors and raw is not None:
            output = float(raw * self.factors[variable])
        return output

    # Displays getters

    def get_single(self, variable: str, direction: str) -> float:
        '''
        Returns the latest value for the given variable and direction, or None if there is no data.
        '''
        output = None
        if variable in self.variables:
            register = self.variables[variable]
            output = self.modbuffer.get_single(register, direction)
            output = self.convert(variable, output)
        return output

    # House getters
    def get_heater(self, direction: str) -> float:
        '''
        Returns the latest heater value for the given direction, or None if there is no data.
        Units will be 1 or 0
        '''
        return self.get_single("heater", direction)
    
    def get_temperature(self, direction: str) -> float:
        '''
        Returns the latest temperature value for the given direction, or None if there is no data.
        Units will be degrees (F)
        '''
        return self.get_single("temperature", direction)