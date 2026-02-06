from .context import Context
from customtkinter import CTk

from ..pages.demo.sprites import Sprites

class Router:

    def __init__(self, root: CTk, start_page: str):
        self.context = Context(root, self)

        self.pages = {
            "demo/sprites": Sprites
        }

        self.current_page = start_page

        self.show(self.current_page)

    
    def show(self, next_page: str):
        self.pages[next_page](self.context)
        self.current_page = next_page

    def refresh(self):
        self.show(self.current_page)

    