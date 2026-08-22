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

        def get_title():
            return self.context.labels.get("agnostic_model", "stripchart_title")
        def get_units():
            return self.context.labels.get("agnostic_model", "stripchart_units")
        def get_factor():
            return 1.0

        def get_histories():
            # Every register's history, across every exchange type, overlaid on
            # one combined chart - keys are "<variable name> <direction>" so
            # each line's legend identifies both. Registers with no data yet
            # (e.g. no sniffed third-party traffic) are skipped rather than
            # burning a color-cycle slot on an invisible line.
            histories = {}
            for key in self.context.states.get_registers():
                variable_name = self.context.labels.variable_name(key)
                for direction, points in self.context.net.buffer.modbus.get_all_histories_and_legends(key).items():
                    if not points:
                        continue
                    histories[f"{variable_name} {direction}"] = points
            return histories

        strip_chart = StripChart(wrapper, context, (0, 0),
                                    get_title, get_units, get_factor,
                                    get_histories)
        strip_chart.start_animation()
        self.menu_bar.minimize_button(strip_chart, master)