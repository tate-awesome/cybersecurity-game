from collections import deque
from threading import Lock
import time as Time
from scapy.all import Packet
from . import modbus_util as modbus
from .meta_packet import MetaPacket

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
        self.packet_number = 1
        self.start_time = Time.time()

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

        self.console_buffers = {}
        '''
        Console elements:

            "nmap": MetaPacket or str

            "arp": MetaPacket or dict[str,str]

            "sniff": MetaPacket

            "dos": ?

            "mitm": ?
        '''
        for key in ["nmap", "arp", "sniff", "dos", "mitm"]:
            self.console_buffers[key] = {
                "deque": deque(maxlen=self.max_size),
                "lock": Lock()
            }

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
        # Variable seismographs
        # Time-separated boat position trails
        # Sniffer puts MetaPackets
        # NMAP results
        # ARP lines

    def put(self, source: str, purpose: str, data: Packet or list[str]):
        if source == "nmap":
            print("\n\n")
            print(purpose)
            if isinstance(data, Packet):
                data.summary()
                data.show()
            elif isinstance(data, list) and all(isinstance(s, str) for s in data):
                print("ste")
                print("\t".join(data))

    def put_packet(self, pkt: Packet, dir: str):
        '''
        Processes the packet.
        '''

        # Get time for matching deque times
        current_time = Time.time() - self.start_time

        # Get variable from pkt
        if modbus.is_x(pkt):
            variable = "x"
            value = modbus.get_coord(pkt)
        elif modbus.is_y(pkt):
            variable = "y"
            value = modbus.get_coord(pkt)
        elif modbus.is_theta(pkt):
            variable = "theta"
            value = modbus.get_coord(pkt)
        elif modbus.is_commands(pkt) and len(modbus.get_commands(pkt)) > 1:
            # Do speed first
            values = modbus.get_commands(pkt)
            with self.trails[f"speed_{dir}"]["lock"]:
                self.trails[f"speed_{dir}"]["deque"].append((values[0], current_time, self.number))
            # Do rudder with the rest
            variable = "rudder"
            value = values[1]
        else:
            variable = "None"
            value = "None"

        # Lock and store value

            # Write single register response and read holding registers request aren't useful (for now)
        if not variable == "None" and not value == "None":
            with self.trails[f"{variable}_{dir}"]["lock"]:
                self.trails[f"{variable}_{dir}"]["deque"].append((value, current_time, self.number))
        
        # Lock and store packet
        with self.trails[f"packets_{dir}"]["lock"]:
            self.trails[f"packets_{dir}"]["deque"].append((pkt, current_time, self.number))

        # Do callbacks
        for cb in list(self.packet_callbacks.values()):
            mpkt = MetaPacket(pkt, current_time, self.number, dir, variable, value)
            self.executor.submit(cb, mpkt)
        # Update number
        self.number = self.number + 1


    def clear(self):
        '''
        Clears all deques
        '''
        for var in ["x", "y", "theta", "speed", "rudder", "packets"]:
            for dir in ["in", "out"]:
                self.trails[f"{var}_{dir}"]["deque"].clear()


    def get_trail(self, var: str, dir: str):
        '''
        Returns a copy of the full deque for the variable and direction.

        May return an empty deque.

        Param:
            var: (x, y, theta, speed, rudder, packets)
            dir: (in, out)

        Returns:
            list: tuple: (value|packet, time, number)
        '''
        with self.trails[f"{var}_{dir}"]["lock"]:
            snapshot = list(self.trails[f"{var}_{dir}"]["deque"])
        return snapshot


    def get_last_tuple(self, var: str, dir: str) -> None | tuple[Packet | int, float, int]:
        '''
        Returns the last tuple in the deque for the given variable and direction.

        Returns None if the deque is empty.

        Returns:
            tuple: value|packet, time, number
        '''
        trail = self.get_trail(var, dir)
        if len(trail) < 1:
            return None
        else:
            return trail[-1]


    def get_last_position(self, dir: str, convert=True):
        '''
        Returns the latest boat position, in meters. Useful for drawing the boat sprite.
        X and y should be between 0 and 200.
        Returns:
            list: [x, y]
            OR
            None, if any are missing
        '''
        values = []
        for var in ["x", "y"]:
            last_tuple = self.get_last_tuple(var, dir)
            if last_tuple == None:
                return None
            else:
                values.append(last_tuple[0] * self.factors[var] ** convert)

        return values

    def get_last_bearing(self, dir: str, convert=True):
        bearing = self.get_last_tuple("theta", dir)
        if bearing is None:
            return None
        if convert:
            return bearing[0] * self.factors["theta"]
        else:
            return bearing[0]

    def get_all_positions(self, dir: str, convert=True, flatten=False):
        '''
        Returns a list of all previous boat positions by assigning the last y to every x value.

        Returns:
            if flatten:
                list: [x0, xy0, x1, y1,...]
            else:
                list: [tuple(x0, y0), tuple(x1, y1), ...]
        '''
        points = []
        j = 0
        last_y = None

        xs = self.get_trail("x", dir)
        ys = self.get_trail("y", dir)

        for x_val, x_time, _ in xs:

            while j < len(ys) and ys[j][1] <= x_time:
                last_y = ys[j][0]
                j += 1
            if last_y is not None:
                next = (x_val * (self.factors["x"] ** convert) , last_y * (self.factors["y"] ** convert))
                if flatten:
                    points.extend(next)
                else:
                    points.append(next)

        return points


# def get_knit_packets():
#     '''
#     Returns a list of received and forwarded packet tuples, sorted by time.
#     Useful for the wireshark clone.

#     Returns:
#         list:
#             tuple: (packet, time, number, direction)
#     '''
#     # with trails["packets_in"]["lock"]:
#     #     snapshot_in = list(trails["packets_in"]["deque"])
#     # with trails["packets_out"]["lock"]:
#     #     snapshot_out = list(trails["packets_out"]["deque"])
#     snapshot_in = get_trail("packets","in")
#     snapshot_out = get_trail("packets", "out")

#     # Add direction field to each packet
#     snapshot_in = [(pkt, ts, num, "in") for pkt, ts, num in snapshot_in]
#     snapshot_out = [(pkt, ts, num, "out") for pkt, ts, num in snapshot_out]

#     # Merge and sort by timestamp
#     all_packets = snapshot_in + snapshot_out
#     all_packets.sort(key=lambda x: x[1])  # sort by timestamp

#     return all_packets