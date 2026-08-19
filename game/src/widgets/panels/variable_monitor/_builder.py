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
            def get_title():
                # Resolve nickname and configure label
                nickname = self.context.states.get_register(key, "nickname")
                if len(nickname) > 0:
                    variable_name = nickname
                else:
                    variable_name = self.context.labels.get("modbus_variables", key)
                return variable_name

            def get_units():
                return self.context.states.get_register(key, "units")

            def get_factor():
                return self.context.states.get_register(key, "factor")

            def get_in():
                return self.buffer.get_history(key, "in")
            def get_out():
                return self.buffer.get_history(key, "out")

            strip_chart = StripChart(scrollable, context, (current_row, 0),
                                     get_title, get_units, get_factor, 
                                     [get_in, get_out], time_offset)
            strip_chart.start_animation()
            self.strip_charts[key] = strip_chart
            current_row += 1
        self.context.animation_manager.add_callback("stripchart_visibility", self.refresh_visibility)

        # self.start_animation(framerate_ms=100)

        # menu_bar.minimize_button(scrollable, self.master)
        self.menu_bar.add_button() # set the zero point of the variable monitor
        self.menu_bar.add_button("pause") # pause or resume the variable monitor
        self.menu_bar.add_button() # change the time window duration of the variable monitor # move the time window
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