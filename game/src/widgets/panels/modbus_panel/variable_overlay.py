from ....app_core import Context
from ....widgets import Overlay
from PySide6.QtWidgets import QCheckBox, QFrame, QGridLayout, QLabel, QLineEdit, QPushButton
from typing import Callable


class VariableOverlay:
    '''
    Binds a button to open and close an overlay with checkboxes for each form, which are saved in the context states for persistence.
    The refresh function is called when any checkbox is clicked
    '''
    def __init__(self, button: QPushButton, context: Context, refresh_rows: Callable, refresh_nicknames: Callable):
        self.context = context
        self.style = context.style
        self.refresh_rows = refresh_rows
        self.refresh_nicknames = refresh_nicknames
        self.overlay = Overlay(self.context.root, context, button, self.populate_overlay, "east")

    def populate_overlay(self, overlay: Overlay):
        med = self.style.get_font()
        frame = QFrame()
        frame.setStyleSheet(f"background-color: {self.style.color('panel')};")
        grid = QGridLayout(frame)
        overlay.layout().addWidget(frame)

        row = 0
        col = 0

        # Top Row
        top_labels = self.context.labels.get("modbus_settings")
        for key, text in top_labels.items():
            top_label = QLabel(text)
            top_label.setFont(med)
            grid.addWidget(top_label, row, col)
            col += 1
        col = 0
        row += 1

        show_checkboxes = []
        nick_entries = []
        factor_entries = []
        units_entries = []
        modify_checkboxes = []

        # Variable Rows

        for slot in self.context.states.get_registers().values():
            # "label": "hreg_8",
            variable_name = self.context.labels.get("modbus_variables", slot["label"])
            var_label = QLabel(variable_name)
            var_label.setFont(med)
            grid.addWidget(var_label, row, col)
            col += 1
            # "show": 1.0,
            show_checkbox = QCheckBox()
            grid.addWidget(show_checkbox, row, col)
            self.enrich_checkbox(show_checkbox, slot, "show")
            show_checkboxes.append(show_checkbox)
            col += 1
            # "nickname": "",
            nick_entry = QLineEdit()
            nick_entry.setFont(med)
            grid.addWidget(nick_entry, row, col)
            self.enrich_entry(nick_entry, slot, "nickname")
            nick_entries.append(nick_entry)
            col += 1
            # "factor": 1.0,
            factor_entry = QLineEdit()
            factor_entry.setFont(med)
            grid.addWidget(factor_entry, row, col)
            self.enrich_entry(factor_entry, slot, "factor")
            factor_entries.append(factor_entry)
            col += 1
            # "units": "",
            units_entry = QLineEdit()
            units_entry.setFont(med)
            grid.addWidget(units_entry, row, col)
            self.enrich_entry(units_entry, slot, "units")
            units_entries.append(units_entry)
            col += 1
            # "modify": 0
            modify_checkbox = QCheckBox()
            grid.addWidget(modify_checkbox, row, col)
            self.enrich_checkbox(modify_checkbox, slot, "modify")
            modify_checkboxes.append(modify_checkbox)

            col = 0
            row += 1

        # Do All buttons
        def connect(button, function):
            button.clicked.connect(lambda checked=False, function=function: function())

        # Reset All
        def reset_all():
            self.select_all(show_checkboxes)
            self.clear_entries(nick_entries)
            self.set_entries(factor_entries, "1.0")
            self.clear_entries(units_entries)
            self.deselect_all(modify_checkboxes)
        button = QPushButton("Reset All")
        button.setFont(med)
        connect(button, reset_all)
        grid.addWidget(button, row + 1, col)
        col += 1
        # Show
        button = QPushButton("Select All")
        button.setFont(med)
        connect(button, lambda: self.select_all(show_checkboxes))
        grid.addWidget(button, row, col)
        button = QPushButton("Deselect All")
        button.setFont(med)
        connect(button, lambda: self.deselect_all(show_checkboxes))
        grid.addWidget(button, row + 1, col)
        col += 1
        # Nicknames
        button = QPushButton("Clear All")
        button.setFont(med)
        connect(button, lambda: self.clear_entries(nick_entries))
        grid.addWidget(button, row + 1, col)
        col += 1
        # Factors
        button = QPushButton("Reset All")
        button.setFont(med)
        connect(button, lambda: self.set_entries(factor_entries, "1.0"))
        grid.addWidget(button, row + 1, col)
        col += 1
        # Units
        button = QPushButton("Clear All")
        button.setFont(med)
        connect(button, lambda: self.clear_entries(units_entries))
        grid.addWidget(button, row + 1, col)
        col += 1
        # Modify
        button = QPushButton("Select All")
        button.setFont(med)
        connect(button, lambda: self.select_all(modify_checkboxes))
        grid.addWidget(button, row, col)
        button = QPushButton("Deselect All")
        button.setFont(med)
        connect(button, lambda: self.deselect_all(modify_checkboxes))
        grid.addWidget(button, row + 1, col)
        col += 1

    def enrich_entry(self, entry: QLineEdit, slot: dict, key: str):
        # Bind autosave
        def autosave(text, slot=slot, key=key):
            slot[key] = text
            self.refresh_nicknames()
        entry.textEdited.connect(autosave)
        # set_entries needs to trigger this same save when it sets text
        # programmatically, since textEdited (deliberately) doesn't fire for that.
        entry.autosave = lambda: autosave(entry.text())

        # Load saved entry input (before connecting would be pointless here -
        # textEdited never fires for setText() regardless). slot[key] may be
        # a float (e.g. "factor") - tkinter's Entry.insert() stringified it
        # for free, QLineEdit.setText() requires an actual str.
        entry.setText(str(slot[key]))

    def enrich_checkbox(self, checkbox: QCheckBox, slot: dict, key: str):
        # Load previous input before connecting, so restoring it doesn't itself trigger autosave
        value = slot[key]
        checkbox.setChecked(value == "1" or value == 1)

        # Configure for autosave (give it a function with a value container and its key).
        # Stored as "1"/"0" - the convention this settings data already uses
        # everywhere else (matching customtkinter's CTkCheckBox.get(), which
        # returned 1/0, not Qt's own True/False).
        def autosave(checked: bool, slot=slot, key=key):
            slot[key] = "1" if checked else "0"
            self.refresh_rows()
        checkbox.toggled.connect(autosave)

    def select_all(self, checkboxes: list[QCheckBox]):
        for checkbox in checkboxes:
            checkbox.setChecked(True)

    def deselect_all(self, checkboxes: list[QCheckBox]):
        for checkbox in checkboxes:
            checkbox.setChecked(False)

    def clear_entries(self, entries: list[QLineEdit]):
        self.set_entries(entries, "")

    def set_entries(self, entries: list[QLineEdit], text: str):
        for entry in entries:
            entry.setText(text)
            entry.autosave()
