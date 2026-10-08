from ._base_button import ImportantButton


class ClearStatusConsole(ImportantButton):
    '''
    Forgets every status message so far, then asks the status console to
    clear its text (see requested_status_console_clear).
    '''
    LABEL = "menu_bar_buttons_clear_status_button"
    TOOLTIP = "menu_bar_tooltips_clear_status_button"

    def on_click(self):
        self.context.buffer.status.clear()
        self.context.states.set("requested_status_console_clear", value=1)
