from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkEntry
from .....app_core.context import Context

class NmapForm(CTkFrame):
    def __init__(self, master: CTkFrame, context: Context):
        
        # Widgets
        style = context.style

        super().__init__(master, fg_color=style.color("widget"))
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0)

        header = CTkLabel(self, text="NMapping", font=style.get_font())
        header.grid(row=0, column=0, columnspan="3", sticky="ew", pady=style.gaptop)
        self.header = header

        status = CTkLabel(self, text="", font=style.get_font(), anchor="e")
        status.grid(row=1, column=1, sticky="w", pady=style.gaptop, padx=style.gap)
        self.status = status

        button = CTkButton(self, text="Map Network", font=style.get_font(), command=None)
        button.grid(row=1, column=2, sticky="e", pady=style.gap, padx=style.gap)
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