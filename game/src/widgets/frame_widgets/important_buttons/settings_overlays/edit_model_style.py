from ...overlay import Overlay
from .settings_overlay_button import SettingsOverlayButton


class EditModelStyle(SettingsOverlayButton):
    '''
    Opens an editor for how the model panel draws: which parts are drawn
    (model_sprites) and their colors (model_colors). Canvases read these
    every frame. Which model is shown is SelectModelView's.
    '''
    LABEL = "menu_bar_buttons_model_style_button"
    TOOLTIP = "menu_bar_tooltips_model_style_button"

    def populate(self, overlay: Overlay):
        states = self.context.states

        sprites = self.section("model_sprites")
        for key in states.get("model_sprites"):
            sprites.checkbox("model_sprites", key)

        colors = self.section("model_colors")
        for key in states.get("model_colors"):
            colors.color("model_colors", key)
