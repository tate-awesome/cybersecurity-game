from PySide6.QtWidgets import QWidget
from .....app_core import Context
from .....network.hardware import ap_commands
from ...base_form import BaseForm


class APTunnelForm(BaseForm):
    '''
    Toggles routing device traffic purely through the AP (no directly
    hackable TCP/Modbus). Goes through the shared AP poller via
    context.buffer.defender_status - see EncryptionForm.
    '''

    def __init__(self, master: QWidget, context: Context):
        super().__init__(master, context, key="ap_tunnel")

        self.add_header()

        self.add_process_row(
            lambda: ap_commands.set_ap_tunnel(self.context.buffer, True),
            lambda: ap_commands.set_ap_tunnel(self.context.buffer, False),
            lambda: ap_commands.ap_tunnel_enabled(self.context.buffer),
        )
