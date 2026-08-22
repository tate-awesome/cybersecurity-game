from .style import Style
from ...network.network_controller import NetworkController
from .click_manager import ClickManager
from .animation_manager import AnimationManager
from .preferences import Preferences
from .keybinds import KeyBinds
from .input_manager import InputManager
from .localization_manager import LocalizationManager
import os, json, platform
from .paths import Paths
from .json import Json

# imports to move later
from customtkinter import set_appearance_mode, get_appearance_mode, ThemeManager, CTk
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

    def __init__(self, root: CTk, router: "Router"):
        # All immutable members for the session
        self.router: "Router" = router
        self.root: CTk = root
        self.paths: Paths = Paths()
        self.json: Json = Json(self.paths)
        self.style: Style = Style(self)

        self.os_name: str = platform.system()
        self.start_session()
        self.start_page()
        self.start_build()

    def start_session(self):
        '''
        Creates mutable and resettable members for a session with the app
        Often saved by the user for the next session.
        '''
        self.preferences: Preferences = Preferences(self)
        KeyBinds(self)
        self.states: InputManager = InputManager(self)
        self.labels: LocalizationManager = LocalizationManager(self)
        self.style.load_preferred_theme()
        self.style.load_preferred_mode()

    def reset_session(self):
        '''
        Resets members in a session
        '''
        self.states.reset()
        self.labels.reset()
        self.style.load_default_theme()
        self.style.load_default_mode()

    def start_page(self):
        '''
        Creates mutable and resettable members for a page
        Keep on refresh.
        Reset on page exit.
        '''
        self.net: NetworkController | None = NetworkController(self) # base class with things lots of inits need

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
        self.click_manager: ClickManager = ClickManager(self.root)
        self.animation_manager: AnimationManager = AnimationManager(self.root)

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

    def help_message(self, widget="root"):
        # TODO get help from progress and current page and source widget
        return "You need to do something"

    def refresh_net(self, constructor: type[NetworkController]):
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