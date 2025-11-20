        
# Receives and stores packets to display boat model and network data
# Stores boat data ready to be accessed
# Receives packets on its own time
# Pings the window when a new packet comes
class Model:
    def __init__(self, game_type, tick_rate):       
        # self.get_command_is_tweaked = False
        # self.get_pos_is_tweaked = False
        self.packets_this_tick = 0
        self.packet_history = []
        self.pip_channels = []
        self.pos_history = []
        self.false_history = []
        self.rudder_history = []
        self.speed_history = []
        self.dir_history = []
        self.left_sidebar_hidden = False
        self.right_sidebar_hidden = True
        self.lying_position = []


    def receive_packet(self):
        return