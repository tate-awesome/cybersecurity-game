from ._base_button import ToggleButton


class FreeScrollStatusConsole(ToggleButton):
    '''
    Switches status_console "scroll" between "live" (follow new lines) and
    "free" (stop following so the student can scroll back) - the status
    console reads it every frame.
    '''
    LABEL = "menu_bar_buttons_free_scroll"
    ACTIVE_LABEL = "menu_bar_buttons_live_scroll"

    def starts_active(self) -> bool:
        return self.context.states.get("status_console", "scroll") == "free"

    def start(self):
        self.context.states.set("status_console", "scroll", value="free")

    def stop(self):
        self.context.states.set("status_console", "scroll", value="live")
