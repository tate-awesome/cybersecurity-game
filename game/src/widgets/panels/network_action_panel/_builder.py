from PySide6.QtWidgets import QWidget
from ....app_core import Context
from ..panel import Panel

from .forms.arp import ArpForm
from .forms.nmap import NmapForm
from .forms.dos import DosForm
from .forms.sniff import SniffForm
from .forms.nfq import NFQForm
from .forms.wifi import WifiForm
from .forms.ap_connect import APConnectForm
from .forms.encryption import EncryptionForm
from .forms.ap_tunnel import APTunnelForm
from .forms.kalman import KalmanForm

from ....widgets import Scrollable
from ...frame_widgets.important_buttons import AbortAllNetworkActions, ChooseShownNetworkActionForms

FORM_CLASSES = {
    "wifi": WifiForm,
    "nmap": NmapForm,
    "arp": ArpForm,
    "dos": DosForm,
    "sniff": SniffForm,
    "nfq": NFQForm,
    # Defender-only forms - invisible everywhere except a page whose
    # "available" settings group explicitly offers them (the defender
    # lessons - see assets/pages/workspaces/defender_*).
    # ap_connect is listed first since encryption/ap_tunnel/kalman look up
    # its process by name rather than creating their own if it's missing.
    "ap_connect": APConnectForm,
    "encryption": EncryptionForm,
    "ap_tunnel": APTunnelForm,
    "kalman": KalmanForm,
}

class Builder(Panel):
    KEY = "network_action_panel"
    # The settings keys (see _packages/_default.json) this panel reads or writes -
    # the workspace editor lists it under each of them
    # Its NFQ form runs the packet interceptor, which rewrites registers - hence modbus_registers and modbus_packet_modify_enabled
    SETTINGS = (
        "available",
        "network_action_forms_shown",
        "network_action_form_inputs",
        "game_progress",
        "modbus_registers",
        "modbus_packet_modify_enabled",
    )
    def __init__(self, master: QWidget, context: Context, available_forms: list[str] | None = None):

        super().__init__(master, context, self.KEY)

        self.scrollable = Scrollable(self, context)

        available_forms: dict[str, int] = self.context.states.get("available")
        if available_forms is None:
            available_forms = list(FORM_CLASSES.keys())


        self.forms = {}
        for key in FORM_CLASSES:
            if key not in available_forms or available_forms[key] == 0 or available_forms[key] == "0":
                print(f"Form is invisible: {key!r}")
                continue
            self.forms[key] = FORM_CLASSES[key](self.scrollable, context)

        for i, form in enumerate(self.forms.values()):
            self.scrollable.grid_layout.addWidget(form, i, 0)
        self.shown_forms = None  # network_action_forms_shown as of the last refresh_forms
        self.refresh_forms()
        self.scrollable.columnconfigure(0, weight=1)
        self.scrollable.add_deadspace("grid")
        self.context.animation_manager.add_callback(f"network_action_forms_{id(self)}", self.refresh_forms)

        self.menu_bar.add_important(ChooseShownNetworkActionForms)
        self.menu_bar.add_important(AbortAllNetworkActions)
        minimize_button = self.menu_bar.minimize_button(self.scrollable, master)


    def refresh_forms(self):
        '''
        Shows/hides forms to match network_action_forms_shown - polled every
        frame, so it only acts (and scrolls back to the top) when that changed.
        '''
        shown = dict(self.context.states.get("network_action_forms_shown"))
        if shown == self.shown_forms:
            return
        self.shown_forms = shown
        for key in shown:
            if key not in self.forms:
                # This lesson's available_forms doesn't include this form -
                # nothing to show/hide, and the "Show Forms" overlay still
                # lists every form regardless of what a given lesson offers.
                continue
            if self.context.states.get("network_action_forms_shown", key) == "1" or self.context.states.get("network_action_forms_shown", key) == 1:
                self.show_form(key)
            else:
                self.hide_form(key)
        self.scrollable.top()

    def hide_form(self, name: str):
        if name not in self.forms:
            raise KeyError(f"No hacking-panel form named {name!r} (check 'network_action_forms_shown' in settings)")
        form = self.forms[name]
        if form.isHidden():
            return
        form.hide()

    def show_form(self, name: str):
        if name not in self.forms:
            raise KeyError(f"No hacking-panel form named {name!r} (check 'network_action_forms_shown' in settings)")
        form = self.forms[name]
        if not form.isHidden():
            return
        form.show()
