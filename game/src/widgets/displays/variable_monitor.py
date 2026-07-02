from customtkinter import *

from ...app_core.context import Context
from .. import StripChart, MenuBar
from ...network.data_buffer import DataBuffer
from typing import cast, Callable

class VariableMonitor(CTkFrame):
    def __init__(self, parent, context: Context, variables: dict[str, Callable[None, list[float, float]]]):
        super().__init__(parent, fg_color=context.style.color("panel"))
        style = context.style
        self.pack(fill="both", expand=True, padx=style.nogap, pady=style.nogap, ipadx=style.nogap[0], ipady=style.nogap[0])
        self.parent = parent
        self.context = context
        self.variables = variables
        self.buffer = cast(DataBuffer, self.context.net.data_buffer)

        menu_bar = MenuBar(self, context, "Variable Monitor")
        menu_bar.configure(fg_color=style.color("widget"))
        menu_bar.pack_configure(padx=style.nogap, pady=style.nogap) #TODO fix for padding

        for var_name, var_func in self.variables.items():
            strip_chart = StripChart(self, context, var_func, var_name)

        menu_bar.add_button("Customize") # set the zero point of the variable monitor
        menu_bar.add_button("Pause") # pause or resume the variable monitor
        menu_bar.add_button("Time Window") # change the time window duration of the variable monitor # move the time window
        menu_bar.add_button("Crosshairs on") # turn on the crosshairs