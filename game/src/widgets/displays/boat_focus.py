from ...widgets.style import Style
from ...network.data_buffer import DataBuffer
from ...drawing.viewport import ViewPort
from ...widgets.map import Map
import math


class BoatFocus:
    def __init__(self, style: Style, parent, context):
        self.parent = parent
        self.style = style
        self.context = context
        self.buffer = context.net.data_buffer

        map = Map(style, parent, self.draw_boat_display, 100, 20)

    def draw_boat_display(self, canvas, draw_lock, scale: float, offset: tuple[float, float]):
            bearing = self.buffer.get_bearing("in")
            rudder = self.buffer.get_rudder("in")
            speed = self.buffer.get_speed("in")
            draw = ViewPort(canvas, scale, offset)
            with draw_lock:
                canvas.delete("all")
                draw.boat((0,0), bearing)
                draw.arc((0, 0), 50, bearing, rudder+bearing, "red")
                draw.line([(0,0), (-speed*math.cos(bearing)*50, -speed*math.sin(bearing)*50)], "blue")
        