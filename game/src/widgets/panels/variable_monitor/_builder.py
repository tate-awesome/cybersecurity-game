from ....app_core.context import Context
from ....network.data_buffer import DataBuffer
from ... import Scrollable
from ...canvases.strip_chart import StripChart
from ..panel import Panel
from typing import cast, Callable

class Builder(Panel):
    def __init__(self, master, context: Context, variables: dict[str, Callable[None, list[float, float]]]):
        super().__init__(master, context, "Variable Monitor")
        self.variables = variables
        self.buffer = cast(DataBuffer, self.context.net.data_buffer)

        scrollable = Scrollable(self, context)
        scrollable.configure(fg_color=self.style.color("panel"))
        time_offset = [0.0, 0.0] # reference to two floats: time scale and time offset, used to synchronize the time axis of all strip charts in this monitor

        self.strip_charts = []

        for var_name, var_func in self.variables.items():
            strip_chart = StripChart(scrollable, context, var_func, var_name, time_offset)
            self.strip_charts.append(strip_chart)

        self.start_animation(framerate_ms=100)

        # menu_bar.minimize_button(scrollable, self.master)
        self.menu_bar.add_button("Customize") # set the zero point of the variable monitor
        self.menu_bar.add_button("Pause") # pause or resume the variable monitor
        self.menu_bar.add_button("Time Window") # change the time window duration of the variable monitor # move the time window
        self.menu_bar.add_button("Crosshairs on") # turn on the crosshairs


    def animation_loop(self):
        for strip_chart in self.strip_charts:
            strip_chart.frame_callback()
        if self.do_animation_loop:
            self.after_id = self.after(self.framerate_ms, self.animation_loop)
            
    def start_animation(self, framerate_ms: float = 100):
        self.framerate_ms = framerate_ms
        self.do_animation_loop = True
        self.animation_loop()


    def stop_animation(self):
        self.do_animation_loop = False
        if self.after_id is not None:
            self.after_cancel(self.after_id)
            self.after_id = None