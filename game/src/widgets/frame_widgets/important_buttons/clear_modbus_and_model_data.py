from ._base_button import ImportantButton


class ClearModbusAndModelData(ImportantButton):
    '''Clears the sniffed modbus readings and the submarine/HVAC models built from them.'''
    LABEL = "menu_bar_buttons_clear_modbus"
    TOOLTIP = "menu_bar_tooltips_clear_modbus"

    def on_click(self):
        self.context.buffer.reset_modbus()
