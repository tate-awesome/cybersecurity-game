from ._base_button import ImportantButton


class ResetTheme(ImportantButton):
    '''Puts the theme and everything the theme editor changes back to the defaults, keeping light or dark (see Style.reset_theme).'''
    LABEL = "menu_bar_buttons_reset_theme_button"
    TOOLTIP = "menu_bar_tooltips_reset_theme_button"

    def on_click(self):
        self.context.style.reset_theme()
