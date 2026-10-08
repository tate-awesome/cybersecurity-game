from ._base_button import ImportantButton


class LoadMcapIntoPacketBuffer(ImportantButton):
    '''Asks for a replay file from mcaptures and loads it into the packet buffer as fast as it takes packets.'''
    LABEL = "menu_bar_buttons_load_json_fast_button"
    TOOLTIP = "menu_bar_tooltips_load_json_fast_button"

    def on_click(self):
        self.context.buffer.replay.load_json(realtime=False)
