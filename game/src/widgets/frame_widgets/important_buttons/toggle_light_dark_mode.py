from ._base_button import ImportantButton


class ToggleLightDarkMode(ImportantButton):
    '''Swaps the current theme between its light and dark variant.'''
    LABEL = "menu_bar_buttons_toggle_button"
    TOOLTIP = "menu_bar_tooltips_toggle_button"

    def on_click(self):
        self.context.style.toggle_mode()
