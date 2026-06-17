from customtkinter import CTkFrame, CTkLabel, CTkEntry, CTkButton
from ...app_core.context import Context
from ...network.mod_table import ModTable
from ...network.meta_packet import MetaPacket

class MitmForm(CTkFrame):

    def __init__(self, master: CTkFrame, context: Context):
        # Assign local references
        self.context = context
        style = context.style
        
        # Create form
        super().__init__(master, fg_color=style.color("widget"))
        self.pack(side="top", fill="x", expand=False, padx=style.nogap, pady=style.gaptop)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0)

        header = CTkLabel(self, text="MITM Attack", font=style.get_font())
        header.grid(row=0, column=0, columnspan="3", sticky="ew", pady=style.gaptop)
        self.header = header

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
        r = 1
        for name in ["x", "y", "theta", "speed", "rudder"]:
            label = CTkLabel(self, text=f"{self.names[name]}_out = {self.names[name]}_in *", font=style.get_font(), anchor="w")
            label.grid(row=r, column=1, sticky="w", pady=style.gaptop, padx=style.gap)
            self.labels[name] = label

            subframe = CTkFrame(self, bg_color="transparent", fg_color="transparent")
            subframe.grid(row=r, column=2, sticky="ew", pady=style.gaptop, padx=style.gap)
            subframe.grid_columnconfigure(0, weight=1)
            subframe.grid_columnconfigure(1, weight=0)
            subframe.grid_columnconfigure(2, weight=1)
            self.frames[name] = subframe

            mult = CTkEntry(subframe, width=46, font=style.get_font())
            mult.grid(row=0, column=0, sticky="ew")
            self.mults[name] = mult

            plus1 = CTkLabel(subframe, text="  +  ", font=style.get_font())
            plus1.grid(row=0, column=1, sticky="ew")

            offset = CTkEntry(subframe, width=46, font=style.get_font())
            offset.grid(row=0, column=2, sticky="ew")
            self.offsets[name] = offset

            r = r+1

        # Save button
        save_status = CTkLabel(self, text="", font=style.get_font(), anchor="e")
        save_status.grid(row=r, column=1, sticky="w", pady=style.gaptop, padx=style.gap)
        self.save_status = save_status

        save_button = CTkButton(self, text="Save Modifiers", font=style.get_font(), command=None)
        save_button.grid(row=r, column=2, sticky="e", pady=style.gaptop, padx=style.gap)
        self.save_button = save_button

        r = r+1

        status = CTkLabel(self, text="", font=style.get_font(), anchor="e")
        status.grid(row=r, column=1, sticky="w", pady=style.gaptop, padx=style.gap)
        self.status = status

        # Start/Stop button
        button = CTkButton(self, text="Start Attack", font=style.get_font(), command=None)
        button.grid(row=r, column=2, sticky="e", pady=style.gap, padx=style.gap)
        self.button = button

        self.entries = list(self.mults.values())
        self.entries.extend(list(self.offsets.values()))

        # Define stop/start
        def start_mitm():
            self.context.states["game_progress"]["mitm"] = True
            self.context.root.update_idletasks()
            self.context.net.start_mitm()

        def stop_mitm():
            self.context.root.update_idletasks()
            self.context.net.stop_mitm()

        # Autosave & preset
        start_on = context.net.mitm_is_running()
        self.bind_reversible(start_mitm, stop_mitm, "Attack", start_on)


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

    def deactivate(self):
        import platform
        os_name = platform.system()
        if os_name == "Windows":
            # NFQ is not possible
            self.status.configure(text="NFQ is not supported on Windows.")
            self.button.configure(state="disabled", text="Disabled")