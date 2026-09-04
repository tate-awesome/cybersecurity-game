from customtkinter import CTkFrame

from ....app_core import Context
from ...canvases.house import House
from ...canvases.world_map import WorldMap
from ...canvases.defender_world_map import DefenderWorldMap
from ...canvases.defender_hvac_chart import DefenderHVACChart
from ..panel import Panel

MODELS = {
    # Order matters as a fallback: a page whose "model_type" isn't
    # "hvac"/"submarine" (e.g. the "agnostic" default) starts on
    # whichever of these comes first.
    "submarine": WorldMap,
    "hvac": House,
    "defender_submarine": DefenderWorldMap,
    "defender_hvac": DefenderHVACChart,
}

# Defender-flavored models are driven by the AP's own reported mode
# (context.buffer.defender_status.submarine_mode) instead of a manual
# dropdown pick - see _auto_switch. Only a page whose modbus_model_visibility
# actually enables one of these (DefenderVPanels) ever exercises this.
DEFENDER_MODELS = {"defender_submarine", "defender_hvac"}

class Builder(Panel):
    '''
    Combines the old separate hvac_panel/submarine_panel into one panel
    with a dropdown that swaps which model canvas is shown. Only one
    model is ever built at a time - switching destroys the outgoing
    canvas (after stopping its animation loop, since a live canvas
    calling into a destroyed widget every frame would raise forever) and
    builds the new one in its place.
    '''

    KEY = "modbus_model_panel"

    def __init__(self, master, context: Context):
        super().__init__(master, context, self.KEY)

        available_models: dict[str, int] = self.context.states.get("modbus_model_visibility")
        if available_models is None:
            available_models = list(MODELS.keys())

        self.labels_by_key: dict[str, str] = {}
        for key in MODELS:
            if key not in available_models or available_models[key] in (0, "0"):
                print(f"Model is invisible: {key!r}")
                continue
            self.labels_by_key[key] = self.context.labels.get("modbus_model_options", key)
        self.key_by_label = {label: key for key, label in self.labels_by_key.items()}

        self.body = CTkFrame(self, fg_color="transparent")
        self.body.pack(side="top", fill="both", expand=True)

        self.model = None
        self.model_key = None

        if self.labels_by_key:
            preferred = self.context.states.get("model_type")
            start_key = preferred if preferred in self.labels_by_key else next(iter(self.labels_by_key))

            self.menu_bar.add_dropdown(
                list(self.labels_by_key.values()),
                command=self.select_model_by_label,
                default=self.labels_by_key[start_key],
            )
            self.select_model(start_key)
        else:
            print("No models are visible for this page")

        self.menu_bar.minimize_button(self.body, master)

        # If a defender-flavored model is visible, it takes over model
        # selection entirely from here on - the dropdown stays (so both
        # remain individually inspectable) but whichever one matches the
        # AP's current mode wins on every tick, overriding a manual pick.
        if DEFENDER_MODELS & set(self.labels_by_key):
            self.context.animation_manager.add_callback(f"ModbusModelAutoSwitch_{id(self)}", self._auto_switch)

    def _auto_switch(self):
        submarine_mode = bool(self.context.buffer.defender_status.get("submarine_mode", True))
        key = "defender_submarine" if submarine_mode else "defender_hvac"
        if key in self.labels_by_key:
            self.select_model(key)

    def select_model_by_label(self, label: str):
        key = self.key_by_label.get(label)
        if key is not None:
            self.select_model(key)

    def select_model(self, key: str):
        if key == self.model_key or key not in MODELS:
            return

        if self.model is not None:
            self.model.stop_animation()
            self.model.destroy()

        self.model = MODELS[key](self.body, self.context)
        self.model_key = key
        self.context.states.set("model_type", value=key)
