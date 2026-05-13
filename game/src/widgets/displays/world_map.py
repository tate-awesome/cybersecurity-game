from ...app_core.context import Context
from ...network.meta_packet import MetaPacket
from ...network.data_buffer import DataBuffer

from ...drawing.viewport import ViewPort
from ...widgets.map import Map

class WorldMap:
    def __init__(self, style, parent, context, buffer: DataBuffer):
        self.style = style
        self.parent = parent
        self.context = context
        self.buffer = buffer

        
        map = Map(style, parent, self.draw_full_map, 100, 20)

    def draw_full_map(self, canvas, draw_lock, scale: float, offset: tuple[float, float]):
            positions = self.buffer.get_simple_path("in")
            bearing = self.buffer.get_bearing("in")
            draw = ViewPort(canvas, scale, offset)
            with draw_lock:
                canvas.delete("all")
                draw.grid_lines()
                if len(positions) < 1: return
                draw.line(positions, "white")
                if bearing is None: return
                last_position = positions[-1]
                draw.boat(last_position, bearing, "white", "black")