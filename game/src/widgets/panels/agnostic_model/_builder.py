from ....app_core import Context
from ...canvases.world_map import WorldMap
from ...canvases.strip_chart import StripChart
from ..panel import Panel
from typing import cast

class Builder(Panel):
    def __init__(self, master, context: Context):
        super().__init__(master, context, "submarine_panel")

        for key in self.registers:
            def get_title(k=key):
                # Resolve nickname and configure label
                nickname = self.context.states.get_register(k, "nickname")
                if len(nickname) > 0:
                    variable_name = nickname
                else:
                    variable_name = self.context.labels.get("modbus_variables", k)
                return variable_name

            def get_units(k=key):
                return self.context.states.get_register(k, "units")

            def get_factor(k=key):
                return self.context.states.get_register(k, "factor")

            def get_in(k=key):
                return self.buffer.get_history(k, "in")
            def get_out(k=key):
                return self.buffer.get_history(k, "out")

        strip_chart = StripChart(scrollable, context, (current_row, 0),
                                    get_title, get_units, get_factor, 
                                    [get_in, get_out], time_offset)
            strip_chart.start_animation()
            self.strip_charts[key] = strip_chart
            current_row += 1
                self.context.animation_manager.add_callback("stripchart_visibility", self.refresh_visibility)
        map = WorldMap(self, context)

        self.menu_bar.minimize_button(map, master)