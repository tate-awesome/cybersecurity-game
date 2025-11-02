import threading
import random
import queue
import time
import math

class Boat:
    def __init__(self):
        # Send the boat off to the target.
        self.tick_rate = 0.5 #seconds
        self.sub_target = [800, 800]
        self.sub_pos = {"x": 200, "y": 200, "dir": 0} # Outgoing by system - x y dir(degrees)
        self.sub_command = {"speed": 10, "rudder": 0} # Outgoing by control -  speed, rudder (degrees per distance)
        self.new_pos_packet = False
        self.new_command_packet = False
        # 0x 1y 2dir 3speed 4rudderd
        self.running = True
        # These methods are how the sub and controller get data (like receiving packets)
        # They can be reassigned to an external get() that manipulates information
        self.get_sub_pos = self.default_get_sub_pos
        self.get_command = self.default_get_command
    
    def kill(self): #me when
        self.running = False

    def default_get_sub_pos(self):
        return self.sub_pos

    def default_get_command(self):
        return self.sub_command

    def start(self):
        c = threading.Thread(target=self.control, daemon=True)
        s = threading.Thread(target=self.system, daemon=True)
        c.start()
        s.start()

    def control(self):
        # Controller thread. "gets" sub location and sets its command directly
        while self.running:
            try:
                def wrap_pi(a):
                    return (a + math.pi) % (2 * math.pi) - math.pi
                # Smart controller settings
                Kp_heading = 1.1        # (rad/s) per rad of heading error
                omega_max  = math.pi/5  # max angular velocity (rad/s)
                Kp_dist    = 0.5        # speed per meter (so speed = Kp_dist * distance)
                speed_max  = 5        # max forward speed (units / s)
                rudder_max = 2.0        # fallback maximum for rudder (rads per distance) if speed small
                eps = 1e-6

                # Received position
                pos = self.get_sub_pos()
                x_pos = pos["x"]
                y_pos = pos["y"]
                dir = pos["dir"]*math.pi/180 # use as radians

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
                omega_des = Kp_heading * heading_err
                if omega_des > omega_max:
                    omega_des = omega_max
                elif omega_des < -omega_max:
                    omega_des = -omega_max

                # Set speed, clamped to max
                speed_des = Kp_dist * distance
                heading_factor = max(2.0, math.cos(heading_err)) 
                speed_des *= heading_factor
                # clamp speed
                speed_des = max(0.0, min(speed_des, speed_max))

                if speed_des > eps:
                    rudder_cmd = omega_des / speed_des
                    # clamp rudder to some reasonable magnitude
                    if rudder_cmd > rudder_max:
                        rudder_cmd = rudder_max
                    elif rudder_cmd < -rudder_max:
                        rudder_cmd = -rudder_max
                else:
                    # if standing still, set rudder to a value that will make it turn once you move
                    rudder_cmd = math.copysign(rudder_max, omega_des) if abs(omega_des) > 1e-6 else 0.0

                # Set command
                self.sub_command["speed"] = speed_des
                self.sub_command["rudder"] = rudder_cmd*180/math.pi #store as degrees
                self.new_command_packet = True

            except Exception as e:
                print("Exception: "+str(e))
                pass
            time.sleep(self.tick_rate)

    def system(self):
        # Sub thread. "gets" command and simulates movement. Then sets its position directly
        while self.running:
            try:
                def wrap_pi(a):
                    return (a + math.pi) % (2 * math.pi) - math.pi
                command = self.get_command()
                speed = command["speed"]
                rudder = command["rudder"]*math.pi/180 # use as rads per distance
                x_pos = self.sub_pos["x"]
                y_pos = self.sub_pos["y"]
                dir = self.sub_pos["dir"]*math.pi/180 # use as rads

                # angle change = time_step * speed * angle per time
                dir = dir + self.tick_rate * rudder
                # position change = time step * speed * cis(direction)
                x_pos = x_pos + self.tick_rate * speed * math.cos(dir)
                y_pos = y_pos + self.tick_rate * speed * math.sin(dir)

                # send new sub data
                self.sub_pos["x"] = x_pos
                self.sub_pos["y"] = y_pos
                self.sub_pos["dir"] = wrap_pi(dir) * 180 / math.pi #store as degrees, clipped to +-180

                self.new_pos_packet = True
                # print(str(self.sub_pos["x"])+"   "+str(self.sub_pos["y"])+"   "+str(self.sub_pos["dir"]))

                # Move target if we've landed
                if (self.sub_pos["x"] - self.sub_target[0] < 0.0001) and (self.sub_pos["y"] - self.sub_target[1] < 0.0001):
                    self.sub_target[0] = random.randint(100, 900)
                    self.sub_target[1] = random.randint(100, 900)
            except Exception as e:
                print("Exception: "+str(e))
                pass
            time.sleep(self.tick_rate)
        