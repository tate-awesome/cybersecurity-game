from ._base_button import ToggleButton


class ToggleDebugLabels(ToggleButton):
    '''
    Switches labels debug mode (see LocalizationManager.is_debug) - every
    widget shows its label key instead of its text - and rebuilds the page
    so they all pick it up.
    '''
    LABEL = "menu_bar_buttons_debug_labels_button"
    ACTIVE_LABEL = "menu_bar_buttons_resolve_labels_button"
    TOOLTIP = "menu_bar_tooltips_debug_labels_button"

    def is_active(self) -> bool:
        return self.context.labels.is_debug()

    def show_state(self):
        # Always real text - this button has to stay findable in debug mode
        self.setText(self.context.labels.get_text(self.ACTIVE_LABEL if self.active else self.LABEL))

    def start(self):
        self.context.labels.set_debug(True)
        self.context.router.refresh()

    def stop(self):
        self.context.labels.set_debug(False)
        self.context.router.refresh()
