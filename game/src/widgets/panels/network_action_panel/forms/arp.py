from customtkinter import CTkFrame
from .....app_core import Context
from .....network.hardware import ArpSpoofer
from ...base_form import BaseForm


class ArpForm(BaseForm):
    def __init__(self, master: CTkFrame, context: Context):

        super().__init__(master, context, key="arp")
        self.process = self.get_process(ArpSpoofer)

        self.add_header()

        label1, entry1 = self.add_labeled_entry("Target IP:")
        label2, entry2 = self.add_labeled_entry("Host IP:")
        self.add_attack_button(lambda: self.process.start(entry1.get(), entry2.get()), self.process.stop, self.process.is_running)
