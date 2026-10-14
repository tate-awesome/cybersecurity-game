from ._base_button import ImportantButton


class OpenAppearanceSettings(ImportantButton):
    '''Opens the settings page on its Appearance tab - the theme editor, imported themes and resetting the theme are there (Back returns here).'''
    LABEL = "menu_bar_buttons_appearance_settings_button"
    TOOLTIP = "menu_bar_tooltips_appearance_settings_button"

    def on_click(self):
        # Imported here - pages import widgets, so not at the top
        from ....pages.settings import SettingsPage
        SettingsPage.selected_tab = SettingsPage.APPEARANCE_TAB
        self.context.router.show("settings")
