            self.convert = {
            "x": lambda x: x * 0.01,
            "y": lambda y: y * 0.01,
            "theta": lambda theta: theta * 0.001,
            "speed": lambda speed: speed * 5.0 / 4096.0,
            "rudder": lambda rudder: rudder * 5.0 / 4095.0 - 2.5
        }
        '''
        Keys:
            "x", "y", "theta", "speed", "rudder"
        Values:
            float
        '''

    
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
    
    
    def extract_agnostic_modbus(self, source: str, pkt: Packet) -> tuple[list[str], list[float]]:
        variables = []
        values = []

        

        if pkt.haslayer("Read Holding Registers Response"):
            variables = ["speed"]
            mbl = pkt.getlayer(ModbusADUResponse)
            values = [self.convert["speed"](mbl.payload.registerVal[0])]

            if len(mbl.payload.registerVal) > 1:
                variables.append("rudder")
                values.append(self.convert["rudder"](mbl.payload.registerVal[1]))

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
            values = [self.convert[var](z)]
        
        else:
            variables = []
            values = []

        return variables, values


   def extract_modbus(self, source: str, pkt: Packet) -> tuple[list[str], list[float]]:
        '''
        Returns the modbus variables and values in the packet.
        If there's no modbus, return empty lists
        '''
        # Extract variables
        if pkt.haslayer("Read Holding Registers Response"):
            variables = ["speed"]
            mbl = pkt.getlayer(ModbusADUResponse)
            values = [self.convert["speed"](mbl.payload.registerVal[0])]

            if len(mbl.payload.registerVal) > 1:
                variables.append("rudder")
                values.append(self.convert["rudder"](mbl.payload.registerVal[1]))

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
            values = [self.convert[var](z)]
        
        else:
            variables = []
            values = []

        return variables, values
