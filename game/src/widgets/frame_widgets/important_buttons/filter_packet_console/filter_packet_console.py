from .....app_core import Context
from .._base_button import ImportantButton
from .filter_overlay import FilterOverlay


class FilterPacketConsole(ImportantButton):
    '''
    Opens the packet filter editor (packet_filter_checkboxes/entries) - the
    packet console follows the setting.
    '''
    LABEL = "menu_bar_buttons_filters_overlay"

    def __init__(self, context: Context):
        super().__init__(context)
        FilterOverlay(self, context)
