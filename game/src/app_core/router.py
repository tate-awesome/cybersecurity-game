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

from ..pages.title.title import Title
from ..pages.title.select_mode import SelectMode
from ..pages.title.select_demo import SelectDemo

class Router:

    def __init__(self, root: CTk, start_page: str):
        self.context = Context(root, self)

        self.pages = {

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

        # Page zoom control
        self.context.root.bind("<Control-plus>", self.zoom_in)     # Ctrl +
        self.context.root.bind("<Control-minus>", self.zoom_out)    # Ctrl -
        self.context.root.bind("<Control-0>", self.zoom_default)     # Ctrl 0
        # Linus key event
        self.context.root.bind("<Control-equal>", self.zoom_in)         # Ctrl = also works as Ctrl +
        
        # On close
        root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Key events
        # def debug_key(e):
        #     print(e.keysym, e.state)
        # self.context.root.bind("<Key>", debug_key)       # Ctrl _ also works as Ctrl -
        
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
        # TODO find a less hacky way to make the sashes update
        self.refresh()
    

    def select_theme(self):

        file_path = askopenfilename(
            title="Select a theme file",
            filetypes=(("json", "*.json"),)
        )
        try:
            ThemeManager.load_theme(file_path)
        finally:
            self.refresh()


    def zoom_in(self, event=None):
        next_index = self.context.ui_scales.index(int(self.context.ui_scale)) + 1
        if next_index >= len(self.context.ui_scales):
            return
        self.context.ui_scale = float(self.context.ui_scales[next_index])
        self.refresh()

    def zoom_out(self, event=None):
        next_index = self.context.ui_scales.index(int(self.context.ui_scale)) - 1
        if next_index < 0:
            return
        self.context.ui_scale = float(self.context.ui_scales[next_index])
        self.refresh()

    def zoom_default(self, event=None):
        self.context.ui_scale = 100.0
        self.refresh()

    def on_close(self):
        self.quit()
    