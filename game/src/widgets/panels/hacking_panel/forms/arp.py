from customtkinter import CTkFrame, CTkLabel, CTkEntry, CTkButton
from .....app_core.context import Context


class ArpForm(CTkFrame):
    def __init__(self, master: CTkFrame, context: Context):

        # Widgets
        style = context.style

        super().__init__(master, fg_color=style.color("widget"))
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0)

        header = CTkLabel(self, text="ARP Spoofing", font=style.get_font())
        header.grid(row=0, column=0, columnspan="3", sticky="ew", pady=style.gaptop)
        self.header = header

        label1 = CTkLabel(self, text="Target IP:", font=style.get_font(), anchor="e")
        label1.grid(row=1, column=1, sticky="w", pady=style.gaptop, padx=style.gap)
        self.label1 = label1

        entry1 = CTkEntry(self, font=style.get_font())
        entry1.grid(row=1, column=2, sticky="ew", pady=style.gaptop, padx=style.gap)
        self.entry1 = entry1

        label2 = CTkLabel(self, text="Host IP:", font=style.get_font(), anchor="e")
        label2.grid(row=2, column=1, sticky="w", pady=style.gaptop, padx=style.gap)
        self.label2 = label2

        entry2 = CTkEntry(self, font=style.get_font())
        entry2.grid(row=2, column=2, sticky="ew", pady=style.gaptop, padx=style.gap)
        self.entry2 = entry2

        status = CTkLabel(self, text="", font=style.get_font(), anchor="e")
        status.grid(row=3, column=1, sticky="w", pady=style.gaptop, padx=style.gap)
        self.status = status

        button = CTkButton(self, text="Start ARP Spoof", font=style.get_font(), command=None)
        button.grid(row=3, column=2, sticky="e", pady=style.gap, padx=style.gap)
        self.button = button

        self.inputs = [entry1, entry2]

        # Bindings

        def start():
            context.states["game_progress"]["arp"] = True
            target_ip = str(self.entry1.get())
            host_ip = str(self.entry2.get())
            context.root.update_idletasks()
            context.net.start_arp(target_ip, host_ip)
        def stop():
            context.root.update_idletasks()
            context.net.stop_arp()
        
        start_on = context.net.arp_is_running()
        self.bind_reversible(start, stop, "ARP Spoof", start_on)

        self.load_saved_input(context.states["hack_forms"]["arp"])
        self.bind_input_autosave(context.states["hack_forms"]["arp"])

    def bind_input_autosave(self, save_slots: list[str]):
        for entry, slot_index in zip(self.inputs, range(len(save_slots))):
            def autosave(event=None, e=entry, idx=slot_index):
                save_slots[idx] = e.get()
            entry.bind("<KeyRelease>", autosave)

    def load_saved_input(self, save_slots: list[str]):
        entries = self.inputs
        for i in range(len(entries)):
            entries[i].delete(0, "end")
            entries[i].insert(0, save_slots[i])

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