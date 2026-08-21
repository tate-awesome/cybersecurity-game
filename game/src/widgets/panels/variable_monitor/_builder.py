from ....app_core import Context
from ... import Scrollable
from ...canvases.strip_chart import StripChart
from ..panel import Panel
from typing import Callable

class Builder(Panel):
    def __init__(self, master, context: Context):
        super().__init__(master, context, "stripchart_panel")
        self.registers = self.context.states.get_registers()
        self.buffer = self.context.net.buffer.modbus

        scrollable = Scrollable(self, context)
        scrollable.configure(fg_color=self.style.color("panel"))
        scrollable.columnconfigure(0, weight=1)
        time_offset = [0.0, 0.0] # reference to two floats: time scale and time offset, used to synchronize the time axis of all strip charts in this monitor
        current_row = 0

        self.strip_charts = {}

        for key in self.registers:
            def get_title(k=key):
                variable_name = self.context.labels.variable_name(k)
                return variable_name

            def get_units(k=key):
                return self.context.states.get_register(k, "units")

            def get_factor(k=key):
                return self.context.states.get_register(k, "factor")

            def get_in(k=key):
                return self.buffer.get_history(k, "in")
            def get_out(k=key):
                return self.buffer.get_history(k, "out")
            def get_legend_in():
                return self.context.labels.get("stripcharts", "in")
            def get_legend_out():
                return self.context.labels.get("stripcharts", "out")

            strip_chart = StripChart(scrollable, context, (current_row, 0),
                                     get_title, get_units, get_factor, 
                                     [get_in, get_out], [get_legend_in, get_legend_out], time_offset)
            strip_chart.start_animation()
            self.strip_charts[key] = strip_chart
            current_row += 1
        self.context.animation_manager.add_callback("stripchart_visibility", self.refresh_visibility)

        # self.start_animation(framerate_ms=100)

        # menu_bar.minimize_button(scrollable, self.master)
        self.menu_bar.add_button() # set the zero point of the variable monitor
        self.menu_bar.add_button("pause") # pause or resume the variable monitor

        def start_fit():
            self.context.states.set("fit_stripchart_line", value=1)
        def stop_fit():
            self.context.states.set("fit_stripchart_line", value=0)
        fit_now = self.context.states.get("fit_stripchart_line")
        self.menu_bar.reversible_button(start_fit, stop_fit, "fit_stripchart", "unfit_stripchart",
                                         start_active=(fit_now == 1 or fit_now == "1"))

        self.menu_bar.add_button() # turn on the crosshairs

    def refresh_visibility(self):
        for key in self.context.states.get_registers():
            state = self.context.states.get_register(key, "show")
            widget = self.strip_charts[key]
            if state == "1" or state == 1:
                if not widget.winfo_ismapped():
                    self.update_idletasks()
                    widget.grid()
            else:
                if widget.winfo_ismapped():
                    self.update_idletasks()
                    widget.grid_remove()