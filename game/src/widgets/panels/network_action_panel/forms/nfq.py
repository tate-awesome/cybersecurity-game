from customtkinter import CTkFrame
from .....app_core import Context
from ...base_form import BaseForm

class NFQForm(BaseForm):
    def __init__(self, master: CTkFrame, context: Context):

        super().__init__(master, context, key="nfq")

        self.header = self.add_header()

        self.add_attack_button(self.context.net.start_nfq, self.context.net.stop_nfq, self.context.net.nfq_is_running)