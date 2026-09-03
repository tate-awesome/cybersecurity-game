from customtkinter import CTkFrame
from .....app_core import Context
from .....network.hardware import Sniffer
from ...base_form import BaseForm

class SniffForm(BaseForm):
    def __init__(self, master: CTkFrame, context: Context):

        super().__init__(master, context, key="sniff")
        self.process = self.get_process(Sniffer)

        self.header = self.add_header()

        self.add_attack_button(self.process.start, self.process.stop, self.process.is_running)
