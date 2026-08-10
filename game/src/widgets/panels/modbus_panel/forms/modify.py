from customtkinter import CTkFrame, CTkLabel, CTkEntry, CTkButton
from .....app_core.context import Context
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

        self.add_title_row()

        for key in self.context.states["modbus_variables"]:
            self.add_row(key)

        # self.context.animation_manager.add_callback("modbus_table", self.update)
        self.save_button()
        self.bind_input_save()
        self.bind_input_alert()

        self.add_attack_button(self.enable_modify, self.disable_modify, self.modify_is_enabled)

        self.load_saved_input()


    def add_title_row(self):
        self.current_column = 0
        def label(text):
            text = self.context.labels["modbus_modifier_columns"][text]
            label = CTkLabel(self, text=text, font=self.style.get_font("mono"))
            label.grid(row=self.current_row, column=self.current_column, sticky="ew", pady=self.style.gap, padx=self.style.gap)
            self.current_column += 1
            return label
        label("variable")
        label("multiplier")
        label("offset")
        self.current_row += 1

    def add_row(self, key):
        this_row = {}
        w = 90
        self.current_column = 0
        slot = self.context.states["modbus_variables"][key]

        def label(text):
            label = CTkLabel(self, text=text, font=self.style.get_font("mono"))
            label.grid(row=self.current_row, column=self.current_column, sticky="w", pady=self.style.gapbot, padx=self.style.gap)
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

        if slot["show"] == 0 or slot["show"] == "0":
            self.hide_row(key)


    def refresh_nicknames(self):
        for key, row in self.rows.items():
            # Resolve nickname and configure label
            slot = self.context.states["modbus_variables"][key]
            if len(slot["nickname"]) > 0:
                variable_name = slot["nickname"]
            else:
                variable_name = self.context.labels["modbus_variables"][key]
            row["name"].configure(text=variable_name)

    def refresh_rows(self):
        self.update_idletasks()
        for key, variable in self.context.states["modbus_variables"].items():
            state = variable["show"]
            if state == "1" or state == 1:
                self.show_row(key)
            else:
                self.hide_row(key)

    def show_row(self, key: str):
        row = self.rows[key]
        for _, widget in row.items():
            if not widget.winfo_ismapped():
                widget.grid()

    def hide_row(self, key: str):
        row = self.rows[key]
        for _, widget in row.items():
            if widget.winfo_ismapped():
                widget.grid_remove()

    def save_button(self):
        save_status = CTkLabel(self, text="", font=self.style.get_font(), anchor="e")
        save_status.grid(row=self.current_row, column=0, sticky="", pady=self.style.gaptop, padx=self.style.gap)
        self.save_status = save_status

        save_button = CTkButton(self, text="Save Modifiers", font=self.style.get_font(), command=None)
        save_button.grid(row=self.current_row, column=2, sticky="", pady=self.style.gaptop, padx=self.style.gap)
        self.save_button = save_button

        self.current_row += 1

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
                self.context.states["modbus_variables"][key]["multiplier"] = mult
                offset = float(row["offset"].get())
                self.context.states["modbus_variables"][key]["offset"] = offset

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
            slot = self.context.states["modbus_variables"][key]

            mult = f"{float(slot["multiplier"]):g}"
            row["multiplier"].delete(0, "end")
            row["multiplier"].insert(0, mult)

            offset = f"{float(slot["offset"]):g}"
            row["offset"].delete(0, "end")
            row["offset"].insert(0, offset)
        
        self.save_status.configure(text="Modifiers Saved.")

    def enable_modify(self):
        self.context.states["modbus_modify_enabled"] = 1

    def disable_modify(self):
        self.context.states["modbus_modify_enabled"] = 0

    def modify_is_enabled(self):
        state = self.context.states["modbus_modify_enabled"]
        if state == 1: return True
        else: return False
        