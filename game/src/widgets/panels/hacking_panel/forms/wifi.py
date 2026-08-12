from customtkinter import CTkFrame, CTkLabel, CTkEntry, CTkButton
from .....app_core.context import Context
from .base_form import BaseForm


class WifiForm(BaseForm):
    def __init__(self, master: CTkFrame, context: Context):

        super().__init__(master, context, "wifi", "Connection")
        
        self.add_header("WiFi Connection")

        label1, entry1 = self.add_labeled_entry("Device Name:")
        self.add_attack_button(lambda: context.net.start_wifi(entry1.get()), context.net.stop_wifi, context.net.wifi_is_running)