from .....app_core import Context
from .._base_button import ImportantButton
from .checkbox_overlay import CheckboxOverlay


class ChooseShownModbusTableForms(ImportantButton):
    '''Opens checkboxes choosing which ModBus table panel forms are shown (modbus_table_forms_shown) - the panel follows the setting.'''
    LABEL = "menu_bar_buttons_forms_overlay"

    def __init__(self, context: Context):
        super().__init__(context)
        CheckboxOverlay(self, context, "modbus_table_forms_shown", "Show Forms", "available", label_group="modbus_forms")
