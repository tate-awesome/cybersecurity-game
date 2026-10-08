from PySide6.QtWidgets import QWidget
from .....app_core import Context
from .....network.hardware import ap_commands
from ...base_form import BaseForm


class KalmanForm(BaseForm):
    '''
    Toggles the Kalman filter for whichever mode the AP is in - submarine's
    (DefenderV0's middle-pane toggle) or HVAC's (HVACView's), which the AP
    keeps separately. Goes through the shared AP poller via
    context.buffer.defender_status - see EncryptionForm. Hidden in every
    shipped config (its toggle lives in defender_flag_panel), but kept.
    '''

    def __init__(self, master: QWidget, context: Context):
        super().__init__(master, context, key="kalman")

        self.add_header()

        self.add_process_row(
            lambda: ap_commands.set_kalman(self.context.buffer, True),
            lambda: ap_commands.set_kalman(self.context.buffer, False),
            lambda: ap_commands.kalman_enabled(self.context.buffer),
        )

