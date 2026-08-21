from customtkinter import CTkFrame, CTkLabel, CTkEntry, CTkButton
from .....app_core import Context
from .base_form import BaseForm

class Modify(BaseForm):
    def __init__(self, master: CTkFrame, context: Context):
        super().__init__(master, context, "Modifying")
        # Assign local references
        self.buffer = context.net.buffer.modbus
        # Create form
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.add_header("ModBus Modifiers")

        # Create value table entries
        self.rows = {}
        self.entries = []

        self.add_label_row("modbus_modifier", ["variable", "multiplier", "offset"])

        for key in self.context.states.get_registers():
            self.add_var_row(key)

        # self.context.animation_manager.add_callback("modbus_table", self.update)
        self.save_status, self.save_button = self.add_button("Save Modifiers")
        self.bind_input_save()
        self.bind_input_alert()

        self.add_attack_button(self.enable_modify, self.disable_modify, self.modify_is_enabled)

        _, reset_button = self.add_button("Reset Modifiers")
        reset_button.configure(command=self.reset_modifiers)

        self.load_saved_input()

    def add_var_row(self, key):
        this_row = {}
        self.current_column = 0

        def label(text):
            label = CTkLabel(self, text=text, font=self.style.get_font("mono"))
            label.grid(row=self.current_row, column=self.current_column, sticky="", pady=self.style.gapbot)
            self.current_column += 1
            return label

        def entry():
            entry = CTkEntry(self, font=self.style.get_font("mono"))
            entry.grid(row=self.current_row, column=self.current_column, sticky="")
            self.entries.append(entry)
            self.current_column += 1
            return entry

        this_row["name"] = label("-")
        this_row["multiplier"] = entry()
        this_row["offset"] = entry()
        self.rows[key] = this_row
        self.current_row += 1

        self.row_visibility(key)


    def refresh_nicknames(self):
        for key, row in self.rows.items():
            variable_name = self.context.labels.variable_name(key)
            row["name"].configure(text=variable_name)

    def refresh_rows(self):
        self.update_idletasks()
        for key in self.context.states.get_registers():
            self.row_visibility(key)

    def row_visibility(self, key: str):
        state = self.context.states.get_register(key, "show")
        row = self.rows[key]
        for _, widget in row.items():
            if (state == 0 or state == "0") and widget.winfo_ismapped():
                widget.grid_remove()
            elif (state == 1 or state == "1") and not widget.winfo_ismapped():
                widget.grid()

    def add_button(self, text) -> tuple[CTkLabel, CTkButton]:
        status = CTkLabel(self, text="", font=self.style.get_font(), anchor="e")
        status.grid(row=self.current_row, column=0, sticky="", pady=self.style.gapbot)

        button = CTkButton(self, text=text, font=self.style.get_font(), command=None)
        button.grid(row=self.current_row, column=2, sticky="", pady=self.style.gapbot)
        self.current_row += 1

        return status, button

    def bind_input_save(self):
        def save():
            # Validate
            valid = True
            for _, row in self.rows.items():
                try:
                    float(row["multiplier"].get())
                    float(row["offset"].get())
                except:
                    valid = False
                    pass

            if not valid:
                self.save_status.configure(text="! Must be Numbers !")
                return

            # Then save
            for key, row in self.rows.items():
                mult = float(row["multiplier"].get())
                self.context.states.set_register(key, "multiplier", mult)
                offset = float(row["offset"].get())
                self.context.states.set_register(key, "offset", offset)

            self.save_status.configure(text="Modifiers Saved.")

        self.save_button.configure(command=save)
        def event_callback(event=None):
            save()
        
        for entry in self.entries:
            entry.bind("<Return>", event_callback)

    def bind_input_alert(self):
        def alert(event=None):
            self.save_status.configure(text="! Unsaved Modifiers !")
        for entry in self.entries:
            entry.bind("<Key>", alert)

    def load_saved_input(self):
        for key, row in self.rows.items():
            multiplier_str = self.context.states.get_register(key, "multiplier")
            offset_str = self.context.states.get_register(key, "offset")

            mult = f"{float(multiplier_str):g}"
            row["multiplier"].delete(0, "end")
            row["multiplier"].insert(0, mult)

            offset = f"{float(offset_str):g}"
            row["offset"].delete(0, "end")
            row["offset"].insert(0, offset)
        
        self.save_status.configure(text="Modifiers Saved.")

    # Enable Modify Button

    def enable_modify(self):
        self.context.states.set("modbus_modify_enabled", value=1)

    def disable_modify(self):
        self.context.states.set("modbus_modify_enabled", value=0)

    def modify_is_enabled(self):
        state = self.context.states.get("modbus_modify_enabled")
        if state == 1: return True
        else: return False

    # Reset button

    def reset_modifiers(self):
        for key, row in self.rows.items():
            self.context.states.set_register(key, "multiplier", 1)
            self.context.states.set_register(key, "offset", 0)
        self.load_saved_input()