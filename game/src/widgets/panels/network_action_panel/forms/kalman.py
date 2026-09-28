from PySide6.QtWidgets import QWidget
from .....app_core import Context
from .....network.hardware import ap_commands
from ...base_form import BaseForm


class KalmanForm(BaseForm):
    '''
    Toggles the submarine Kalman filter (DefenderV0's middle-pane toggle).
    Greyed out while the AP is in HVAC mode rather than switching to HVAC's
    separate filter, so its status always means the same thing. Goes
    through the shared AP poller via context.buffer.defender_status - see
    EncryptionForm.
    '''

    abortable = False

    def __init__(self, master: QWidget, context: Context):
        super().__init__(master, context, key="kalman")

        self.add_header()

        self.add_process_row(
            lambda: ap_commands.set_kalman(self.context.buffer, True),
            lambda: ap_commands.set_kalman(self.context.buffer, False),
            lambda: ap_commands.kalman_enabled(self.context.buffer),
        )

        self.context.animation_manager.add_callback(f"KalmanForm_{id(self)}", self._refresh_mode)
        self._refresh_mode()

    def _refresh_mode(self):
        enabled = ap_commands.submarine_mode(self.context.buffer)
        if self.isEnabled() != enabled:
            self.setEnabled(enabled)
