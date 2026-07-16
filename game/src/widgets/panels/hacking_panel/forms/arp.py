from customtkinter import CTkFrame, CTkLabel, CTkEntry, CTkButton
from .....app_core.context import Context
from .base_form import BaseForm


class ArpForm(BaseForm):
    def __init__(self, master: CTkFrame, context: Context):

        super().__init__(master, context, "arp", "Spoofer")
        
        self.add_header("ARP Spoofing")

        label1, entry1 = self.add_labeled_entry("Target IP:")
        label2, entry2 = self.add_labeled_entry("Host IP:")
        self.add_attack_button(lambda: context.net.start_arp(entry1.get(), entry2.get()), context.net.stop_arp, context.net.arp_is_running)