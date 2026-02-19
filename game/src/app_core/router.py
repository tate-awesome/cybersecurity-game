from .context import Context
from customtkinter import CTk, get_appearance_mode, set_appearance_mode, ThemeManager
from tkinter.filedialog import askopenfilename
import os

from ..pages.demo.sprites import Sprites
from ..pages.demo.saved_map import SavedMap
from ..pages.demo.boat_motion import BoatMotion
from ..pages.demo.triangle import Triangle
from ..pages.demo.hardware_map import HardwareMap

from ..pages.attacker.attacker import AttackerV0

from ..pages.title.title import Title
from ..pages.title.select_mode import SelectMode
from ..pages.title.select_demo import SelectDemo

from .keybinds import KeyBinds

class Router:

    def __init__(self, root: CTk, start_page: str):
        self.context = Context(root, self)
        KeyBinds(root, self.context, self.refresh, self.quit)
        self.show(start_page)


    pages = {

            "title": Title,
            "title/title": Title,
            "title/select_mode": SelectMode,
                "attacker/v0": AttackerV0,

            "title/select_demo": SelectDemo,
                "demo/sprites": Sprites,
                "demo/saved_map": SavedMap,
                "demo/boat_motion": BoatMotion,
                "demo/triangle": Triangle,
                "demo/hardware_map": HardwareMap,
        }
    

    def show(self, next_page: str):
        self.clear()
        self.pages[next_page](self.context)
        self.current_page = next_page


    def refresh(self):
        self.clear()
        self.show(self.current_page)
    

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
    

    def select_theme(self):

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        themes_dir = os.path.join(BASE_DIR, "..", "..", "assets", "themes")
        try:
            file_path = askopenfilename(
            initialdir=themes_dir,
            title="Select a theme file",
            filetypes=(("json", "*.json"),)
            )
            ThemeManager.load_theme(file_path)
        except:
            pass
        finally:
            self.refresh()
    