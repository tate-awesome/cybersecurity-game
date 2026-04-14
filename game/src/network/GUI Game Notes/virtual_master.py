import threading
import random
import time
import math

class Master:
    def __init__(self, control_rate_s, control_character, boat_character, send_func):
        self.tick_rate = control_rate_s    # Downtime between instructions
        self.sub_target = [300, 300]        # Default target
        self.speed = 0                      # Default command
        self.rudder = 0                     # Default command
        self.request_packet = bytes([0x01, 0x04, 0x00, 0x00, 0x00, 0x03, 0xB0, 0x0B])
        self.send_func = send_func
          
        self.settings(control_character, boat_character)
        self.running = True                 # Run on init
        self.start()                        # Start
    
    def speed_packet(self, int_in):
        # Master send throttle command:
        # 01 06 00 01 02 58 D9 CB
        # -----------------------------
        # 01	Slave 1
        # 06	Write Single Register
        # 00 01	Register 1 (throttle)
        # 00 0F	Value 15
        # 89 CA	CRC
        return bytes([0x01, 0x06, 0x00, 0x01]) + int(int_in).to_bytes(2, "big") + bytes([0x89, 0xCA])
    
    def rudder_packet(self, int_in):
        # 01 06 00 00 00 0F 89 CA
        # -----------------------------
        # 01	Slave 1
        # 06	Write Single Register
        # 00 00	Register 0 (rudder)
        # 00 0F	Value 15
        # 89 CA	CRC
        return bytes([0x01, 0x06, 0x00, 0x00]) + int(int_in).to_bytes(2, "big") + bytes([0x89, 0xCA])

    def settings(self, control_character, boat_character):
        # Smart controller settings

        # control_character = {
        #     "heading_correction": 1.1,  # Turning rate (rad/s) per rad of heading error
        #     "allowable_error": 1e-6,    # Margin of error on target/heading
        #     "speed_correction": 0.5,    # Speed (m/s) per meter of distance error
        # }

        # boat_character = {
        #     "max_turning_rate": math.pi/5,  # Max angular speed (rad/s)
        #     "max_speed": 5,                 # Max speed (m/s)
        #     "max_stationary_turning_rate": 2.0 # Fallback turning rate when speed low
        # }

        self.Kp_heading = control_character["heading_correction"]
        self.eps = control_character["allowable_error"]
        self.Kp_dist    = control_character["speed_correction"]

        self.omega_max  = boat_character["max_turning_rate"]
        self.speed_max  = boat_character["max_speed"]
        self.rudder_max = boat_character["max_stationary_turning_rate"]
    
    def stop(self):                         #me when
        self.running = False

    def start(self):
        c = threading.Thread(target=self.control, daemon=True)
        c.start()

    def control(self):
        # Controller thread. Requests position on a loop
        while self.running:
            try:
                self.send_func(self.request_packet)
            except Exception as e:
                print(e)
                pass
            time.sleep(self.tick_rate)

    def receive_func(self, packet):
        # Triggered externally when boat sends packet
        packet_x = -1
        packet_y = -1
        packet_dir = -1
        try:
            #     Slave respond with data:
            # 01 04 06 00 5A 04 B0 03 20 49 7C
            # ---------------------------------------------------
            # 01	Slave 1
            # 04	Affirm Function 4 read registers
            # 06	6 bytes of data
            # 00 5A	Direction = 90° converted to 2 bytes in hex
            # 04 B0	X = 1200        converted to 2 bytes in hex
            # 03 20	Y = 800         converted to 2 bytes in hex
            # 49 7C	CRC  
            if packet[1] == 0x04:
                packet_dir = int.from_bytes(packet[3:5], "big")
                packet_x = int.from_bytes(packet[5:7], "big")
                packet_y = int.from_bytes(packet[7:9], "big")
            else:
                print("Unimportant "+packet[1]+" packet received")
                return
            
            def wrap_pi(a):
                return (a + math.pi) % (2 * math.pi) - math.pi
            

            # Received position
            x_pos = packet_x
            y_pos = packet_y
            dir = wrap_pi((packet_dir-360)*math.pi/180) # use as radians

            # Move target if we've landed
            if (abs(x_pos - self.sub_target[0]) < 5) and (abs(y_pos - self.sub_target[1]) < 5):
                self.sub_target[0] = random.randint(100, 900)
                self.sub_target[1] = random.randint(100, 900)

            # Target
            x_target = self.sub_target[0]
            y_target = self.sub_target[1]

            # Geometry
            dx = x_target - x_pos
            dy = y_target - y_pos
            distance = math.hypot(dx, dy)

            # Bearing
            bearing = math.atan2(dy, dx)
            heading_err = wrap_pi(bearing - dir)

            # Set rudder, clamped to max
            omega_des = self.Kp_heading * heading_err / self.tick_rate
            if omega_des > self.omega_max:
                omega_des = self.omega_max
            elif omega_des < -self.omega_max:
                omega_des = -self.omega_max

            # Set speed, clamped to max
            speed_des = self.Kp_dist * distance
            heading_factor = max(2.0, math.cos(heading_err)) 
            speed_des *= heading_factor
            # clamp speed
            speed_des = max(0.0, min(speed_des, self.speed_max))

            if speed_des > self.eps:
                rudder_cmd = omega_des / speed_des
                # clamp rudder to some reasonable magnitude
                if rudder_cmd > self.rudder_max:
                    rudder_cmd = self.rudder_max
                elif rudder_cmd < -self.rudder_max:
                    rudder_cmd = -self.rudder_max
            else:
                # if standing still, set rudder to a value that will make it turn once you move
                rudder_cmd = math.copysign(self.rudder_max, omega_des) if abs(omega_des) > 1e-6 else 0.0

            rudder_des = wrap_pi(rudder_cmd)*180/math.pi + 360 #send as degrees + 360
            # Set command
            self.send_func(self.rudder_packet(rudder_des))
            self.send_func(self.speed_packet(speed_des))

        except Exception as e:
            print("Exception: "+str(e))
            pass