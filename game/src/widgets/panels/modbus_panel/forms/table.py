from customtkinter import CTkFrame, CTkLabel
from .....app_core import Context
from .base_form import BaseForm

class MitmTable(BaseForm):
    def __init__(self, master: CTkFrame, context: Context):
        super().__init__(master, context, "NFQ")
        # Assign local references
        self.buffer = context.net.buffer.modbus
        # Create form
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)

        self.add_header("ModBus Readings")

        # Create value table entries
        self.rows = {}

        self.add_label_row("modbus_table", ["name", "in", "out", "source"])

        for key in self.context.states.get_registers():
            labels = self.add_label_row("modbus_table", ["-", "-", "-", "-"])
            self.rows[key] = {}
            self.rows[key]["name"] = labels[0]
            self.rows[key]["incoming"] = labels[1]
            self.rows[key]["outgoing"] = labels[2]
            self.rows[key]["source"] = labels[3]

        self.context.animation_manager.add_callback("modbus_table", self.update)

    def refresh_nicknames(self):
        for key, row in self.rows.items():
            variable_name = self.context.labels.variable_name(key)
            row["name"].configure(text=variable_name)

    def refresh_rows(self):
        self.update_idletasks()
        for key in self.context.states.get_registers():
            state = self.context.states.get_register(key, "show")
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

    def update(self):
        for key in self.rows:
            this_row = self.rows[key]
            in_str = "-"
            out_str = "-"
            command = "-"
            factor_str = self.context.states.get_register(key, "factor")
            factor = 1.0
            try: 
                f = float(factor_str)
                factor = f
            except:
                message = "err: factor"
                this_row["incoming"].configure(text=message)
                this_row["outgoing"].configure(text=message)
                this_row["source"].configure(text=message)
                continue


            # TODO switch to a get dump type of thing where it dumps all the changed values

            in_value = self.buffer.get_single(key, "in")
            if not in_value is None:
                in_str = f"{in_value*factor:.2f}"

            out_value = self.buffer.get_single(key, "out")
            if not out_value is None:
                out_str = f"{out_value*factor:.2f}"

            command = self.buffer.get_command(key)


            this_row["incoming"].configure(text=in_str)
            this_row["outgoing"].configure(text=out_str)
            this_row["source"].configure(text=command)