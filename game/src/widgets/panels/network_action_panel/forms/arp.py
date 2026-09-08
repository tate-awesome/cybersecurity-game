from PySide6.QtWidgets import QWidget, QLineEdit
from .....app_core import Context
from .....network.hardware import ArpSpoofer
from ...base_form import BaseForm


class ArpForm(BaseForm):
    def __init__(self, master: QWidget, context: Context):

        super().__init__(master, context, key="arp")
        self.process = self.get_process(ArpSpoofer)

        self.add_header()

        _, entry1 = self.add_labeled_entry("Target IP:")
        _, entry2 = self.add_labeled_entry("Host IP:")
        self.add_process_row(lambda: self.process.start(entry1.text(), entry2.text()), self.process.stop, self.process.is_running)
