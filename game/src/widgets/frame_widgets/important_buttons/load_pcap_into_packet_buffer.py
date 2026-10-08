from ._base_button import ImportantButton


class LoadPcapIntoPacketBuffer(ImportantButton):
    '''Asks for a pcap file and loads its packets into the packet buffer as fast as it takes them.'''
    LABEL = "menu_bar_buttons_pcap_button"
    TOOLTIP = "menu_bar_tooltips_pcap_button"

    def on_click(self):
        self.context.buffer.loader.load_pcap(realtime=False)
