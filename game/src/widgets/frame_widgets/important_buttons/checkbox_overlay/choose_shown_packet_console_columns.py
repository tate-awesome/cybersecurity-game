from .....app_core import Context
from .._base_button import ImportantButton
from .checkbox_overlay import CheckboxOverlay


class ChooseShownPacketConsoleColumns(ImportantButton):
    '''Opens checkboxes choosing which packet console columns are shown (packet_columns) - the panel follows the setting.'''
    LABEL = "menu_bar_buttons_columns_overlay"
    TOOLTIP = "menu_bar_tooltips_columns_overlay"

    def __init__(self, context: Context):
        super().__init__(context)
        CheckboxOverlay(self, context, "packet_columns", "Show Columns")
