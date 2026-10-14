from ._base_button import ImportantButton


class OpenAppearanceSettings(ImportantButton):
    '''Opens the settings page on its Appearance tab - the theme editor, imported themes and resetting the theme are there (Back returns here).'''
    LABEL = "menu_bar_buttons_appearance_settings_button"
    TOOLTIP = "menu_bar_tooltips_appearance_settings_button"
    OPENS = "page"

    def on_click(self):
        # Imported here - pages import widgets, so not at the top
        from ....pages.settings import SettingsPage
        SettingsPage.selected_tab = SettingsPage.APPEARANCE_TAB
        page = self.context.router.current_frame
        if isinstance(page, SettingsPage) and type(page) is SettingsPage:
            # Already here - going to it does nothing (see Router.show), so just switch tabs
            page.tabs.setCurrentIndex(SettingsPage.APPEARANCE_TAB)
            return
        self.context.router.show("settings")
