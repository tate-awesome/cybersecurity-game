from PySide6.QtWidgets import QWidget
from .....app_core import Context
from .....network.hardware import ArpSpoofer
from ...base_form import BaseForm


class ArpForm(BaseForm):
    def __init__(self, master: QWidget, context: Context):

        super().__init__(master, context, key="arp", flat=True)
        self.process = self.get_process(ArpSpoofer)

        self.add_header()

        _, entry1 = self.add_labeled_entry("Target IP:")
        _, entry2 = self.add_labeled_entry("Host IP:")
        # Locked inputs for the run; the Starting button stays clickable so the
        # wait for the victims' MACs can be cancelled.
        self.add_process_row(lambda: self.process.start(entry1.text(), entry2.text()), self.process.stop,
                             self.process.is_running, lock_entries=True)
