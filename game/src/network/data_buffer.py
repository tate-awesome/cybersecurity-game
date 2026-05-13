from collections import deque
from threading import Lock
import time as Time
from scapy.all import Packet, ARP, Ether
from . import modbus_util as modbus
from .meta_packet import MetaPacket, MetaStatus
from math import hypot

from scapy.contrib.modbus import ModbusADURequest, ModbusADUResponse

# Tabview -> tab -> console -> update loop (100ms) pulls everything from buffer to display (print for now)
# Hack widget -> hack.start -> handler -> hack.put -> buffer["hack"].packet OR NMAP result OR ARP lines

# Map -> get_trails -> buffer.all_trails[list[list[tuple[float,float]]]] -> for each trail in trails drawline(trail)
# Also Hack widget -> hack.start -> handler -> var_buffer.put(x, y, t, s, r) -> if(last_time > 50): new trail, if(last_time > 50): break_variable_seismograph, if(t): last_t = t, if (x,y): last_xy = x, y,

class DataBuffer:
    '''
    Holds data from different network actions to be easily accessed by different GUI elements.
    '''
    def __init__(self, max_size = 5000):
        self.max_size = max_size
        self.start_time = Time.time()
        self.mac = ARP().hwsrc

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

        # Buffers for console use
        self.console_buffers = {}
        '''
        For the Console:
            "packets":
                "numbers": {
                    "absolute": n,
                    "this_hack": n
                }
                "buffer": deque[MetaPacket],
                "lock": Lock()
            "status":
                "number": n,
                "buffer": deque[MetaStatus],
                "lock": Lock()

        '''
        self.console_buffers["packets"] = {
                "numbers": {},
                "print_pointer": 0,
                "buffer": deque(maxlen=self.max_size),
                "lock": Lock()
            }
        for key in ["absolute", "nmap", "arp", "sniff", "dos", "mitm", "pcap"]:
            self.console_buffers["packets"]["numbers"][key] = 1
        self.console_buffers["status"] = {
            "number": 1,
            "print_pointer": 0,
            "buffer": deque(maxlen=self.max_size),
            "lock": Lock()
        }

        # Buffers for the map
        self.map_buffers = {}
        '''
        Map elements:
        "status_in", "status_out":
            "latest_x": (value, time) or None,
            "latest_y": (value, time) or None,
            "segment": int,
        "points_in", "points_out":
            "deque":
                {"x": float,
                "y": float,
                "time": float,
                "segment": int}
            "lock": Lock()
        '''
        self.map_buffers["points_in"] = {
            "deque": deque(maxlen=self.max_size),
            "lock": Lock()
        }
        self.map_buffers["points_out"] = {
            "deque": deque(maxlen=self.max_size),
            "lock": Lock()
        }
        self.map_buffers["status_in"] = {
            "latest_x": None,
            "latest_y": None,
            "segment": 0,
            "last_point": None,
        }
        self.map_buffers["status_out"] = {
            "latest_x": None,
            "latest_y": None,
            "segment": 0,
            "last_point": None,
        }
        
        # Buffers for the tracers
        self.tracer_buffers = {}
        '''
        Tracers hold modbus values over time for dot plots and stuff
        Tracer elements: 

            "x_in", "y_in", "theta_in", "speed_in", "rudder_in": list[tuple[time,value]]
            "x_out", "y_out", "theta_out", "speed_out", "rudder_out": list[tuple[time,value]]
        '''
        for var in ["x", "y", "theta", "speed", "rudder"]:
            for dir in ["in", "out"]:
                key = f"{var}_{dir}"
                self.tracer_buffers[key] = {
                    "deque": deque(maxlen=self.max_size),
                    "lock": Lock()
                }

    def put(self, source: str, purpose: str, data: Packet | None=None):
        '''
        Put status messages and packets into appropriate buffers.

        source: the network action - "nmap", "arp", "dos", "sniff", "mitm", "pcap"

        purpose: a message about the packet, or a status message
        '''
        # Set time
        current_time = Time.time() - self.start_time

        # Put status message in "status" buffer
        if not isinstance(data, Packet):
            try:
                meta_status = MetaStatus(source, purpose, current_time, self.console_buffers["status"]["number"])
                with self.console_buffers["status"]["lock"]:
                    self.console_buffers["status"]["buffer"].append(meta_status)
                self.console_buffers["status"]["number"] += 1
            except Exception:
                print(f"Failed to put {purpose}")
            finally:
                return
        
        # Set numbers for this packet
        absolute_number = self.console_buffers["packets"]["numbers"]["absolute"]
        self.console_buffers["packets"]["numbers"]["absolute"] = absolute_number+1
        hack_number = self.console_buffers["packets"]["numbers"][source]
        self.console_buffers["packets"]["numbers"][source] = hack_number+1
        
        # Calculate first packet time
        if absolute_number == 1:
            self.first_packet_time = data.time if hasattr(data, "time") else current_time

        # Create a MetaPacket
        variables, values = self.extract_modbus(source, data)
        mpkt = MetaPacket(data, self.first_packet_time, absolute_number, hack_number,
            source, purpose,
            variables, values)

        # Put MetaPacket in the buffer
        with self.console_buffers["packets"]["lock"]:
            self.console_buffers["packets"]["buffer"].append(mpkt)
        if len(variables) < 1 or len(values) < 1:
            return

        # Put variables in the tracer buffers
        for i, var in enumerate(variables):
            with self.tracer_buffers[f"{var}_{mpkt.direction}"]["lock"]:
                self.tracer_buffers[f"{var}_{mpkt.direction}"]["deque"].append((mpkt.time, values[i]))

        # Put x and y into the segments buffer
        if not "x" in variables and not "y" in variables:
            return
        self.put_position(variables[0], mpkt.direction, values[0], mpkt.time)

        return

    # Helper functions
    def extract_modbus(self, source: str, pkt: Packet) -> tuple[list[str], list[float]]:
        '''
        Returns the modbus variables and values in the packet.
        If there's no modbus, return empty lists
        '''
        # Extract variables
        if pkt.haslayer("Read Holding Registers Response"):
            variables = ["speed"]
            mbl = pkt.getlayer(ModbusADUResponse)
            values = [self.convert["speed"](mbl.payload.registerVal[0])]

            if len(mbl.payload.registerVal) > 1:
                variables.append("rudder")
                values.append(self.convert["rudder"](mbl.payload.registerVal[1]))

        elif pkt.haslayer("Write Single Register"):
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
    
    def put_position(self, variable: str, direction: str, value: float, time: float):
        '''
        variable: "x" or "y"
        direction: "in" or "out"
        value: the value of the variable (0-200)
        time: the time the variable was recorded, relative to the start of the program
        (put any data in the dict self.map_buffers. Each buffer has a "deque" and a "lock".)
        '''

        MAX_PAIR_DT = 0.25     # max x/y timestamp mismatch
        MAX_GAP = 2.0          # seconds before segment break
        MAX_SPEED = 40.0       # units/sec before segment break

        status = self.map_buffers[f"status_{direction}"]

        if variable == "x":
            status["latest_x"] = (value, time)

        elif variable == "y":
            status["latest_y"] = (value, time)

        else:
            return

        latest_x = status["latest_x"]
        latest_y = status["latest_y"]

        # Need both before composing
        if latest_x is None or latest_y is None:
            return

        x, tx = latest_x
        y, ty = latest_y

        # Do not accept point pairs with wildly different timestamps
        if abs(tx - ty) > MAX_PAIR_DT:
            return

        # Use average time
        point_time = (tx + ty) / 2.0

        new_point = {
            "x": x,
            "y": y,
            "time": point_time,
            "segment": status["segment"],
        }

        last_point = status["last_point"]

        if last_point is not None:

            dt = point_time - last_point["time"]

            # Time went backwards
            if dt <= 0:
                return

            dx = x - last_point["x"]
            dy = y - last_point["y"]

            distance = hypot(dx, dy)
            speed = float(distance) / float(dt)

            # Break track if:
            # - data gap too large
            # - impossible movement
            if dt > MAX_GAP or speed > MAX_SPEED:
                status["segment"] += 1
                new_point["segment"] = status["segment"]

        buffer = self.map_buffers["points_"+direction]

        with buffer["lock"]:
            buffer["deque"].append(new_point)

        status["last_point"] = new_point

    
    # Console getters
    def print_filtered_console_buffer(self, source: str, filter: callable):
        with self.console_buffers[source]["lock"]:
            snapshot = list(self.console_buffers[source]["mpkt"])
        for mpkt in snapshot:
            if filter(mpkt):
                print(mpkt)

    def print_status(self, source: str):
        with self.console_buffers[source]["lock"]:
            snapshot = list(self.console_buffers[source]["status"])
        for status in snapshot:
            print(status)
    
    def get_status(self) -> list[MetaStatus]:
        with self.console_buffers["status"]["lock"]:
            snapshot = list(self.console_buffers["status"]["buffer"])
        return snapshot
    
    def pop_status(self):
        with self.console_buffers["status"]["lock"]:
            if self.console_buffers["status"]["print_pointer"] < len(self.console_buffers["status"]["buffer"]):
                status = self.console_buffers["status"]["buffer"][self.console_buffers["status"]["print_pointer"]]
                self.console_buffers["status"]["print_pointer"] += 1
                return status
            else:
                return None
    
    def reset_status_print_pointer(self):
        with self.console_buffers["status"]["lock"]:
            self.console_buffers["status"]["print_pointer"] = 0

    def get_packets(self, filter: callable) -> list[MetaPacket]:
        with self.console_buffers["packets"]["lock"]:
            snapshot = list(self.console_buffers["packets"]["buffer"])

        return [mpkt for mpkt in snapshot if filter(mpkt)]
    
    def pop_packet(self, filter: callable) -> MetaPacket:
        with self.console_buffers["packets"]["lock"]:
            if self.console_buffers["packets"]["print_pointer"] < len(self.console_buffers["packets"]["buffer"]):
                packet = self.console_buffers["packets"]["buffer"][self.console_buffers["packets"]["print_pointer"]]
                self.console_buffers["packets"]["print_pointer"] += 1
                if filter(packet):
                    return packet
        return None
    
    # Displays getters
    def get_tracer_data(self, variable: str, direction: str) -> list[tuple[float,float]]:
        '''
        Returns a list of (time, value) tuples for the given variable and direction.
        '''
        with self.tracer_buffers[f"{variable}_{direction}"]["lock"]:
            snapshot = list(self.tracer_buffers[f"{variable}_{direction}"]["deque"])
        return snapshot
    
    def get_latest_value(self, variable: str, direction: str) -> float:
        '''
        Returns the latest value for the given variable and direction, or 0 if there is no data.
        '''
        snapshot = self.get_tracer_data(variable, direction)
        if len(snapshot) < 1:
            return 0
        return snapshot[-1][1]
    
    def get_bearing(self, direction: str) -> float:
        '''
        Returns the latest theta value for the given direction, or 0 if there is no data.
        '''
        return self.get_latest_value("theta", direction)
    
    def get_rudder(self, direction: str) -> float:
        '''
        Returns the latest rudder value for the given direction, or 0 if there is no data.
        '''
        return self.get_latest_value("rudder", direction)
    
    def get_speed(self, direction: str) -> float:
        '''
        Returns the latest speed value for the given direction, or 0 if there is no data.
        '''
        return self.get_latest_value("speed", direction)
    
    def get_position(self, direction: str) -> tuple[float,float]:
        '''
        Returns the latest (x, y) position for the given direction, or (0, 0) if there is no data.
        '''
        x = self.get_latest_value("x", direction)
        y = self.get_latest_value("y", direction)
        return (x, y)
    
    def get_simple_path(self, direction: str) -> list[tuple[float,float]]:
        '''
        Returns the path of points as a simple list of tuple[x,y]
        '''
        buffer = self.map_buffers[f"points_{direction}"]
        with buffer["lock"]:
            snapshot = list(buffer["deque"])
        return [(point["x"], point["y"]) for point in snapshot]