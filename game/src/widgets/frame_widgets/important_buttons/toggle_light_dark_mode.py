import darkdetect

from ._base_button import ToggleButton


class ToggleLightDarkMode(ToggleButton):
    '''
    Swaps the current theme between its light and dark variant - labeled
    with what clicking does ("Switch to Light Mode" while dark), read from
    the theme itself, so it follows a mode changed anywhere else too. When
    the system (darkdetect) prefers the mode it switches to, the label says
    so, and the tooltip names the system's mode.

    A theme with only one mode (see Style.theme_modes) has nothing to switch
    to - the button is off, says which mode the theme is in ("Dark Mode
    Only"), and its tooltip says to pick another theme for the other.
    '''
    LABEL = "menu_bar_buttons_switch_to_dark_mode_button"
    ACTIVE_LABEL = "menu_bar_buttons_switch_to_light_mode_button"
    TOOLTIP = "menu_bar_tooltips_toggle_button"

    def is_active(self) -> bool:
        return self.context.style.current_theme.startswith("dark")

    def theme_only_mode(self) -> str | None:
        '''The current theme's one mode, if it only has one - else None.'''
        modes = self.context.style.theme_modes()
        return modes[0] if len(modes) == 1 else None

    def sync_state(self):
        super().sync_state()
        # A one-mode theme can replace one with both without the mode changing
        if self.theme_only_mode() != self.only_mode:
            self.show_state()

    def show_state(self):
        super().show_state()
        labels = self.context.labels
        self.only_mode = self.theme_only_mode()
        self.setEnabled(self.only_mode is None)
        if self.only_mode is not None:
            if self.icons is None:
                self.setText(labels.get(f"menu_bar_buttons_{self.only_mode}_mode_only_button"))
            self.setToolTip(labels.get(f"menu_bar_tooltips_toggle_button_{self.only_mode}_only"))
            return
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
