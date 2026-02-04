import threading
import random
import time
import math

class Slave:
    def __init__(self, physics_rate_s, boat_character, send_func):
        self.tick_rate = physics_rate_s
        self.x_pos = 200
        self.y_pos = 200
        self.dir = 0

        self.speed = 10                      # Default command
        self.rudder = 0                     # Default command
        self.send_func = send_func

        self.settings(boat_character)
        self.running = True
        self.start()
    
    def position_packet(self):
        # Slave respond with data:
        # 01 04 06 00 5A 04 B0 03 20 49 7C
        # ---------------------------------------------------
        # 01	Slave 1
        # 04	Affirm Function 4 read registers
        # 06	6 bytes of data
        # 00 5A	Direction = 90° converted to 2 bytes in hex
        # 04 B0	X = 1200        converted to 2 bytes in hex
        # 03 20	Y = 800         converted to 2 bytes in hex
        # 49 7C	CRC  
        head = bytes([0x01, 0x04, 0x06])
        dir = int(self.dir * 180/math.pi+360).to_bytes(2, "big") # send as degrees
        x = int(self.x_pos).to_bytes(2, "big")
        y = int(self.y_pos).to_bytes(2, "big")
        crc = bytes([0x49, 0x7C])
        return head + dir + x + y + crc
    
    def settings(self, boat_character):

        # boat_character = {
        #     "max_turning_rate": math.pi/5,  # Max angular speed (rad/s)
        #     "max_speed": 5,                 # Max speed (m/s)
        #     "max_stationary_turning_rate": 2.0 # Fallback turning rate when speed low
        # }

        self.omega_max  = boat_character["max_turning_rate"]
        self.speed_max  = boat_character["max_speed"]
        self.rudder_max = boat_character["max_stationary_turning_rate"]
    
    def stop(self): #me when
        self.running = False

    def start(self):
        s = threading.Thread(target=self.system, daemon=True)
        s.start()

    def receive_func(self, packet):
        # Master read data:
        # 01 04 00 (00 or 01) 00 03 B0 0B
        # ------------------------
        # 01      slave id 01
        # 04      read registers
        # 00 00   start register 0
        # 00 03   read 3 registers
        # B0 0B   CRC

        # Master send rudder command:
        # 01 06 00 00 00 0F 89 CA
        # -----------------------------
        # 01	Slave 1
        # 06	Write Single Register
        # 00 00	Register 0 (rudder)
        # 00 0F	Value 15
        # 89 CA	CRC

        # Master send throttle command:
        # 01 06 00 01 02 58 D9 CB
        # -----------------------------
        # 01	Slave 1
        # 06	Write Single Register
        # 00 01	Register 1 (throttle)
        # 02 58	Value 15
        # D9 CB	CRC
        try:
            if packet[1] == 0x04:
                self.send_func(self.position_packet())
            elif packet[1] == 0x06 and packet[3] == 0x00:
                self.rudder = int.from_bytes(packet[4:6], "big")
            elif packet[1] == 0x06 and packet[3] == 0x01:
                self.speed = int.from_bytes(packet[4:6], "big")
            else:
                print("bad backet")
        except Exception as e:
            print(e)
            pass


    def system(self):
        # Sub thread. Simulates movement
        while self.running:
            try:

                def wrap_pi(a):
                    return (a + math.pi) % (2 * math.pi) - math.pi

                speed = self.speed
                rudder = wrap_pi((self.rudder-360)*math.pi/180) # use as rads per distance
                x_pos = self.x_pos
                y_pos = self.y_pos
                dir = wrap_pi(self.dir) # stored as rads

                # angle change = time_step * speed * angle per time
                dir = dir + self.tick_rate * rudder

                # position change = time step * speed * cis(direction)
                x_pos = x_pos + self.tick_rate * speed * math.cos(dir)
                y_pos = y_pos + self.tick_rate * speed * math.sin(dir)

                # simulate position change
                self.x_pos = x_pos
                self.y_pos = y_pos
                self.dir = dir #stored in rads

                # print(f"boat:   {self.x_pos}     {self.y_pos}   {self.dir*180/math.pi}")
                # print(f"comm:   {speed}     {rudder*180/math.pi}")

            except Exception as e:
                print("Exception: "+str(e))
                pass
            time.sleep(self.tick_rate)
        