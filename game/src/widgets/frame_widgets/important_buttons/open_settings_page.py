from ._base_button import ImportantButton


class OpenSettingsPage(ImportantButton):
    '''Opens the settings page (Back returns here).'''
    LABEL = "menu_bar_buttons_settings_button"
    TOOLTIP = "menu_bar_tooltips_settings_button"

    def on_click(self):
        self.context.router.show("settings")
