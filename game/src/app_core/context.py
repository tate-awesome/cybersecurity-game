'''
Shared data for a game session. Passed to next pages on navigation
'''

class Context:
    '''
    Important data that needs to be shared across pages, such as the network controller and the router.
    Every page builder function should take a Context object as an argument and build the page on the root CTk object.
    '''

    def __init__(self, root, router):
        self.net = None
        self.router = router
        self.root = root

        self.ui_scale = 100.0
        self.ui_scales = [25, 33, 50, 67, 75, 80, 90, 100, 110, 125, 133, 140, 150, 175, 200, 250, 300, 400, 500]

        self.states = self.get_base_preset()
        self.labels = self.get_base_labels()
        
        '''
        Tracks the state of the hacks on the GUI.
        False = Fresh state
        True = Has been done - use network_controller to see if it's running.
        TODO: Use for game progression and unlocking elements
        '''

    def get_base_labels(self):
        return {
            "packet_columns": {
                "time": "Time",
                "number": "No.",
                "length": "Length",
                "hack_info": "Hack Info",
                "transaction": "Transaction",
                "layers": "Layers",
                "purpose": "Purpose",
                "summary": "Summary",
                "modbus": "MODBUS Info"
            },

            "packet_filter_categories": {
                "source": "From Source",
                "protocol": "Includes Protocol",
                "direction": "Direction"
            },

            "packet_filter_checkboxes": {            
                "nmap": "NMapping",
                "arp": "ARP Spoofing",
                "dos": "Denial of Service",
                "sniff": "Packet Sniffing",
                "mitm": "MITM Attack",
                "pcap": "PCAP File",
                "TCP": "TCP",
                "ARP": "ARP",
                "UDP": "UDP",
                "DNS": "DNS",
                "MODBUSADU": "MODBUSADU",
                "WRITE SINGLE REGISTER": "WRITE SINGLE REGISTER",
                "READ HOLDING REGISTERS RESPONSE": "READ HOLDING REGISTERS RESPONSE",
                "out": "Sent",
                "in": "Received",
                "other": "Observed"
            },

            "packet_filter_entries": {
                "address_filter": "IP/MAC Addresses Involved (Separated by \"|\")"
            }
        }


    def get_base_preset(self):
        '''
        Returns a preset with default values for all checkboxes and entries.
        Useful for resetting the game states before loading a .json preset file, which may not have all values defined.
        Add a default value here if you want to include data that should survive a soft refresh.
        '''
        
        return {

            "game_progress": {
                "nmap": False,
                "arp": False,
                "sniff": False,
                "mitm": False,
                "dos": False
                },
            
            "hack_forms": {
                "arp": ["",""],
                "sniff": ["",""],
                "dos": ["",""]
            },

            "packet_filter_checkboxes": {
                "nmap": 0,
                "arp": 0,
                "dos": 0,
                "sniff": 0,
                "mitm": 0,
                "pcap": 0,
                "TCP": 0,
                "ARP": 0,
                "UDP": 0,
                "DNS": 0,
                "misc": 0,
                "MODBUSADU": 0,
                "WRITE SINGLE REGISTER": 0,
                "READ HOLDING REGISTERS RESPONSE": 0,
                "out": 0,
                "in": 0,
                "other": 0
            },

            "packet_filter_entries": {
                "address_filter": ""
            },

            "packet_filter_function": {
                "summary": "Currently filtering for any packets.",
                "function": lambda mpkt: True
            },

            "packet_columns": {
                "time": 1,
                "number": 1,
                "length": 0,
                "hack_info": 0,
                "transaction": 0,
                "layers": 0,
                "purpose": 1,
                "summary": 1,
                "modbus": 0
            },

            "map_customization": {
                "Show/Hide Elements": {
                    "in Boat": "1",
                    "in Path": "1",
                    "in Path Discontinuity": "1",
                    "out Boat": "1",
                    "out Path": "1",
                    "out Path Discontinuity": "1"
                },
                "Show/Hide Labels": {
                    "in Boat": "1",
                    "in Boat Position": "1",
                    "out Boat": "1",
                    "out Boat Position": "1",
                    "Grid Numbers": "1",
                    "Grid Lines": "1"
                },
                "Colors": {
                    "in Boat": "yellow",
                    "in Path": "yellow",
                    "in Path Discontinuity": "yellow",
                    "out Boat": "cyan",
                    "out Path": "cyan",
                    "out Path Discontinuity": "cyan"
                },
            }
        }



    def load_preset(self, preset: dict = {}):
        '''
        Loads a preset from a .json file or a provided dictionary.
        If the preset is missing any values, it will use the default values from get_base_preset() to fill in the gaps.
        This allows for easy creation of new presets without having to define every single value.
        Call with preset=None to reset all values to their defaults.
        '''
        base_preset = self.get_base_preset()

        merged_preset = {**base_preset, **preset}

        self.states = merged_preset


    def help_message(self, widget="root"):
        # TODO get help from progress and current page and source widget
        return "You need to do something"

    def refresh_net(self, constructor):
        '''
        Gets the correct network controller for the current page.
        If the net doesn't exist yet, it will be created using the provided constructor and saved to the context.
        If it already exists, it will be returned as is to preserve the state.
        Helps the net controller persist across page navigation without having to pass it as an argument to every page builder function.
        '''
        # Defer to the existing net
        if self.net is None:
            self.net = constructor()
        net = self.net
        return net

    def destroy_net(self):
        if self.net is not None:
            self.net.abort_all()
            self.net = None # Set to None is as good as clearing it manually, since all references to the old net will be lost and it will be garbage collected.
    
    def destroy_context(self):
        self.destroy_net()
        self.load_preset()