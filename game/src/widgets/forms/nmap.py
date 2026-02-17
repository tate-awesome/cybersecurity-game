from customtkinter import *
from ..style import Style

class NMap:
    def __init__(self, style: Style, parent):
        frame = CTkFrame(parent)
        frame.pack(side="top", fill="x", expand=False, padx=style.GAP, pady=(style.GAP, 0))
        frame.columnconfigure(0, weight=0)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=0)
        self.frame = frame

        header = CTkLabel(frame, text="NMapping", font=style.get_font())
        header.grid(row=0, column=0, columnspan="3", sticky="ew", pady=(style.GAP,0))
        self.header = header

        status = CTkLabel(frame, text="", font=style.get_font())
        status.grid(row=1, column=1, sticky="w", pady=(style.GAP,0), padx=style.GAP)
        self.status = status

        button = CTkButton(frame, text="Map Network", font=style.get_font(), command=None)
        button.grid(row=1, column=2, sticky="e", pady=style.GAP, padx=style.GAP)
        self.button = button

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