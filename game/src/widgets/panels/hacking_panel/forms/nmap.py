from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkEntry
from .....app_core import Context
from ...base_form import BaseForm

class NmapForm(BaseForm):
    def __init__(self, master: CTkFrame, context: Context):

        super().__init__(master, context, key="nmap", attack_noun="Network Map")

        self.header = self.add_header()

        status, button = self.add_button("", "Map Network")

        # Bind button
        def do_attack():
            context.states.set("game_progress", "nmap", value=1)

            status.configure(text="Pinging...")
            context.root.update_idletasks()

            context.net.do_nmap()

            status.configure(text="NMap Complete")

        button.configure(command = do_attack)

        # Load status
        if context.states.get("game_progress", "nmap") == 1:
            status.configure(text="NMap Complete")
        else:
            status.configure(text="")
