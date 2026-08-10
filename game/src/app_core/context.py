'''
Shared data for a page. Passed to next pages on navigation.
'''

from .style import Style
from ..network.network_controller import NetworkController
from .click_manager import ClickManager
from .animation_manager import AnimationManager
import os, json, platform

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
        self.os_name = self.get_os()
        self.states = self.get_default_settings()
        self.labels = self.get_default_labels()
        self.net =  NetworkController(self)
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
        self.destroy_managers()

    def reset(self):
        self.destroy_context()
        self.generate()

    def deep_merge(self, base_dict: dict, better_dict: dict):
        for key, value in better_dict.items():
            if (
                isinstance(value, dict)
                and isinstance(base_dict.get(key), dict)
            ):
                self.deep_merge(base_dict[key], value)
            else:
                base_dict[key] = value

        return base_dict
    
    def get_default_settings(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(BASE_DIR, "..", "..", "assets", "settings", "_packages", "_default.json")
        with open(file_path) as json_file:
            package = json.load(json_file)
        default = self.unpack_settings(package)
        return default

    def unpack_settings(self, package: dict):
        '''
        returns a merged dict of all the files specified in the given package
        '''
        data = {}
        if "_files" in package.keys():
            files = package["_files"]
            for folder, file in files.items():
                BASE_DIR = os.path.dirname(os.path.abspath(__file__))
                file_path = os.path.join(BASE_DIR, "..", "..", "assets", "settings", folder, file)
                with open(file_path) as json_file:
                    new = json.load(json_file)
                self.deep_merge(data, new)
        else:
            data = package
        return data

    def add_settings(self, new_settings: dict = {}):
        '''
        Loads settings to overwrite parts of the current states
        If the new settings includes a "_files" key, it will unpack the given files shallowly
        '''
        base_settings = self.states.copy()

        unpacked_settings = self.unpack_settings(new_settings)

        merged_settings = self.deep_merge(base_settings, unpacked_settings)
        self.states = merged_settings

    def get_default_labels(self):
        data = {}
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(BASE_DIR, "..", "..", "assets", "labels", "_default.json")
        with open(file_path) as json_file:
            data = json.load(json_file)
        return data

    def load_labels(self, labels: dict = {}):
        base_labels = self.get_base_labels()
        merged_labels = self.deep_merge(base_labels, labels)
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

    def get_os(self):
        return platform.system()