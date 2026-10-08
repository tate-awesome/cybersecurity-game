from .....app_core import Context
from .._base_button import PanelButton
from .checkbox_overlay import CheckboxOverlay


class ChooseShownDefenderModbusForms(PanelButton):
    '''Opens checkboxes choosing which defender ModBus panel forms are shown (defender_modbus_forms_shown) - the panel follows the setting.'''
    PANEL = "defender_modbus_panel"
    LABEL = "menu_bar_buttons_defender_forms_button"
    TOOLTIP = "menu_bar_tooltips_defender_forms_button"

    def __init__(self, context: Context):
        super().__init__(context)
        CheckboxOverlay(self, context, "defender_modbus_forms_shown", "Show Forms", "available", label_group="defender_modbus_forms")
