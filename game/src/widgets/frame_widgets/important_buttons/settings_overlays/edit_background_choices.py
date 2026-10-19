from .....app_core.context.style import NO_BACKGROUND
from ....visuals import VISUALS
from ...overlay import Overlay
from .settings_overlay_button import SettingsOverlayButton


class EditBackgroundChoices(SettingsOverlayButton):
    '''
    Opens a checkbox per visual (and Cycle All) - which ones the background
    pickers offer (see visuals.background_choices). "Cycle All" takes turns
    with only the ones left on. Hiding the background playing now switches
    to No Background, so it's never playing something its picker can't show.
    '''
    LABEL = "menu_bar_buttons_background_choices_button"
    TOOLTIP = "menu_bar_tooltips_background_choices_button"

    def populate(self, overlay: Overlay):
        labels = self.context.labels
        choices = self.section("background_choices")
        for key in [*VISUALS, "cycle"]:
            choices.toggle(("background_choices",), key not in self.context.style.background_hidden,
                           lambda on, key=key: self.set_offered(key, on),
                           text=labels.get(f"visual_names_{key}"), tooltip=labels.get(f"visual_descriptions_{key}"))

    def set_offered(self, key: str, on: bool):
        style = self.context.style
        hidden = [other for other in style.background_hidden if other != key] + ([] if on else [key])
        visual = NO_BACKGROUND if not on and style.background_visual == key else None
        style.set_background(hidden=hidden, visual=visual)
