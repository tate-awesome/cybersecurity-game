from customtkinter import *
from ..style import Style
from ...network.mod_table import ModTable

class MITM:
    def __init__(self, style: Style, parent: CTkBaseClass):
        frame = CTkFrame(parent)
        frame.pack(side="top", fill="x", expand=False, padx=style.GAP, pady=(style.GAP, 0))
        frame.columnconfigure(0, weight=0)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=0)
        self.frame = frame

        header = CTkLabel(frame, text="MITM Attack", font=style.get_font())
        header.grid(row=0, column=0, columnspan="3", sticky="ew", pady=(style.GAP,0))
        self.header = header

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
        r = 1
        for name in ["x", "y", "theta", "speed", "rudder"]:
            label = CTkLabel(frame, text=f"{self.names[name]}_out = {self.names[name]}_in *", font=style.get_font())
            label.grid(row=r, column=1, sticky="w", pady=(style.GAP,0), padx=style.GAP)
            self.labels[name] = label

            subframe = CTkFrame(frame, bg_color="transparent", fg_color="transparent")
            subframe.grid(row=r, column=2, sticky="ew", pady=(style.GAP,0), padx=style.GAP)
            subframe.grid_columnconfigure(1, weight=1)
            self.frames[name] = subframe

            mult = CTkEntry(subframe, width=46, font=style.get_font())
            mult.grid(row=0, column=0, sticky="w")
            self.mults[name] = mult

            plus1 = CTkLabel(subframe, text="+", font=style.get_font())
            plus1.grid(row=0, column=1, sticky="ew")

            offset = CTkEntry(subframe, width=46, font=style.get_font())
            offset.grid(row=0, column=2, sticky="e")
            self.offsets[name] = offset

            r = r+1

        save_status = CTkLabel(frame, text="", font=style.get_font())
        save_status.grid(row=r, column=1, sticky="w", pady=(style.GAP,0), padx=style.GAP)
        self.save_status = save_status

        save_button = CTkButton(frame, text="Save Modifiers", font=style.get_font(), command=None)
        save_button.grid(row=r, column=2, sticky="e", pady=style.GAP, padx=style.GAP)
        self.save_button = save_button

        r = r+1

        status = CTkLabel(frame, text="", font=style.get_font())
        status.grid(row=r, column=1, sticky="w", pady=(style.GAP,0), padx=style.GAP)
        self.status = status

        button = CTkButton(frame, text="Start Attack", font=style.get_font(), command=None)
        button.grid(row=r, column=2, sticky="e", pady=(style.GAP,0), padx=style.GAP)
        self.button = button

        self.entries = list(self.mults.values())
        self.entries.extend(list(self.offsets.values()))
        
        
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

            mult = str(table.get(name, "mult"))
            self.mults[name].delete(0, "end")
            self.mults[name].insert(0, mult)

            offset = str(table.get(name, "offset"))
            self.offsets[name].delete(0, "end")
            self.offsets[name].insert(0, offset)
        
        self.save_status.configure(text="Modifiers Saved.")


    def bind_reversible(self, start_func: callable, stop_func: callable, func_name: str, start_on: bool):
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
