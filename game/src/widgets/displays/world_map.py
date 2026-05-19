from ...app_core.context import Context
from ...network.meta_packet import MetaPacket
from ...network.data_buffer import DataBuffer

from ...drawing.viewport import ViewPort
from ...widgets.map import Map

from customtkinter import *

class WorldMap:
    def __init__(self, style, parent, context, buffer: DataBuffer):
        self.style = style
        self.parent = parent
        self.context = context
        self.buffer = buffer
        

    def create_menu_bar(self, parent):
        frame = CTkFrame(parent)
        frame.pack(side="top", fill="x", pady=self.style.gaptop, padx=self.style.gap)

        header = CTkLabel(frame, text="Packet Stream", font=self.style.get_font(), padx=self.style.igap)
        header.pack(fill=Y, side="left", padx=self.style.gap)
        return frame

    def create_menu_button(self, frame, text, function=None):
        med = self.style.get_font()
        button = CTkButton(frame, text=text, command=function, font=med)
        button.pack(side="right", padx=self.style.gap, pady=self.style.gap)
        return button

    def draw_full_map(self, canvas, draw_lock, scale: float, offset: tuple[float, float]):
            positions = self.buffer.get_simple_path("in")
            bearing = self.buffer.get_bearing("in")
            draw = ViewPort(canvas, scale, offset)
            with draw_lock:
                canvas.delete("all")
                draw.ocean()
                draw.grid_lines()
                if len(positions) < 1: return
                draw.line(positions, "yellow")
                if bearing is None: return
                last_position = positions[-1]
                draw.boat(last_position, bearing, "yellow", "yellow")