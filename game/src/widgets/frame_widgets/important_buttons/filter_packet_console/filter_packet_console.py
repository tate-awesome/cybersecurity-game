from .._base_button import ImportantButton
from .filter_overlay import FilterPopup


class FilterPacketConsole(ImportantButton):
    '''
    Opens the packet filter editor (packet_console "filter" - see
    FilterPopup) - the packet console follows the setting.
    '''
    LABEL = "menu_bar_buttons_filters_overlay"
    OPENS = "popup"

    def on_click(self):
        FilterPopup(self.context)
