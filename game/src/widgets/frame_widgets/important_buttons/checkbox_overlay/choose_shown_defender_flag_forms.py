from .....app_core import Context
from .._base_button import PanelButton
from .checkbox_overlay import CheckboxOverlay


class ChooseShownDefenderFlagForms(PanelButton):
    '''Opens checkboxes choosing which defender flag panel forms are shown (defender_flag_forms_shown) - the panel follows the setting.'''
    PANEL = "defender_flag_panel"
    LABEL = "menu_bar_buttons_defender_flag_forms_button"
    TOOLTIP = "menu_bar_tooltips_defender_flag_forms_button"

    def __init__(self, context: Context):
        super().__init__(context)
        CheckboxOverlay(self, context, "defender_flag_forms_shown", context.labels.get("form_overlay_title_forms"), "available", label_group="defender_flag_forms", reorderable=True)
