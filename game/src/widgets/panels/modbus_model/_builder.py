from customtkinter import CTkFrame

from ....app_core import Context
from ...canvases.house import House
from ...canvases.world_map import WorldMap
from ..panel import Panel

MODELS = {
    # Order matters as a fallback: a page whose "model_type" isn't
    # "hvac"/"submarine" (e.g. the "agnostic" default) starts on
    # whichever of these comes first.
    "submarine": WorldMap,
    "hvac": House,
}

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
