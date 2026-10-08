from ._base_button import ImportantButton


class ClearPacketConsole(ImportantButton):
    '''
    Clears the captured packets and the network graph built from them, then
    asks the packet console to clear its rows (see PacketTreeview.clear_if_requested).
    '''
    LABEL = "menu_bar_buttons_clear_packet_console_button"
    TOOLTIP = "menu_bar_tooltips_clear_packet_console_button"

    def on_click(self):
        self.context.buffer.packets.reset()
        self.context.buffer.network.reset()
        self.context.states.set("requested_packet_treeview_clear", value=1)
