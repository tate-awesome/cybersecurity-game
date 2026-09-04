import threading
import requests
from customtkinter import CTkFrame
from .....app_core import Context
from .....network.hardware import APPoller
from ...base_form import BaseForm


class EncryptionForm(BaseForm):
    '''
    Toggles AP-level encryption. Shares the AP Connect form's poller
    process (same process_manager key, "ap_connect") instead of starting
    its own - encryption is posted through that same connection, not a
    separate one. Not itself a Process/get_process() case: there's no
    background thread of its own to start/stop, only a one-shot POST whose
    result already lives in context.buffer.defender_status.
    '''

    def __init__(self, master: CTkFrame, context: Context):
        super().__init__(master, context, key="encryption")

        self.process = self.context.process_manager.get_process("ap_connect")
        if self.process is None:
            self.process = APPoller(self.context.buffer, self.context)
            self.context.process_manager.add_process("ap_connect", self.process)

        self.add_header()

        label, entry = self.add_labeled_entry("Key:")
        self.key_entry = entry

        def start_encryption():
            key = self.key_entry.get().strip()
            if not key:
                self.context.buffer.put("encryption", "Refused to enable encryption with an empty key")
                return
            if not key.isascii():
                self.context.buffer.put("encryption", "Refused to enable encryption: key must be ASCII")
                return
            self._post_encryption(True, key)

        def stop_encryption():
            self._post_encryption(False, self.key_entry.get().strip())

        self.add_attack_button(
            start_encryption, stop_encryption,
            lambda: bool(self.context.buffer.defender_status.get("encryption_status", False)),
        )

        self.context.animation_manager.add_callback(f"EncryptionForm_{id(self)}", self._refresh_status)

    def _post_encryption(self, enabled: bool, key: str):
        self.context.buffer.put("encryption", "Enabling encryption..." if enabled else "Disabling encryption...")

        def _request():
            try:
                resp = requests.post(
                    f"{self.process.url}/set_encryption",
                    json={"encryption_status": enabled, "encryption_key": key},
                    timeout=3,
                )
                if resp.ok:
                    self.context.buffer.defender_status.put("encryption_status", enabled)
                    self.context.buffer.put("encryption", "Encryption is on" if enabled else "Encryption is off")
                else:
                    self.context.buffer.put("encryption", f"AP rejected encryption request (HTTP {resp.status_code})")
            except Exception as e:
                self.context.buffer.put("encryption", f"Failed to reach AP: {e}")

        threading.Thread(target=_request, daemon=True).start()

    def _refresh_status(self):
        if self.context.buffer.defender_status.get("encryption_status", False):
            self.configure_on()
        else:
            self.configure_off()
