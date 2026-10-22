from .....app_core import Context
from .._base_button import PanelButton
from .columns_overlay import PacketColumnsOverlay


class ChooseShownPacketConsoleColumns(PanelButton):
    '''Opens the columns overlay: which packet console columns are shown, in what order (packet_columns) - the panel follows the setting.'''
    PANEL = "packet_panel"
    LABEL = "menu_bar_buttons_columns_overlay"
    TOOLTIP = "menu_bar_tooltips_columns_overlay"

    def __init__(self, context: Context):
        super().__init__(context)
        PacketColumnsOverlay(self, context)
