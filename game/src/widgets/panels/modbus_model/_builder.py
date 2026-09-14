from PySide6.QtWidgets import QVBoxLayout, QWidget

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
# actually enables one of these (the defender lessons) ever exercises this.
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

        self.body = QWidget()
        self.body.setLayout(QVBoxLayout())
        self.body.layout().setContentsMargins(0, 0, 0, 0)
        # Stretch 1: see Scrollable.__init__ for why (same Panel-body/
        # trailing-filler interaction).
        self.layout().addWidget(self.body, 1)

        self.model = None
        self.model_key = None
        self.model_dropdown = None

        if self.labels_by_key:
            preferred = self.context.states.get("model_type")
            start_key = preferred if preferred in self.labels_by_key else next(iter(self.labels_by_key))

            self.model_dropdown = self.menu_bar.add_dropdown(
                list(self.labels_by_key.values()),
                command=self.select_model_by_label,
                default=self.labels_by_key[start_key],
            )
            self.select_model(start_key)
        else:
            print("No models are visible for this page")


        # If a defender-flavored model is visible, it takes over model
        # selection entirely from here on - whichever one matches the AP's
        # current mode wins on every tick, overriding a manual pick (and
        # updating the dropdown to match - see select_model's _sync_dropdown
        # call), as long as the Auto-Switch checkbox stays checked.
        # Unchecking it (or picking a model from the dropdown, see
        # select_model_by_label) removes _auto_switch from the animation
        # manager entirely rather than having it check a flag every tick
        # and no-op.
        self.auto_switch_checkbox = None
        self._auto_switch_callback_name = f"ModbusModelAutoSwitch_{id(self)}"
        # available_models is a dict keyed by "auto_switch" too (see
        # visibility/_default.json's modbus_model_visibility) unless it fell
        # back to the plain list of every MODELS key above, in which case
        # nothing has hidden the checkbox and it defaults to visible.
        auto_switch_visible = (
            not isinstance(available_models, dict)
            or available_models.get("auto_switch") not in (0, "0")
        )
        if auto_switch_visible and DEFENDER_MODELS & set(self.labels_by_key):
            auto_switch_enabled = bool(self.context.states.get("modbus_model_auto_switch"))
            self.auto_switch_checkbox = self.menu_bar.add_checkbox(
                self.context.labels.get("menu_bar_buttons", "auto_switch"),
                checked=auto_switch_enabled,
                command=self._set_auto_switch,
            )
            if auto_switch_enabled:
                self.context.animation_manager.add_callback(self._auto_switch_callback_name, self._auto_switch)

        self.menu_bar.minimize_button(self.body, master)

    def _set_auto_switch(self, enabled: bool):
        self.context.states.set("modbus_model_auto_switch", value=1 if enabled else 0)
        if enabled:
            self.context.animation_manager.add_callback(self._auto_switch_callback_name, self._auto_switch)
            self._auto_switch()
        else:
            self.context.animation_manager.remove_callback(self._auto_switch_callback_name)

    def _auto_switch(self):
        submarine_mode = bool(self.context.buffer.defender_status.get("submarine_mode", True))
        key = "defender_submarine" if submarine_mode else "defender_hvac"
        if key in self.labels_by_key:
            self.select_model(key)

    def select_model_by_label(self, label: str):
        key = self.key_by_label.get(label)
        if key is None:
            return
        # A manual dropdown pick overrides auto-switching - uncheck the box
        # (which itself drops the animation-manager callback via
        # _set_auto_switch) so the very next tick doesn't immediately
        # switch back out from under the user's pick.
        if self.auto_switch_checkbox is not None:
            self.auto_switch_checkbox.setChecked(False)
        self.select_model(key)

    def select_model(self, key: str):
        if key == self.model_key or key not in MODELS:
            return

        if self.model is not None:
            self.model.stop_animation()
            # deleteLater() alone only schedules the actual deletion for the
            # next event loop iteration - it doesn't detach the widget from
            # the layout immediately, so removeWidget() first ensures the
            # outgoing and incoming model can't ever both be in there together.
            self.body.layout().removeWidget(self.model)
            self.model.deleteLater()

        self.model = MODELS[key](self.body, self.context)
        self.model_key = key
        self.context.states.set("model_type", value=key)
        self._sync_dropdown(key)

    def _sync_dropdown(self, key: str):
        '''
        Keeps the dropdown's displayed text matching whichever model is
        actually showing, including when _auto_switch changes it out from
        under a manual pick - not just at construction. Signals are
        blocked around the change so this can't loop back into
        select_model_by_label as though the user had picked it themselves
        (which would also uncheck the Auto-Switch checkbox).
        '''
        if self.model_dropdown is None:
            return
        label = self.labels_by_key.get(key)
        if label is None:
            return
        index = self.model_dropdown.findText(label)
        if index < 0 or self.model_dropdown.currentIndex() == index:
            return
        self.model_dropdown.blockSignals(True)
        self.model_dropdown.setCurrentIndex(index)
        self.model_dropdown.blockSignals(False)
