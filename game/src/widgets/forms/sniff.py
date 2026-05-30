from customtkinter import *
from ..style import Style

class Sniff:
    def __init__(self, style: Style, parent, context, start_sniff, sniff_is_running, stop_sniff):

        # Widgets

        frame = CTkFrame(parent, fg_color=style.color("widget"))
        frame.pack(side="top", fill="x", expand=False, padx=style.nogap, pady=style.gaptop)
        frame.columnconfigure(0, weight=0)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=0)
        self.frame = frame

        header = CTkLabel(frame, text="Packet Sniffing", font=style.get_font())
        header.grid(row=0, column=0, columnspan="3", sticky="ew", pady=style.gaptop)
        self.header = header

        # label1 = CTkLabel(frame, text="Print to GUI:", font=style.get_font(), anchor="e")
        # label1.grid(row=1, column=1, sticky="w", pady=style.gaptop, padx=style.gap)
        # self.label1 = label1

        # box1 = CTkCheckBox(frame, text="")
        # box1.grid(row=1, column=2, sticky="ew", pady=style.gaptop, padx=style.gap)
        # self.box1 = box1

        # label2 = CTkLabel(frame, text="Print to Console:", font=style.get_font(), anchor="e")
        # label2.grid(row=2, column=1, sticky="w", pady=style.gaptop, padx=style.gap)
        # self.label2 = label2

        # box2 = CTkCheckBox(frame, text="")
        # box2.grid(row=2, column=2, sticky="ew", pady=style.gaptop, padx=style.gap)
        # self.box2 = box2

        status = CTkLabel(frame, text="", font=style.get_font(), anchor="e")
        status.grid(row=3, column=1, sticky="w", pady=style.gaptop, padx=style.gap)
        self.status = status

        button = CTkButton(frame, text="Start sniffing", font=style.get_font(), command=None)
        button.grid(row=3, column=2, sticky="ew", pady=style.gap, padx=style.gap)
        self.button = button

        # self.inputs = [box1, box2]

        # Bindings

        def sniff_handler(mpkt):
            if sniff.box1.get() == 1:
                mpkt.wireshark_line(True)
            if sniff.box2.get() == 1:
                mpkt.show()

        def start():
            context.states["game_progress"]["sniff"] = True
            context.root.update_idletasks()
            # net.buffer.add_callback("sniff_handler", sniff_handler)
            start_sniff()

        def stop():
            context.root.update_idletasks()
            stop_sniff()
            # net.buffer.remove_callback("sniff_handler")

        start_on = sniff_is_running()
        self.bind_reversible(start, stop, "Sniffing", start_on)

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