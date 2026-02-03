from ..pages.hacker import Hacker
from ..pages.demos import Demos
from customtkinter import CTk

class Router:

    def __init__(self, root: CTk, start_page: str):
        self.root = root

        self.pages = {
            "hacker_final":     Hacker.final,
            "map_demo":         Demos.map
        }

        self.current_page = start_page

        self.show(self.current_page)

    
    def show(self, next_page: str):
        self.pages[next_page](self.root)

    