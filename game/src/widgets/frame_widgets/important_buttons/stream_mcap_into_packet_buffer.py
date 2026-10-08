from ._base_button import ImportantButton


class StreamMcapIntoPacketBuffer(ImportantButton):
    '''Asks for a replay file from mcaptures and replays it into the packet buffer with its recorded timing.'''
    LABEL = "menu_bar_buttons_load_button"
    TOOLTIP = "menu_bar_tooltips_load_button"

    def on_click(self):
        self.context.buffer.replay.load_json(realtime=True)
