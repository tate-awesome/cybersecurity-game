from ...app_core import Context
from ...widgets import TriangleCanvas
from ...widgets.frame_widgets.menu_bar import DEMO_MENU_BAR
from ...pages.page import Page
from ...widgets import MenuBar

class Triangle(Page):
    '''
    Demo page for testing canvas, animations, camera, drawing, sprites, and transforms
    '''
    def __init__(self, context: Context):
        super().__init__(context)
        menu_bar = MenuBar(self, context, "triangle_demo")
        menu_bar.add_config_buttons(DEMO_MENU_BAR)

        world_map = TriangleCanvas(self, context)