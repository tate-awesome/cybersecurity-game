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

        self.progress = {
            "nmap": False,
            "arp": False,
            "sniff": False,
            "mitm": False,
            "dos": False
        }
        '''
        Tracks the state of the hacks on the GUI.
        False = Fresh state
        True = Has been done - use network_controller to see if it's running.
        TODO: Use for game progression and unlocking elements
        '''

        self.inputs = {
        # Hacking Forms
            "arp": ["192.168.8.137","192.168.8.243"],
            "sniff": ["",""],
            "dos": ["192.168.8.114:200","192.168.8.114:201"],
            
        # Filter overlay
            "checkbox_filters": {
                "Source": {
                    "NMapping": {
                        "state": "",
                        "function": lambda mpkt: mpkt.hack == "nmap"
                    },
                    "ARP Spoofing": {
                        "state": "",
                        "function": lambda mpkt: mpkt.hack == "arp"
                    },
                    "Denial of Service": {
                        "state": "",
                        "function": lambda mpkt: mpkt.hack == "dos"
                    },
                    "Packet Sniffing": {
                        "state": "",
                        "function": lambda mpkt: mpkt.hack == "sniff"
                    },
                    "MITM Attack": {
                        "state": "",
                        "function": lambda mpkt: mpkt.hack == "nfq"
                    },
                    "PCAP File": {
                        "state": "",
                        "function": lambda mpkt: mpkt.hack == "pcap"
                    }
                },

                "Protocol": {
                    "TCP": {
                        "state": "",
                        "function": lambda mpkt: "TCP" in mpkt.protocols
                    },
                    "ARP": {
                        "state": "",
                        "function": lambda mpkt: "ARP" in mpkt.protocols
                    },
                    "UDP": {
                        "state": "",
                        "function": lambda mpkt: "UDP" in mpkt.protocols
                    },
                    "DNS": {
                        "state": "",
                        "function": lambda mpkt: "DNS" in mpkt.protocols
                    },
                    "MODBUSADU": {
                        "state": "",
                        "function": lambda mpkt: "MODBUSADU" in mpkt.protocols
                    },
                    "WRITE SINGLE REGISTER": {
                        "state": "",
                        "function": lambda mpkt: "WRITE SINGLE REGISTER" in mpkt.protocols
                    },
                    "READ HOLDING REGISTERS RESPONSE": {
                        "state": "",
                        "function": lambda mpkt: "READ HOLDING REGISTERS RESPONSE" in mpkt.protocols
                    }
                },

                "Direction": {
                    "Sent": {
                        "state": "",
                        "function": lambda mpkt: mpkt.direction == "out"
                    },
                    "Received": {
                        "state": "",
                        "function": lambda mpkt: mpkt.direction == "in"
                    },
                    "Observed": {
                        "state": "",
                        "function": lambda mpkt: mpkt.direction == "other"
                    }
                }
            },

        # Filter overlay text inputs
            "text_filters": {
                "address_filter": {
                    "label": "IP/MAC Addresses Involved (Separated by \"|\")",
                    "text": ""
                }
            },
        # Filter overlay
            "packet_filter_function": {
                "summary": "Currently filtering for any packets.",
                "function": lambda mpkt: True
            },

        # Column overlay
            "column_selections": {
                "Time": {
                    "state": "1",
                    "function": lambda mpkt: mpkt.time_word,
                    "width": 120
                },
                "No.": {
                    "state": "1",
                    "function": lambda mpkt: mpkt.absolute_number,
                    "width": 70
                },
                "Length": {
                    "state": "0",
                    "function": lambda mpkt: mpkt.length,
                    "width": 80
                },
                "Hack info": {
                    "state": "1",
                    "function": lambda mpkt: mpkt.hack_word,
                    "width": 120
                },
                "Transaction": {
                    "state": "1",
                    "function": lambda mpkt: mpkt.transaction_word,
                    "width": 500
                },
                "Layers": {
                    "state": "1",
                    "function": lambda mpkt: mpkt.proto_str,
                    "width": 250
                },
                "Purpose": {
                    "state": "0",
                    "function": lambda mpkt: mpkt.purpose,
                    "width": 400
                },
                "Summary": {
                    "state": "1",
                    "function": lambda mpkt: mpkt.summary,
                    "width": 600
                },
                "Modbus info": {
                    "state": "0",
                    "function": lambda mpkt: mpkt.modbus_word,
                    "width": 400
                },
            },

        # Map customization overlay
            "customization": {
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
            },
        # Map settings bar
            "path_length": 100
        }
        '''
        Primary storage for checkbox/entry values, which are changed/checked by many different GUI elements.
        Values retreived when building GUI elements.
        Defaults are set here.
        Some styling/filter values are stored here because the checkbox name is the primary key
        '''


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