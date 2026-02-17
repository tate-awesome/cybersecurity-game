from customtkinter import *
from ..style import Style

class Sniff:
    def __init__(self, style: Style, parent, options: list[str]):
        frame = CTkFrame(parent)
        frame.pack(side="top", fill="x", expand=False, padx=style.GAP, pady=(style.GAP, 0))
        frame.columnconfigure(0, weight=0)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=0)
        self.frame = frame

        header = CTkLabel(frame, text="Traffic Sniffing", font=style.get_font())
        header.grid(row=0, column=0, columnspan="3", sticky="ew", pady=(style.GAP,0))
        self.header = header

        label = CTkLabel(frame, text="Packet Handler:", font=style.get_font())
        label.grid(row=1, column=1, sticky="w", pady=(style.GAP,0), padx=style.GAP)
        self.label = label

        option = CTkOptionMenu(frame, font=style.get_font(), values=options)
        option.grid(row=1, column=2, sticky="e", pady=(style.GAP,0), padx=style.GAP)
        self.option = option

        button = CTkButton(frame, text="Start sniffing", font=style.get_font(), command=None)
        button.grid(row=2, column=2, sticky="e", pady=style.GAP, padx=style.GAP)
        self.button = button

        self.options = [option]

    def bind_options_autosave(self, save_slots: list[str], max_len=6):
        """
        Binds a callback to all CTkOptionMenus that saves the selected option to the
        corresponding save slot whenever an option is selected.
        Automatically shortens the displayed value if it's longer than max_len.
        """
        def shorten(text: str, max_len=max_len) -> str:
            return text if len(text) <= max_len else text[:max_len] + "…"

        for option, idx in zip(self.options, range(len(save_slots))):
            def autosave(selected_value, i=idx, opt=option):
                # Save the full value
                save_slots[i] = selected_value
                # Shorten the displayed text if needed
                opt.set(shorten(selected_value))
            
            option.configure(command=autosave)

    def load_saved_options(self, save_slots: list[str]):
        """
        Sets the selected option of each CTkOptionMenu to the corresponding string
        from the save slot.
        """
        for option, value in zip(self.options, save_slots):
            if value in option._values:  # make sure it's a valid option
                option.set(value)