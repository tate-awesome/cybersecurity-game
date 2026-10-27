from .._base_button import ImportantButton
from .filter_overlay import FilterModal


class FilterPacketConsole(ImportantButton):
    '''
    Opens the packet filter editor (packet_console "filter" - see
    FilterModal) - the packet console follows the setting.
    '''
    LABEL = "menu_bar_buttons_filters_overlay"
    OPENS = "modal"

    def on_click(self):
        FilterModal(self.context)
