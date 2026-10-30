from PySide6.QtWidgets import QWidget
from .....app_core import Context
from .....network.hardware import ap_commands
from .... import modal
from ...base_form import BaseForm


class EncryptionForm(BaseForm):
    '''
    Toggles AP-level encryption, like DefenderV0's encryption block: the key
    must be non-empty ASCII to turn it on, the key entry is locked while
    it's on, and turning it off clears the key. Not a Process of its own -
    the command goes out through the shared AP poller via
    context.buffer.defender_status (see ap_commands), and the button reads
    its state back from there.
    '''

    def __init__(self, master: QWidget, context: Context):
        super().__init__(master, context, key="encryption", flat=True)

        self.add_header()

        label, entry = self.add_labeled_entry("Key:")
        self.key_entry = entry

        def start_encryption():
            key = self.key_entry.text().strip()
            if not key:
                modal.message(self, self.context, "Please enter an encryption key before enabling encryption.")
                return
            if not key.isascii():
                modal.message(self, self.context, "Encryption key must be ASCII.")
                return
            ap_commands.set_encryption(self.context.buffer, True, key)

        def stop_encryption():
            ap_commands.set_encryption(self.context.buffer, False, self.key_entry.text().strip())
            self.key_entry.clear()
            self.context.states.get("network_action_form_inputs", self.key)[0] = ""

        # The key is locked while encryption is on (not stopped) - see lock_entries
        self.add_process_row(start_encryption, stop_encryption,
                             lambda: ap_commands.encryption_enabled(self.context.buffer), lock_entries=True)
