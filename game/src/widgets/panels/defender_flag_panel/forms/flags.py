from PySide6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget
from .....app_core import Context
from .....network.hardware import ap_commands
from ...base_form import BaseForm

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

SUBMARINE_TITLE = "SUBMARINE ERROR DETECTION FLAGS"
HVAC_TITLE = "HVAC ERROR DETECTION FLAG"


class FlagsForm(BaseForm):
    '''
    The AP's error-detection flags, lit while their reading is past its
    filtering threshold. Whichever group matches the AP's current mode is
    shown - checked every animation tick, like defender_modbus_panel's
    SlidersForm.
    '''

    # None follows the AP's mode; True/False locks the form to the submarine/
    # HVAC flags whatever mode the AP is in (see SubmarineFlagsForm/
    # HVACFlagsForm).
    LOCKED_MODE: bool | None = None

    def __init__(self, master: QWidget, context: Context):
        super().__init__(master, context, process_noun="Flags")

        self._submarine_mode = True if self.LOCKED_MODE is None else self.LOCKED_MODE

        self.add_header(SUBMARINE_TITLE if self._submarine_mode else HVAC_TITLE)

        body = QWidget()
        body.setLayout(QVBoxLayout())
        body.layout().setContentsMargins(0, 0, 0, 0)
        body.layout().setSpacing(4)
        self.grid_layout.addWidget(body, self.current_row, 0, 1, 3)
        self.current_row += 1

        self.dots: dict[str, QLabel] = {}
        if self.LOCKED_MODE in (None, True):
            self.submarine_frame = self._build_group(body, SUBMARINE_FLAGS)
        if self.LOCKED_MODE in (None, False):
            self.hvac_frame = self._build_group(body, HVAC_FLAGS)
        if self.LOCKED_MODE is None:
            self.hvac_frame.hide()

        self.context.animation_manager.add_callback(f"DefenderFlagsForm_{id(self)}", self.refresh)
        self.refresh()

    def _build_group(self, parent: QWidget, defs) -> QWidget:
        frame = QWidget()
        frame.setLayout(QVBoxLayout())
        frame.layout().setContentsMargins(0, 0, 0, 0)
        frame.layout().setSpacing(4)
        parent.layout().addWidget(frame)
        for key, text in defs:
            row = QWidget()
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(0, 0, 0, 0)
            frame.layout().addWidget(row)

            dot = QLabel("●")
            dot.setFont(self.style.get_font("small"))
            self.style.set_tone(dot, "muted")
            row_layout.addWidget(dot)

            label = QLabel(text)
            label.setFont(self.style.get_font("small"))
            row_layout.addWidget(label, 1)
            self.dots[key] = dot
        return frame

    def refresh(self):
        buffer = self.context.buffer
        if self.LOCKED_MODE is None:
            submarine_mode = ap_commands.submarine_mode(buffer)
            if submarine_mode != self._submarine_mode:
                self._submarine_mode = submarine_mode
                self.header.setText(SUBMARINE_TITLE if submarine_mode else HVAC_TITLE)
                self.submarine_frame.setVisible(submarine_mode)
                self.hvac_frame.setVisible(not submarine_mode)

        for key, dot in self.dots.items():
            raised = bool(buffer.defender_status.get(key, False))
            self.style.set_tone(dot, "bad" if raised else "muted")


class SubmarineFlagsForm(FlagsForm):
    '''FlagsForm locked to the submarine flags, whatever mode the AP is in.'''
    LOCKED_MODE = True


class HVACFlagsForm(FlagsForm):
    '''FlagsForm locked to the HVAC flag, whatever mode the AP is in.'''
    LOCKED_MODE = False
