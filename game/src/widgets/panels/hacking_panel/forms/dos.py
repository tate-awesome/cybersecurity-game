from customtkinter import CTkFrame, CTkLabel, CTkEntry, CTkButton
from .....app_core.context import Context
from .base_form import BaseForm


class DosForm(BaseForm):
    def __init__(self, master: CTkFrame, context: Context):

        super().__init__(master, context, "dos", "DoS Attack")

        self.add_header("Denial of Service")

        label1, entry1 = self.add_labeled_entry("Target IP:Port")
        label2, entry2 = self.add_labeled_entry("Target IP:Port")
        self.add_attack_button(lambda: context.net.start_dos(entry1.get(), entry2.get()), context.net.stop_dos, context.net.dos_is_running)