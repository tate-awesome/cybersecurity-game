


if network_type == "saved":
            print("saved network mode")
            sca.GET_HISTORY("Hardware Files\modbus_Traffic.pcapng")
            def refresh_history():
                print("Checking history...")
                self.real_pos_history = sca.current_history
                self.fake_pos_history = sca.current_history
                threading.Timer(1, refresh_history).start()
                # Reschedule the function to run again after 2 seconds
            threading.Timer(1, refresh_history).start()


            
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
            # if simple_modbus.command ==