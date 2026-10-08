from ...widgets.map import Map
from ...app_core import Context
from threading import Lock
from ...drawing.viewport import ViewPort
from ...pages.page import Page
from ...widgets import MenuBar
from ...widgets.frame_widgets.menu_bar import DEMO_MENU_BAR


class Sprites(Page):
    def __init__(self, context: Context):
        super().__init__(context)
        menu_bar = MenuBar(self, context, "sprites_demo")
        menu_bar.add_config_buttons(DEMO_MENU_BAR)
        world_map = Map(self, context, self.frame_callback, 100)


    def frame_callback(self, canvas, draw_lock: Lock, scale: float, offset: tuple[float, float]):
        draw = ViewPort(canvas, scale, offset)
        with draw_lock:
            draw.ocean()
            draw.line([(0, 0), (200, 200)], "white")
            draw.boat((100,100), 0)
            draw.boat((100,100), 3.14/2)
            draw.boat((100,100), -3.14/4)
            draw.boat((0,0), -3.14/4)
            draw.boat((200,0), -3.14/4)
            draw.boat((0,200), -3.14/4)
            draw.boat((200,200), -3.14/4)