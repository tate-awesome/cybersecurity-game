from customtkinter import CTkFrame
from .....app_core import Context
from .....network.hardware import NMapper
from ...base_form import BaseForm

class NmapForm(BaseForm):
    def __init__(self, master: CTkFrame, context: Context):

        super().__init__(master, context, key="nmap", process_noun="Network Map")
        self.process = self.get_process(NMapper)

        self.add_header()

        self.add_process_row(self.process.start, self.process.stop, self.process.is_running)
