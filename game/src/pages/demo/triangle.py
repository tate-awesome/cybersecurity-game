from ...app_core.context import Context
from customtkinter import CTkCanvas
from threading import Lock
from ...widgets import TriangleCanvas
from ...pages.page import Page
from ...widgets import MenuBar

class Triangle(Page):
    '''
    Demo page for testing canvas, animations, camera, drawing, sprites, and transforms
    '''
    def __init__(self, context: Context):
        super().__init__(context)
        menu_bar = MenuBar(self, context, "Triangle Demo", False)
        menu_bar.quit_button()
        menu_bar.back_button()

        world_map = TriangleCanvas(self, context)