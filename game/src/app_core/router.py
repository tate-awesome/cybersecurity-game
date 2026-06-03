from customtkinter import CTk, get_appearance_mode, set_appearance_mode, ThemeManager
from tkinter.filedialog import askopenfilename
import os, json

from .context import Context
from .keybinds import KeyBinds

# Import page builder objects here
# /demo
from ..pages.demo.sprites import Sprites
from ..pages.demo.saved_map import SavedMap
from ..pages.demo.boat_motion import BoatMotion
from ..pages.demo.triangle import Triangle
from ..pages.demo.hardware_map import HardwareMap

# /attacker
from ..pages.attacker.attacker import AttackerV0
from ..pages.defender.defender import DefenderV0

# /title
from ..pages.title.title import Title
from ..pages.title.select_mode import SelectMode
from ..pages.title.select_demo import SelectDemo


class Router:
    '''
    Handles page navigation by calling page builder functions. (Pages can't import each other because of circular imports)
    Builds the first page on startup
    '''
    
    def __init__(self, root: CTk, start_page: str):
        '''
        Creates the app's Context object and shows the first page.
        '''
        self.context = Context(root, self)
        self.navigation_stack = []
        KeyBinds(root, self.context, self.refresh, self.quit)
        self.show(start_page)


    def show(self, next_page: str):
        '''
        Displays the specified page, which should be a key in the pages dict. Clears the current page first.
        '''
        pages = {
            "title": Title,
            "title/title": Title,
            "title/select_mode": SelectMode,
                "attacker/v0": AttackerV0,
                "defender/v0": DefenderV0,
            "title/select_demo": SelectDemo,
                "demo/sprites": Sprites,
                "demo/saved_map": SavedMap,
                "demo/boat_motion": BoatMotion,
                "demo/triangle": Triangle,
                "demo/hardware_map": HardwareMap,
        }
        '''
        Dict mapping page names to page builder functions.
        Add new pages here to make them accessible by the router.
        All page builder functions should take a Context object as an argument and build the page on the root CTk object.
        '''
        self.clear()
        if next_page == "back" and len(self.navigation_stack) > 1:
            self.navigation_stack.pop() # Remove current page
            next_page = self.navigation_stack.pop() # Pop previous page
            pages[next_page](self.context)
            return

        if next_page not in pages:
            print(f"Page '{next_page}' not found. Redirecting to title page.")
            next_page = "title"

        # Handle first page ever
        if len(self.navigation_stack) == 0:
            self.navigation_stack.append(next_page)
        # Handle refresh
        if next_page == self.navigation_stack[-1]:
            ...
        else:
            self.navigation_stack.append(next_page)
        pages[next_page](self.context)


    def refresh(self):
        '''
        Refreshes the current page by clearing the root CTk object and rebuilding the current page.
        Useful for updating the UI after changing themes or making changes to the context.
        '''
        self.show(self.navigation_stack[-1])
    

    def quit(self):
        if self.context.net is not None:
            self.context.net.abort_all()
        self.context.root.destroy()


    def clear(self):
        root = self.context.root
        while len(root.winfo_children()) > 0:
            root.winfo_children()[0].destroy()


    def mode_toggle(self):
        if get_appearance_mode() == "Dark":
            set_appearance_mode("Light")
        else:
            set_appearance_mode("Dark")
        # TODO find a less hacky way to make the sashes update
        self.refresh()
    

    def select_preset(self):

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        presets_dir = os.path.join(BASE_DIR, "..", "..", "assets", "presets")
        try:
            file_path = askopenfilename(
            initialdir=presets_dir,
            title="Select a preset file",
            filetypes=(("json", "*.json"),)
            )
            if file_path == "":
                return
            with open(file_path) as json_file:
                data = json.load(json_file)
            self.context.load_preset(data)
            self.refresh()
        finally:
            return

    
    def go_back(self):
        self.context.destroy_context()
        self.show("back")


    def select_theme(self):

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        themes_dir = os.path.join(BASE_DIR, "..", "..", "assets", "themes")
        try:
            file_path = askopenfilename(
                initialdir=themes_dir,
                title="Select a theme file",
                filetypes=(("json", "*.json"),)
            )
            if file_path == "":
                return
            ThemeManager.load_theme(file_path)
            self.refresh()
        finally:
            return