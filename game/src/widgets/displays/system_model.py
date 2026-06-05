from customtkinter import *

from ..style import Style
from .map import Map
from ...drawing.viewport import ViewPort
from .boat_focus import BoatFocus
from .values_table import ValuesTable
from .. import common
from ...network.data_buffer import DataBuffer
from typing import cast

class SystemModel:
    def __init__(self, style, parent, context):
        self.style = style
        self.parent = parent
        self.context = context
        self.buffer = cast(DataBuffer, self.context.net.data_buffer)

        self.menu_bar = self.create_menu_bar(parent)

        self.create_menu_button(self.menu_bar, "Customize")
        self.create_menu_button(self.menu_bar, "Reset View")
        self.create_menu_button(self.menu_bar, "Clear Values")
        self.create_menu_button(self.menu_bar, "Center on Boat") #Move with boat


        def draw_full_map(canvas, draw_lock, scale: float, offset: tuple[float, float]):
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

        # map_frame = CTkFrame(parent)
        # map_frame.pack(side="top", fill="both", expand=True)
        map = Map(style, parent, draw_full_map, 100)


    def create_menu_bar(self, parent):
        frame = CTkFrame(parent)
        frame.pack(side="top", fill="x", pady=self.style.gaptop, padx=self.style.gap)

        header = CTkLabel(frame, text="System Model", font=self.style.get_font(), padx=self.style.igap)
        header.pack(fill=Y, side="left", padx=self.style.gap)
        return frame

    def create_menu_button(self, frame, text, function=None):
        med = self.style.get_font()
        button = CTkButton(frame, text=text, command=function, font=med)
        button.pack(side="right", padx=self.style.gap, pady=self.style.gap)
        return button
