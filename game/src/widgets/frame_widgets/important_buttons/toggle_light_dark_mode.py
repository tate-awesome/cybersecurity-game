from ._base_button import ToggleButton


class ToggleLightDarkMode(ToggleButton):
    '''
    Swaps the current theme between its light and dark variant - labeled
    with the mode showing now ("Dark Mode" while dark), read from the theme
    itself, so it follows a mode changed anywhere else too.
    '''
    LABEL = "menu_bar_buttons_light_mode_button"
    ACTIVE_LABEL = "menu_bar_buttons_dark_mode_button"
    TOOLTIP = "menu_bar_tooltips_toggle_button"

    def is_active(self) -> bool:
        return self.context.style.current_theme.startswith("dark")

    def start(self):
        self.context.style.toggle_mode()

    def stop(self):
        self.context.style.toggle_mode()
