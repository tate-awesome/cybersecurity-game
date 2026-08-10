from customtkinter import CTkFrame, CTkLabel
from .....app_core.context import Context
from .base_form import BaseForm

class MitmTable(BaseForm):
    def __init__(self, master: CTkFrame, context: Context):
        super().__init__(master, context, "MITM Attack")
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

        self.add_title_row()

        for key in self.context.states["modbus_variables"]:
            self.add_row(key)

        self.context.animation_manager.add_callback("modbus_table", self.update)


    def add_title_row(self):
        self.current_column = 0

        def label(text):
            text = self.context.labels["modbus_table_columns"][text]
            label = CTkLabel(self, text=text, font=self.style.get_font("mono"))
            label.grid(row=self.current_row, column=self.current_column, sticky="ew", pady=self.style.gap, padx=self.style.gap)
            self.current_column += 1
            return label

        label("name")
        label("in")
        label("out")
        label("source")
        self.current_row += 1

    def add_row(self, key):
        this_row = {}
        w = 90
        self.current_column = 0
        slot = self.context.states["modbus_variables"][key]

        def label(text):
            label = CTkLabel(self, text=text, font=self.style.get_font("mono"))
            label.grid(row=self.current_row, column=self.current_column, sticky="ew", pady=self.style.gapbot, padx=self.style.gap)
            self.current_column += 1
            return label

        this_row["name"] = label("-")
        this_row["incoming"] = label("-")
        this_row["outgoing"] = label("-")
        this_row["source"] = label("-")
        self.rows[key] = this_row
        self.current_row += 1

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

    def update(self):
        for key in self.rows:
            this_row = self.rows[key]
            in_str = "-"
            out_str = "-"
            command = "-"
            factor_str = self.context.states["modbus_variables"][key]["factor"]
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
            if not in_value == "-":
                in_str = f"{in_value*factor:.2f}"

            out_value = self.buffer.get_single(key, "out")
            if not out_value == "-":
                out_str = f"{out_value*factor:.2f}"

            command = self.buffer.get_command(key)


            this_row["incoming"].configure(text=in_str)
            this_row["outgoing"].configure(text=out_str)
            this_row["source"].configure(text=command)