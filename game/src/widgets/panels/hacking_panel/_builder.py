from customtkinter import CTkFrame
from ....app_core import Context
from ..panel import Panel

from .forms.arp import ArpForm
from .forms.nmap import NmapForm
from .forms.dos import DosForm
from .forms.sniff import SniffForm
from .forms.nfq import NFQForm
from .forms.wifi import WifiForm

from ....widgets import Scrollable, MenuBar, Overlay, CheckboxOverlay

class Builder(Panel):
    KEY = "network_action_panel"
    def __init__(self, master: CTkFrame, context: Context):

        super().__init__(master, context, self.KEY)

        self.scrollable = Scrollable(self, context)

        self.forms = {}

        self.forms["wifi"] = WifiForm(self.scrollable, context)
        self.forms["nmap"] = NmapForm(self.scrollable, context)
        self.forms["arp"] = ArpForm(self.scrollable, context)
        self.forms["dos"] = DosForm(self.scrollable, context)
        self.forms["sniff"] = SniffForm(self.scrollable, context)
        self.forms["nfq"] = NFQForm(self.scrollable, context)

        for i, form in enumerate(self.forms.values()):
            form.grid(row=i, column=0, pady=self.style.gap, padx=self.style.gap, sticky="ew")
        self.refresh_forms()
        self.scrollable.columnconfigure(0, weight=1)
        self.scrollable.add_deadspace("grid")


        forms_button = self.menu_bar.add_button("forms_overlay")
        overlay = CheckboxOverlay(forms_button, context, self.refresh_forms, "hacking_forms", "Show Forms")

        stop_button = self.menu_bar.add_button("abort_all", self.stop_all)
        minimize_button = self.menu_bar.minimize_button(self.scrollable, master)


    def refresh_forms(self):
        self.update_idletasks()
        for key in self.context.states.get("hacking_forms"):
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