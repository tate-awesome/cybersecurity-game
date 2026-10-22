from PySide6.QtWidgets import QLabel, QWidget
from .....app_core import Context
from ...base_form import BaseForm
from .numbers import NUMBER_ALIGNMENT, TEXT_ALIGNMENT, align_decimals, format_number

# Each column's kind, for its alignment - see numbers
NUMBER_COLUMNS = {"incoming", "outgoing"}

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

        self.add_header("Readings")

        # Create value table entries
        self.rows = {}

        headers = self.add_label_row("modbus_table", ["name", "in", "out", "source"])
        self.align_row(headers)

        for key in self.context.states.get_registers():
            labels = self.add_label_row("modbus_table", ["-", "-", "-", "-"])
            self.rows[key] = {}
            self.rows[key]["name"] = labels[0]
            self.rows[key]["incoming"] = labels[1]
            self.rows[key]["outgoing"] = labels[2]
            self.rows[key]["source"] = labels[3]
            self.align_row(labels)

        self.context.animation_manager.add_callback(f"modbus_table_{id(self)}", self.refresh_values)
        self.refresh_registers()
        self.context.animation_manager.add_callback(f"modbus_table_registers_{id(self)}", self.refresh_registers)

    def align_row(self, labels: list[QLabel]):
        for label, name in zip(labels, ["name", "incoming", "outgoing", "source"]):
            label.setAlignment(NUMBER_ALIGNMENT if name in NUMBER_COLUMNS else TEXT_ALIGNMENT)

    def refresh_registers(self):
        '''
        Follows each register's "show" and "nickname" in modbus_registers
        (edited by EditModbusRegisterDisplay) - polled every frame; both
        steps only touch widgets whose state actually changed.
        '''
        self.refresh_rows()
        self.refresh_nicknames()

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
            raise KeyError(f"No modbus table row for register {key!r} (check 'modbus_registers' in settings)")
        row = self.rows[key]
        for _, widget in row.items():
            if widget.isHidden():
                widget.show()

    def hide_row(self, key: str):
        if key not in self.rows:
            raise KeyError(f"No modbus table row for register {key!r} (check 'modbus_registers' in settings)")
        row = self.rows[key]
        for _, widget in row.items():
            if not widget.isHidden():
                widget.hide()

    def refresh_values(self):
        texts = {}
        for key, this_row in self.rows.items():
            if this_row["name"].isHidden():
                continue
            factor_str = self.context.states.get_register(key, "factor")
            try:
                factor = float(factor_str)
            except (TypeError, ValueError):
                message = "err: factor"
                texts[key] = {"incoming": message, "outgoing": message, "source": message}
                continue

            # TODO switch to a get dump type of thing where it dumps all the changed values

            in_value = self.buffer.get_single(key, "in")
            out_value = self.buffer.get_single(key, "out")
            texts[key] = {
                "incoming": "-" if in_value is None else format_number(in_value*factor),
                "outgoing": "-" if out_value is None else format_number(out_value*factor),
                "source": self.buffer.get_command(key) or "-",
            }

        # Line up each number column's decimal points across the shown rows
        for column in NUMBER_COLUMNS:
            aligned = align_decimals([row[column] for row in texts.values()])
            for row, text in zip(texts.values(), aligned):
                row[column] = text

        for key, row in texts.items():
            for name, text in row.items():
                label = self.rows[key][name]
                if label.text() != text:
                    label.setText(text)
