from ....app_core import Context
from ... import Scrollable
from ...canvases.strip_chart import StripChart
from ..panel import Panel

SUBMARINE_VARIABLES = ["x", "y", "theta", "speed", "rudder"]
HVAC_VARIABLES = ["temperature", "heater"]
VARIABLES = SUBMARINE_VARIABLES + HVAC_VARIABLES


class Builder(Panel):
    '''
    Defender-page counterpart to modbus_chart_panel: one strip chart per
    named defender_modbus variable, plotting every history it actually has
    (client/server clean/noisy readings, plus target where recorded),
    shown/hidden by whichever variables belong to the AP's current mode
    (context.buffer.defender_status.submarine_mode) - checked every
    animation tick, not a static settings toggle.
    '''

    KEY = "defender_stripchart_panel"

    # The settings keys (see _packages/_default.json) this panel reads or writes -
    # the workspace editor lists it under each of them
    # Draws with the strip chart canvas
    SETTINGS = (
        "strip_chart_colors",
        "strip_chart_auto_fit",
        "strip_chart_auto_fit_max_seconds",
    )

    def __init__(self, master, context: Context):
        super().__init__(master, context, self.KEY)
        self.modbus = self.context.buffer.defender_modbus

        scrollable = Scrollable(self, context)
        scrollable.columnconfigure(0, weight=1)
        time_offset = [0.0, 0.0]
        current_row = 0

        self.strip_charts = {}

        for key in VARIABLES:
            def get_title(k=key):
                return self.context.labels.get(f"modbus_variables_{k}")

            def get_units(k=key):
                return ""

            def get_factor(k=key):
                return 1.0

            def get_histories(k=key):
                # Every attribute this variable actually has history for -
                # client/server clean/noisy readings and target - same as
                # variable_monitor's unfiltered get_all_histories_and_legends
                # for the attacker-side stripcharts. Which attributes exist
                # is already decided by what poll_unpacker ever put() for
                # this variable (e.g. HVAC's "heater"/"temperature" only
                # ever get a client_clean history, plus target for temperature).
                raw = self.modbus.get_all_histories_and_legends(k)
                return {
                    self.context.labels.get(f"defender_modbus_readout_{attribute}"): history
                    for attribute, history in raw.items()
                }

            def get_now(k=key):
                # The poller's own clock, not the packet one - so these
                # scroll as soon as polling starts, sniffer or not.
                return self.modbus.get_relative_now(k)

            strip_chart = StripChart(scrollable, context, (current_row, 0),
                                     get_title, get_units, get_factor,
                                     get_histories, time_offset=time_offset,
                                     now_getter=get_now)
            strip_chart.start_animation()
            self.strip_charts[key] = strip_chart
            current_row += 1

        self._submarine_mode = None
        self.context.animation_manager.add_callback(f"DefenderStripchartVisibility_{id(self)}", self.refresh_visibility)
        self.refresh_visibility()

        self.menu_bar.minimize_button(scrollable, master)

    def refresh_visibility(self):
        submarine_mode = bool(self.context.buffer.defender_status.get("submarine_mode", True))
        if submarine_mode == self._submarine_mode:
            return
        self._submarine_mode = submarine_mode
        active_variables = SUBMARINE_VARIABLES if submarine_mode else HVAC_VARIABLES

        for key, widget in self.strip_charts.items():
            widget.setVisible(key in active_variables)

        # HVAC history's clock only advances while some HVAC view is
        # showing it (see DefenderModbusBuffer.pause_hvac) - these charts
        # count, or they'd plot every sample at one frozen x position
        # whenever the HVAC model isn't also on screen.
        if submarine_mode:
            self.modbus.pause_hvac(self)
        else:
            self.modbus.resume_hvac(self)
