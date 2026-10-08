from ._base_button import ImportantButton


class SelectColorTheme(ImportantButton):
    '''Opens a picker for the theme's color family (keeps light/dark as is).'''
    LABEL = "menu_bar_buttons_theme_button"
    TOOLTIP = "menu_bar_tooltips_theme_button"

    def on_click(self):
        self.context.style.select_theme()
