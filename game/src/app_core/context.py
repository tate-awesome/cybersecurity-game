'''
Shared data for a page. Passed to next pages on navigation.
'''

from .style import Style
from ..network.network_controller import NetworkController
from .click_manager import ClickManager
from .animation_manager import AnimationManager
import os, json

class Context:
    '''
    Important data that needs to be shared across pages, such as the network controller and the router.
    Every page builder function should take a Context object as an argument and build the page on the root CTk object.
    '''

    def __init__(self, root, router, style: Style):
        self.router = router
        self.root = root
        self.style = style
        self.generate()

    def generate(self):
        self.net =  NetworkController(self)
        self.states = self.get_base_preset()
        self.labels = self.get_base_labels()
        self.create_managers()

    def create_managers(self):
        self.click_manager = ClickManager(self.root)
        self.animation_manager = AnimationManager(self.root)

    def destroy_managers(self):
        if hasattr(self, "click_manager"):
            self.click_manager.delete()
        if hasattr(self, "animation_manager"):
            self.animation_manager.delete()

    def destroy_context(self):
        if self.net is not None:
            self.net.abort_all()
            self.net = None 
        self.load_preset()
        self.load_labels()
        self.destroy_managers()

    def reset(self):
        self.destroy_context()
        self.generate()
    
    def get_base_preset(self):
        data = {}
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(BASE_DIR, "..", "..", "assets", "presets", "_default.json")
        with open(file_path) as json_file:
            data = json.load(json_file)
        return data
    
    def get_base_labels(self):
        data = {}
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(BASE_DIR, "..", "..", "assets", "labels", "_default.json")
        with open(file_path) as json_file:
            data = json.load(json_file)
        return data

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

    def load_labels(self, labels: dict = {}):
        base_labels = self.get_base_labels()

        merged_labels = {**base_labels, **labels}

        self.labels = merged_labels


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
            self.net = constructor(self)
            return self.net