from ._base_button import ToggleButton


class PausePacketConsole(ToggleButton):
    '''
    Switches packet_console "mode" between "live" and "paused" - the packet
    console and network graph read it every frame.
    '''
    LABEL = "menu_bar_buttons_pause"
    ACTIVE_LABEL = "menu_bar_buttons_unpause"

    def is_active(self) -> bool:
        return self.context.states.get("packet_console", "mode") == "paused"

    def start(self):
        self.context.states.set("packet_console", "mode", value="paused")

    def stop(self):
        self.context.states.set("packet_console", "mode", value="live")
