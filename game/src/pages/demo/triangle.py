from ...app_core.context import Context
from customtkinter import CTkCanvas
from threading import Lock
from ...widgets.map import Map
from ...widgets.style import Style

class Triangle:
    def __init__(self, context: Context):       
        style = Style(context)
        world_map = Map(style, context.root, self.draw_test_plane, 100)

    def draw_test_plane(self, canvas: CTkCanvas, draw_lock: Lock, scale: float, offset: tuple[float, float]):
        from ...drawing.viewport import ViewPort
        draw = ViewPort(canvas, scale, offset)
        with draw_lock:
            canvas.delete("all")
            draw.test_triangle()