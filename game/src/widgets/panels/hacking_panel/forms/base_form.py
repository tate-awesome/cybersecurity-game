from customtkinter import CTkFrame, CTkEntry, CTkLabel, CTkButton
from abc import ABC, abstractmethod
from typing import Callable
from .....app_core.context import Context

class BaseForm(ABC, CTkFrame):
    def __init__(self, master: CTkFrame, context: Context, key: str, attack_noun: str):
        '''
        attack_noun is used like "start sniffer" "start DoS attack" "stopping MITM attack" "ARP Spoofer is running" "MITM attack is on"
        '''

        self.style = context.style
        self.context = context
        self.key = key
        self.attack_noun = attack_noun

        super().__init__(master, fg_color=self.style.color("widget"))

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0)

        self.current_row = 0
        self.entry_index = 0
        self.entries = []
        self.start_attack = lambda: None
        self.stop_attack = lambda: None


    def add_header(self, text: str):
        self.header = CTkLabel(self, text=text, font=self.style.get_font())
        self.header.grid(row=self.current_row, column=0, columnspan="10", sticky="ew", pady=self.style.gaptop)
        self.current_row += 1

    def add_labeled_entry(self, label: str):
        '''
        Adds a labeled entry for the curent row in the form.
        This entry has autosave and auto-loading for its text input.
        '''

        # Create widgets
        label = CTkLabel(self, text=label, font=self.style.get_font(), anchor="e")
        label.grid(row=self.current_row, column=1, sticky="w", pady=self.style.gaptop, padx=self.style.gap)

        entry = CTkEntry(self, font=self.style.get_font())
        entry.grid(row=self.current_row, column=2, sticky="ew", pady=self.style.gaptop, padx=self.style.gap)
        self.entries.append(entry)

        # Bind autosave
        save_slots = self.context.states["hack_forms"][self.key]
        def autosave(event=None, e=entry, idx=self.entry_index):
            save_slots[idx] = e.get()
        entry.bind("<KeyRelease>", autosave)

        # Load saved entry input
        entry.delete(0, "end")
        entry.insert(0, save_slots[self.entry_index])

        # Update current index
        self.current_row += 1
        self.entry_index += 1

        return label, entry

    def add_attack_button(self, start_attack_func: Callable, stop_attack_func: Callable, attack_status_func: Callable[None, bool], default_status: str = ""):

        # Create widgets
        self.attack_status = CTkLabel(self, text=default_status, font=self.style.get_font(), anchor="e")
        self.attack_status.grid(row=self.current_row, column=1, sticky="w", pady=self.style.gaptop, padx=self.style.gap)

        self.attack_button = CTkButton(self, text="", font=self.style.get_font(), command=None)
        self.attack_button.grid(row=self.current_row, column=2, sticky="ew", pady=self.style.gap, padx=self.style.gap)

        # Set function definitions
        self.start_attack = start_attack_func
        self.stop_attack = stop_attack_func

        # Configure attack state
        if attack_status_func():
            self.configure_on()
        else:
            self.configure_off()
        
        # Bind <Return>
        def return_handler(event=None):
            self.click_start()
        for entry in self.entries:
            entry.bind("<Return>", return_handler)
        
        # Update current index
        self.current_row += 1

    def click_start(self):
        self.context.states["game_progress"][self.key] = True
        self.attack_button.configure(text=f"Starting {self.attack_noun}...")
        self.start_attack()
        self.context.root.update_idletasks()
        self.configure_on()
    
    def configure_on(self):
        self.attack_button.configure(command=self.click_stop, text=f"Stop {self.attack_noun}")
        self.attack_status.configure(text=f"{self.attack_noun} is on")

    def click_stop(self):
        self.attack_button.configure(text=f"Stopping {self.attack_noun}...")
        self.stop_attack()
        self.context.root.update_idletasks()
        self.configure_off()
    
    def configure_off(self):
        self.attack_button.configure(command=self.click_start, text=f"Start {self.attack_noun}")
        self.attack_status.configure(text=f"{self.attack_noun} is off")

    def add_button(self, default_status: str = "", button_text: str= "", button_func: Callable = None):
        # Create widgets
        status = CTkLabel(self, text=default_status, font=self.style.get_font(), anchor="e")
        status.grid(row=self.current_row, column=1, sticky="w", pady=self.style.gaptop, padx=self.style.gap)

        button = CTkButton(self, text=button_text, font=self.style.get_font(), command=button_func)
        button.grid(row=self.current_row, column=2, sticky="ew", pady=self.style.gap, padx=self.style.gap)

        # Update current index
        self.current_row += 1

        return status, button