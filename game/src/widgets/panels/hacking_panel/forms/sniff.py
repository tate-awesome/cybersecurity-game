from customtkinter import CTkFrame, CTkLabel, CTkButton
from .....app_core.context import Context
from .base_form import BaseForm

class SniffForm(BaseForm):
    def __init__(self, master: CTkFrame, context: Context):

        super().__init__(master, context)

        self.header = self.add_header("Packet Sniffing")

        status = CTkLabel(self, text="", font=self.style.get_font(), anchor="e")
        status.grid(row=3, column=1, sticky="w", pady=self.style.gaptop, padx=self.style.gap)
        self.status = status

        button = CTkButton(self, text="Start sniffing", font=self.style.get_font(), command=None)
        button.grid(row=3, column=2, sticky="ew", pady=self.style.gap, padx=self.style.gap)
        self.button = button

        # self.inputs = [box1, box2]

        # Bindings

        def start():
            context.states["game_progress"]["sniff"] = True
            context.root.update_idletasks()
            context.net.start_sniff()

        def stop():
            context.root.update_idletasks()
            context.net.stop_sniff()

        start_on = context.net.sniff_is_running()
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