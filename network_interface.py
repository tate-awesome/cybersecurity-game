import virtual_master
import virtual_slave
import math

class Network_Interface:
    def __init__(self, network_type):
        self.mod = Network_Interface.Mod()
        self.actual_packet_history = []
        self.propatated_packet_history = []
        self.actual_boat_history = []
        self.propagated_boat_history = []
        self.real_pos_history = []
        self.fake_pos_history = []
        self.current_real_direction = 0
        self.current_fake_direction = 0
        self.target = [0, 0]

        if network_type == "virtual":

            print("virtual network mode")

            boat_character = {
                "max_turning_rate": math.pi/2,  # Max angular speed (rad/s)
                "max_speed": 10,                 # Max speed (m/s)
                "max_stationary_turning_rate": 2 # Fallback turning rate when speed low
            }

            control_character = {
                "heading_correction": 0.5,  # Turning rate (rad/s) per rad of heading error
                "allowable_error": 1e-6,    # Margin of error on target/heading
                "speed_correction": 0.2,    # Speed (m/s) per meter of distance error
            }


            Slave = virtual_slave.Slave(0.2, boat_character, None)
            Master = virtual_master.Master(0.1, control_character, boat_character, None)

            def master_to_slave(packet):
                # print("master to slave")
                self.add_to_real_history("Master", "Slave", packet)
                
                self.target = Master.sub_target
                fake_packet = packet
                self.add_to_fake_history("Master", "Slave", fake_packet)
                Slave.receive_func(fake_packet)

            def slave_to_master(packet):
                # print("slave to master")
                self.add_to_real_history("Slave", "Master", packet)
                fake_packet = packet
                self.add_to_fake_history("Slave", "Master", fake_packet)
                Master.receive_func(fake_packet)
            
            Slave.send_func = slave_to_master
            Master.send_func = master_to_slave
        
        
    class Boat_State:
        timestamp: float
        x: int
        y: int
        dir: int
        rudder: int
        speed: int
        def __init__(self, time, x, y, dir, rud, spe):
            self.timestamp = time
            self.x = x
            self.y = y
            self.dir = dir
            self.rudder = rud
            self.speed = spe

    # Holds all packet altering data
    # Only use these methods and members to change propagating packets
    class Mod:
        def __init__(self):
            self.rudder_scale = 1.0
            self.rudder_offset = 0.0
            self.speed_scale = 1.0
            self.speed_offset = 0.0

            self.x_scale = 1.0
            self.x_offset = 0.0
            self.y_scale = 1.0
            self.y_offset = 0.0
            self.dir_scale = 1.0
            self.dir_offset = 0.0

        def rudder(self, scale, offset):
            self.rudder_scale = scale
            self.rudder_offset = offset

        def speed(self, scale, offset):
            self.speed_scale = scale
            self.speed_offset = offset
        
        def x(self, scale, offset):
            self.x_scale = scale
            self.x_offset = offset

        def y(self, scale, offset):
            self.y_scale = scale
            self.y_offset = offset

        def dir(self, scale, offset):
            self.dir_scale = scale
            self.dir_offset = offset
            
        
    def add_to_real_history(self, origin, destination, modbus_body):
        # print(f"{origin}\t-->\t{destination}\t\t{modbus_body.hex(' ')}")
        packet = bytearray(modbus_body)
        if origin == "Slave" and packet[1] == 0x04:
            packet_x = -1
            packet_y = -1
            packet_dir = -1
            packet_dir = int.from_bytes(packet[3:5], "big")
            packet_x = int.from_bytes(packet[5:7], "big")
            packet_y = int.from_bytes(packet[7:9], "big")
            # self.Boat_State(time.time(), packet_x, packet_y, packet_dir, 0, 0)
            if len(self.real_pos_history) == 0:
                self.real_pos_history.append(packet_x)
                self.real_pos_history.append(packet_y)
            elif self.real_pos_history[-2] != packet_x or self.real_pos_history[-1] != packet_y:
                self.real_pos_history.append(packet_x)
                self.real_pos_history.append(packet_y)
            self.current_real_direction = packet_dir
        return
    def add_to_fake_history(self, origin, destination, modbus_body):
        packet = bytearray(modbus_body)
        if origin == "Slave" and packet[1] == 0x04:
            packet_x = -1
            packet_y = -1
            packet_dir = -1
            packet_dir = int.from_bytes(packet[3:5], "big")
            packet_x = int.from_bytes(packet[5:7], "big")
            packet_y = int.from_bytes(packet[7:9], "big")
            # self.Boat_State(time.time(), packet_x, packet_y, packet_dir, 0, 0)
            if len(self.fake_pos_history) == 0:
                self.fake_pos_history.append(packet_x)
                self.fake_pos_history.append(packet_y)
            elif self.fake_pos_history[-2] != packet_x or self.fake_pos_history[-1] != packet_y:
                self.fake_pos_history.append(packet_x)
                self.fake_pos_history.append(packet_y)
            self.current_fake_direction = packet_dir
        return
    
