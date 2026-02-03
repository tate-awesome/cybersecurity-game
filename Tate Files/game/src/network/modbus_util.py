from scapy.contrib.modbus import ModbusADURequest, ModbusADUResponse
from scapy.all import Packet
from .mod_table import ModTable

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

def is_modbus(pkt: Packet) -> bool:
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


def modify_coord(pkt, table: ModTable):
    mbl = pkt.getlayer(ModbusADURequest)

    if mbl.payload.registerAddr == 10: # X address
        var = "x"
    elif mbl.payload.registerAddr == 11: # Y address
        var = "y"
    else: # Theta address
        var = "theta"

    z = mbl.payload.registerValue
    mult = table.get(var, "offset")
    offset = table.get(var, "offset")
    mbl.payload.registerValue = int(z * mult + offset)
    return pkt

def modify_commands(pkt, table: ModTable):
    mbl = pkt.getlayer(ModbusADUResponse)

    mult = table.get("speed", "mult")
    offset = table.get("speed", "offset")

    speed = mbl.payload.registerVal[0]
    mbl.payload.registerVal[0] = int(speed * mult + offset)

    mult = table.get("rudder", "mult")
    offset = table.get("rudder", "offset")

    rudder = mbl.payload.registerVal[1]
    mbl.payload.registerVal[1] = int(rudder * mult + offset)
    return pkt