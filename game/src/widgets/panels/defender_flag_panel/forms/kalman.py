from PySide6.QtWidgets import QLabel, QPushButton, QWidget
from .....app_core import Context
from .....network.hardware import ap_commands
from ...base_form import BaseForm


class KalmanToggleForm(BaseForm):
    '''
    The Kalman filter's status and an on/off toggle for it - for whichever
    mode the AP is in (submarine's or HVAC's - the AP keeps them
    separately), like the original page's middle pane and HVACView
    respectively.
    '''

    # None follows the AP's mode; True/False locks the form to the submarine/
    # HVAC Kalman filter whatever mode the AP is in (see
    # SubmarineKalmanToggleForm/HVACKalmanToggleForm).
    LOCKED_MODE: bool | None = None
    TITLE = "KALMAN FILTER"

    def __init__(self, master: QWidget, context: Context):
        super().__init__(master, context, process_noun="Kalman Filter")

        self.add_header(self.TITLE)

        self.kalman_label = QLabel("")
        self.kalman_label.setFont(self.style.get_font())
        self.grid_layout.addWidget(self.kalman_label, self.current_row, 0, 1, 3)
        self.current_row += 1

        button = QPushButton("Toggle Kalman Filter")
        button.setFont(self.style.get_font())
        button.clicked.connect(lambda checked=False: self._set(not self._enabled()))
        self.grid_layout.addWidget(button, self.current_row, 0, 1, 3)
        self.current_row += 1

        self.context.animation_manager.add_callback(f"DefenderKalmanToggleForm_{id(self)}", self.refresh)
        self.refresh()

    def _enabled(self) -> bool:
        buffer = self.context.buffer
        if self.LOCKED_MODE is None:
            return ap_commands.kalman_enabled(buffer)
        if self.LOCKED_MODE:
            return ap_commands.submarine_kalman_enabled(buffer)
        return ap_commands.hvac_kalman_enabled(buffer)

    def _set(self, enabled: bool):
        buffer = self.context.buffer
        if self.LOCKED_MODE is None:
            ap_commands.set_kalman(buffer, enabled)
        elif self.LOCKED_MODE:
            ap_commands.set_submarine_kalman(buffer, enabled)
        else:
            ap_commands.set_hvac_kalman(buffer, enabled)

    def refresh(self):
        on = self._enabled()
        self.kalman_label.setText("Status: ON" if on else "Status: OFF")
        self.style.set_tone(self.kalman_label, "good" if on else "muted")


class SubmarineKalmanToggleForm(KalmanToggleForm):
    '''KalmanToggleForm locked to the submarine Kalman filter, whatever mode the AP is in.'''
    LOCKED_MODE = True
    TITLE = "SUBMARINE KALMAN FILTER"


class HVACKalmanToggleForm(KalmanToggleForm):
    '''KalmanToggleForm locked to the HVAC Kalman filter, whatever mode the AP is in.'''
    LOCKED_MODE = False
    TITLE = "HVAC KALMAN FILTER"
