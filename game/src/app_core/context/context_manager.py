from .style import Style
from ...network.process_manager import ProcessManager
from ...network.buffer import Buffer
from .click_manager import ClickManager
from .animation_manager import AnimationManager
from .preferences import Preferences
from .keybinds import KeyBinds
from .input_manager import InputManager
from .localization_manager import LocalizationManager
from .page_manager import PageManager
from .paths import Paths
from .json import Json

from PySide6.QtWidgets import QMainWindow

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..router import Router



class ContextManager:
    '''
    Shared data passed to each page on navigation.

    Holds what needs to outlive a single page, such as the process manager
    and the router. Every page builder takes a Context and builds the page as
    the root window's central widget.
    '''

    def __init__(self, root: QMainWindow, router: "Router"):
        # All immutable members for the session
        self.router: Router = router
        self.root: QMainWindow = root
        self.paths: Paths = Paths()
        self.json: Json = Json(self.paths)
        self.style: Style = Style(self)

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
        self.pages: PageManager = PageManager(self)
        self.states: InputManager = InputManager(self)
        self.labels: LocalizationManager = LocalizationManager(self)
        self.buffer: Buffer = Buffer(self)
        self.style.load_preferred_theme()

    def reset_session(self):
        '''
        Resets members in a session
        '''
        self.pages.reload()
        self.states.reset()
        self.labels.reset()
        self.style.load_default_theme()

    def start_page(self):
        '''
        Creates mutable and resettable members for a page
        Keep on refresh.
        Reset on page exit.
        '''
        self.process_manager: ProcessManager = ProcessManager(self)

    def reset_page(self, save: bool = True):
        '''
        Resets page members on page exit (navigating away or closing the
        app), autosaving the page first unless save=False. Must be called
        while the page's widgets are still alive, since saving reads the
        live pane sizes off them.
        '''
        if save:
            self.save_page()
        self.process_manager.abort_all()

    def save_page(self):
        '''
        Autosaves the current page's differences from its own defaults
        to user_data (see PageManager.save_current_page).
        '''
        self.pages.save_current_page()

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
