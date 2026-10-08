from .....app_core import Context
from .._base_button import PanelButton
from .checkbox_overlay import CheckboxOverlay


class ChooseShownPacketConsoleColumns(PanelButton):
    '''Opens checkboxes choosing which packet console columns are shown (packet_columns) - the panel follows the setting.'''
    PANEL = "packet_panel"
    LABEL = "menu_bar_buttons_columns_overlay"
    TOOLTIP = "menu_bar_tooltips_columns_overlay"

    def __init__(self, context: Context):
        super().__init__(context)
        CheckboxOverlay(self, context, "packet_columns", "Show Columns")
