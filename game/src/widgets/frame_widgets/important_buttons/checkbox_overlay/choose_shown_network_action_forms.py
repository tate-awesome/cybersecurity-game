from .....app_core import Context
from .._base_button import ImportantButton
from .checkbox_overlay import CheckboxOverlay


class ChooseShownNetworkActionForms(ImportantButton):
    '''Opens checkboxes choosing which network action forms are shown (network_action_forms_shown) - the panel follows the setting.'''
    LABEL = "menu_bar_buttons_forms_overlay"

    def __init__(self, context: Context):
        super().__init__(context)
        CheckboxOverlay(self, context, "network_action_forms_shown", "Show Forms", "available", label_group="hacking_forms")
