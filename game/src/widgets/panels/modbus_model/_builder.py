from PySide6.QtWidgets import QVBoxLayout, QWidget

from ....app_core import Context
from ...canvases.house import House
from ...canvases.world_map import WorldMap
from ...canvases.defender_world_map import DefenderWorldMap
from ...canvases.defender_hvac_chart import DefenderHVACChart
from ..panel import Panel

MODELS = {
    # Order matters as a fallback: a panel whose "start_on" isn't one of
    # its available models (e.g. the "" default) starts on whichever of
    # these comes first.
    "sniffed_submarine_map": WorldMap,
    "sniffed_hvac_house": House,
    "ap_polled_submarine_map": DefenderWorldMap,
    "ap_polled_hvac_chart": DefenderHVACChart,
}

# Models read from the AP ("ap_polled_*") can be driven by the AP's own reported mode
# (context.buffer.defender_status.submarine_mode) instead of a manual
# dropdown pick - see _auto_switch. That flips between both of them, so it's
# only offered on a panel where both are available.
DEFENDER_MODELS = {"ap_polled_submarine_map", "ap_polled_hvac_chart"}


def is_on(value) -> bool:
    return value in (1, "1", True)


class Builder(Panel):
    '''
    The ModBus models, one at a time, set up per copy of this panel by its
    "model_panels" entry (keyed by its layout id, e.g. "modbus_model_panel_2"):
    which models it offers ("available"), which it starts on ("start_on"),
    and its Auto-Switch checkbox. More than one model gets a dropdown that
    swaps which canvas is shown; exactly one is just that model, titled
    after it. Picks and the checkbox are written back to the entry, so
    autosave remembers them for that copy alone.

    Only one model is ever built at a time - switching destroys the outgoing
    canvas (after stopping its animation loop, since a live canvas
    calling into a destroyed widget every frame would raise forever) and
    builds the new one in its place.
    '''

    KEY = "modbus_model_panel"
    # How many copies a layout can hold - one per "model_panels" entry in
    # _packages/_default.json (the layout editor and schema hold to it too)
    MAX_COPIES = 5

    # The settings keys (see _packages/_default.json) this panel reads or writes -
    # the workspace editor lists it under each of them
    # Its hvac/submarine models draw with the house and submarine map canvases
    SETTINGS = (
        "model_panels",
        "model_sprites",
        "model_colors",
    )

    def __init__(self, master, context: Context, panel_id: str | None = None):
        settings = context.states.get("model_panels").get(panel_id)
        if not isinstance(settings, dict):
            super().__init__(master, context, f"err: no model_panels entry for {panel_id}")
            return
        models = [key for key in MODELS if is_on(settings["available"].get(key))]
        # A panel with one model is titled after it, e.g. "Polled HVAC Chart"
        super().__init__(master, context, f"{models[0]}_panel" if len(models) == 1 else self.KEY)
        self.panel_id = panel_id

        self.body = QWidget()
        self.body.setLayout(QVBoxLayout())
        self.body.layout().setContentsMargins(0, 0, 0, 0)
        # Stretch 1: see Scrollable.__init__ for why (same Panel-body/
        # trailing-filler interaction).
        self.layout().addWidget(self.body, 1)

        self.model = None
        self.model_key = None
        self.model_dropdown = None
        self.auto_switch_checkbox = None
        self.labels_by_key = {key: self.context.labels.get(f"modbus_model_options_{key}") for key in models}
        self.key_by_label = {label: key for key, label in self.labels_by_key.items()}
        if not models:
            print(f"{panel_id} has no models available")
            self.menu_bar.minimize_button(self.body, master)
            return

        start_key = settings["start_on"] if settings["start_on"] in models else models[0]
        if len(models) > 1:
            self.model_dropdown = self.menu_bar.add_dropdown(
                list(self.labels_by_key.values()),
                command=self.select_model_by_label,
                default=self.labels_by_key[start_key],
            )
        # Not saved: start_on only changes once a model is actually picked
        self.select_model(start_key, save=False)

        # Auto-switching follows the AP's current mode on every tick,
        # overriding a manual pick (and updating the dropdown to match - see
        # select_model's _sync_dropdown call), as long as the Auto-Switch
        # checkbox stays checked. It never runs without the checkbox, so
        # there's always a way to turn it off. Unchecking it (or picking a
        # model from the dropdown, see select_model_by_label) removes
        # _auto_switch from the animation manager entirely rather than
        # having it check a flag every tick and no-op.
        self._auto_switch_callback_name = f"ModbusModelAutoSwitch_{id(self)}"
        if DEFENDER_MODELS <= set(models) and is_on(settings["show_auto_switch_checkbox"]):
            auto_switch_enabled = is_on(settings["auto_switch_on_poll"])
            self.auto_switch_checkbox = self.menu_bar.add_checkbox(
                self.context.labels.get("menu_bar_buttons_auto_switch"),
                checked=auto_switch_enabled,
                command=self._set_auto_switch,
            )
            if auto_switch_enabled:
                self.context.animation_manager.add_callback(self._auto_switch_callback_name, self._auto_switch)

        self.menu_bar.minimize_button(self.body, master)

    def _set_auto_switch(self, enabled: bool):
        self.context.states.set("model_panels", self.panel_id, "auto_switch_on_poll", value=1 if enabled else 0)
        if enabled:
            self.context.animation_manager.add_callback(self._auto_switch_callback_name, self._auto_switch)
            self._auto_switch()
        else:
            self.context.animation_manager.remove_callback(self._auto_switch_callback_name)

    def _auto_switch(self):
        submarine_mode = bool(self.context.buffer.defender_status.get("submarine_mode", True))
        key = "ap_polled_submarine_map" if submarine_mode else "ap_polled_hvac_chart"
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

    def select_model(self, key: str, save: bool = True):
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
        if save:
            self.context.states.set("model_panels", self.panel_id, "start_on", value=key)
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
