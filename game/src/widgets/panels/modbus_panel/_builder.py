from customtkinter import CTkFrame
from ....app_core.context import Context
from ..panel import Panel

from .forms.table import MitmTable
from .forms.modify import Modify
from .form_overlay import FormOverlay
from .variable_overlay import VariableOverlay

from ....widgets import Scrollable, MenuBar, Overlay

class Builder(Panel):

    def __init__(self, master: CTkFrame, context: Context):

        super().__init__(master, context, "ModBus")

        self.scrollable = Scrollable(self, context)

        self.forms = {}
        
        self.forms["table"] = MitmTable(self.scrollable, context)
        self.forms["modify"] = Modify(self.scrollable, context)

        for i, form in enumerate(self.forms.values()):
            form.grid(row=i, column=0, pady=self.style.gap, padx=self.style.gap, sticky="ew")
        # self.refresh_forms()
        self.scrollable.columnconfigure(0, weight=1)
        self.scrollable.add_deadspace("grid")

        variables_button = self.menu_bar.add_button("Variables")
        variables_overlay = VariableOverlay(variables_button, context, self.refresh_rows, self.refresh_nicknames)

        forms_button = self.menu_bar.add_button("Forms")
        forms_overlay = FormOverlay(forms_button, context, self.refresh_forms)

        clear_button = self.menu_bar.add_button("Clear Readings", self.context.net.buffer.modbus.reset)

        # stop_button = self.menu_bar.add_button("Stop All", self.stop_all)

        self.update_idletasks()
        self.refresh_nicknames()
        self.refresh_rows()
        self.refresh_forms()


    def refresh_forms(self):
        self.update_idletasks()
        for key in self.context.states["modbus_forms"]:
            state = self.context.states["modbus_forms"][key]
            if state == "1" or state == 1:
                self.show_forms(key)
            else:
                self.hide_forms(key)
        self.scrollable.top()

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
        self.refresh_rows()
        self.refresh_nicknames()

    def refresh_rows(self):
        self.forms["table"].refresh_rows()
        self.forms["modify"].refresh_rows()
        self.scrollable.top()

    def refresh_nicknames(self):
        self.forms["table"].refresh_nicknames()
        self.forms["modify"].refresh_nicknames()

    def stop_all(self):
        for form in self.forms.values():
            form.click_stop()