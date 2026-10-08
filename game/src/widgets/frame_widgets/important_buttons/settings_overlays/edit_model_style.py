from ...overlay import Overlay
from .settings_overlay_button import SettingsOverlayButton


class EditModelStyle(SettingsOverlayButton):
    '''
    Opens an editor for how the model panel draws: which parts are drawn
    (model_sprites), their colors (model_colors), and which model is shown
    (modbus_model_selected, modbus_model_auto_switch). Canvases read these
    every frame, and the model panel follows its two settings.
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

        model = self.section("model_panel")
        dropdown = model.dropdown(("modbus_model_selected",), self.context.labels.group("modbus_model_options"))
        auto_switch = model.checkbox("modbus_model_auto_switch")
        # A manual pick overrides auto-switching, same as the model panel's own dropdown
        dropdown.currentIndexChanged.connect(lambda index: auto_switch.setChecked(False))
