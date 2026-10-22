from PySide6.QtWidgets import QWidget
from ....app_core import Context
from ..panel import Panel
from ...frame_widgets.important_buttons.checkbox_overlay.checkbox_overlay import form_order

from .forms.table import MitmTable
from .forms.modify import Modify
from .forms.combined import CombinedTable

from ....widgets import Scrollable
from ...frame_widgets.important_buttons import ChooseShownModbusTableForms, ClearModbusAndModelData, EditModbusRegisterDisplay, SelectRegisterPreset

FORM_CLASSES = {
    "combined": CombinedTable,
    "table": MitmTable,
    "modify": Modify
}

class Builder(Panel):
    KEY = "modbus_table_panel"
    # The settings keys (see _packages/_default.json) this panel reads or writes -
    # the workspace editor lists it under each of them
    SETTINGS = (
        "available",
        "modbus_table_forms_shown",
        "form_order",
        "modbus_registers",
        "modbus_packet_modify_enabled",
    )

    def __init__(self, master: QWidget, context: Context):

        super().__init__(master, context, self.KEY)

        self.scrollable = Scrollable(self, context)

        self.available_forms: dict[str, int] = self.context.states.get("available")
        if self.available_forms is None:
            self.available_forms = list(FORM_CLASSES.keys())

        self.forms = {}
        for key in FORM_CLASSES:
            self.forms[key] = FORM_CLASSES[key](self.scrollable, context)

        for i, form in enumerate(self.forms.values()):
            self.scrollable.grid_layout.addWidget(form, i, 0)
        # self.refresh_forms()
        self.scrollable.columnconfigure(0, weight=1)
        self.scrollable.add_deadspace("grid")

        self.menu_bar.add_important(EditModbusRegisterDisplay)
        self.menu_bar.add_important(SelectRegisterPreset)
        self.menu_bar.add_important(ChooseShownModbusTableForms)
        self.menu_bar.add_important(ClearModbusAndModelData)

        minimize_button = self.menu_bar.minimize_button(self.scrollable)

        self.shown_forms = None  # modbus_table_forms_shown as of the last refresh_forms
        self._shown_order = None  # its key order as of the last refresh_forms
        self.refresh_forms()
        self.context.animation_manager.add_callback(f"modbus_table_forms_{id(self)}", self.refresh_forms)


    def refresh_forms(self):
        '''
        Shows/hides forms to match modbus_table_forms_shown - polled every
        frame, so it only acts (and scrolls back to the top) when that changed.
        '''
        shown = dict(self.context.states.get("modbus_table_forms_shown"))
        order = form_order(self.context, "modbus_table_forms_shown")
        # A drag in the overlay changes only the order (see form_order), not
        # which keys are "1"/"0", so compare that separately.
        if shown == self.shown_forms and order == self._shown_order:
            return
        self.shown_forms = shown
        self._shown_order = order
        for row, key in enumerate(k for k in order if k in self.forms):
            self.scrollable.grid_layout.addWidget(self.forms[key], row, 0)
        for key in shown:
            state = self.context.states.get("modbus_table_forms_shown", key)

            invisible = key not in self.available_forms or self.available_forms[key] == 0 or self.available_forms[key] == "0"
            selected = state == "1" or state == 1
            if not invisible and selected:
                self.show_forms(key)
            else:
                self.hide_forms(key)
        self.scrollable.top()

    def hide_forms(self, name: str):
        if name not in self.forms:
            raise KeyError(f"No modbus-panel form named {name!r} (check 'modbus_table_forms_shown' in settings)")
        form = self.forms[name]
        if form.isHidden():
            return
        form.hide()

    def show_forms(self, name: str):
        if name not in self.forms:
            raise KeyError(f"No modbus-panel form named {name!r} (check 'modbus_table_forms_shown' in settings)")
        form = self.forms[name]
        if not form.isHidden():
            return
        form.show()
