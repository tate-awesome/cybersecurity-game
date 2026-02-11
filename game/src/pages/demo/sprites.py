from ...widgets.map import Map
from ...widgets.style import Style
from ...app_core.context import Context
from customtkinter import CTkCanvas
from threading import Lock
from ...drawing.viewport import ViewPort


class Sprites:
    def __init__(self, context: Context):
        style = Style(context.ui_scale)
        world_map = Map(style, context.root, self.frame_callback, 100)

    
    def frame_callback(self, canvas: CTkCanvas, draw_lock: Lock, scale: float, offset: tuple[float, float]):
        draw = ViewPort(canvas, scale, offset)
        with draw_lock:
            canvas.delete("all")
            draw.ocean()
            draw.line([(0, 0), (200, 200)], "white")
            draw.boat((100,100), 0)
            draw.boat((100,100), 3.14/2)
            draw.boat((100,100), -3.14/4)
            draw.boat((0,0), -3.14/4)
            draw.boat((200,0), -3.14/4)
            draw.boat((0,200), -3.14/4)
            draw.boat((200,200), -3.14/4)