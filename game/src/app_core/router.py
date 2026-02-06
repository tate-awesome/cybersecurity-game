from .context import Context
from customtkinter import CTk

from ..pages.demo.sprites import Sprites
from ..pages.demo.saved_map import SavedMap
from ..pages.demo.boat_motion import BoatMotion

class Router:

    def __init__(self, root: CTk, start_page: str):
        self.context = Context(root, self)

        self.pages = {
            "demo/sprites": Sprites,
            "demo/saved_map": SavedMap,
            "demo/boat_motion": BoatMotion
        }

        self.current_page = start_page

        self.show(self.current_page)

    
    def show(self, next_page: str):
        self.pages[next_page](self.context)
        self.current_page = next_page

    def refresh(self):
        self.show(self.current_page)

    