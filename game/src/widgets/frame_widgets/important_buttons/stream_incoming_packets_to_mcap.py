from ._base_button import ToggleButton


class StreamIncomingPacketsToMcap(ToggleButton):
    '''Starts/stops continuously writing captured packets to a JSON Lines file in mcaptures.'''
    LABEL = "menu_bar_buttons_stream_button"
    ACTIVE_LABEL = "menu_bar_buttons_stream_button_active"
    TOOLTIP = "menu_bar_tooltips_stream_button"

    def start(self):
        self.context.buffer.file_stream.start()

    def stop(self):
        self.context.buffer.file_stream.stop()
