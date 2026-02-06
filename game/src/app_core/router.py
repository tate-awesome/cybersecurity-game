from ..pages.hacker import Hacker
from ..pages.demos import Demos
from .context import Context
from customtkinter import CTk

class Router:

    def __init__(self, root: CTk, start_page: str):
        self.context = Context(root, self)

        self.pages = {
            "hacker_final":     Hacker.final,
            "net_map_demo":     Demos.net_map,
            "sprite_demo":      Demos.sprites,
            "triangle_demo":    Demos.triangle,
            "saved_map_demo":   Demos.saved_map,
            "boat_motion_demo": Demos.boat_motion_map
        }

        self.current_page = start_page

        self.show(self.current_page)

    
    def show(self, next_page: str):
        self.pages[next_page](self.context)
        self.current_page = next_page

    def refresh(self):
        self.show(self.current_page)

    