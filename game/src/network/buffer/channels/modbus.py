from collections import deque
from threading import Lock
from scapy.all import Packet

from ..meta_packet import MetaPacket
from scapy.contrib.modbus import *
from .transaction_manager import TransactionManager
from time import time

class ModbusBuffer:
    def __init__(self, context, max_size: int = 5000):
        self.context = context
        self.max_size = max_size

        self.singles_lock = Lock()
        self.commands_lock = Lock()
        
        self.slot_name = "modbus_variables"

        self.convert = {
            "x": lambda x: x * 0.01,
            "y": lambda y: y * 0.01,
            "theta": lambda theta: theta * 0.001,
            "speed": lambda speed: speed * 5.0 / 4096.0,
            "rudder": lambda rudder: rudder * 5.0 / 4095.0 - 2.5
        }
        '''
        Keys:
            "x", "y", "theta", "speed", "rudder"
        Values:
            float
        '''

        self.tracer_buffers = {}
        '''
        Tracers hold modbus values over time for dot plots and stuff
        Tracer elements: 

            "x_in", "y_in", "theta_in", "speed_in", "rudder_in": list[tuple[time,value]]
            "x_out", "y_out", "theta_out", "speed_out", "rudder_out": list[tuple[time,value]]
        '''
        for var in ["x", "y", "theta", "speed", "rudder"]:
            for dir in ["in", "out", "other"]:
                key = f"{var}_{dir}"
                self.tracer_buffers[key] = {
                    "deque": deque(maxlen=self.max_size),
                    "lock": Lock()
                }
        self.stripchart_buffers = {}
        self.stripchart_locks = {}
        self.singles = {}
        self.single_times = {}
        self.commands = {}
        self.reset()

    def reset(self):
        for var_name in self.context.states[self.slot_name]:
            for dir in ["in", "out"]:
                key = f"{var_name}_{dir}"
                self.stripchart_buffers[key] = deque(maxlen=self.max_size)
                self.stripchart_locks[key] = Lock()
                self.singles[key] = "-"
                self.single_times[key] = time()
            self.commands[var_name] = "-"

    def put(self, mpkt: MetaPacket):
        # only one update/entry per useful (read response / write request) and primary (first to be put())
        if not mpkt.is_modbus or len(mpkt.variables) < 1 or len(mpkt.variables) < 1 or not mpkt.is_useful_modbus or not mpkt.is_primary_modbus:
            return

        for i, var in enumerate(mpkt.variables):
            key = f"{var}_{mpkt.direction}"
            with self.stripchart_locks[key]:
                self.stripchart_buffers[key].append((mpkt.time, mpkt.values[i]))
            with self.singles_lock:
                self.singles[key] = mpkt.values[i]
                self.single_times[key] = time()
            with self.commands_lock:
                self.commands[var] = mpkt.command_word

        # TODO consider doing a dump so locks only engage once instead of 60 times
    def get_single(self, variable: str, direction: str) -> str:
        with self.singles_lock:
            value = self.singles[f"{variable}_{direction}"]
        return value

    def get_time(self, variable: str, direction: str) -> float:
        with self.singles_lock:
            value = self.single_times[f"{variable}_{direction}"]
        return value

    def get_command(self, variable: str) -> str:
        with self.commands_lock:
            value = self.commands[variable]
        return value

    def get_tracer_data(self, variable: str, direction: str) -> list[tuple[float,float]]:
        '''
        Returns a list of (time, value) tuples for the given variable and direction.
        '''
        with self.tracer_buffers[f"{variable}_{direction}"]["lock"]:
            snapshot = list(self.tracer_buffers[f"{variable}_{direction}"]["deque"])
        return snapshot

    def extract_variables(self, pkt: Packet) -> tuple[list[str], list[float]]:
        variables = []
        values = []

        slot = self.context.states[self.slot_name]

        if pkt.haslayer(ModbusPDU03ReadHoldingRegistersResponse):
            mbl = pkt.getlayer(ModbusADUResponse)
            mbl.payload.registerVal
            variables = ["speed"]
            mbl = pkt.getlayer(ModbusADUResponse)
            values = [self.convert["speed"](mbl.payload.registerVal[0])]

            if len(mbl.payload.registerVal) > 1:
                variables.append("rudder")
                values.append(self.convert["rudder"](mbl.payload.registerVal[1]))

        elif pkt.haslayer(ModbusPDU06WriteSingleRegisterRequest):
            mbl = pkt.getlayer(ModbusADURequest)
            if mbl.payload.registerAddr == 10: # X address
                var = "x"
            elif mbl.payload.registerAddr == 11: # Y address
                var = "y"
            else: # Theta address
                var = "theta"

            z = mbl.payload.registerValue

            variables = [var]
            values = [self.convert[var](z)]
        
        else:
            variables = []
            values = []

        return variables, values
        



    
        #     self.tracer_buffers = {}
        # '''
        # Tracers hold modbus values over time for dot plots and stuff
        # Tracer elements: 

        #     "x_in", "y_in", "theta_in", "speed_in", "rudder_in": list[tuple[time,value]]
        #     "x_out", "y_out", "theta_out", "speed_out", "rudder_out": list[tuple[time,value]]
        # '''
        # for var in ["x", "y", "theta", "speed", "rudder"]:
        #     for dir in ["in", "out", "other"]:
        #         key = f"{var}_{dir}"
        #         self.tracer_buffers[key] = {
        #             "deque": deque(maxlen=self.max_size),
        #             "lock": Lock()
        #         }
    


from scapy.contrib.modbus import ModbusADURequest, ModbusADUResponse
from scapy.all import Packet

# Safely decodes and modifies modbus packets. 

'''
useful pkt info:
pkt.summary()
modbus_layer.funcCode
modbus_layer.payload
'''

func_meanings = {
    1: "Read Coils",
    2: "Read Discrete Inputs",
    3: "Read Holding Registers",
    4: "Read Input Registers",
    5: "Write Single Coil",
    6: "Write Single Register",
    15: "Write Multiple Coils",
    16: "Write Multiple Registers"
}

register_meanings = {
    3: "Speed Feedback",    # 12-bit count Bytes = X*5/4095
    4: "Rudder Feedback",   # 12-bit count Bytes = X*30/4095
    10: "X Position",       # Bytes = meters*100
    11: "Y Position",       # meters*100
    12: "Theta (Heading)"   # milli-radians
}

def is_modbus(self, pkt: Packet) -> bool:
    '''
    Returns True if pkt has a ModBus layer. Returns False otherwise

    '''
    return pkt.haslayer(ModbusADURequest) or pkt.haslayer(ModbusADUResponse)

def is_commands(pkt: Packet) -> bool:
    '''
    Returns True if pkt has a "Read Holding Registers Response" layer. Returns False otherwise
    '''
    if not is_modbus(pkt):
        return False
    return pkt.haslayer("Read Holding Registers Response")

def get_commands(pkt: Packet) -> list:
    '''
    Returns payload.registerVal[] from the ModbusADUResponse layer of pkt if it is a command. Returns False otherwise

    [0] is speed

    [1] is rudder
    '''
    if not is_commands(pkt):
        return False
    mbl = pkt.getlayer(ModbusADUResponse)
    return mbl.payload.registerVal

def get_speed(pkt: Packet) -> int:
    '''
    Returns the speed command from a "Read Holding Registers Response" packet. Returns False if not available
    '''
    return get_commands(pkt)[0]

def set_speed(pkt, new):
    if not is_commands(pkt):
        return False
    mbl = pkt.getlayer(ModbusADUResponse)
    pl = getattr(mbl, "payload", "?")
    rv = getattr(pl, "registerVal", "?")
    rv[0] = new
    setattr(pl, "registerVal", rv)
    return pkt

def get_rudder(pkt):
    return get_commands(pkt)[1]

def set_rudder(pkt, new):
    if not is_commands(pkt):
        return False
    mbl = pkt.getlayer(ModbusADUResponse)
    pl = getattr(mbl, "payload", "?")
    rv = getattr(pl, "registerVal", "?")
    rv[1] = new
    setattr(pl, "registerVal", rv)
    return pkt




# If packet is coords (xyt). This is the useful one to mod
def is_coord(pkt):
    if not is_modbus(pkt):
        return False
    if pkt.haslayer("Write Single Register"):
        return True

def get_coord(pkt):
    if not is_coord(pkt):
        return "?"
    mbl = pkt.getlayer(ModbusADURequest)
    pl = getattr(mbl, "payload", "?")
    return getattr(pl, "registerValue", "?")

def set_coord(pkt, new):
    if not is_coord(pkt):
        return False
    mbl = pkt.getlayer(ModbusADURequest)
    pl = getattr(mbl, "payload", "?")
    setattr(pl, "registerValue", new)
    return pkt

def is_x(pkt):
    if not is_coord(pkt):
        return False
    mbl = pkt.getlayer(ModbusADURequest)
    pl = getattr(mbl, "payload", "?")
    if getattr(pl, "registerAddr", "?") == 10:
        return True
    else:
        return False

def is_y(pkt):
    if not is_coord(pkt):
        return False
    mbl = pkt.getlayer(ModbusADURequest)
    pl = getattr(mbl, "payload", "?")
    if getattr(pl, "registerAddr", "?") == 11:
        return True
    else:
        return False

def is_theta(pkt):
    if not is_coord(pkt):
        return False
    mbl = pkt.getlayer(ModbusADURequest)
    pl = getattr(mbl, "payload", "?")
    if getattr(pl, "registerAddr", "?") == 12:
        return True
    else:
        return False


def get_transId(pkt):
    if not is_modbus(pkt):
        return "?"
    mbl = pkt.getlayer(ModbusADURequest) or pkt.getlayer(ModbusADUResponse)
    return getattr(mbl, "transId", "?")




def print_scannable(pkt, show_transId = False, show_x = True, show_y = True, show_theta = True, show_speed = True, show_rudder = True, convert = False, print_to_console = True):

    if not (is_commands(pkt) or is_coord(pkt)):
        return

    out = ""

    if show_transId:
        out += f"ID: {get_transId(pkt)}  "
    
    if show_x:
        out += "X:"
        if is_x(pkt):
            x = get_coord(pkt)
            if convert:
                x = x/100.0
                out += f"{x:>6.2f}"
            else:
                out += f"{x:>6}"
        else:
            out += " "*6

    if show_y:
        out += "  Y:"
        if is_y(pkt):
            y = get_coord(pkt)
            if convert:
                y = y/100.0
                out += f"{y:>6.2f}"
            else:
                out += f"{y:>6}"
        else:
            out += " "*6

    if show_theta:
        out += "  Theta:"
        if is_theta(pkt):
            t = get_coord(pkt)
            if convert:
                t = (t/100.0)
                out += f"{t:>6.2f}"
            else:
                out += f"{t:>6}"
        else:
            out += " "*6
    
    if show_speed:
        out += "  Speed:"
        if is_commands(pkt):
            s = get_speed(pkt)
            if convert:
                s = (s/4095.0) * 5.0
                out += f"{s:>6.4f}"
            else:
                out += f"{s:>6}"
        else:
            out += " "*6

    if show_rudder:
        out += "  Rudder:"
        if is_commands(pkt):
            r = get_rudder(pkt)
            if convert:
                r = (r/4095.0) * 30.0
                out += f"{r:>2.3}"
            else:
                out += f"{r:>6}"
        else:
            out += " "*6
    if print_to_console:
        print(out)
    else:
        return out

