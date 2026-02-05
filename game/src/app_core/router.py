from ..pages.hacker import Hacker
from ..pages.demos import Demos
from customtkinter import CTk

class Router:

    def __init__(self, root: CTk, start_page: str):
        self.root = root

        self.pages = {
            "hacker_final":     Hacker.final,
            "net_map_demo":     Demos.net_map,
            "sprite_demo":     Demos.sprites,
            "triangle_demo":    Demos.triangle,
            "saved_map_demo": Demos.saved_map,
            "boat_motion_demo": Demos.boat_motion_map
        }

        self.current_page = start_page

        self.show(self.current_page)

    
    def show(self, next_page: str):
        self.pages[next_page](self.root)

    