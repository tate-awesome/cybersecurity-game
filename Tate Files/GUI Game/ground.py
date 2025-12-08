import os
from tkinter.filedialog import askopenfilename

from scapy.packet import Packet
from scapy.fields import ShortField, ByteField, FieldListField
from scapy.layers.inet import TCP
from scapy.all import bind_layers
from scapy.all import rdpcap
from scapy.contrib.modbus import *

class Modbus(Packet):
    name = "Modbus"
    fields_desc = [
        ShortField("Transaction_ID", 0),
        ShortField("Protocol_ID", 0),
        ShortField("Length", 0),
        ByteField("Unit_ID", 0),
        ByteField("Function_Code", 0),
        FieldListField("Data", None, ByteField("", 0),
                       length_from=lambda pkt: pkt.Length - 2)
    ]

bind_layers(TCP, Modbus, dport=502)
bind_layers(TCP, Modbus, sport=502)








BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = askopenfilename(
    initialdir=f"{BASE_DIR}../../Hardware Files",
    title="Select a file",
    filetypes=(("PCAP files", "*.pcap*"),)
)

# "No.", "Time", "Source", "Destination", "Protocol", "Length", "Info"
packets = rdpcap(file_path)
unpacked = []
initial_time = 0
for i, pkt in enumerate(packets):
    # print(pkt.summary())
    # pkt.show()
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

    # Info
    pkt_info = dict()
    pkt_data["Info"] = pkt_info

    pkt_info["summary"] = pkt.summary()
    if (pkt.haslayer(ModbusADURequest) or pkt.haslayer(ModbusADUResponse)):
        modbus_layer = pkt.getlayer(ModbusADURequest) or pkt.getlayer(ModbusADUResponse)

        # Info: request or response
        type = "Request" if pkt.haslayer(ModbusADURequest) else ("Response" if pkt.haslayer(ModbusADUResponse) else "Modbus")

        # Info: transaction ID
        trans_id = getattr(modbus_layer, "transId", "?")

        # Info: function code
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

        # Info: registers and values
        register_meanings = {
            3: "Speed Feedback",    # 12-bit count (X/4095)*5.0
            4: "Rudder Feedback",   # 12-bit count (X/4095)*30
            10: "X Position",       # meters*100
            11: "Y Position",       # meters*100
            12: "Theta (Heading)"   # milli-radians
        }
        payload = getattr(modbus_layer, "payload", "?")

        # Change info based on func code
        register_string = ""

        if func_code == 6:
            register_addr = getattr(payload, "registerAddr", "?")
            register_value = getattr(payload, "registerValue", "?")
            register_name = register_meanings[register_addr]
            register_string = f"{register_name} = {register_value}"
            print(f"{type} {trans_id}: {func_name}: {register_string}") 
            # Response: Write Single Register: Theta (Heading) = 3142

        elif func_code == 3 and type == "Request":
            start_addr = getattr(payload, "startAddr", "?")
            quantity = getattr(payload, "quantity", "?")    # Note: quantity is always and forever 2
            i = 1
            register_string = register_meanings[start_addr]
            while i <= quantity - 1:
                register_string += ", " + register_meanings[start_addr + i]
                i += 1
            print(f"{type} {trans_id}: {func_name}: {register_string}")
            # Request: Read Holding Registers: X Position, Y Position

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

            print(f"{type} {trans_id}: {func_name}: {register_string}")
            # modbus_layer.show()
        pkt_info["Info"] = f"{type} {trans_id}: {func_name}: {register_string}"

        # start_addr = getattr(modbus_layer, "startAddr", "?")
        # output_addr = getattr(payload, "outputAddr", "?")

        

        
        
        def decode_modbus(pkt):
            class simple_modbus:
                modbus_layer = pkt.getlayer(ModbusADURequest) or pkt.getlayer(ModbusADUResponse)
                func_code = getattr(modbus_layer, "funcCode", "?")
                command = modbus_layer.command()
                protocol_id = getattr(modbus_layer, "protoId", "?")
                length = getattr(modbus_layer, "len", "?")
                unit_id = getattr(modbus_layer, "unitId", "?")

                payload = getattr(modbus_layer, "payload", "?")
                func_code = getattr(payload, "funcCode", "?")
                start_addr = getattr(modbus_layer, "startAddr", "?")
                quantity = getattr(payload, "quantity", "?")

                output_addr = getattr(payload, "outputAddr", "?")
                output_value = getattr(payload, "outputValue", "?")

                modbus_layer.show()

            # transaction_id = modbus_layer
            # b1 = transaction_id.to_bytes(2, 'big')

            # # Protocol ID
            # protocol_id = modbus_layer.Protocol_ID
            # b2 = protocol_id.to_bytes(2, 'big')

            # # Units ID
            # unit_id = modbus_layer.Unit_ID
            # b3 = unit_id.to_bytes(1, 'big')

            # # Func Code
            # func_code = modbus_layer.funcCode
            # b4 = func_code.to_bytes(1, 'big')

            # # "Data"
            # modbus_body = modbus_layer.Data
            # print(modbus_body)

            # msg_type = type(modbus_layer).__name
            # print(pkt[Modbus])
            return simple_modbus
    

   
#    ['_PickleType', '__all_slots__', '__bool__', '__bytes__', '__class__', '__class_getitem__', '__contains__', '__deepcopy__', '__delattr__',
#  '__delitem__', '__dict__', '__dir__', '__div__', '__doc__', '__eq__', '__firstlineno__', '__format__', '__ge__', '__getattr__', 
# '__getattribute__', '__getitem__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__iterlen__', 
# '__le__', '__len__', '__lt__', '__module__', '__mul__', '__ne__', '__new__', '__nonzero__', '__orig_bases__', '__parameters__', '__rdiv__',
#  '__reduce__', '__reduce_ex__', '__repr__', '__rmul__', '__rtruediv__', '__setattr__', '__setitem__', '__setstate__', '__signature__', 
# '__sizeof__', '__slots__', '__static_attributes__', '__str__', '__subclasshook__', '__truediv__', '__weakref__', '_answered', '_command', 
# '_defrag_pos', '_do_summary', '_name', '_overload_fields', '_pkt', '_raw_packet_cache_field_value', '_resolve_alias', '_show_or_dump', 
# '_superdir', 'add_parent', 'add_payload', 'add_underlayer', 'aliastypes', 'answers', 'build', 'build_done', 'build_padding', 'build_ps', 
# 'canvas_dump', 'class_default_fields', 'class_default_fields_ref', 'class_dont_cache', 'class_fieldtype', 'class_packetfields', 
# 'clear_cache', 'clone_with', 'command', 'comment', 'copy', 'copy_field_value', 'copy_fields_dict', 'decode_payload_as', 'default_fields', 
# 'default_payload_class', 'delfieldval', 'deprecated_fields', 'direction', 'dispatch_hook', 'display', 'dissect', 'dissection_done', 
# 'do_build', 'do_build_payload', 'do_build_ps', 'do_dissect', 'do_dissect_payload', 'do_init_cached_fields', 'do_init_fields', 'dst', 
# 'explicit', 'extract_padding', 'fields', 'fields_desc', 'fieldtype', 'firstlayer', 'fragment', 'from_hexcap', 'get_field', 
# 'getfield_and_val', 'getfieldval', 'getlayer', 'guess_payload_class', 'hashret', 'haslayer', 'hide_defaults', 'init_fields', 
# 'iterpayloads', 'json', 'lastlayer', 'layers', 'lower_bonds', 'match_subclass', 'mysummary', 'name', 'original', 'overload_fields', 
# 'overloaded_fields', 'packetfields', 'parent', 'payload', 'payload_guess', 'pdfdump', 'post_build', 'post_dissect', 'post_dissection', 
# 'post_transforms', 'pre_dissect', 'prepare_cached_fields', 'process_information', 'psdump', 'raw_packet_cache', 'raw_packet_cache_fields',
#  'remove_parent', 'remove_payload', 'remove_underlayer', 'route', 'self_build', 'sent_time', 'setfieldval', 'show', 'show2', 'show_indent',
#  'show_summary', 'sniffed_on', 'sprintf', 'src', 'stop_dissection_after', 'summary', 'svgdump', 'time', 'type', 'underlayer', 
# 'upper_bonds', 'wirelen']