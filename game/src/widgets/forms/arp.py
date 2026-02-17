from customtkinter import *
from ..style import Style


class ARP:
    def __init__(self, style: Style, parent):
        frame = CTkFrame(parent)
        frame.pack(side="top", fill="x", expand=False, padx=style.GAP, pady=(style.GAP, 0))
        frame.columnconfigure(0, weight=0)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=0)
        self.frame = frame

        header = CTkLabel(frame, text="ARP Spoofing", font=style.get_font())
        header.grid(row=0, column=0, columnspan="3", sticky="ew", pady=(style.GAP,0))
        self.header = header

        label1 = CTkLabel(frame, text="Target IP:", font=style.get_font())
        label1.grid(row=1, column=1, sticky="w", pady=(style.GAP,0), padx=style.GAP)
        self.label1 = label1

        entry1 = CTkEntry(frame, font=style.get_font())
        entry1.grid(row=1, column=2, sticky="e", pady=(style.GAP,0), padx=style.GAP)
        self.entry1 = entry1

        label2 = CTkLabel(frame, text="Host IP:", font=style.get_font())
        label2.grid(row=2, column=1, sticky="w", pady=(style.GAP,0), padx=style.GAP)
        self.label2 = label2

        entry2 = CTkEntry(frame, font=style.get_font())
        entry2.grid(row=2, column=2, sticky="e", pady=(style.GAP,0), padx=style.GAP)
        self.entry2 = entry2

        status = CTkLabel(frame, text="", font=style.get_font())
        status.grid(row=3, column=1, sticky="w", pady=(style.GAP,0), padx=style.GAP)
        self.status = status

        button = CTkButton(frame, text="Start ARP Spoof", font=style.get_font(), command=None)
        button.grid(row=3, column=2, sticky="e", pady=style.GAP, padx=style.GAP)
        self.button = button

        self.entries = [entry1, entry2]

    def bind_entries_autosave(self, save_slots: list[str]):
        for entry, slot_index in zip(self.entries, range(len(save_slots))):
            def autosave(event=None, e=entry, idx=slot_index):
                save_slots[idx] = e.get()
                print(e.get())
            entry.bind("<KeyRelease>", autosave)

    def load_saved_entries(self, save_slots: list[str]):
        entries = self.entries
        for i in range(len(entries)):
            entries[i].delete(0, "end")
            entries[i].insert(0, save_slots[i])

    def bind_reversible(self, start_func: callable, stop_func: callable, func_name: str, start_on):
        button = self.button
        entries = self.entries
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