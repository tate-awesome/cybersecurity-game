from ....app_core import Context
from ...canvases.world_map import WorldMap
from ...canvases.strip_chart import StripChart
from ...frame_widgets.scrollable import Scrollable
from customtkinter import CTkFrame
from ..panel import Panel
from typing import cast

class Builder(Panel):
    def __init__(self, master, context: Context):
        super().__init__(master, context, "agnostic_panel")
        wrapper = CTkFrame(self)
        wrapper.pack(fill="both", expand=True)
        wrapper.columnconfigure(0, weight=1)
        wrapper.rowconfigure(0, weight=1)

        getters = []
        def get_title():
            variable_name = self.context.labels.get("agnostic_model", "stripchart_title")
            return variable_name
        def get_units():
            return self.context.labels.get("agnostic_model", "stripchart_units")
        def get_factor():
                return 1.0
        for key in self.context.states.get_registers():
            getters.append(lambda k=key: self.context.net.buffer.modbus.get_history(k, "in"))
            getters.append(lambda k=key: self.context.net.buffer.modbus.get_history(k, "out"))
            def legend_in(k=key):
                return f"{self.context.labels.get("")}{self.context.labels.get("stripcharts", "in")}"
            def legend_out(k=key):
                return
        strip_chart = StripChart(wrapper, context, (0, 0),
                                    get_title, get_units, get_factor, 
                                    getters)
        strip_chart.start_animation()
        self.menu_bar.minimize_button(strip_chart, master)