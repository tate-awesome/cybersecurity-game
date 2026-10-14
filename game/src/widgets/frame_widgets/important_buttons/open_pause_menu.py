from ._base_button import ImportantButton


class OpenPauseMenu(ImportantButton):
    '''Opens the pause menu (see PauseMenu) - the same as Esc.'''
    LABEL = "menu_bar_buttons_home_button"
    TOOLTIP = "menu_bar_tooltips_home_button"
    ICON = "menu-2"

    def on_click(self):
        self.context.router.pause_menu.open()
