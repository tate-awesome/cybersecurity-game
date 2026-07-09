from customtkinter import *

from ...app_core.context import Context
from .. import MenuBar
from .values_table import ValuesTable
from ...network.data_buffer import DataBuffer
from typing import cast

class NetworkVisualizer(CTkFrame):
    def __init__(self, master, context: Context):
        super().__init__(master, fg_color=context.style.color("panel"))
        style = context.style
        self.pack(fill="both", expand=True, padx=style.nogap, pady=style.nogap)
        self.style = style
        self.master = master
        self.context = context
        self.buffer = cast(DataBuffer, self.context.net.data_buffer)

        menu_bar = MenuBar(self, context, "System Model")
        menu_bar.configure(fg_color=style.color("widget"))



        menu_bar.minimize_button(None, master)
        menu_bar.add_button("Freeze Time")
        menu_bar.add_button("Show Less")
        menu_bar.add_button("Show More")