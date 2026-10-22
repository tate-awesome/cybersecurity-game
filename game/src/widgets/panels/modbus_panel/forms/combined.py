from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QPushButton, QWidget
from .....app_core import Context
from ....frame_widgets.important_buttons.edit_modbus_register_display.variable_overlay import VariableOverlay
from ...base_form import BaseForm

COLUMNS = ["register", "units", "in", "multiplier", "offset", "out", "type"]

class CombinedTable(BaseForm):
    '''
    MitmTable and Modify in one: each register's sniffed in/out values with
    its multiplier/offset entries between them, so a row reads left to
    right as the value going through the modifier. Entries save as they're
    typed (a value that isn't a number yet is just left unsaved, and put
    back to the saved one when the entry is left).
    '''
    def __init__(self, master: QWidget, context: Context):
        super().__init__(master, context, process_noun="Modifying")
        self.buffer = context.buffer.modbus
        self.status_on_text = self.context.labels.get("modbus_combined_status_on")
        self.status_off_text = self.context.labels.get("modbus_combined_status_off")

        for column in range(len(COLUMNS)):
            self.grid_layout.setColumnStretch(column, 1)
        self.grid_layout.setColumnStretch(0, 2)

        headers = self.add_label_row("modbus_combined", COLUMNS)
        headers[COLUMNS.index("units")].setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.add_divider()

        self.rows = {}
        # Each row's widgets as placed in the grid (entries' wrappers rather
        # than the entries themselves) - hiding only the entries would leave
        # their wrappers occupying the row, so the grid would still add a
        # row's worth of spacing for every hidden register.
        self.row_cells: dict[str, list[QWidget]] = {}
        for key in self.context.states.get_registers():
            self.add_register_row(key)

        add_register = QPushButton(self.context.labels.get("modbus_combined_add_register"))
        add_register.setFont(self.style.get_font())
        VariableOverlay(add_register, context)
        self.grid_layout.addWidget(self.fixed_width_wrapper(add_register), self.current_row, 0, 1, -1)
        self.current_row += 1
        self.add_divider()

        self.reset_button = QPushButton(self.context.labels.get("modbus_combined_reset"))
        self.reset_button.setFont(self.style.get_font())
        self.wire_button(self.reset_button, self.reset_modifiers)
        self.add_process_row(self.enable_modify, self.disable_modify, self.modify_is_enabled)

        self.refresh_registers()
        self.context.animation_manager.add_callback(f"modbus_combined_{id(self)}", self.refresh_values)
        self.context.animation_manager.add_callback(f"modbus_combined_registers_{id(self)}", self.refresh_registers)

    def add_divider(self):
        divider = QWidget()
        divider.setFixedHeight(1)
        divider.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.style.live_style(divider, lambda: f"QWidget {{ background: {self.style.color('border')}; }}")
        self.grid_layout.addWidget(divider, self.current_row, 0, 1, -1)
        self.current_row += 1

    def add_register_row(self, key: str):
        row = {}
        cells = []

        def label(name: str, alignment: Qt.AlignmentFlag):
            label = QLabel("-")
            label.setFont(self.style.get_font("mono"))
            label.setAlignment(alignment)
            self.grid_layout.addWidget(label, self.current_row, len(cells))
            cells.append(label)
            row[name] = label

        def entry(name: str):
            entry = QLineEdit()
            entry.setFont(self.style.get_font("mono"))
            entry.setAlignment(Qt.AlignmentFlag.AlignCenter)
            # See Modify.add_var_row - fixed width without locking the column
            entry.setFixedWidth(self.style.igap * 6)
            entry.textEdited.connect(lambda text, key=key: self.save_register(key))
            entry.editingFinished.connect(lambda key=key: self.load_register(key, force=True))
            wrapper = self.fixed_width_wrapper(entry, Qt.AlignmentFlag.AlignCenter)
            self.grid_layout.addWidget(wrapper, self.current_row, len(cells))
            cells.append(wrapper)
            row[name] = entry

        left = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        label("register", left)
        label("units", left)
        label("in", Qt.AlignmentFlag.AlignCenter)
        entry("multiplier")
        entry("offset")
        label("out", Qt.AlignmentFlag.AlignCenter)
        label("type", Qt.AlignmentFlag.AlignCenter)

        self.rows[key] = row
        self.row_cells[key] = cells
        self.current_row += 1
        self.load_register(key, force=True)

    def place_process_row(self):
        row = QWidget()
        layout = QHBoxLayout(row)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(self.style.igap)
        layout.addWidget(self.process_button)
        layout.addWidget(self.reset_button)
        layout.addStretch()
        self.process_status.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(self.process_status)
        self.grid_layout.addWidget(row, self.current_row, 0, 1, -1)

    def configure_on(self):
        super().configure_on()
        self.style.set_tone(self.process_status, "good")

    def configure_off(self):
        super().configure_off()
        self.style.set_tone(self.process_status, "muted")

    # Registers

    def refresh_registers(self):
        '''
        Follows each register's "show", "nickname", "units", "multiplier" and
        "offset" in modbus_registers (edited by EditModbusRegisterDisplay,
        presets and resets) - polled every frame; only touches widgets whose
        state actually changed.
        '''
        for key in self.context.states.get_registers():
            shown = self.context.states.get_register(key, "show") in (1, "1")
            for widget in self.row_cells[key]:
                if widget.isHidden() == shown:
                    widget.setVisible(shown)
            if not shown:
                continue
            row = self.rows[key]
            self.set_text(row["register"], self.register_name(key))
            self.set_text(row["units"], str(self.context.states.get_register(key, "units")))
            self.load_register(key)

    def register_name(self, key: str) -> str:
        name = self.context.labels.get(f"modbus_variables_{key}")
        nickname = self.context.states.get_register(key, "nickname")
        if nickname:
            return f"{name}  {nickname}"
        return name

    def set_text(self, label: QLabel, text: str):
        if label.text() != text:
            label.setText(text)

    def load_register(self, key: str, force: bool = False):
        '''
        Fills key's entries from its saved multiplier/offset - skipping one
        being typed in unless force, so polling doesn't fight the user.
        '''
        row = self.rows[key]
        for slot in ("multiplier", "offset"):
            entry = row[slot]
            if entry.hasFocus() and not force:
                continue
            text = f"{float(self.context.states.get_register(key, slot)):g}"
            if entry.text() != text:
                entry.setText(text)

    def save_register(self, key: str):
        row = self.rows[key]
        for slot in ("multiplier", "offset"):
            try:
                value = float(row[slot].text())
            except ValueError:
                continue
            self.context.states.set_register(key, slot, value)

    def reset_modifiers(self):
        for key in self.rows:
            self.context.states.set_register(key, "multiplier", 1)
            self.context.states.set_register(key, "offset", 0)
            self.load_register(key, force=True)

    # Values

    def refresh_values(self):
        for key, row in self.rows.items():
            if row["in"].isHidden():
                continue
            try:
                factor = float(self.context.states.get_register(key, "factor"))
            except (TypeError, ValueError):
                for name in ("in", "out", "type"):
                    self.set_text(row[name], "err: factor")
                continue

            in_value = self.buffer.get_single(key, "in")
            self.set_text(row["in"], "-" if in_value is None else self.format_number(in_value * factor))
            out_value = self.buffer.get_single(key, "out")
            self.set_text(row["out"], "-" if out_value is None else self.format_number(out_value * factor))
            self.set_text(row["type"], self.command_type(self.buffer.get_command(key)))

    def command_type(self, command: str | None) -> str:
        '''"Read Response" -> R, "Write Request" -> W (see MetaPacket's command_word).'''
        if not command:
            return "-"
        verb = command.split(" ")[0].lower()
        if verb in ("read", "write"):
            return self.context.labels.get(f"modbus_combined_{verb}")
        return command

    def format_number(self, value: float, decimals: int = 2) -> str:
        value = round(value, decimals)
        if value == 0:
            value = 0.00
        return f"{value:.{decimals}f}".rstrip("0").rstrip(".")

    # Modify process

    def enable_modify(self):
        self.context.states.set("modbus_packet_modify_enabled", value=1)

    def disable_modify(self):
        self.context.states.set("modbus_packet_modify_enabled", value=0)

    def modify_is_enabled(self):
        return self.context.states.get("modbus_packet_modify_enabled") == 1
