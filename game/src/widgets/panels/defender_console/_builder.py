from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QWidget
from ....app_core import Context
from ....network.hardware import ap_commands
from ... import Scrollable
from ..panel import Panel

ROW_COUNT = 10
SOURCES = {"CLIENT": "client_clean", "SERVER": "server_clean"}

# Submarine: DefenderV0's "PACKET LOG (last 10)" columns - (variable, attribute)
# per column after Time, attribute None meaning the CLIENT/SERVER pick.
SUBMARINE_HEADERS = ["Time", "X (m)", "Y (m)", "Theta", "Speed", "Rudder"]
SUBMARINE_COLUMNS = [("x", None), ("y", None), ("theta", None), ("speed", None), ("rudder", None)]

# HVAC: HVACView's LIVE STATUS card (Current Temp/Target Temp/Heater), one
# row per poll. The AP only reports these once, from the HVAC client, so
# CLIENT/SERVER doesn't apply.
HVAC_HEADERS = ["Time", "Current Temp", "Target Temp", "Heater"]
HVAC_COLUMNS = [("temperature", "client_clean"), ("temperature", "target"), ("heater", "client_clean")]

COLUMN_COUNT = max(len(SUBMARINE_HEADERS), len(HVAC_HEADERS))


class Builder(Panel):
    '''
    DefenderV0's "PACKET LOG (last 10)" as its own panel: the newest 10
    points from context.buffer.defender_modbus, newest first. In submarine
    mode that's the original's x/y/theta/speed/rudder log for whichever
    source the CLIENT/SERVER dropdown picks; in HVAC mode it's a log of
    HVACView's live readout (current/target temperature and heater) instead.
    '''

    KEY = "defender_console_panel"

    def __init__(self, master: QWidget, context: Context):
        super().__init__(master, context, self.KEY)
        self.modbus = self.context.buffer.defender_modbus
        self.source = SOURCES["CLIENT"]
        self._submarine_mode = None
        self._shown_rows = None

        self.source_dropdown = self.menu_bar.add_dropdown(list(SOURCES), self.set_source, "CLIENT")

        self.scrollable = Scrollable(self, context)
        grid = self.scrollable.grid_layout

        self.headers: list[QLabel] = []
        for c in range(COLUMN_COUNT):
            label = QLabel("")
            label.setFont(self.style.get_font("small"))
            label.setStyleSheet("color: gray;")
            grid.addWidget(label, 0, c)
            self.headers.append(label)

        # Built once and re-texted every tick, rather than torn down and
        # rebuilt like the original's _render_log.
        self.cells: list[list[QLabel]] = []
        for r in range(ROW_COUNT):
            background = self.style.color("field") if r % 2 == 0 else self.style.color("widget")
            row = []
            for c in range(COLUMN_COUNT):
                cell = QLabel("")
                cell.setFont(self.style.get_font("mono"))
                cell.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
                cell.setStyleSheet(self.style.themed(f"background-color: {background};", cell))
                grid.addWidget(cell, r + 1, c)
                row.append(cell)
            self.cells.append(row)
        self.scrollable.add_deadspace("grid")

        self.menu_bar.minimize_button(self.scrollable, master)

        self.context.animation_manager.add_callback(f"DefenderConsole_{id(self)}", self.refresh)
        self.refresh()

    def set_source(self, text: str):
        self.source = SOURCES[text]
        self.refresh()

    def _set_mode(self, submarine_mode: bool):
        self._submarine_mode = submarine_mode
        self._shown_rows = None
        headers = SUBMARINE_HEADERS if submarine_mode else HVAC_HEADERS
        grid = self.scrollable.grid_layout
        for c in range(COLUMN_COUNT):
            used = c < len(headers)
            self.headers[c].setText(headers[c] if used else "")
            self.headers[c].setVisible(used)
            for row in self.cells:
                row[c].setVisible(used)
            grid.setColumnStretch(c, 1 if used else 0)
        self.source_dropdown.setEnabled(submarine_mode)

        # HVAC history's clock only advances while some HVAC view is
        # showing it (see DefenderModbusBuffer.pause_hvac) - this log
        # counts, or every row would land on the same frozen time whenever
        # the HVAC model isn't also on screen.
        if submarine_mode:
            self.modbus.pause_hvac(self)
        else:
            self.modbus.resume_hvac(self)

    def latest_rows(self, columns) -> list[tuple]:
        '''
        The newest ROW_COUNT points, newest first: (time, value per column).
        The poll unpacker writes every column of a mode together per point,
        so their sample lists line up index-for-index counting back from
        the newest.
        '''
        samples = [self.modbus.get_samples(variable, attribute or self.source) for variable, attribute in columns]
        length = min(len(history) for history in samples)
        rows = []
        for back in range(1, min(length, ROW_COUNT) + 1):
            points = [history[-back] for history in samples]
            rows.append((points[0][0], *(value for _, value in points)))
        return rows

    def format_time(self, time: float) -> str:
        # Seconds since the first point received from the AP.
        secs = int(time)
        return f"{secs // 3600:02d}:{(secs % 3600) // 60:02d}:{secs % 60:02d}"

    def format_submarine(self, values) -> list[str]:
        output = []
        for value in values:
            try:
                output.append(f"{float(value):.4f}")
            except (TypeError, ValueError):
                output.append(str(value))
        return output

    def format_hvac(self, values) -> list[str]:
        # Same formatting as HVACView's LIVE STATUS card.
        current, target, heater = values
        return [f"{float(current):.1f}°F", f"{float(target):.1f}°F", "ON" if heater else "OFF"]

    def refresh(self):
        submarine_mode = ap_commands.submarine_mode(self.context.buffer)
        if submarine_mode != self._submarine_mode:
            self._set_mode(submarine_mode)

        rows = self.latest_rows(SUBMARINE_COLUMNS if submarine_mode else HVAC_COLUMNS)
        if rows == self._shown_rows:
            return
        self._shown_rows = rows

        for r, cells in enumerate(self.cells):
            if r >= len(rows):
                for cell in cells:
                    cell.setText("")
                continue
            time, *values = rows[r]
            texts = [self.format_time(time)]
            texts += self.format_submarine(values) if submarine_mode else self.format_hvac(values)
            for c, cell in enumerate(cells):
                cell.setText(texts[c] if c < len(texts) else "")
