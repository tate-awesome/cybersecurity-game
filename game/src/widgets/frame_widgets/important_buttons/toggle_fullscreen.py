from ._base_button import ToggleButton


class ToggleFullscreen(ToggleButton):
    '''Switches fullscreen on or off, and saves it - the same as the Toggle Fullscreen keybind (F11 by default).'''
    LABEL = "menu_bar_buttons_enter_fullscreen_button"
    ACTIVE_LABEL = "menu_bar_buttons_exit_fullscreen_button"
    TOOLTIP = "menu_bar_tooltips_fullscreen_button"

    def is_active(self) -> bool:
        return self.context.root.isFullScreen()

    def start(self):
        self.context.keybinds.set_fullscreen(True, save=True)

    def stop(self):
        self.context.keybinds.set_fullscreen(False, save=True)
