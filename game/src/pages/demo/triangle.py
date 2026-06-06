from ...app_core.context import Context
from customtkinter import CTkCanvas
from threading import Lock
from ...widgets.map import Map
from ...pages.page import Page
from ...widgets.frame_widgets.menu_bar import MenuBar

class Triangle(Page):
    def __init__(self, context: Context):
        super().__init__(context)
        menu_bar = MenuBar(self, context, "Triangle Demo", False)
        menu_bar.quit_button()
        menu_bar.back_button()
        world_map = Map(self, context, self.draw_test_plane, 100)


    def draw_test_plane(self, canvas: CTkCanvas, draw_lock: Lock, scale: float, offset: tuple[float, float]):
        from ...drawing.viewport import ViewPort
        draw = ViewPort(canvas, scale, offset)
        with draw_lock:
            canvas.delete("all")
            draw.test_triangle()