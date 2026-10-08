from ._base_button import ImportantButton


class ClearAllCapturedBufferData(ImportantButton):
    '''
    Clears everything captured so far (packets, network graph, modbus
    readings, models, status messages - see Buffer.reset), then asks the
    packet and status consoles to clear theirs.
    '''
    LABEL = "menu_bar_buttons_clear_packets_button"
    TOOLTIP = "menu_bar_tooltips_clear_packets_button"

    def on_click(self):
        self.context.buffer.reset()
        self.context.buffer.status.clear()
        self.context.states.set("requested_packet_treeview_clear", value=1)
        self.context.states.set("requested_status_console_clear", value=1)
