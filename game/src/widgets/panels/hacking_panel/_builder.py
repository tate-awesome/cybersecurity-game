from customtkinter import CTkFrame
from ....app_core.context import Context

from .forms.arp import ArpForm
from .forms.nmap import NmapForm
from .forms.dos import DosForm
from .forms.sniff import SniffForm
from .forms.mitm import MitmForm
from .forms.mitm2 import Mitm2Form

from .form_overlay import FormOverlay

from ....widgets import Scrollable, MenuBar, Overlay

class Builder(CTkFrame):

    def __init__(self, master: CTkFrame, context: Context):
        self.style = context.style
        self.context = context

        super().__init__(master, fg_color=self.style.color("panel"))
        self.pack(**self.style.packing("panel"))

        menu_bar = MenuBar(self, context, "Attacks")
        scrollable = Scrollable(self, context)

        self.forms = {}
        
        self.forms["nmap"] = NmapForm(scrollable, context)
        self.forms["arp"] = ArpForm(scrollable, context)
        self.forms["dos"] = DosForm(scrollable, context)
        self.forms["sniff"] = SniffForm(scrollable, context)
        self.forms["mitm"] = MitmForm(scrollable, context)
        self.forms["mitm2"] = Mitm2Form(scrollable, context)

        for i, form in enumerate(self.forms.values()):
            form.grid(row=i, column=0, pady=self.style.gap, padx=self.style.gap, sticky="ew")
        self.refresh_forms()
        scrollable.columnconfigure(0, weight=1)
        scrollable.add_deadspace("grid")

        forms_button = menu_bar.add_button("Forms")
        overlay = FormOverlay(forms_button, context, self.refresh_forms)


    def refresh_forms(self):
        self.update_idletasks()
        for key in self.context.states["hacking_forms"]:
            if self.context.states["hacking_forms"][key] == "1" or self.context.states["hacking_forms"][key] == 1:
                self.show_form(key)
            else:
                self.hide_form(key)

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