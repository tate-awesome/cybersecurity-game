from PySide6.QtWidgets import QWidget
from .....app_core import Context
from .....network.hardware import Denier
from ...base_form import BaseForm


class DosForm(BaseForm):
    def __init__(self, master: QWidget, context: Context):

        super().__init__(master, context, key="dos")
        self.process = self.get_process(Denier)

        self.add_header()

        label1, entry1 = self.add_labeled_entry("Target IP:Port")
        label2, entry2 = self.add_labeled_entry("Target IP:Port")
        self.add_process_row(lambda: self.process.start([entry1.get(), entry2.get()]), self.process.stop, self.process.is_running)
