from PySide6.QtWidgets import QWidget
from .....app_core import Context
from ...base_form import BaseForm

class MitmTable(BaseForm):
    def __init__(self, master: QWidget, context: Context):
        super().__init__(master, context, process_noun="NFQ")
        # Assign local references
        self.buffer = context.buffer.modbus
        # Create form

        self.grid_layout.setColumnStretch(0, 1)
        self.grid_layout.setColumnStretch(1, 1)
        self.grid_layout.setColumnStretch(2, 1)
        self.grid_layout.setColumnStretch(3, 1)

        self.add_header("ModBus Readings")

        # Create value table entries
        self.rows = {}

        self.add_label_row("modbus_table", ["name", "in", "out", "source"])

        for key in self.context.states.get_registers():
            labels = self.add_label_row("modbus_table", ["-", "-", "-", "-"])
            self.rows[key] = {}
            self.rows[key]["name"] = labels[0]
            self.rows[key]["incoming"] = labels[1]
            self.rows[key]["outgoing"] = labels[2]
            self.rows[key]["source"] = labels[3]

        self.context.animation_manager.add_callback("modbus_table", self.refresh_values)

    def refresh_nicknames(self):
        for key, row in self.rows.items():
            variable_name = self.context.labels.variable_name(key)
            row["name"].setText(variable_name)

    def refresh_rows(self):
        for key in self.context.states.get_registers():
            state = self.context.states.get_register(key, "show")
            if state == "1" or state == 1:
                self.show_row(key)
            else:
                self.hide_row(key)

    def show_row(self, key: str):
        if key not in self.rows:
            raise KeyError(f"No modbus table row for register {key!r} (check 'modbus_variables' in settings)")
        row = self.rows[key]
        for _, widget in row.items():
            if widget.isHidden():
                widget.show()

    def hide_row(self, key: str):
        if key not in self.rows:
            raise KeyError(f"No modbus table row for register {key!r} (check 'modbus_variables' in settings)")
        row = self.rows[key]
        for _, widget in row.items():
            if not widget.isHidden():
                widget.hide()

    def format_number(self, value: float, decimals: int = 2) -> str:
        value = round(value, decimals)
        if value == 0:
            value = 0.00
        return f"{value:.{decimals}f}".rstrip("0").rstrip(".")

    def refresh_values(self):
        for key in self.rows:
            this_row = self.rows[key]
            in_str = "-"
            out_str = "-"
            command = "-"
            factor_str = self.context.states.get_register(key, "factor")
            factor = 1.0
            try:
                f = float(factor_str)
                factor = f
            except:
                message = "err: factor"
                this_row["incoming"].setText(message)
                this_row["outgoing"].setText(message)
                this_row["source"].setText(message)
                continue

            # TODO switch to a get dump type of thing where it dumps all the changed values

            in_value = self.buffer.get_single(key, "in")
            if not in_value is None:
                in_str = self.format_number(in_value*factor)

            out_value = self.buffer.get_single(key, "out")
            if not out_value is None:
                out_str = self.format_number(out_value*factor)

            if com := self.buffer.get_command(key):
                command = com

            this_row["incoming"].setText(in_str)
            this_row["outgoing"].setText(out_str)
            this_row["source"].setText(command)