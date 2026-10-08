from PySide6.QtWidgets import QWidget
from ....app_core import Context
from ..panel import Panel

from .forms.table import MitmTable
from .forms.modify import Modify

from ....widgets import Scrollable
from ...frame_widgets.important_buttons import ChooseShownModbusTableForms, ClearModbusAndModelData, EditModbusRegisterDisplay

FORM_CLASSES = {
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
        self.menu_bar.add_important(ChooseShownModbusTableForms)
        self.menu_bar.add_important(ClearModbusAndModelData)

        minimize_button = self.menu_bar.minimize_button(self.scrollable, master)

        self.shown_forms = None  # modbus_table_forms_shown as of the last refresh_forms
        self.refresh_forms()
        self.context.animation_manager.add_callback(f"modbus_table_forms_{id(self)}", self.refresh_forms)


    def refresh_forms(self):
        '''
        Shows/hides forms to match modbus_table_forms_shown - polled every
        frame, so it only acts (and scrolls back to the top) when that changed.
        '''
        shown = dict(self.context.states.get("modbus_table_forms_shown"))
        if shown == self.shown_forms:
            return
        self.shown_forms = shown
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
