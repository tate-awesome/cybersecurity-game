from customtkinter import CTkFrame
from ....app_core import Context
from ..panel import Panel

from .forms.arp import ArpForm
from .forms.nmap import NmapForm
from .forms.dos import DosForm
from .forms.sniff import SniffForm
from .forms.nfq import NFQForm
from .form_overlay import FormOverlay
from .forms.wifi import WifiForm

from ....widgets import Scrollable, MenuBar, Overlay

class Builder(Panel):

    def __init__(self, master: CTkFrame, context: Context):

        super().__init__(master, context, "Attacks")

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


        forms_button = self.menu_bar.add_button("Forms")
        overlay = FormOverlay(forms_button, context, self.refresh_forms)

        stop_button = self.menu_bar.add_button("Stop All", self.stop_all)
        minimize_button = self.menu_bar.minimize_button(self.scrollable, master)


    def refresh_forms(self):
        self.update_idletasks()
        for key in self.context.states["hacking_forms"]:
            if self.context.states["hacking_forms"][key] == "1" or self.context.states["hacking_forms"][key] == 1:
                self.show_form(key)
            else:
                self.hide_form(key)
        self.scrollable.top()

    def hide_form(self, name: str):
        form = self.forms[name]
        if not form.winfo_ismapped():
            return
        form.grid_remove()  

    def show_form(self, name: str):
        form = self.forms[name]
        if form.winfo_ismapped():
            return
        form.grid()

    def stop_all(self):
        for form in self.forms.values():
            form.click_stop()