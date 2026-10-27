from .._base_button import PanelButton
from .columns_overlay import PacketColumnsPopup


class ChooseShownPacketConsoleColumns(PanelButton):
    '''Opens the columns popup: which packet console columns are shown, in what order (packet_columns) - the panel follows the setting.'''
    PANEL = "packet_panel"
    LABEL = "menu_bar_buttons_columns_overlay"
    TOOLTIP = "menu_bar_tooltips_columns_overlay"
    OPENS = "popup"

    def on_click(self):
        PacketColumnsPopup(self.context)
