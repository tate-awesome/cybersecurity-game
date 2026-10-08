from ._base_button import ImportantButton


class ClearAllCapturedBufferData(ImportantButton):
    '''
    Clears everything captured so far (packets, network graph, modbus
    readings, models - see Buffer.reset), then asks the packet console to
    clear its rows (see PacketTreeview.clear_if_requested).
    '''
    LABEL = "menu_bar_buttons_clear_packets_button"

    def on_click(self):
        self.context.buffer.reset()
        self.context.states.set("requested_packet_treeview_clear", value=1)
