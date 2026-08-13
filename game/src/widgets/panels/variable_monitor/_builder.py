from ....app_core import Context
from ... import Scrollable
from ...canvases.strip_chart import StripChart
from ..panel import Panel
from typing import Callable

class Builder(Panel):
    def __init__(self, master, context: Context, variables: dict[str, Callable[None, list[float, float]]]):
        super().__init__(master, context, "Variable Monitor")
        self.variables = variables

        scrollable = Scrollable(self, context)
        scrollable.configure(fg_color=self.style.color("panel"))
        time_offset = [0.0, 0.0] # reference to two floats: time scale and time offset, used to synchronize the time axis of all strip charts in this monitor

        self.strip_charts = []

        for var_name, var_func in self.variables.items():
            strip_chart = StripChart(scrollable, context, var_func, var_name, time_offset)
            strip_chart.start_animation()
            self.strip_charts.append(strip_chart)

        # self.start_animation(framerate_ms=100)

        # menu_bar.minimize_button(scrollable, self.master)
        self.menu_bar.add_button("Customize") # set the zero point of the variable monitor
        self.menu_bar.add_button("Pause") # pause or resume the variable monitor
        self.menu_bar.add_button("Time Window") # change the time window duration of the variable monitor # move the time window
        self.menu_bar.add_button("Crosshairs on") # turn on the crosshairs