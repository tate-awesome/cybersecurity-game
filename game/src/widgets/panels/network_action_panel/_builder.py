from customtkinter import CTkFrame
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

from ....widgets import Scrollable, MenuBar, Overlay, CheckboxOverlay

FORM_CLASSES = {
    "wifi": WifiForm,
    "nmap": NmapForm,
    "arp": ArpForm,
    "dos": DosForm,
    "sniff": SniffForm,
    "nfq": NFQForm,
    # Defender-only forms - invisible everywhere except a page whose
    # network_action_visibility explicitly enables them (DefenderVPanels).
    # ap_connect is listed first since encryption/ap_tunnel/kalman look up
    # its process by name rather than creating their own if it's missing.
    "ap_connect": APConnectForm,
    "encryption": EncryptionForm,
    "ap_tunnel": APTunnelForm,
    "kalman": KalmanForm,
}

class Builder(Panel):
    KEY = "network_action_panel"
    def __init__(self, master: CTkFrame, context: Context, available_forms: list[str] | None = None):

        super().__init__(master, context, self.KEY)

        self.scrollable = Scrollable(self, context)

        available_forms: dict[str, int] = self.context.states.get("network_action_visibility")
        if available_forms is None:
            available_forms = list(FORM_CLASSES.keys())


        self.forms = {}
        for key in FORM_CLASSES:
            if key not in available_forms or available_forms[key] == 0 or available_forms[key] == "0":
                print(f"Form is invisible: {key!r}")
                continue
            self.forms[key] = FORM_CLASSES[key](self.scrollable, context)

        for i, form in enumerate(self.forms.values()):
            form.grid(row=i, column=0, pady=self.style.gap, padx=self.style.gap, sticky="ew")
        self.refresh_forms()
        self.scrollable.columnconfigure(0, weight=1)
        self.scrollable.add_deadspace("grid")


        forms_button = self.menu_bar.add_button("forms_overlay")
        overlay = CheckboxOverlay(forms_button, context, self.refresh_forms, "hacking_forms", "Show Forms", "network_action_visibility")

        stop_button = self.menu_bar.add_button("abort_all", self.stop_all)
        minimize_button = self.menu_bar.minimize_button(self.scrollable, master)


    def refresh_forms(self):
        self.update_idletasks()
        for key in self.context.states.get("hacking_forms"):
            if key not in self.forms:
                # This lesson's available_forms doesn't include this form -
                # nothing to show/hide, and the "Show Forms" overlay still
                # lists every form regardless of what a given lesson offers.
                continue
            if self.context.states.get("hacking_forms", key) == "1" or self.context.states.get("hacking_forms", key) == 1:
                self.show_form(key)
            else:
                self.hide_form(key)
        self.scrollable.top()

    def hide_form(self, name: str):
        if name not in self.forms:
            raise KeyError(f"No hacking-panel form named {name!r} (check 'hacking_forms' in settings)")
        form = self.forms[name]
        if not form.winfo_ismapped():
            return
        form.grid_remove()

    def show_form(self, name: str):
        if name not in self.forms:
            raise KeyError(f"No hacking-panel form named {name!r} (check 'hacking_forms' in settings)")
        form = self.forms[name]
        if form.winfo_ismapped():
            return
        form.grid()

    def stop_all(self):
        for form in reversed(self.forms.values()):
            try:
                form.click_stop()
            except Exception as e:
                print(f"Error stopping {form}: {e}")