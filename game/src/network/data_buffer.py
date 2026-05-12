from collections import deque
from threading import Lock
import time as Time
from scapy.all import Packet, ARP, Ether
from . import modbus_util as modbus
from .meta_packet import MetaPacket, MetaStatus

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

        self.factors = {
            "x": 0.01,
            "y": 0.01,
            "theta": 0.001,
            "speed": 5.0 / 4096.0,
            "rudder": 5.0 / 4095.0
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

            "previous_trails_in": list[list[tuple[float,float]]]
            "previous_trails_out": list[list[tuple[float,float]]]
            "current_trail_in": list[tuple[float,float]]
            "current_trail_out": list[tuple[float,float]]

            "position_in": list[float,float,float]
            "position_out": list[float,float,float]
        '''
        for var in ["all_trails","current_trail"]:
            for dir in ["in", "out"]:
                key = f"{var}_{dir}"
                self.map_buffers[key] = {
                    "deque": list(),
                    "lock": Lock()
                }
        
        # Buffers for the tracers
        self.tracer_buffers = {}
        '''
        Tracer elements: 

            "x_in", "y_in", "theta_in", "speed_in", "rudder_in": list[tuple[float,float]]
            "x_out", "y_out", "theta_out", "speed_out", "rudder_out": list[tuple[float,float]]
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
        
        # Create a MetaPacket
        variables, values = self.extract_modbus(source, data)
        mpkt = MetaPacket(data, current_time, absolute_number, hack_number,
            source, purpose,
            variables, values)

        # Put MetaPacket in the buffer
        with self.console_buffers["packets"]["lock"]:
            self.console_buffers["packets"]["buffer"].append(mpkt)

        # TODO put in the tracer and map and stuff
        return

    def extract_modbus(self, source: str, pkt: Packet) -> tuple[list[str], list[float]]:
        '''
        Returns the modbus variables and values in the packet.
        If there's no modbus, return empty lists
        '''
        # Extract variables
        if pkt.haslayer("Read Holding Registers Response"):
            variables = ["speed"]
            mbl = pkt.getlayer(ModbusADUResponse)
            values = [mbl.payload.registerVal[0]*self.factors["speed"]]

            if len(mbl.payload.registerVal) > 1:
                variables.append("rudder")
                values.append(mbl.payload.registerVal[1]*self.factors["rudder"])

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
            values = [z*self.factors[var]]
        
        else:
            variables = []
            values = []

        return variables, values
    
    # Console
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