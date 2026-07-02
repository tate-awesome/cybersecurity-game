from customtkinter import *

from ...app_core.context import Context
from .. import WorldMap, MenuBar
from ...drawing.viewport import ViewPort
from .boat_focus import BoatFocus
from .values_table import ValuesTable
from ...network.data_buffer import DataBuffer
from typing import cast

class BoatModel:
    def __init__(self, parent, context: Context):
        self.style = context.style
        self.parent = parent
        self.context = context
        self.buffer = cast(DataBuffer, self.context.net.data_buffer)

        menu_bar = MenuBar(parent, context, "System Model")


        map = WorldMap(self.parent, context)

        menu_bar.add_button("Customize")
        menu_bar.add_button("Reset View", map.camera.reset_scale)
        menu_bar.add_button("Clear Values")
        menu_bar.add_button("Center on Boat")


    def create_menu_button(self, frame, text, function=None):
        med = self.style.get_font()
        button = CTkButton(frame, text=text, command=function, font=med)
        button.pack(side="right", padx=self.style.gap, pady=self.style.gap)
        return button
