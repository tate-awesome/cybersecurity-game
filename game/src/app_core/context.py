'''
Shared data for a page. Passed to next pages on navigation.
'''

from .style import Style
from ..network.network_controller import NetworkController

class Context:
    '''
    Important data that needs to be shared across pages, such as the network controller and the router.
    Every page builder function should take a Context object as an argument and build the page on the root CTk object.
    '''

    def __init__(self, root, router, style: Style):
        self.net =  NetworkController()
        self.router = router
        self.root = root
        self.style = style

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

            "world_map_sprites": {
                "boat_in": 1,
                "boat_out": 1,
                "path_in": 1,
                "path_out": 1,

                "boat_in_label": 1,
                "boat_out_label": 1,
                "boat_in_position": 1,
                "boat_out_position": 1,

                "grid_numbers": 1,
                "grid_lines": 1,

                "ocean": 1,
            },
            
            "world_map_colors": {
                "ocean": "#003459",
                "grid_lines": "white",
                "grid_axes": "red",
                "grid_numbers": "white",
                "boat_in_fill": "yellow",
                "boat_in_outline": "yellow",
                "boat_out_fill": "yellow",
                "boat_out_outline": "yellow",
                "path_in": "yellow",
                "path_out": "yellow"
            },

            "strip_chart_sprites": {
                "grid_lines": 1,
                "grid_axes": 1,
                "grid_numbers": 1,
                "head_in": 1,
                "head_out": 1,
                "path_in": 1,
                "path_out": 1,
                "head_in_label": 1,
                "head_out_label": 1
            },

            "strip_chart_colors": {
                "background": "white",
                "grid_lines": "black",
                "grid_axes": "red",
                "grid_numbers": "black",
                "path_in": "blue",
                "path_out": "green",
                "head_in": "blue",
                "head_out": "green"
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
        If the net is a different type, it will create a new net with the constructor.
        If it already exists, it will be returned as is to preserve the state.
        Helps the net controller persist across refreshes without having to pass it as an argument to every page builder function.
        '''
        # Check type
        if type(self.net) is constructor:
            return self.net
        else:
            self.net = constructor()
            return self.net

    def destroy_net(self):
        if self.net is not None:
            self.net.abort_all()
            self.net = None # Set to None is as good as clearing it manually, since all references to the old net will be lost and it will be garbage collected.
    
    def destroy_context(self):
        self.destroy_net()
        self.load_preset()