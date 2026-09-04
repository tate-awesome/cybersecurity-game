from customtkinter import CTkFrame
from ....app_core import Context
from ..panel import Panel

from .forms.mode import ModeForm
from .forms.readout import ReadoutForm
from .forms.sliders import SlidersForm

from ....widgets import Scrollable, CheckboxOverlay

FORM_CLASSES = {
    "mode": ModeForm,
    "readout": ReadoutForm,
    "sliders": SlidersForm,
}


class Builder(Panel):
    '''
    Defender-page counterpart to modbus_table_panel: mode label, live
    client/server readout table, and filter sliders, all reading from
    context.buffer.defender_modbus/defender_status (AP-polled telemetry)
    instead of context.buffer.modbus (sniffed MetaPackets).
    '''

    KEY = "defender_modbus_panel"

    def __init__(self, master: CTkFrame, context: Context):
        super().__init__(master, context, self.KEY)

        self.scrollable = Scrollable(self, context)

        self.available_forms: dict[str, int] = self.context.states.get("defender_modbus_visibility")
        if self.available_forms is None:
            self.available_forms = list(FORM_CLASSES.keys())

        self.forms = {}
        for key in FORM_CLASSES:
            if key not in self.available_forms or self.available_forms[key] in (0, "0"):
                print(f"Form is invisible: {key!r}")
                continue
            self.forms[key] = FORM_CLASSES[key](self.scrollable, context)

        for i, form in enumerate(self.forms.values()):
            form.grid(row=i, column=0, pady=self.style.gap, padx=self.style.gap, sticky="ew")
        self.scrollable.columnconfigure(0, weight=1)
        self.scrollable.add_deadspace("grid")

        forms_button = self.menu_bar.add_button("forms_overlay")
        overlay = CheckboxOverlay(forms_button, context, self.refresh_forms,
                                   "defender_modbus_forms", "Show Forms", "defender_modbus_visibility")

        self.update_idletasks()
        self.refresh_forms()

    def refresh_forms(self):
        self.update_idletasks()
        for key in self.context.states.get("defender_modbus_forms"):
            if key not in self.forms:
                continue
            state = self.context.states.get("defender_modbus_forms", key)
            if state == "1" or state == 1:
                self.show_form(key)
            else:
                self.hide_form(key)
        self.scrollable.top()

    def hide_form(self, name: str):
        if name not in self.forms:
            raise KeyError(f"No defender_modbus_panel form named {name!r} (check 'defender_modbus_forms' in settings)")
        form = self.forms[name]
        if not form.winfo_ismapped():
            return
        form.grid_remove()

    def show_form(self, name: str):
        if name not in self.forms:
            raise KeyError(f"No defender_modbus_panel form named {name!r} (check 'defender_modbus_forms' in settings)")
        form = self.forms[name]
        if form.winfo_ismapped():
            return
        form.grid()
