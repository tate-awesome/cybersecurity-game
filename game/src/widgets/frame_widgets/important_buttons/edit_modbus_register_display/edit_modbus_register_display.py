from .....app_core import Context
from .._base_button import ImportantButton
from .variable_overlay import VariableOverlay


class EditModbusRegisterDisplay(ImportantButton):
    '''
    Opens the register editor: which registers are shown, their nicknames,
    factors, units, and whether they're modified (modbus_registers) - the
    ModBus forms follow the setting.
    '''
    LABEL = "menu_bar_buttons_variables_overlay"
    TOOLTIP = "menu_bar_tooltips_variables_overlay"

    def __init__(self, context: Context):
        super().__init__(context)
        VariableOverlay(self, context)
