from customtkinter import *
from ..style import Style

class Sniff:
    def __init__(self, style: Style, parent):
        frame = CTkFrame(parent)
        frame.pack(side="top", fill="x", expand=False, padx=style.GAP, pady=(style.GAP, 0))
        frame.columnconfigure(0, weight=0)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=0)
        self.frame = frame

        header = CTkLabel(frame, text="Packet Sniffing", font=style.get_font())
        header.grid(row=0, column=0, columnspan="3", sticky="ew", pady=(style.GAP,0))
        self.header = header

        label1 = CTkLabel(frame, text="Print to GUI:", font=style.get_font())
        label1.grid(row=1, column=1, sticky="w", pady=(style.GAP,0), padx=style.GAP)
        self.label1 = label1

        box1 = CTkCheckBox(frame, text="")
        box1.grid(row=1, column=2, sticky="w", pady=(style.GAP,0), padx=style.GAP)
        self.box1 = box1

        label2 = CTkLabel(frame, text="Print to Console:", font=style.get_font())
        label2.grid(row=2, column=1, sticky="w", pady=(style.GAP,0), padx=style.GAP)
        self.label2 = label2

        box2 = CTkCheckBox(frame, text="")
        box2.grid(row=2, column=2, sticky="w", pady=(style.GAP,0), padx=style.GAP)
        self.box2 = box2

        status = CTkLabel(frame, text="", font=style.get_font())
        status.grid(row=3, column=1, sticky="w", pady=(style.GAP,0), padx=style.GAP)
        self.status = status

        button = CTkButton(frame, text="Start sniffing", font=style.get_font(), command=None)
        button.grid(row=3, column=2, sticky="e", pady=style.GAP, padx=style.GAP)
        self.button = button

        self.inputs = [box1, box2]

    def bind_input_autosave(self, save_slots: list[str]):
        """
        Binds a callback to self.boxes (list of CTkCheckBoxes) that saves the
        selected state to the corresponding save slot whenever toggled.
        """
        for box, idx in zip(self.inputs, range(len(save_slots))):
            def autosave(i=idx, b=box):
                # Save as string to match save_slots type
                save_slots[i] = str(b.get())

            box.configure(command=autosave)


    def load_saved_input(self, save_slots: list[str]):
        """
        Sets the selected state of each CTkCheckBox from the corresponding save slot.
        """
        for box, value in zip(self.inputs, save_slots):
            if value == "1":
                box.select()
            else:
                box.deselect()


    def bind_reversible(self, start_func: callable, stop_func: callable, func_name: str, start_on):
        button = self.button
        entries = self.inputs
        status = self.status

        def configure_on():
            button.configure(command=stop, text=f"Stop {func_name}")
            status.configure(text=f"{func_name} is on")
        def configure_off():
            button.configure(command=start, text=f"Start {func_name}")
            status.configure(text=f"{func_name} is off")
        
        def stop():
            button.configure(text=f"Stopping {func_name}...")
            stop_func()
            configure_off()

        def start():
            button.configure(text=f"Starting {func_name}...")
            start_func()
            configure_on()

        if start_on:
            configure_on()
        else:
            configure_off()

        if entries is None:
            return
        def event_callback(event=None):
            start()
        for entry in entries:
            entry.bind("<Return>", event_callback)