from scapy.packet import Packet
from scapy.fields import ShortField, ByteField, FieldListField
from scapy.layers.inet import TCP
from scapy.all import bind_layers
from scapy.all import rdpcap
from scapy.contrib.modbus import *
# ModbusADURequest, ModbusADUResponse, ModbusPDU03ReadHoldingRegistersRequest


# Callback function for each packet
def print_packet(packet):
    print(packet.summary())  # prints a one-line summary of the packet

def print_full_packet(packet):
    packet.show()  # prints all layers and fields
    print("-" * 80)

# Start sniffing
# iface=None will sniff on the default interface
# count=0 means sniff indefinitely
# store=False avoids storing packets in memory

#sniff(iface=None, prn=print_full_packet, store=False)

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

func_meanings = {
            1: "Read Coils (0x01)",
            2: "Read Discrete Inputs (0x02)",
            3: "Read Holding Registers (0x03)",
            4: "Read Input Registers (0x04)",
            5: "Write Single Coil (0x05)",
            6: "Write Single Register (0x06)",
            15: "Write Multiple Coils (0x0F)",
            16: "Write Multiple Registers (0x10)"
        }

def filters(pkt):
    # out *= pkt.haslayer(Modbus)

    # Filter for packets with modbus layer
    if not (pkt.haslayer(ModbusADURequest) or pkt.haslayer(ModbusADUResponse)):
        return False
    
    # Get modbus layer
    adu = pkt.getlayer(ModbusADURequest) or pkt.getlayer(ModbusADUResponse)
    func_code = adu.funcCode
    pdu = adu.payload

    # Filter for ONLY code==3
    if func_code != 3:
        return False
    
    # Filter for packets with start addr
    # try:
    #     start = pdu.startAddr
    # except:
    #     return False
    
    # Filter for output address
    # try:
    #     outaddr = pdu.outputAddr
    # except:
    #     return False
    
    # Filter for register value
    try:
        regval = pdu.registerVal
    except:
        return False
    
    
    # If all pass
    return True


current_history = []
# Load packets from a pcapng file
def GET_HISTORY(path):
    packets = rdpcap(path)
    # Or full details
    for pkt in packets:
        # print_full_packet(pkt)
        # print(pkt.summary())
        if filters(pkt):
            
            # print("-"*40)
            
            # Get to the modbus
            modbus_layer = pkt.getlayer(ModbusADURequest) or pkt.getlayer(ModbusADUResponse)
            
            # Function code:
            # print(modbus_layer.funcCode)

            # Modbus body as a string
            # print(modbus_layer.command())

            # Modbus ADU (header) as members
            adu = modbus_layer
            # print("Transaction ID:", adu.transId)
            # print("Protocol ID   :", adu.protoId)
            # print("Length        :", adu.len)
            # print("Unit ID       :", adu.unitId)

            # Modbus PDU (body) as members
            pdu = adu.payload
            # print("Function Code :", pdu.funcCode)
            # print("Start Addr    :", pdu.startAddr)
            # print("Quantity      :", pdu.quantity)

            # print_full_packet(pkt)

            # Modbus PDU values values values!!
            # print("Output Addr   :", pdu.outputAddr)
            # print("Output Values :", pdu.outputValue)
            print("Register Value:", pdu.registerVal)
            print(pdu.registerVal[0])
            print(pdu.registerVal[1])
            focus = [15, 255]
            scale = 50
            x = pdu.registerVal[0]
            y = pdu.registerVal[1]
            x2 = (x - focus[0])*scale + 500
            y2 = (y - focus[1])*scale + 500
            current_history.append(x2)
            current_history.append(y2)

            # # Transaction IDp
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

# Print summary of each packet
# for pkt in packets:
#     



def decode_modbus(pkt):
    class simple_modbus:
        modbus_layer = pkt.getlayer(ModbusADURequest) or pkt.getlayer(ModbusADUResponse)
        func_code = modbus_layer.funcCode
        command = modbus_layer.command()
        protocol_id = modbus_layer.protoId
        length = modbus_layer.len
        unit_id = modbus_layer.unitId

        payload = modbus_layer.payload
        func_code = payload.funcCode
        start_addr = payload.startAddr
        quantity = payload.quantity

        output_addr = payload.outputAddr
        output_value = payload.outputValue

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




# print(parent.keys()) #get attributes
# Net = network_interface.Network_Interface("virtual")

def unpack(file_path):
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
        pkt_data["Info"] = pkt.summary()
        if (pkt.haslayer(ModbusADURequest) or pkt.haslayer(ModbusADUResponse)):
            simple_modbus = decode_modbus(pkt)
            if simple_modbus.command ==