'''
The map buffer builds structures that can be easily displayed on the map.
It receives data from ModbusBuffer.
in position
out position
in path
out path
in bearing
out bearing

'''

from threading import Lock
from collections import deque
from math import hypot
from ..meta_packet import MetaPacket
from .modbus import ModbusBuffer

class MapBuffer:
    '''
    Buffer specific to the submarine model widget.
    Uses ModBusBuffer to get single values
    Builds its own ready to use deques for paths

    "simple" - deque[tuple[x: float, y: float]] - ready to draw line on canvas
                built by putting two new coordinates in each tuple
    "segments" - deque[list[tuple[x: float, y: float]]] - collection of lists of tuples, to represent discontinuities
    '''
    def __init__(self, context, modbuffer: ModbusBuffer, max_size: int = 5000):
        self.max_size = max_size
        self.context = context
        self.modbuffer = modbuffer

        self.variables = {
            "speed": "hreg_3",
            "rudder": "hreg_4",
            "x": "hreg_10",
            "y": "hreg_11",
            "theta": "hreg_12"
        }

        self.registers = {value: key for key, value in self.variables.items()}

        self.factors = {
            "speed": 0.00122,
            "rudder": 0.00122,
            "x": 0.01,
            "y": 0.01,
            "theta": 0.001
        }

        self.path_buffers = {}
        self.path_locks = {}
        self.reset()

    def reset(self):
        self.path_buffers = {
            "point_in": list(),
            "simple_in": deque(),
            "segment_in": deque(),
            "segments_in": deque(),
            "point_out": list(),
            "simple_out": deque(),
            "segment_out": deque(),
            "segments_out": deque()
        }
        self.path_locks = {
            "simple": Lock(),
            "segment": Lock(),
            "segments": Lock()
        }
    
    def put(self, mpkt: MetaPacket):
        # Modbuffer already has the single values - bearing, rudder, speed
        # Only build paths here
        is_primary = mpkt.get("is_primary")
        is_useful = mpkt.get("is_useful")
        variables = mpkt.get("variables")
        values = mpkt.get("values")
        if is_useful and is_primary and len(variables) == 1 and len(values) == 1:
            if variables[0] in ["hreg_10", "hreg_11"]:
                variable = self.registers[variables[0]]
                direction = mpkt.get("direction")
                value = self.convert(variable, values[0])
                time = mpkt.get("time")
                self.put_path(variable, direction, value, time)

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

    # Boat getters
    def get_bearing(self, direction: str) -> float:
        '''
        Returns the latest theta value for the given direction, or "-" if there is no data.
        '''
        return self.get_single("theta", direction)
    
    def get_rudder(self, direction: str) -> float:
        '''
        Returns the latest rudder value for the given direction, or "-" if there is no data.
        '''
        return self.get_single("rudder", direction)
    
    def get_speed(self, direction: str) -> float:
        '''
        Returns the latest speed value for the given direction, or 0 if there is no data.
        '''
        return self.get_single("speed", direction)

    def get_all_histories_and_legends(self, variable: str) -> dict[str, list[tuple[float, float]]]:
        '''
        Returns every exchange-type bucket's history for one model variable
        (e.g. "speed"), translated to the underlying register and delegated to
        ModbusBuffer - same translation get_single() already does.
        '''
        register = self.variables[variable]
        return self.modbuffer.get_all_histories_and_legends(register)
    
    def get_position(self, direction: str) -> tuple[float,float]:
        '''
        Returns the latest (x, y) position for the given direction, or (0, 0) if there is no data.
        '''
        x = self.get_single("x", direction)
        y = self.get_single("y", direction)
        if x is None or y is None:
            return None
        return (x, y)

    # Path getters    
    def get_simple_path(self, direction: str) -> list[tuple[float,float]]:
        '''
        Returns the path of points as a simple list of tuple[x,y]
        '''
        with self.path_locks["simple"]:
            output = list(self.path_buffers[f"simple_{direction}"])
        return output

    def put_path(self, variable: str, direction: str, value: float, time: float):
        '''
        variable: "x" or "y"
        direction: "in" or "out"
        value: the converted value of the variable (0-200) meters
        time: the time the packet was received
        '''
        self.put_simple_path(variable, direction, value, time)
        
        # MAX_PAIR_DT = 0.25     # max x/y timestamp mismatch
        # MAX_GAP = 2.0          # seconds before segment break
        # MAX_SPEED = 40.0       # units/sec before segment break

        # status = self.map_buffers[f"status_{direction}"]

        # if variable == "x":
        #     status["latest_x"] = (value, time)

        # elif variable == "y":
        #     status["latest_y"] = (value, time)

        # else:
        #     return

        # latest_x = status["latest_x"]
        # latest_y = status["latest_y"]

        # # Need both before composing
        # if latest_x is None or latest_y is None:
        #     return

        # x, tx = latest_x
        # y, ty = latest_y

        # # Do not accept point pairs with wildly different timestamps
        # if abs(tx - ty) > MAX_PAIR_DT:
        #     return

        # # Use average time
        # point_time = (tx + ty) / 2.0

        # new_point = {
        #     "x": x,
        #     "y": y,
        #     "time": point_time,
        #     "segment": status["segment"],
        # }

        # last_point = status["last_point"]

        # if last_point is not None:

        #     dt = point_time - last_point["time"]

        #     # Time went backwards
        #     if dt <= 0:
        #         return

        #     dx = x - last_point["x"]
        #     dy = y - last_point["y"]

        #     distance = hypot(dx, dy)
        #     speed = float(distance) / float(dt)

        #     # Break track if:
        #     # - data gap too large
        #     # - impossible movement
        #     if dt > MAX_GAP or speed > MAX_SPEED:
        #         status["segment"] += 1
        #         new_point["segment"] = status["segment"]

        # buffer = self.map_buffers["points_"+direction]

        # with buffer["lock"]:
        #     buffer["deque"].append(new_point)

        # status["last_point"] = new_point

    def put_simple_path(self, variable: str, direction: str, value: float, time: float):
        point_key = f"point_{direction}"
        path_key = f"simple_{direction}"
        current_point = self.path_buffers[point_key]
        buffer = self.path_buffers[path_key]
        # No coords, put the value in\
        if len(current_point) < 1:
            # print(f"1: {current_point}")
            if variable == "x":
                current_point.append(value)
                current_point.append(None)
            else:
                current_point.append(None)
                current_point.append(value)
            # print(f"2: {current_point}")
        # In progress, put the value in, then submit and reset the point
        elif len(current_point) == 2:
            # print(f"3: {current_point}")
            if variable == "x" and current_point[0] is None:
                current_point[0] = value
            elif variable == "y" and current_point[1] is None:
                current_point[1] = value
            if current_point[0] is not None and current_point[1] is not None:
                # print(f"4: {current_point}")
                with self.path_locks["simple"]:
                    buffer.append(tuple(current_point))
                # print(time)
                self.path_buffers[point_key] = list()