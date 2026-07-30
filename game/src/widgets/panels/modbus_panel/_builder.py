from customtkinter import CTkFrame
from ....app_core.context import Context
from ..panel import Panel

from .forms.mitm import MitmForm
from .forms.table import MitmTable
from .form_overlay import FormOverlay
from .variable_overlay import VariableOverlay

from ....widgets import Scrollable, MenuBar, Overlay

class Builder(Panel):

    def __init__(self, master: CTkFrame, context: Context):

        super().__init__(master, context, "Attacks")

        scrollable = Scrollable(self, context)

        self.forms = {}
        
        self.forms["mitm"] = MitmForm(scrollable, context)
        self.forms["table"] = MitmTable(scrollable, context)

        for i, form in enumerate(self.forms.values()):
            form.grid(row=i, column=0, pady=self.style.gap, padx=self.style.gap, sticky="ew")
        # self.refresh_forms()
        scrollable.columnconfigure(0, weight=1)
        scrollable.add_deadspace("grid")

        forms_button = self.menu_bar.add_button("Forms")
        forms_overlay = FormOverlay(forms_button, context, self.refresh_forms)

        variables_button = self.menu_bar.add_button("Variables")
        variables_overlay = VariableOverlay(variables_button, context, self.refresh_rows)

        stop_button = self.menu_bar.add_button("Stop All", self.stop_all)


    def refresh_forms(self):
        self.update_idletasks()
        for key in self.context.states["modbus_variables"]:
            state = self.context.states["modbus_variables"][key]["show"]
            if state == "1" or state == 1:
                self.show_forms(key)
            else:
                self.hide_forms(key)

    def hide_forms(self, name: str):
        form = self.forms[name]
        if not form.winfo_ismapped():
            return
        form.grid_remove()  

    def show_forms(self, name: str):
        form = self.forms[name]
        if form.winfo_ismapped():
            return
        form.grid()

    def refresh_rows(self):
        ...

    def stop_all(self):
        for form in self.forms.values():
            form.click_stop()