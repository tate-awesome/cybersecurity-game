from ._base_button import ToggleButton


class ToggleStripChartAutoFit(ToggleButton):
    '''Switches strip charts between fitting their data and aligning time (the strip_chart_auto_fit setting).'''
    LABEL = "menu_bar_buttons_fit_stripchart"
    ACTIVE_LABEL = "menu_bar_buttons_unfit_stripchart"

    def is_active(self) -> bool:
        return self.context.states.get("strip_chart_auto_fit") in (1, "1")

    def start(self):
        self.context.states.set("strip_chart_auto_fit", value=1)

    def stop(self):
        self.context.states.set("strip_chart_auto_fit", value=0)
