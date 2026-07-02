from customtkinter import *

from ...app_core.context import Context
from .. import WorldMap, MenuBar
from ...drawing.viewport import ViewPort
from .boat_focus import BoatFocus
from .values_table import ValuesTable
from ...network.data_buffer import DataBuffer
from typing import cast

class BoatModel(CTkFrame):
    def __init__(self, parent, context: Context):
        super().__init__(parent, fg_color=context.style.color("panel"))
        style = context.style
        self.pack(fill="both", expand=True, padx=style.nogap, pady=style.nogap, ipadx=style.nogap[0], ipady=style.nogap[0])
        self.style = style
        self.parent = parent
        self.context = context
        self.buffer = cast(DataBuffer, self.context.net.data_buffer)

        menu_bar = MenuBar(self, context, "System Model")
        menu_bar.configure(fg_color=style.color("widget"))


        map = WorldMap(self, context)

        menu_bar.add_button("Customize")
        menu_bar.add_button("Reset View", map.camera.reset_scale)
        menu_bar.add_button("Clear Values")
        menu_bar.add_button("Center on Boat")