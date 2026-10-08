from ...overlay import Overlay
from .settings_overlay_button import SettingsOverlayButton


class EditStripChartStyle(SettingsOverlayButton):
    '''
    Opens an editor for how strip charts draw: which parts are drawn
    (strip_chart_sprites), their colors (strip_chart_colors - one per line
    for "paths"/"heads"), and fit mode (strip_chart_auto_fit,
    strip_chart_auto_fit_max_seconds). Strip charts read these every frame.
    '''
    LABEL = "menu_bar_buttons_strip_chart_style_button"
    TOOLTIP = "menu_bar_tooltips_strip_chart_style_button"

    def populate(self, overlay: Overlay):
        states = self.context.states

        sprites = self.section("strip_chart_sprites")
        for key in states.get("strip_chart_sprites"):
            sprites.checkbox("strip_chart_sprites", key)

        colors = self.section("strip_chart_colors")
        for key, value in states.get("strip_chart_colors").items():
            if isinstance(value, list):
                for index in range(len(value)):
                    colors.color("strip_chart_colors", key, index)
            else:
                colors.color("strip_chart_colors", key)

        fit = self.section("strip_chart_fit")
        fit.checkbox("strip_chart_auto_fit")
        fit.number("strip_chart_auto_fit_max_seconds")
