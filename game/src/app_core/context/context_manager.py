from .style import Style
from ...network.network_controller import NetworkController
from .click_manager import ClickManager
from .animation_manager import AnimationManager
from .preferences import Preferences
from .keybinds import KeyBinds
import os, json, platform
from .paths import Paths
from .json import Json

# imports to move later
from customtkinter import set_appearance_mode, get_appearance_mode, ThemeManager
import subprocess, webbrowser

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..router import Router



class ContextManager:
    '''
Shared data for a page. Passed to next pages on navigation.
'''
    '''
    Important data that needs to be shared across pages, such as the network controller and the router.
    Every page builder function should take a Context object as an argument and build the page on the root CTk object.
    '''

    def __init__(self, root, router: "Router"):
        # All immutable members for the session
        self.router = router
        self.root = root
        self.paths = Paths()
        self.json = Json(self.paths)
        self.style = Style(self)
        self.os_name = platform.system()
        self.start_session()
        self.start_page()
        self.start_build()

    def start_session(self):
        '''
        Creates mutable and resettable members for a session with the app
        Often saved by the user for the next session.
        '''
        self.preferences = Preferences(self)
        KeyBinds(self)
        self.states = self.get_preferred_settings()
        self.labels = self.get_preferred_labels()
        self.style.load_preferred_theme()
        self.style.load_preferred_mode()

    def reset_session(self):
        '''
        Resets members in a session
        '''
        self.states = self.get_default_settings()
        self.labels = self.get_default_labels()
        self.style.load_default_theme()
        self.style.load_default_mode()

    def start_page(self):
        '''
        Creates mutable and resettable members for a page
        Keep on refresh.
        Reset on page exit.
        '''
        self.net =  NetworkController(self) # base class with things lots of inits need

    def reset_page(self):
        '''
        Resets page members on page exit
        '''
        if self.net is not None:
            self.net.abort_all()
            self.net = None 

    def start_build(self):
        '''
        Creates members for a single page build.
        Reset on refresh and page exit.
        '''
        self.click_manager = ClickManager(self.root)
        self.animation_manager = AnimationManager(self.root)

    def reset_build(self):
        '''
        Resets build members on page refresh and exit
        '''
        if hasattr(self, "click_manager"):
            self.click_manager.delete()
        if hasattr(self, "animation_manager"):
            self.animation_manager.delete()

    def reset_data(self):
        self.reset_session()
        self.preferences.clear()
        self.router.refresh()

    def get_preferred_settings(self):
        default = self.get_default_settings()
        if self.preferences.has("settings"):
            self.json.deep_merge(default, self.preferences.data["settings"])
        return default
    
    def get_default_settings(self):
        file_path = self.paths.packages / "_default.json"
        default = {}
        self.json.merge_from_file(default, file_path)
        return default

    def select_settings(self):
        '''
        Opens a dialog for the user to select a context preset.
        Context presets populate fields and checkboxes.
        '''
        directory = self.paths.settings
        file_path = self.paths.select_path(directory, "Select Settings")
        self.json.merge_from_file(self.states, file_path)
        self.router.refresh()

    def get_preferred_labels(self):
        default = self.get_default_labels()
        if self.preferences.has("labels"):
            self.json.deep_merge(default, self.preferences.data["labels"])
        return default

    def get_default_labels(self):
        data = {}
        file_path = self.paths.labels / "_default.json"
        self.json.merge_from_file(data, file_path)
        return data

    def select_labels(self):
        '''
        Opens a dialog for the user to select a context labels
        Context labels change text in labels
        '''
        directory = self.paths.labels
        file_path = self.paths.select_path(directory, "Select a Labels File")
        self.json.merge_from_file(self.labels, file_path)
        self.router.refresh()

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

    def open_ap_config_page(self):
        url = "http://192.168.4.1"

        sudo_user = os.environ.get("SUDO_USER")

        if sudo_user:
            # Open browser as not sudo
            subprocess.Popen(["sudo", "-u", sudo_user, "xdg-open", url])
        else:
            # 3. Fallback for when you run the script normally without sudo
            webbrowser.open(url)