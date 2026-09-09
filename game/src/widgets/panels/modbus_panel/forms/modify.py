from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QLineEdit, QPushButton, QWidget
from .....app_core import Context
from ...base_form import BaseForm

class Modify(BaseForm):
    def __init__(self, master: QWidget, context: Context):
        super().__init__(master, context, process_noun="Modifying")
        # Assign local references
        self.buffer = context.buffer.modbus
        # Create form

        self.grid_layout.setColumnStretch(0, 0)
        self.grid_layout.setColumnStretch(1, 1)
        self.grid_layout.setColumnStretch(2, 1)

        self.add_header("ModBus Modifiers")

        # Create value table entries
        self.rows = {}
        self.entries = []

        self.add_label_row("modbus_modifier", ["variable", "multiplier", "offset"])

        for key in self.context.states.get_registers():
            self.add_var_row(key)

        # self.context.animation_manager.add_callback("modbus_table", self.update)
        self.save_status, self.save_button = self.add_button("Save Modifiers")
        self.bind_input_save()
        self.bind_input_alert()

        self.add_process_row(self.enable_modify, self.disable_modify, self.modify_is_enabled)

        _, reset_button = self.add_button("Reset Modifiers")
        self.wire_button(reset_button, self.reset_modifiers)

        self.load_saved_input()

    def add_var_row(self, key):
        this_row = {}
        self.current_column = 0

        def label(text):
            label = QLabel(text)
            label.setFont(self.style.get_font("mono"))
            label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            self.grid_layout.addWidget(label, self.current_row, self.current_column)
            self.current_column += 1
            return label

        def entry():
            entry = QLineEdit()
            entry.setFont(self.style.get_font("mono"))
            entry.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.grid_layout.addWidget(entry, self.current_row, self.current_column)
            self.entries.append(entry)
            self.current_column += 1
            return entry

        this_row["name"] = label("-")
        this_row["multiplier"] = entry()
        this_row["offset"] = entry()
        self.rows[key] = this_row
        self.current_row += 1

        self.row_visibility(key)


    def refresh_nicknames(self):
        for key, row in self.rows.items():
            variable_name = self.context.labels.variable_name(key)
            row["name"].setText(variable_name)

    def refresh_rows(self):
        for key in self.context.states.get_registers():
            self.row_visibility(key)

    def row_visibility(self, key: str):
        state = self.context.states.get_register(key, "show")
        row = self.rows[key]
        for _, widget in row.items():
            if (state == 0 or state == "0") and not widget.isHidden():
                widget.hide()
            elif (state == 1 or state == "1") and widget.isHidden():
                widget.show()

    def add_button(self, text) -> tuple[QLabel, QPushButton]:
        status = QLabel("")
        status.setFont(self.style.get_font())
        status.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.grid_layout.addWidget(status, self.current_row, 0, 1, 2)

        button = QPushButton(text)
        button.setFont(self.style.get_font())
        self.grid_layout.addWidget(button, self.current_row, 2)
        self.current_row += 1

        return status, button

    def bind_input_save(self):
        def save():
            # Validate
            valid = True
            for _, row in self.rows.items():
                try:
                    float(row["multiplier"].text())
                    float(row["offset"].text())
                except:
                    valid = False
                    pass

            if not valid:
                self.save_status.setText("! Must be Numbers !")
                return

            # Then save
            for key, row in self.rows.items():
                mult = float(row["multiplier"].text())
                self.context.states.set_register(key, "multiplier", mult)
                offset = float(row["offset"].text())
                self.context.states.set_register(key, "offset", offset)

            self.save_status.setText("Modifiers Saved.")

        self.wire_button(self.save_button, save)

        for entry in self.entries:
            entry.returnPressed.connect(save)

    def bind_input_alert(self):
        def alert(text=None):
            self.save_status.setText("! Unsaved Modifiers !")
        for entry in self.entries:
            entry.textEdited.connect(alert)

    def load_saved_input(self):
        for key, row in self.rows.items():
            multiplier_str = self.context.states.get_register(key, "multiplier")
            offset_str = self.context.states.get_register(key, "offset")

            mult = f"{float(multiplier_str):g}"
            row["multiplier"].setText(mult)

            offset = f"{float(offset_str):g}"
            row["offset"].setText(offset)

        self.save_status.setText("Modifiers Saved.")

    # Enable Modify Button

    def enable_modify(self):
        self.context.states.set("modbus_modify_enabled", value=1)

    def disable_modify(self):
        self.context.states.set("modbus_modify_enabled", value=0)

    def modify_is_enabled(self):
        state = self.context.states.get("modbus_modify_enabled")
        if state == 1: return True
        else: return False

    # Reset button

    def reset_modifiers(self):
        for key, row in self.rows.items():
            self.context.states.set_register(key, "multiplier", 1)
            self.context.states.set_register(key, "offset", 0)
        self.load_saved_input()
