from .context import Context
from customtkinter import CTk, get_appearance_mode, set_appearance_mode, ThemeManager
import os
from tkinter.filedialog import askopenfilename

from ..pages.demo.sprites import Sprites
from ..pages.demo.saved_map import SavedMap
from ..pages.demo.boat_motion import BoatMotion
from ..pages.demo.triangle import Triangle
from ..pages.demo.hardware_map import HardwareMap

from ..pages.attacker.attacker import AttackerV0

class Router:

    def __init__(self, root: CTk, start_page: str):
        self.context = Context(root, self)

        self.pages = {
            "demo/sprites": Sprites,
            "demo/saved_map": SavedMap,
            "demo/boat_motion": BoatMotion,
            "demo/triangle": Triangle,
            "demo/hardware_map": HardwareMap,

            "attacker/v0": AttackerV0
        }

        self.current_page = start_page

        self.show(self.current_page)

    
    def show(self, next_page: str):
        self.clear()
        self.pages[next_page](self.context)
        self.current_page = next_page


    def refresh(self):
        self.clear()
        self.show(self.current_page)
    

    def quit(self):
        # TODO abort all threads and network activity
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
    

    def select_theme(self):

        file_path = askopenfilename(
            title="Select a theme file",
            filetypes=(("json", "*.json"),)
        )
        try:
            ThemeManager.load_theme(file_path)
        finally:
            self.refresh()
    