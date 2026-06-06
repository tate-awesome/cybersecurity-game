from customtkinter import CTk, get_appearance_mode, set_appearance_mode, ThemeManager
from tkinter.filedialog import askopenfilename
import os, json

from .context import Context
from .style import Style
from .keybinds import KeyBinds

# Import page builder objects here
# /demo
from ..pages.demo.sprites import Sprites
from ..pages.demo.boat_motion import BoatMotion
from ..pages.demo.triangle import Triangle

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
        self.style = Style(root)
        self.context = Context(root, self, self.style)
        self.navigation_stack = []
        self.show(start_page)

        # Bind window commands (zoom, f11, Quit)
        KeyBinds(root, self.style, self.refresh, self.quit)


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
                "demo/boat_motion": BoatMotion,
                "demo/triangle": Triangle,
        }
        '''
        Dict mapping page names to page builder functions.
        Add new pages here to make them accessible by the router.
        All page builder functions should take a Context object as an argument and build the page on the root CTk object.
        '''

        # Handle 404
        if next_page not in pages:
            print(f"Page '{next_page}' not found. Redirecting to title page.")
            self.navigation_stack = []
            next_page = "title"

        # Handle first page ever (usually title or 404 reset)
        if len(self.navigation_stack) == 0:
            self.navigation_stack.append(next_page)

        # Handle deeper page (not refresh)
        if not next_page == self.navigation_stack[-1]:
            self.navigation_stack.append(next_page)
        
        # Clear the window
        self.clear()

        # Call the page builder
        pages[next_page](self.context)


    def refresh(self):
        '''
        Refreshes the current page by clearing the root CTk object and rebuilding the current page.
        Useful for updating the UI after changing themes or making changes to the context.
        '''
        self.show(self.navigation_stack[-1])
    

    def quit(self):
        '''
        Deletes all ongoing processes and destroys the CTk root.
        Called on Close event or by the Quit button.
        '''
        if self.context.net is not None:
            self.context.net.abort_all()
        self.context.root.destroy()


    def clear(self):
        '''
        Deletes all widgets inside the root
        '''
        root = self.context.root
        while len(root.winfo_children()) > 0:
            root.winfo_children()[0].destroy()


    def mode_toggle(self):
        '''
        Toggles the appearance mode (light/dark mode)
        '''
        if get_appearance_mode() == "Dark":
            set_appearance_mode("Light")
        else:
            set_appearance_mode("Dark")
        # set_appearance_mode refreshes all CTk elements automatically, but we have some TK elements and custom colors.
        self.refresh()
    

    def select_preset(self):
        '''
        Opens a dialog for the user to select a context preset.
        Context presets populate fields and checkboxes.
        '''
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
        '''
        Navigates backwards in the page history.
        '''
        if len(self.navigation_stack) < 1:
            return
        self.context.destroy_context()
        self.navigation_stack.pop()
        self.show(self.navigation_stack[-1])


    def select_theme(self):
        '''
        Opens a dialog for the user to select a CTk theme.
        '''
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