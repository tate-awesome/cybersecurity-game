from PySide6.QtWidgets import QWidget
from .....app_core import Context
from .....network.hardware import Sniffer
from ...base_form import BaseForm

class SniffForm(BaseForm):
    def __init__(self, master: QWidget, context: Context):

        super().__init__(master, context, key="sniff", flat=True)
        # Runs in the elevated helper when that's on (see network/helper), else in-process
        self.process = self.get_process(Sniffer, capability="sniff")

        self.header = self.add_header()

        self.add_process_row(self.process.start, self.process.stop, self.process.is_running)
