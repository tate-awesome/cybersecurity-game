from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QWidget
from ....app_core import Context
from ....network.hardware import ap_commands
from ... import Scrollable
from ..panel import Panel

ROW_COUNT = 10
FIELDS = ["x", "y", "theta", "speed", "rudder"]
COLUMNS = ["Time", "X (m)", "Y (m)", "Theta", "Speed", "Rudder"]
SOURCES = {"CLIENT": "client_clean", "SERVER": "server_clean"}


class Builder(Panel):
    '''
    DefenderV0's "PACKET LOG (last 10)" as its own panel: the newest 10
    submarine points from whichever source the CLIENT/SERVER dropdown picks,
    newest first, read from context.buffer.defender_modbus. Like the
    original it only has anything to show in submarine mode - the AP's HVAC
    telemetry isn't a per-packet log.
    '''

    KEY = "defender_console_panel"

    def __init__(self, master: QWidget, context: Context):
        super().__init__(master, context, self.KEY)
        self.modbus = self.context.buffer.defender_modbus
        self.source = SOURCES["CLIENT"]
        self._shown_rows = None

        self.menu_bar.add_dropdown(list(SOURCES), self.set_source, "CLIENT")

        self.scrollable = Scrollable(self, context)
        grid = self.scrollable.grid_layout
        for i, column in enumerate(COLUMNS):
            label = QLabel(column)
            label.setFont(self.style.get_font("small"))
            label.setStyleSheet("color: gray;")
            grid.addWidget(label, 0, i)
            self.scrollable.columnconfigure(i, 1)

        # Built once and re-texted every tick, rather than torn down and
        # rebuilt like the original's _render_log.
        self.cells: list[list[QLabel]] = []
        for r in range(ROW_COUNT):
            background = self.style.color("field") if r % 2 == 0 else self.style.color("widget")
            row = []
            for c in range(len(COLUMNS)):
                cell = QLabel("")
                cell.setFont(self.style.get_font("mono"))
                cell.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
                cell.setStyleSheet(self.style.themed(f"background-color: {background};", cell))
                grid.addWidget(cell, r + 1, c)
                row.append(cell)
            self.cells.append(row)

        self.hvac_label = QLabel("The packet log is only available in submarine mode.")
        self.hvac_label.setFont(self.style.get_font())
        self.hvac_label.setStyleSheet("color: gray;")
        self.hvac_label.setWordWrap(True)
        grid.addWidget(self.hvac_label, ROW_COUNT + 1, 0, 1, len(COLUMNS))
        self.scrollable.add_deadspace("grid")

        self.menu_bar.minimize_button(self.scrollable, master)

        self.context.animation_manager.add_callback(f"DefenderConsole_{id(self)}", self.refresh)
        self.refresh()

    def set_source(self, text: str):
        self.source = SOURCES[text]
        self.refresh()

    def latest_rows(self) -> list[tuple]:
        '''
        The newest ROW_COUNT points, newest first: (time, x, y, theta, speed,
        rudder). The poll unpacker writes all five fields together per
        point, so their sample lists line up index-for-index.
        '''
        samples = {field: self.modbus.get_samples(field, self.source) for field in FIELDS}
        length = min(len(history) for history in samples.values())
        rows = []
        for i in range(length - 1, max(-1, length - 1 - ROW_COUNT), -1):
            index = {field: len(samples[field]) - length + i for field in FIELDS}
            time = samples["x"][index["x"]][0]
            rows.append((time, *(samples[field][index[field]][1] for field in FIELDS)))
        return rows

    def refresh(self):
        submarine_mode = ap_commands.submarine_mode(self.context.buffer)
        self.hvac_label.setVisible(not submarine_mode)
        rows = self.latest_rows() if submarine_mode else []
        if rows == self._shown_rows:
            return
        self._shown_rows = rows

        for r, cells in enumerate(self.cells):
            if r >= len(rows):
                for cell in cells:
                    cell.setText("")
                continue
            time, *values = rows[r]
            # Seconds since the first point received from the AP.
            secs = int(time)
            cells[0].setText(f"{secs // 3600:02d}:{(secs % 3600) // 60:02d}:{secs % 60:02d}")
            for cell, value in zip(cells[1:], values):
                try:
                    cell.setText(f"{float(value):.4f}")
                except (TypeError, ValueError):
                    cell.setText(str(value))
