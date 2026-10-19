from ...visuals import background_choices
from ..overlay import Overlay
from .settings_overlays.settings_overlay_button import SettingsOverlayButton


class SelectBackground(SettingsOverlayButton):
    '''
    Opens the background selector, like the theme selector (see
    SelectColorTheme): No Background, then each visual the pickers offer
    (see visuals.background_choices) - picking one plays it behind every page.
    '''
    LABEL = "menu_bar_buttons_select_background_button"
    TOOLTIP = "menu_bar_tooltips_select_background_button"

    def populate(self, overlay: Overlay):
        style, labels = self.context.style, self.context.labels
        backgrounds = self.section("backgrounds")
        for key, name in background_choices(self.context).items():
            button = backgrounds.button(name, lambda key=key: self.apply(overlay, key),
                                        labels.get(f"visual_descriptions_{key}"))
            button.setCheckable(True)
            button.setChecked(key == style.background_visual)

    def apply(self, overlay: Overlay, key: str):
        overlay.close_chain()
        self.context.style.set_background(visual=key)
