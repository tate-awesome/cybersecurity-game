from customtkinter import CTkFrame
from .....app_core import Context
from .....network.hardware import Wifi
from ...base_form import BaseForm


class WifiForm(BaseForm):
    def __init__(self, master: CTkFrame, context: Context):

        super().__init__(master, context, key="wifi")
        # Stopped last on page-exit cleanup (ProcessManager.abort_all): other
        # processes' teardown (e.g. ArpSpoofer restoring ARP tables) needs
        # working networking, so switching networks back must happen after.
        self.process = self.get_process(Wifi, tags=["stop_last"])

        self.add_header()

        label1, entry1 = self.add_labeled_entry("Device Name:")
        self.add_attack_button(lambda: self.process.start(entry1.get()), self.process.stop, self.process.is_running)
