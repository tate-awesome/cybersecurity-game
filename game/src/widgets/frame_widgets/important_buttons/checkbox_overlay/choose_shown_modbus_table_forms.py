from .....app_core import Context
from .._base_button import PanelButton
from .checkbox_overlay import CheckboxOverlay


class ChooseShownModbusTableForms(PanelButton):
    '''Opens checkboxes choosing which ModBus table panel forms are shown (modbus_table_forms_shown) - the panel follows the setting.'''
    PANEL = "modbus_table_panel"
    LABEL = "menu_bar_buttons_modbus_forms_button"
    TOOLTIP = "menu_bar_tooltips_modbus_forms_button"

    def __init__(self, context: Context):
        super().__init__(context)
        CheckboxOverlay(self, context, "modbus_table_forms_shown", "Show Forms", "available", label_group="modbus_forms")
