from customtkinter import *

from ...app_core.context import Context
from .. import StripChart, MenuBar
from ...network.data_buffer import DataBuffer
from typing import cast, Callable
from .. import Scrollable

class VariableMonitor(CTkFrame):
    def __init__(self, parent, context: Context, variables: dict[str, Callable[None, list[float, float]]]):
        super().__init__(parent)
        style = context.style
        self.pack(fill="both", expand=True)
        self.parent = parent
        self.context = context
        self.variables = variables
        self.buffer = cast(DataBuffer, self.context.net.data_buffer)

        menu_bar = MenuBar(self, context, "Variable Monitor")
        # menu_bar.configure(fg_color=style.color("widget"))

        scrollable = Scrollable(self, context)
        self.configure(fg_color=style.color("panel"))
        scrollable.configure(fg_color=style.color("panel"))
        menu_bar.configure(fg_color=style.color("widget"))
        time_offset = [0.0, 0.0] # reference to two floats: time scale and time offset, used to synchronize the time axis of all strip charts in this monitor

        self.strip_charts = []

        for var_name, var_func in self.variables.items():
            strip_chart = StripChart(scrollable, context, var_func, var_name)

        menu_bar.add_button("Customize") # set the zero point of the variable monitor
        menu_bar.add_button("Pause") # pause or resume the variable monitor
        menu_bar.add_button("Time Window") # change the time window duration of the variable monitor # move the time window
        menu_bar.add_button("Crosshairs on") # turn on the crosshairs