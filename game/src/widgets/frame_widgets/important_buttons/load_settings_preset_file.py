from ._base_button import ImportantButton


class LoadSettingsPresetFile(ImportantButton):
    '''Asks for a settings JSON file and merges it over the current settings.'''
    LABEL = "menu_bar_buttons_preset_button"
    TOOLTIP = "menu_bar_tooltips_preset_button"

    def on_click(self):
        self.context.states.select()
