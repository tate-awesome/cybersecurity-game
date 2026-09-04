import threading
import requests
from customtkinter import CTkFrame
from .....app_core import Context
from .....network.hardware import APPoller
from ...base_form import BaseForm


class APTunnelForm(BaseForm):
    '''
    Toggles routing device traffic purely through the AP (no directly
    hackable TCP/Modbus). Shares the AP Connect form's poller process - see
    EncryptionForm for why this isn't a Process/get_process() case.
    '''

    def __init__(self, master: CTkFrame, context: Context):
        super().__init__(master, context, key="ap_tunnel")

        self.process = self.context.process_manager.get_process("ap_connect")
        if self.process is None:
            self.process = APPoller(self.context.buffer, self.context)
            self.context.process_manager.add_process("ap_connect", self.process)

        self.add_header()

        self.add_attack_button(
            lambda: self._post_ap_communication(True),
            lambda: self._post_ap_communication(False),
            lambda: bool(self.context.buffer.defender_status.get("ap_communication", False)),
        )

        self.context.animation_manager.add_callback(f"APTunnelForm_{id(self)}", self._refresh_status)

    def _post_ap_communication(self, enabled: bool):
        self.context.buffer.put("ap_tunnel", "Enabling AP tunnel..." if enabled else "Disabling AP tunnel...")

        def _request():
            try:
                resp = requests.post(
                    f"{self.process.url}/set_AP_communication",
                    json={"AP_communication": enabled},
                    timeout=3,
                )
                if resp.ok:
                    self.context.buffer.defender_status.put("ap_communication", enabled)
                    self.context.buffer.put("ap_tunnel", "AP Tunnel is on" if enabled else "AP Tunnel is off")
                else:
                    self.context.buffer.put("ap_tunnel", f"AP rejected tunnel request (HTTP {resp.status_code})")
            except Exception as e:
                self.context.buffer.put("ap_tunnel", f"Failed to reach AP: {e}")

        threading.Thread(target=_request, daemon=True).start()

    def _refresh_status(self):
        if self.context.buffer.defender_status.get("ap_communication", False):
            self.configure_on()
        else:
            self.configure_off()
