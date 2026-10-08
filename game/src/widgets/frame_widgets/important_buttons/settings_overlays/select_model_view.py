from ...overlay import Overlay
from .settings_overlay_button import SettingsOverlayButton


class SelectModelView(SettingsOverlayButton):
    '''
    Opens a picker for which model the model panel shows (one button per
    model this workspace offers - see "available") and the Auto-Switch
    checkbox. Writes modbus_model_selected/modbus_model_auto_switch, which
    every flexible model panel follows (one fixed by "model_panels" ignores them).
    '''
    LABEL = "menu_bar_buttons_model_view_button"
    TOOLTIP = "menu_bar_tooltips_model_view_button"
    CURRENT_MARKER = "●"

    def populate(self, overlay: Overlay):
        states = self.context.states
        available = states.get("available")
        selected = states.get("modbus_model_selected")

        models = self.section("model_panel")
        for key, text in self.context.labels.group("modbus_model_options").items():
            if isinstance(available, dict) and available.get(key) in (0, "0", None):
                continue
            if key == selected:
                text = f"{self.CURRENT_MARKER} {text}"
            models.button(text, lambda key=key: self.select(overlay, key))
        models.checkbox("modbus_model_auto_switch")

    def select(self, overlay: Overlay, key: str):
        # A manual pick overrides auto-switching, same as the model panel's own dropdown
        self.context.states.set("modbus_model_auto_switch", value=0)
        self.context.states.set("modbus_model_selected", value=key)
        overlay.close_chain()
