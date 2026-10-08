from .....app_core import Context
from .._base_button import PanelButton
from .checkbox_overlay import CheckboxOverlay


class ChooseShownNetworkActionForms(PanelButton):
    '''Opens checkboxes choosing which network action forms are shown (network_action_forms_shown) - the panel follows the setting.'''
    PANEL = "network_action_panel"
    LABEL = "menu_bar_buttons_network_forms_button"
    TOOLTIP = "menu_bar_tooltips_network_forms_button"

    def __init__(self, context: Context):
        super().__init__(context)
        CheckboxOverlay(self, context, "network_action_forms_shown", "Show Forms", "available", label_group="hacking_forms")
