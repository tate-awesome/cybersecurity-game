from customtkinter import CTkFrame, CTkLabel, CTkEntry, CTkButton
from .....app_core.context import Context
from .....network.mod_table import ModTable
from .base_form import BaseForm
from typing import Callable

class MitmForm(BaseForm):

    def __init__(self, master: CTkFrame, context: Context):

        super().__init__(master, context, "nfq", "MITM Attack")
        self.add_header("MITM Attack")
        self.has_attack_button = False
        # Create value table entries
        self.labels = {}
        self.frames = {}
        self.mults = {}
        self.offsets = {}
        self.names = {
            "x": "X",
            "y": "Y",
            "theta": "T",
            "speed": "S",
            "rudder": "R"
        }
        for name in ["x", "y", "theta", "speed", "rudder"]:
            label = CTkLabel(self, text=f"{self.names[name]}_out = {self.names[name]}_in *", font=self.style.get_font(), anchor="w")
            label.grid(row=self.current_row, column=1, sticky="w", pady=self.style.gaptop, padx=self.style.gap)
            self.labels[name] = label

            subframe = CTkFrame(self, bg_color="transparent", fg_color="transparent")
            subframe.grid(row=self.current_row, column=2, sticky="ew", pady=self.style.gaptop, padx=self.style.gap)
            subframe.grid_columnconfigure(0, weight=1)
            subframe.grid_columnconfigure(1, weight=0)
            subframe.grid_columnconfigure(2, weight=1)
            self.frames[name] = subframe

            mult = CTkEntry(subframe, width=46, font=self.style.get_font())
            mult.grid(row=0, column=0, sticky="ew")
            self.mults[name] = mult

            plus1 = CTkLabel(subframe, text="  +  ", font=self.style.get_font())
            plus1.grid(row=0, column=1, sticky="ew")

            offset = CTkEntry(subframe, width=46, font=self.style.get_font())
            offset.grid(row=0, column=2, sticky="ew")
            self.offsets[name] = offset

            self.current_row = self.current_row+1

        # Save button
        save_status = CTkLabel(self, text="", font=self.style.get_font(), anchor="e")
        save_status.grid(row=self.current_row, column=1, sticky="w", pady=self.style.gaptop, padx=self.style.gap)
        self.save_status = save_status

        save_button = CTkButton(self, text="Save Modifiers", font=self.style.get_font(), command=None)
        save_button.grid(row=self.current_row, column=2, sticky="e", pady=self.style.gaptop, padx=self.style.gap)
        self.save_button = save_button

        self.current_row = self.current_row+1
        self.current_row = self.current_row

        status = CTkLabel(self, text="", font=self.style.get_font(), anchor="e")
        status.grid(row=self.current_row, column=1, sticky="w", pady=self.style.gaptop, padx=self.style.gap)
        self.status = status

        # Start/Stop button

        self.entries = list(self.mults.values())
        self.entries.extend(list(self.offsets.values()))
        self.add_attack_button(context.net.start_nfq, context.net.stop_nfq, context.net.nfq_is_running)


        self.bind_input_alert()
        self.load_saved_input(self.context.net.table)
        self.bind_input_save(self.context.net.table) # Bind save button on entry change
        # self.deactivate() # Disable button on windows
        
        
    def bind_input_save(self, table: ModTable):
        def save():

            # Validate
            valid = True
            for name in ["x", "y", "theta", "speed", "rudder"]:
                try:
                    float(self.mults[name].get())
                    float(self.offsets[name].get())
                except:
                    valid = False
                    pass

            if not valid:
                self.save_status.configure(text="! Must be Numbers !")
                return

            # Then save
            for name in ["x", "y", "theta", "speed", "rudder"]:
                mult = float(self.mults[name].get())
                table.set(name, "mult", mult)
                offset = float(self.offsets[name].get())
                table.set(name, "offset", offset)

            self.save_status.configure(text="Modifiers Saved.")

        self.save_button.configure(command=save)
        def event_callback(event=None):
            save()
        
        for entry in self.entries:
            entry.bind("<Return>", event_callback)

    
    def bind_input_alert(self):
        def alert(event=None):
            self.save_status.configure(text="! Unsaved Modifiers !")
        for name in ["x", "y", "theta", "speed", "rudder"]:
            self.mults[name].bind("<Key>", alert)
            self.offsets[name].bind("<Key>", alert)

    def load_saved_input(self, table: ModTable):
        for name in ["x", "y", "theta", "speed", "rudder"]:

            mult = str(table.get_readable(name, "mult"))
            self.mults[name].delete(0, "end")
            self.mults[name].insert(0, mult)

            offset = str(table.get_readable(name, "offset"))
            self.offsets[name].delete(0, "end")
            self.offsets[name].insert(0, offset)
        
        self.save_status.configure(text="Modifiers Saved.")

    def add_attack_button(self, start_attack_func: Callable, stop_attack_func: Callable, attack_status_func: Callable[None, bool], default_status: str = ""):

        if self.has_attack_button:
            return

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

        self.has_attack_button = True

    def click_start(self):
        self.context.states["game_progress"][self.key] = 1
        self.attack_button.configure(text=f"Starting {self.attack_noun}...")
        self.start_attack()
        self.context.root.update_idletasks()
        self.configure_on()
    
    def configure_on(self):
        self.attack_button.configure(command=self.click_stop, text=f"Stop {self.attack_noun}")
        self.attack_status.configure(text=f"{self.attack_noun} is on")

    def click_stop(self):
        if not self.has_attack_button:
            return
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