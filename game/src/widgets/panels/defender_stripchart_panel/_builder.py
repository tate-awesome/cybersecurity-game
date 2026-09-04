from ....app_core import Context
from ... import Scrollable
from ...canvases.strip_chart import StripChart
from ..panel import Panel

SUBMARINE_VARIABLES = ["x", "y", "theta", "speed", "rudder"]
HVAC_VARIABLES = ["temperature"]
VARIABLES = SUBMARINE_VARIABLES + HVAC_VARIABLES

# The four client/server clean/noisy channels - not "target", which barely
# moves and isn't worth a line on a rolling time chart the way it is as a
# reference column in the readout table.
CHANNELS = ["client_clean", "client_noisy", "server_clean", "server_noisy"]


class Builder(Panel):
    '''
    Defender-page counterpart to modbus_chart_panel: one strip chart per
    named defender_modbus variable, plotting its four client/server
    clean/noisy histories, shown/hidden by whichever variables belong to
    the AP's current mode (context.buffer.defender_status.submarine_mode) -
    checked every animation tick, not a static settings toggle.
    '''

    KEY = "defender_stripchart_panel"

    def __init__(self, master, context: Context):
        super().__init__(master, context, self.KEY)
        self.modbus = self.context.buffer.defender_modbus

        scrollable = Scrollable(self, context)
        scrollable.configure(fg_color=self.style.color("panel"))
        scrollable.columnconfigure(0, weight=1)
        time_offset = [0.0, 0.0]
        current_row = 0

        self.strip_charts = {}

        for key in VARIABLES:
            def get_title(k=key):
                return self.context.labels.get("modbus_variables", k)

            def get_units(k=key):
                return ""

            def get_factor(k=key):
                return 1.0

            def get_histories(k=key):
                raw = self.modbus.get_all_histories_and_legends(k)
                return {
                    self.context.labels.get("defender_modbus_readout", attribute): raw[attribute]
                    for attribute in CHANNELS if attribute in raw
                }

            strip_chart = StripChart(scrollable, context, (current_row, 0),
                                     get_title, get_units, get_factor,
                                     get_histories, time_offset=time_offset)
            strip_chart.start_animation()
            self.strip_charts[key] = strip_chart
            current_row += 1

        self.context.animation_manager.add_callback(f"DefenderStripchartVisibility_{id(self)}", self.refresh_visibility)
        self.refresh_visibility()

        self.menu_bar.minimize_button(scrollable, master)

    def refresh_visibility(self):
        submarine_mode = bool(self.context.buffer.defender_status.get("submarine_mode", True))
        active_variables = SUBMARINE_VARIABLES if submarine_mode else HVAC_VARIABLES

        for key, widget in self.strip_charts.items():
            visible = key in active_variables
            if visible and not widget.winfo_ismapped():
                self.update_idletasks()
                widget.grid()
            elif not visible and widget.winfo_ismapped():
                self.update_idletasks()
                widget.grid_remove()
