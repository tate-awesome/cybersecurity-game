from ...app_core import Context
from ...widgets import TriangleCanvas
from ...pages.page import Page
from ...widgets import MenuBar

class Triangle(Page):
    '''
    Demo page for testing canvas, animations, camera, drawing, sprites, and transforms
    '''
    def __init__(self, context: Context):
        super().__init__(context)
        menu_bar = MenuBar(self, context, "triangle_demo")
        menu_bar.toggle_button()
        menu_bar.theme_button()
        menu_bar.labels_button()
        menu_bar.page_button()
        menu_bar.back_button()
        menu_bar.quit_button()

        world_map = TriangleCanvas(self, context)