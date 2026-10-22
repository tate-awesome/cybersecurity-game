from .....app_core import Context
from .._base_button import ImportantButton
from .host_overlay import HostOverlay


class EditNetworkHosts(ImportantButton):
    '''
    Opens the host editor: a nickname for every device (MAC address) seen
    so far, and whether the network graph hides it (network_hosts) - the
    network graph follows the setting.
    '''
    LABEL = "menu_bar_buttons_network_hosts_overlay"
    TOOLTIP = "menu_bar_tooltips_network_hosts_overlay"

    def __init__(self, context: Context):
        super().__init__(context)
        HostOverlay(self, context)
