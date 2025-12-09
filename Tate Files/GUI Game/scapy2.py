import os
from tkinter.filedialog import askopenfilename

from scapy.all import rdpcap
from scapy.contrib.modbus import *

import json


def get_register_string(func_code, payload):
    
    # Default string
    register_string = "No info"

    register_meanings = {
        3: "Speed Feedback",    # 12-bit count (X/4095)*5.0
        4: "Rudder Feedback",   # 12-bit count (X/4095)*30
        10: "X Position",       # meters*100
        11: "Y Position",       # meters*100
        12: "Theta (Heading)"   # milli-radians
    }
    if func_code == 6:
        register_addr = getattr(payload, "registerAddr", "?")
        register_value = getattr(payload, "registerValue", "?")
        register_name = register_meanings[register_addr]
        register_string = f"{register_name} = {register_value}"
        # Theta (Heading) = 3142

    elif func_code == 3 and type == "Request":
        start_addr = getattr(payload, "startAddr", "?")
        quantity = getattr(payload, "quantity", "?")    # Note: quantity is always and forever 2
        i = 1
        register_string = register_meanings[start_addr]
        while i <= quantity - 1:
            register_string += ", " + register_meanings[start_addr + i]
            i += 1
        # X Position, Y Position

    elif func_code == 3 and type == "Response":
        # Using straight registerVal is touchy.
        register_val = getattr(payload, "registerVal", "?")
        # if len(register_val) == 2:
            # We got the expected 2 register values
        register_string = register_val
        # else:
        #     modbus_layer.show()

        #     # We got the bad 4 register values and need to go manually
        #     raw_bytes = getattr(payload, "load", "?")  # or payload[Raw].load if needed
        #     pdu = raw_bytes[7:]              # skip MBAP header
        #     func_code = pdu[0]
        #     byte_count = pdu[1]

        #     register_bytes = pdu[2:2+byte_count]  # slice exactly the number of bytes reported
        #     register_string = [int.from_bytes(register_bytes[i:i+2], "big") for i in range(0, len(register_bytes), 2)]

        # modbus_layer.show()
    return register_string

def get_packet_info(pkt, pkt_data):
    
    pkt_info = dict()

    pkt_info["summary"] = pkt.summary()

    # Modbus should be request or response
    if (not pkt.haslayer(ModbusADURequest) and not pkt.haslayer(ModbusADUResponse)):
        return
    
    # Set layer to whatever returns
    modbus_layer = pkt.getlayer(ModbusADURequest) or pkt.getlayer(ModbusADUResponse)

    # request or response
    type = "Request" if pkt.haslayer(ModbusADURequest) else ("Response" if pkt.haslayer(ModbusADUResponse) else "Modbus")

    # transaction ID
    trans_id = getattr(modbus_layer, "transId", "?")

    # function code
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
    func_code = getattr(modbus_layer, "funcCode", "?")
    func_name = func_meanings[func_code]

    payload = getattr(modbus_layer, "payload", "?")

    # Change info based on func code
    register_string = get_register_string(func_code, payload)

    # Set info members: modbus_summary, modbus_layer, type, trans_id, func_code, 
    # func_name, payload, register_summary
    pkt_info["modbus_summary"] = f"{type} {trans_id}: {func_name}: {register_string}"
    pkt_info["modbus_layer"] = modbus_layer
    pkt_info["type"] = type
    pkt_info["trans_id"] = trans_id
    pkt_info["func_code"] = func_code
    pkt_info["func_name"] = func_name
    pkt_info["payload"] = payload
    pkt_info["register_summary"] = register_string

    return pkt_info

def create_tree_from_selected_pcap():
    # 1. Ask for file name
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    file_path = askopenfilename(
        initialdir=f"{BASE_DIR}../../Hardware Files",
        title="Select a file",
        filetypes=(("PCAP files", "*.pcap*"),)
    )

    # 2. Get every packet data
    packets = rdpcap(file_path)
    unpacked = []
    initial_time = 0
    for i, pkt in enumerate(packets):
        
        # "No.", "Time", "Source", "Destination", "Protocol", "Length", "Info"
        pkt_data = dict()
        # No.
        pkt_data["No."] = i

        # Time
        pkt_data["Time"] = getattr(pkt, "time", "?")
        
        # Source
        pkt_data["Source"] = getattr(pkt, "src", "?")

        # Destination
        pkt_data["Destination"] = getattr(pkt, "dst", "?")

        # Protocol
        def highest_layer(pkt):
            layer = pkt
            while hasattr(layer, "payload") and layer.payload:
                # If payload is just raw bytes, there are no more layers to decode
                if layer.payload.__class__.__name__ == "Raw":
                    break
                layer = layer.payload
            return layer.__class__.__name__
        pkt_data["Protocol"] = highest_layer(pkt)
        if (pkt.haslayer(ModbusADURequest) or pkt.haslayer(ModbusADUResponse)):
            pkt_data["Protocol"] = "Modbus/TCP"

        # Length
        pkt_data["Length"] = len(pkt)

        # Info --> modbus_summary, modbus_layer, type, trans_id, func_code, 
        #          func_name, payload, register_summary
        pkt_data["Info"] = get_packet_info(pkt, pkt_data)

        unpacked.append(pkt_data)

    # "No.", "Time", "Source", "Destination", "Protocol", "Length", "Info"
    return unpacked

def pretty_dict(obj, indent=0, indent_step=4):
    """
    Pretty-print dicts, lists, and primitive types in a JSON-like format.
    """
    space = " " * indent

    # Primitive values
    if isinstance(obj, (int, float, str, bool)) or obj is None:
        return repr(obj)

    # Dicts
    if isinstance(obj, dict):
        if not obj:
            return "{}"
        lines = ["{"]
        for i, (k, v) in enumerate(obj.items()):
            key_repr = repr(k)
            val_repr = pretty_dict(v, indent + indent_step, indent_step)
            lines.append(" " * (indent + indent_step) + f"{key_repr}: {val_repr},")
        lines.append(space + "}")
        return "\n".join(lines)

    # Lists / tuples
    if isinstance(obj, (list, tuple)):
        if not obj:
            return "[]"
        bracket_open = "[" if isinstance(obj, list) else "("
        bracket_close = "]" if isinstance(obj, list) else ")"
        lines = [bracket_open]
        for x in obj:
            lines.append(" " * (indent + indent_step) + pretty_dict(x, indent + indent_step, indent_step) + ",")
        lines.append(space + bracket_close)
        return "\n".join(lines)

    # Fallback (e.g., EDecimal)
    return repr(obj)


print(pretty_dict(create_tree_from_selected_pcap()))