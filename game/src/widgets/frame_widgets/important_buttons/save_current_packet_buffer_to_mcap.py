from ._base_button import ImportantButton


class SaveCurrentPacketBufferToMcap(ImportantButton):
    '''Asks where to save, then writes the packet buffer to a replay file in mcaptures.'''
    LABEL = "menu_bar_buttons_save_button"
    TOOLTIP = "menu_bar_tooltips_save_button"

    def on_click(self):
        self.context.buffer.replay.save_json()
