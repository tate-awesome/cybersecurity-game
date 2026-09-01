from customtkinter import CTkFrame
from ....app_core import Context
from ..panel import Panel

from .forms.table import MitmTable
from .forms.modify import Modify
from .variable_overlay import VariableOverlay

from ....widgets import Scrollable, MenuBar, Overlay, CheckboxOverlay

FORM_CLASSES = {
    "table": MitmTable,
    "modify": Modify
}

class Builder(Panel):
    KEY = "modbus_table_panel"

    def __init__(self, master: CTkFrame, context: Context):

        super().__init__(master, context, self.KEY)

        self.scrollable = Scrollable(self, context)

        self.available_forms: dict[str, int] = self.context.states.get("modbus_table_visibility")
        if self.available_forms is None:
            self.available_forms = list(FORM_CLASSES.keys())

        self.forms = {}
        for key in FORM_CLASSES:
            self.forms[key] = FORM_CLASSES[key](self.scrollable, context)

        for i, form in enumerate(self.forms.values()):
            form.grid(row=i, column=0, pady=self.style.gap, padx=self.style.gap, sticky="ew")
        # self.refresh_forms()
        self.scrollable.columnconfigure(0, weight=1)
        self.scrollable.add_deadspace("grid")

        variables_button = self.menu_bar.add_button("variables_overlay")
        variables_overlay = VariableOverlay(variables_button, context, self.refresh_rows, self.refresh_nicknames)

        forms_button = self.menu_bar.add_button("forms_overlay")
        forms_overlay = CheckboxOverlay(forms_button, context, self.refresh_forms, "modbus_forms", "Show Forms", "modbus_table_visibility")

        clear_button = self.menu_bar.add_button("clear_modbus", self.context.net.buffer.reset_modbus)

        self.update_idletasks()
        self.refresh_nicknames()
        self.refresh_rows()
        self.refresh_forms()


    def refresh_forms(self):
        self.update_idletasks()
        for key in self.context.states.get("modbus_forms"):
            state = self.context.states.get("modbus_forms", key)

            invisible = key not in self.available_forms or self.available_forms[key] == 0 or self.available_forms[key] == "0"
            selected = state == "1" or state == 1
            if not invisible and selected:
                self.show_forms(key)
            else:
                self.hide_forms(key)
        self.scrollable.top()

    def hide_forms(self, name: str):
        if name not in self.forms:
            raise KeyError(f"No modbus-panel form named {name!r} (check 'modbus_forms' in settings)")
        form = self.forms[name]
        if not form.winfo_ismapped():
            return
        form.grid_remove()

    def show_forms(self, name: str):
        if name not in self.forms:
            raise KeyError(f"No modbus-panel form named {name!r} (check 'modbus_forms' in settings)")
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