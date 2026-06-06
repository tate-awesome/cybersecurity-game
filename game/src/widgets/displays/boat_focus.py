from ...network.data_buffer import DataBuffer
from ...drawing.viewport import ViewPort
from ..map import Map
from typing import cast
import math
from customtkinter import CTkFrame


class BoatFocus:
    def __init__(self, parent, context):
        self.parent = parent
        self.context = context
        self.buffer = cast(DataBuffer, context.net.data_buffer)
        self.frame = CTkFrame(parent, fg_color="green")

        map = Map(style, self.frame, self.draw_boat_display, 100, 20, 40)

    def draw_boat_display(self, canvas, draw_lock, scale: float, offset: tuple[float, float]):
            bearing = self.buffer.get_bearing("in")
            draw = ViewPort(canvas, 1.0, (0,0), 20, ((-100, -100), (100, 100)))
            rudder = self.buffer.get_rudder("in")
            speed = self.buffer.get_speed("in")
            size = 33.3333
            with draw_lock:
                canvas.delete("all")
                draw.test_triangle()
                # draw.ocean()
                draw.boat((0,0), bearing+math.pi, "blue", "blue", scale=size*speed/5)
                draw.boat((0,0), 0, "grey", "black", scale=size)
                draw.arc((0, 0), 90, bearing, rudder+bearing, "red")
                draw.line([(0,0), (-speed*math.cos(bearing)*50, -speed*math.sin(bearing)*50)], "blue")
        