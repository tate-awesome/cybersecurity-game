from collections import deque
from threading import Lock
import time as Time
from . import Modbus as mb
from .Modbus import bytes_to_units as convert

data_size: int = 5000
number = 1


trails = {}
'''
Keys:
    x_in, y_in, theta_in, speed_in, rudder_in,
    x_out, y_out, theta_out, speed_out, rudder_out,
    packets_in, packets_out

Values:
    Dict:
        "deque":
            For variables:
                Tuple: (value: int, time: float, number: int)
            For packets:
                Tuple: (packet: Packet, time: float, number: int)
        "lock": Lock()
    
'''
for var in ["x", "y", "theta", "speed", "rudder", "packets"]:
    for dir in ["in", "out"]:
        key = f"{var}_{dir}"
        trails[key] = {
            "deque": deque(maxlen=data_size), # queue as tuple(var, time, number)
            "lock": Lock()
        }

# NFQ side - setters

def put(pkt, modified):
    '''
    Puts the packet and its variable(s) into the appropriate deques.
    Params:
        pkt: the packet to be queued
        modified: (True = forwarded/out, False = received/in)
    '''
    global number

    # Get time for matching deque times
    current_time = Time.time()

    # Determine source
    if modified:
        source = "out"
    else:
        source = "in"

    # Get variable from pkt
    if mb.is_x(pkt):
        variable = "x"
        value = mb.get_coord(pkt)
    elif mb.is_y(pkt):
        variable = "y"
        value = mb.get_coord(pkt)
    elif mb.is_theta(pkt):
        variable = "theta"
        value = mb.get_coord(pkt)
    elif mb.is_commands(pkt):
        # Do speed first
        values = mb.get_commands(pkt)
        with trails[f"speed_{source}"]["lock"]:
            trails[f"speed_{source}"]["deque"].append((values[0], current_time, number))
        # Do rudder with the rest
        variable = "rudder"
        value = values[1]
    else:
        variable = "None"
        value = "None"

    # Lock and store value

        # Write single register response and read holding registers request aren't useful (for now)
    if not variable == "None" and not value == "None":
        with trails[f"{variable}_{source}"]["lock"]:
            trails[f"{variable}_{source}"]["deque"].append((value, current_time, number))
    
    # Lock and store packet

    with trails[f"packets_{source}"]["lock"]:
        trails[f"packets_{source}"]["deque"].append((pkt, current_time, number))


    # Update number
    number = number + 1


def clear():
    '''
    Clears all deques
    '''
    for var in ["x", "y", "theta", "speed", "rudder", "packets"]:
        for dir in ["in", "out"]:
            trails[f"{var}_{dir}"]["deque"].clear()
    return

# GUI side - getters

def get_last_xyt(dir: str):
    '''
    Returns the latest boat position and bearing, in meters and radians. Useful for drawing the boat sprite.
    X and y should be between 0 and 200. Theta is in radians
    Returns:
        list: [x, y, theta]
        OR
        False, if any are missing
    '''
    vars = []
    for var in ["x", "y", "theta"]:
        with trails[f"{var}_{dir}"]["lock"]:
            if len(trails[f"{var}_{dir}"]["deque"]) < 1:
                return False
            else:
                vars.append(trails[f"{var}_{dir}"]["deque"][-1][0])
    # All variables added
    vars[0] = convert.x(vars[0])
    vars[1] = convert.y(vars[1])
    vars[2] = convert.theta_rad(vars[2])
    # NEXT FLAG what is theta really?
    return vars

def get_last(var, dir):
    '''
    Returns the last item in the deque for the given variable and direction.

    Returns:
        tuple: (value, time, number)
    '''
    with trails[f"{var}_{dir}"]["lock"]:
        if len(trails[f"{var}_{dir}"]["deque"]) < 1:
            return None
        value = trails[f"{var}_{dir}"]["deque"][-1]
    return value

def get_trail(var, dir):
    '''
    Returns a copy of the full deque for the variable and direction. Useful for drawing the history of a value.

    Param:
        var: (x, y, theta, speed, rudder, packets)
        dir: (in, out)

    Returns:
        list: tuple: (value, time, number)
    '''
    with trails[f"{var}_{dir}"]["lock"]:
        snapshot = list(trails[f"{var}_{dir}"]["deque"])
    return snapshot

def get_knit_packets():
    '''
    Returns a list of received and forwarded packet tuples, sorted by time.
    Useful for the wireshark clone.

    Returns:
        list:
            tuple: (packet, time, number, direction)
    '''
    # with trails["packets_in"]["lock"]:
    #     snapshot_in = list(trails["packets_in"]["deque"])
    # with trails["packets_out"]["lock"]:
    #     snapshot_out = list(trails["packets_out"]["deque"])
    snapshot_in = get_trail("packets","in")
    snapshot_out = get_trail("packets", "out")

    # Add direction field to each packet
    snapshot_in = [(pkt, ts, num, "in") for pkt, ts, num in snapshot_in]
    snapshot_out = [(pkt, ts, num, "out") for pkt, ts, num in snapshot_out]

    # Merge and sort by timestamp
    all_packets = snapshot_in + snapshot_out
    all_packets.sort(key=lambda x: x[1])  # sort by timestamp

    return all_packets

def knit_xy(xs, ys):
        points = []
        j = 0
        last_y = None

        for x_val, x_time, _ in xs:
            # advance y pointer
            while j < len(ys) and ys[j][1] <= x_time:
                last_y = ys[j][0]
                j += 1
            if last_y is not None:
                points.append((convert.x(x_val), convert.y(last_y)))
        return points

def get_knit_coordinates_in():
    '''
    Returns a list of received coordinates, in meters. Useful for drawing boat paths.
    Returned values should be between 0 and 200.
    
    Returns:
        list (received):
            tuple:
                x, y
    '''
    x_in = get_trail("x", "in")
    y_in = get_trail("y", "in")

    

    received_coords = knit_xy(x_in, y_in)

    return received_coords


def get_knit_coordinates_out():
    '''
    Returns a list of forwarded coordinates, in meters. Useful for drawing boat paths.
    Returned values should be between 0 and 200.
    
    Returns:
        list (forwarded):
            tuple:
                x, y
    '''
    x_out = get_trail("x", "out")
    y_out = get_trail("y", "out")

    forwarded_coords = knit_xy(x_out, y_out)

    return forwarded_coords

def get_flat_coordinates():
    return
