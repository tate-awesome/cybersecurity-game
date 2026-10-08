from ._base_button import ImportantButton


class StreamPcapIntoPacketBuffer(ImportantButton):
    '''Asks for a pcap file and replays its packets into the packet buffer with their recorded timing.'''
    LABEL = "menu_bar_buttons_stream_pcap_button"
    TOOLTIP = "menu_bar_tooltips_stream_pcap_button"

    def on_click(self):
        self.context.buffer.loader.load_pcap(realtime=True)
