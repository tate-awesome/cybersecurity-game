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

class MapBuffer:
    def __init__(self, context, max_size: int = 5000):
        self.max_size = max_size
        self.context = context
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

            # Buffers for the map
        self.map_buffers = {}
        '''
        Map elements:
        "status_in", "status_out", "status_other":
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
        self.map_buffers["points_other"] = {
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
        self.map_buffers["status_other"] = {
            "latest_x": None,
            "latest_y": None,
            "segment": 0,
            "last_point": None,
        }
    
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
        if x is None or y is None:
            return None
        return (x, y)
    
    def get_simple_path(self, direction: str) -> list[tuple[float,float]]:
        '''
        Returns the path of points as a simple list of tuple[x,y]
        '''
        buffer = self.map_buffers[f"points_{direction}"]
        with buffer["lock"]:
            snapshot = list(buffer["deque"])
        return [(point["x"], point["y"]) for point in snapshot]

    def put(self, mpkt: MetaPacket):
        for i, variable in enumerate(mpkt.variables):
            self.put_position(variable, mpkt.direction, float(mpkt.values[i]), mpkt.time)
            with self.tracer_buffers[f"{variable}_{mpkt.direction}"]["lock"]:
                self.tracer_buffers[f"{variable}_{mpkt.direction}"]["deque"].append((mpkt.time, mpkt.values[i]))
        

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
