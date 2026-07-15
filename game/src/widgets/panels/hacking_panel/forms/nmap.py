from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkEntry
from .....app_core.context import Context
from .base_form import BaseForm

class NmapForm(BaseForm):
    def __init__(self, master: CTkFrame, context: Context):
        
        super().__init__(master, context)

        self.header = self.add_header("NMapping")

        status = CTkLabel(self, text="", font=self.style.get_font(), anchor="e")
        status.grid(row=1, column=1, sticky="w", pady=self.style.gaptop, padx=self.style.gap)
        self.status = status

        button = CTkButton(self, text="Map Network", font=self.style.get_font(), command=None)
        button.grid(row=1, column=2, sticky="e", pady=self.style.gap, padx=self.style.gap)
        self.button = button

        # Bindings

        def do():
            context.states["game_progress"]["nmap"] = True

            self.status.configure(text="Pinging...")
            context.root.update_idletasks()

            self.context.net.do_nmap()

            self.status.configure(text="NMap Complete")
    
        self.bind(context.net.do_nmap, self.button)
        if context.states["game_progress"]["nmap"]:
            self.status.configure(text="NMap Complete")
        else:
            self.status.configure(text="")

    def bind(self, callback: callable, button: CTkButton, entries: list[CTkEntry] = None):
        '''
        Bind the callback to pressing enter on the form or clicking the button
        '''
        button.configure(command=callback)

        if entries is None:
            return
        def event_callback(event=None):
            callback()
        for entry in entries:
            entry.bind("<Return>", event_callback)