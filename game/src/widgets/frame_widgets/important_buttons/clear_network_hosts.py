from ._base_button import ImportantButton


class ClearNetworkHosts(ImportantButton):
    '''
    Forgets every host the network graph has seen (see NetworkGraph.reset),
    so it starts over from the next packets - nicknames are kept, in
    preferences. The packets themselves stay in the packet console.
    '''
    LABEL = "menu_bar_buttons_clear_network_hosts_button"
    TOOLTIP = "menu_bar_tooltips_clear_network_hosts_button"

    def on_click(self):
        self.context.buffer.network.reset()
