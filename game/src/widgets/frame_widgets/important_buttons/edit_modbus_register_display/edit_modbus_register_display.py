from .._base_button import ImportantButton
from .variable_overlay import VariablePopup


class EditModbusRegisterDisplay(ImportantButton):
    '''
    Opens the register editor: which registers are shown, their nicknames,
    factors, units, and whether they're modified (modbus_registers) - the
    ModBus forms follow the setting.
    '''
    LABEL = "menu_bar_buttons_variables_overlay"
    TOOLTIP = "menu_bar_tooltips_variables_overlay"
    OPENS = "popup"

    def on_click(self):
        VariablePopup(self.context)
