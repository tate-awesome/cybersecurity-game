import darkdetect

from ._base_button import ToggleButton


class ToggleLightDarkMode(ToggleButton):
    '''
    Swaps the current theme between its light and dark variant - labeled
    with what clicking does ("Switch to Light Mode" while dark), read from
    the theme itself, so it follows a mode changed anywhere else too. When
    the system (darkdetect) prefers the mode it switches to, the label says
    so, and the tooltip names the system's mode.
    '''
    LABEL = "menu_bar_buttons_switch_to_dark_mode_button"
    ACTIVE_LABEL = "menu_bar_buttons_switch_to_light_mode_button"
    TOOLTIP = "menu_bar_tooltips_toggle_button"

    def is_active(self) -> bool:
        return self.context.style.current_theme.startswith("dark")

    def show_state(self):
        super().show_state()
        labels = self.context.labels
        # Read on every state change, not every frame - darkdetect can spawn a
        # process (gsettings on Linux). None when the system has no preference
        system_dark = darkdetect.isDark()
        tooltip = labels.get(self.TOOLTIP)
        if system_dark is not None:
            tooltip += " " + labels.get(f"menu_bar_tooltips_toggle_button_system_{'dark' if system_dark else 'light'}")
            # Switching to the system's mode (it isn't the current one) - noted on the label
            if self.icons is None and system_dark != self.active:
                self.setText(f"{self.text()}{labels.get('menu_bar_buttons_system_mode_suffix')}")
        self.setToolTip(tooltip)

    def start(self):
        self.context.style.toggle_mode()

    def stop(self):
        self.context.style.toggle_mode()
