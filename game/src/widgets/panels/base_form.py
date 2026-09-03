from customtkinter import CTkFrame, CTkEntry, CTkLabel, CTkButton
from abc import ABC, abstractmethod
from typing import Callable
from ...app_core import Context
from ...network.process import Process

class BaseForm(ABC, CTkFrame):
    '''
    Shared by network_action_panel's and modbus_panel's attack/action forms. The two
    differ only in how they source display text and lay out the attack
    button row:
      - network_action_panel forms pass a `key` and look their text up via
        context.labels (i18n), and track game_progress on start.
      - modbus_panel forms pass no `key` (defaults to None) and build their
        text directly from `attack_noun` (not translated).
    Both branches preserve their original grid layout and call-ordering
    exactly (including update_idletasks() firing before vs. after the
    start/stop function in the two hierarchies) - this file unifies the
    duplicated structure, not the small behavioral differences between them.
    '''
    def __init__(self, master: CTkFrame, context: Context, attack_noun: str = "Attack", key: str | None = None):
        '''
        attack_noun is used like "start sniffer" "start DoS attack" "stopping NFQ" "ARP Spoofer is running" "NFQ is on"
        key, if given, selects the "network_action_forms"/"network_action_panels" i18n text
        for this form instead of building plain text from attack_noun.
        '''

        self.style = context.style
        self.context = context
        self.key = key
        self.attack_noun = attack_noun
        self.has_attack_button = False

        super().__init__(master, fg_color=self.style.color("widget"))

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0)

        if self.key is not None:
            self.status_on_text = self.context.labels.get("network_action_forms", f"{self.key}_on")
            self.status_off_text = self.context.labels.get("network_action_forms", f"{self.key}_off")
            self.start_attack_text = self.context.labels.get("network_action_forms", f"{self.key}_start")
            self.starting_attack_text = self.context.labels.get("network_action_forms", f"{self.key}_starting")
            self.stop_attack_text = self.context.labels.get("network_action_forms", f"{self.key}_stop")
            self.stopping_attack_text = self.context.labels.get("network_action_forms", f"{self.key}_stopping")
        else:
            self.status_on_text = f"{self.attack_noun} is on"
            self.status_off_text = f"{self.attack_noun} is off"
            self.start_attack_text = f"Start {self.attack_noun}"
            self.starting_attack_text = f"Starting {self.attack_noun}..."
            self.stop_attack_text = f"Stop {self.attack_noun}"
            self.stopping_attack_text = f"Stopping {self.attack_noun}..."

        self.current_row = 0
        self.entry_index = 0
        self.entries = []
        self.start_attack = lambda: None
        self.stop_attack = lambda: None

    def get_process(self, process_class: type[Process], *args, tags: list[str] | None = None, **kwargs) -> Process:
        '''
        Retrieves this form's process from context.process_manager, creating
        and registering it under `key` on first visit. Since forms are
        recreated on every refresh, this is how a form regains control of a
        still-running process instead of losing track of it.
        Requires `key` to have been set - it doubles as the process's name.
        tags is passed through to ProcessManager.add_process on first visit
        (e.g. "stop_last") - ignored on later visits, since the process is
        already registered by then.
        '''
        assert self.key is not None, "get_process() requires key to be set"
        process = self.context.process_manager.get_process(self.key)
        if process is None:
            process = process_class(self.context.buffer, self.context, *args, **kwargs)
            self.context.process_manager.add_process(self.key, process, tags)
        return process

    def add_header(self, text: str | None = None):
        '''
        text: explicit header text (modbus_panel forms). If omitted,
        network_action_panel forms look their header up via context.labels using
        `key` (must be set).
        '''
        if text is None:
            assert self.key is not None, "add_header() with no text requires key to be set"
            text = str(self.context.labels.get("hacking_forms", self.key))
        self.header = CTkLabel(self, text=text, font=self.style.get_font())
        self.header.grid(row=self.current_row, column=0, columnspan="10", sticky="ew", pady=self.style.gap)
        self.current_row += 1

    def add_label_row(self, label_slot: str, label_keys: list[str]) -> list[CTkLabel]:
        column = 0
        output = []
        for key in label_keys:
            text = self.context.labels.get(label_slot, key)
            label = CTkLabel(self, text=text, font=self.style.get_font("mono"))
            label.grid(row=self.current_row, column=column, sticky="ew", pady=self.style.gapbot, padx=self.style.nogap)
            column += 1
            output.append(label)
        self.current_row += 1
        return output

    def add_labeled_entry(self, label: str):
        '''
        Adds a labeled entry for the curent row in the form.
        This entry has autosave and auto-loading for its text input.
        Requires `key` to have been set (network_action_forms forms only).
        '''

        assert self.key is not None, "add_labeled_entry() requires key to be set"

        # Create widgets
        label_widget = CTkLabel(self, text=label, font=self.style.get_font(), anchor="e")
        label_widget.grid(row=self.current_row, column=1, sticky="w", pady=self.style.gapbot, padx=self.style.gap)

        entry = CTkEntry(self, font=self.style.get_font())
        entry.grid(row=self.current_row, column=2, sticky="ew", pady=self.style.gapbot, padx=self.style.gap)
        self.entries.append(entry)

        # Bind autosave
        save_slots = self.context.states.get("hack_forms", self.key)
        def autosave(event=None, e=entry, idx=self.entry_index):
            save_slots[idx] = e.get()
        entry.bind("<KeyRelease>", autosave)

        # Load saved entry input
        entry.delete(0, "end")
        entry.insert(0, save_slots[self.entry_index])

        # Update current index
        self.current_row += 1
        self.entry_index += 1

        return label_widget, entry

    def add_attack_button(self, start_attack_func: Callable, stop_attack_func: Callable, attack_status_func: Callable[[], bool], default_status: str = ""):

        if self.has_attack_button:
            return

        # Create widgets
        self.attack_status = CTkLabel(self, text=default_status, font=self.style.get_font(), anchor="e")
        self.attack_button = CTkButton(self, text="", font=self.style.get_font(), command=None)

        if self.key is not None:
            self.attack_status.grid(row=self.current_row, column=1, sticky="w", pady=self.style.gapbot, padx=self.style.gap)
            self.attack_button.grid(row=self.current_row, column=2, sticky="ew", pady=self.style.gapbot, padx=self.style.gap)
        else:
            self.attack_status.grid(row=self.current_row, column=0, sticky="", pady=self.style.gapbot)
            self.attack_button.grid(row=self.current_row, column=2, sticky="", pady=self.style.gapbot)

        # Set function definitions
        self.start_attack = start_attack_func
        self.stop_attack = stop_attack_func

        # Configure attack state
        if attack_status_func():
            self.configure_on()
        else:
            self.configure_off()

        # Bind <Return> - a no-op for modbus_panel forms, which never populate self.entries
        def return_handler(event=None):
            self.click_start()
        for entry in self.entries:
            entry.bind("<Return>", return_handler)

        # Update current index
        self.current_row += 1

        self.has_attack_button = True

    def click_start(self):
        if self.key is not None:
            self.context.states.set("game_progress", self.key, value=1)
            self.attack_button.configure(text=self.starting_attack_text)
            self.context.root.update_idletasks()
            self.start_attack()
        else:
            self.attack_button.configure(text=self.starting_attack_text)
            self.start_attack()
            self.context.root.update_idletasks()
        self.configure_on()

    def configure_on(self):
        self.attack_button.configure(command=self.click_stop, text=self.stop_attack_text)
        self.attack_status.configure(text=self.status_on_text)

    def click_stop(self):
        if not self.has_attack_button:
            return
        if self.key is not None:
            self.attack_button.configure(text=self.stopping_attack_text)
            self.context.root.update_idletasks()
            self.stop_attack()
        else:
            self.attack_button.configure(text=self.stopping_attack_text)
            self.stop_attack()
            self.context.root.update_idletasks()
        self.configure_off()

    def configure_off(self):
        self.attack_button.configure(command=self.click_start, text=self.start_attack_text)
        self.attack_status.configure(text=self.status_off_text)

    def add_button(self, default_status: str = "", button_text: str = "", button_func: Callable | None = None):
        # Create widgets
        status = CTkLabel(self, text=default_status, font=self.style.get_font(), anchor="e")
        status.grid(row=self.current_row, column=1, sticky="w", pady=self.style.gapbot, padx=self.style.gap)

        button = CTkButton(self, text=button_text, font=self.style.get_font(), command=button_func)
        button.grid(row=self.current_row, column=2, sticky="ew", pady=self.style.gapbot, padx=self.style.gap)

        # Update current index
        self.current_row += 1

        return status, button
