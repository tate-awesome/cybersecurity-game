'''
Shared data for a game session. Passed to next pages on navigation
'''

class Context:

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
        
        True = Has been done - use network_controller to see if it's running
        '''

        self.inputs = {
            "arp": ["192.168.8.137","192.168.8.243"],
            "sniff": ["",""],
            "dos": ["192.168.8.114:200","192.168.8.114:201"],
            "checkbox_filters": {
                "Hack": {
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
            "text_filters": {
                "address_filter": {
                    "label": "IP/MAC Addresses Involved (Separated by \"|\")",
                    "text": ""
                }
            },
            "packet_filter_function": {
                "summary": "Currently filtering for any packets.",
                "function": lambda mpkt: True
            },
            "column_selections": {
                "Time": {
                    "state": "1",
                    "function": lambda mpkt: mpkt.time_word
                },
                "No.": {
                    "state": "1",
                    "function": lambda mpkt: mpkt.absolute_number
                },
                "Length": {
                    "state": "0",
                    "function": lambda mpkt: mpkt.length
                },
                "Hack info": {
                    "state": "1",
                    "function": lambda mpkt: mpkt.hack_word
                },
                "Transaction": {
                    "state": "1",
                    "function": lambda mpkt: mpkt.transaction_word
                },
                "Layers": {
                    "state": "1",
                    "function": lambda mpkt: mpkt.proto_str
                },
                "Purpose": {
                    "state": "0",
                    "function": lambda mpkt: mpkt.purpose
                },
                "Summary": {
                    "state": "1",
                    "function": lambda mpkt: mpkt.summary
                },
                "Modbus info": {
                    "state": "0",
                    "function": lambda mpkt: mpkt.modbus_word
                },
            },
            
        }
        '''
        Save slots for the user inputs during GUI refresh.
        arp: target ip, host ip
        sniff: print to gui, print to console
        '''


    def get_all(self):
        '''
        Returns tuple[router, root]
        '''
        return self.router, self.root

    def help_message(self, widget="root"):
        # TODO get help from progress and current page and source widget
        return "You need to do something"

    def refresh_net(self, constructor):
        # Defer to the existing net
        if self.net is None:
            self.net = constructor()
        net = self.net
        return net