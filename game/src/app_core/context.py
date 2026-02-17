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
            "sniff": False
        }
        '''
        Tracks the state of the hacks on the GUI.
        
        False = Fresh state
        
        True = Has been done - use network_controller to see if it's running
        '''

        self.inputs = {
            "arp": ["",""],
            "sniff": ["",""]
        }


    def get_all(self):
        '''
        Returns tuple[router, root]
        '''
        return self.router, self.root

    def help_message(self, widget="root"):
        # TODO get help from progress and current page and source widget
        return "You need to do something"