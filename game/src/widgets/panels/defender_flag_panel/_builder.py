from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget
from ....app_core import Context
from ....network.hardware import ap_commands
from ... import Scrollable
from ..panel import Panel

# (defender_status key, display label) - DefenderV0's SUBMARINE_FLAG_DEFS/
# HVAC_FLAG_DEFS, keyed by the status the poll unpacker actually writes.
SUBMARINE_FLAGS = [
    ("state_anomaly", "State Filtering Threshold Surpassed"),
    ("speed_anomaly", "Speed Filtering Threshold Surpassed"),
    ("rudder_anomaly", "Rudder Filtering Threshold Surpassed"),
]
HVAC_FLAGS = [
    ("hvac_anomaly", "State Filtering Threshold Surpassed"),
]


class Builder(Panel):
    '''
    DefenderV0's middle pane minus its packet log (that's
    defender_console_panel): the error-detection flags for whichever mode
    the AP is in, and the submarine Kalman filter status and toggle -
    greyed out in HVAC mode, like the network_action_panel's Kalman form.
    Reads and commands everything through context.buffer.defender_status.
    '''

    KEY = "defender_flag_panel"

    def __init__(self, master: QWidget, context: Context):
        super().__init__(master, context, self.KEY)

        self.scrollable = Scrollable(self, context)
        self.scrollable.columnconfigure(0, weight=1)

        self.submarine_section, self.submarine_dots = self._build_flags("SUBMARINE ERROR DETECTION FLAGS", SUBMARINE_FLAGS)
        self.hvac_section, self.hvac_dots = self._build_flags("HVAC ERROR DETECTION FLAG", HVAC_FLAGS)
        self.kalman_section = self._build_kalman()

        for row, section in enumerate([self.submarine_section, self.hvac_section, self.kalman_section]):
            self.scrollable.grid_layout.addWidget(section, row, 0)
        self.scrollable.add_deadspace("grid")

        self.menu_bar.minimize_button(self.scrollable, master)

        self._submarine_mode = None
        self.context.animation_manager.add_callback(f"DefenderFlagPanel_{id(self)}", self.refresh)
        self.refresh()

    def _section(self, title: str) -> QWidget:
        section = QWidget()
        section.setStyleSheet(self.style.themed(f"background-color: {self.style.color('widget')};", section))
        layout = QVBoxLayout(section)
        layout.setContentsMargins(self.style.igap, self.style.igap, self.style.igap, self.style.igap)
        layout.setSpacing(4)
        label = QLabel(title)
        label.setFont(self.style.get_font())
        layout.addWidget(label)
        return section

    def _build_flags(self, title: str, defs) -> tuple[QWidget, dict[str, QLabel]]:
        section = self._section(title)
        dots = {}
        for key, text in defs:
            row = QWidget()
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(0, 0, 0, 0)
            section.layout().addWidget(row)

            dot = QLabel("●")
            dot.setFont(self.style.get_font("small"))
            dot.setStyleSheet("color: gray;")
            row_layout.addWidget(dot)

            label = QLabel(text)
            label.setFont(self.style.get_font("small"))
            row_layout.addWidget(label, 1)
            dots[key] = dot
        return section, dots

    def _build_kalman(self) -> QWidget:
        section = self._section("KALMAN FILTER")

        self.kalman_label = QLabel("")
        self.kalman_label.setFont(self.style.get_font())
        section.layout().addWidget(self.kalman_label)

        button = QPushButton("Toggle Kalman Filter")
        button.setFont(self.style.get_font())
        button.clicked.connect(lambda checked=False: ap_commands.set_kalman(
            self.context.buffer, not ap_commands.kalman_enabled(self.context.buffer)))
        section.layout().addWidget(button)
        return section

    def refresh(self):
        buffer = self.context.buffer
        submarine_mode = ap_commands.submarine_mode(buffer)
        if submarine_mode != self._submarine_mode:
            self._submarine_mode = submarine_mode
            self.submarine_section.setVisible(submarine_mode)
            self.hvac_section.setVisible(not submarine_mode)
            self.kalman_section.setEnabled(submarine_mode)

        for key, dot in (self.submarine_dots | self.hvac_dots).items():
            raised = bool(buffer.defender_status.get(key, False))
            dot.setStyleSheet(f"color: {'red' if raised else 'gray'};")

        on = ap_commands.kalman_enabled(buffer)
        self.kalman_label.setText("Status: ON" if on else "Status: OFF")
        # An explicit stylesheet color overrides the disabled palette, so
        # greying out in HVAC mode has to be done here too.
        self.kalman_label.setStyleSheet(f"color: {'green' if on and submarine_mode else 'gray'};")
