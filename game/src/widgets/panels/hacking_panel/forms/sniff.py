from customtkinter import CTkFrame, CTkLabel, CTkButton
from .....app_core.context import Context
from .base_form import BaseForm

class SniffForm(BaseForm):
    def __init__(self, master: CTkFrame, context: Context):

        super().__init__(master, context, "sniff", "Sniffer")

        self.header = self.add_header("Packet Sniffing")

        self.add_attack_button(self.context.net.start_sniff, self.context.net.stop_sniff, self.context.net.sniff_is_running)