from ._base_button import ImportantButton


class LoadPacketBufferFromMcap(ImportantButton):
    '''Asks for a replay file from mcaptures and replays it into the packet buffer.'''
    LABEL = "menu_bar_buttons_load_button"

    def on_click(self):
        self.context.buffer.replay.load_json()
