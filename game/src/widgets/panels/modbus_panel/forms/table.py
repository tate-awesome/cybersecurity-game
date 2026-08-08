from customtkinter import CTkFrame, CTkLabel
from .....app_core.context import Context
from .base_form import BaseForm

class MitmTable(BaseForm):
    def __init__(self, master: CTkFrame, context: Context):
        super().__init__(master, context, "mitm2", "MITM Attack")
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


        # Resolve nickname and add label
        if len(slot["nickname"]) > 0:
            variable_name = slot["nickname"]
        else:
            variable_name = self.context.labels["modbus_variables"][key]

        this_row["name"] = label(variable_name)

        # Source

        this_row["incoming"] = label("-")
        this_row["outgoing"] = label("-")
        this_row["source"] = label("-")
        self.rows[key] = this_row
        self.current_row += 1

    def refresh_rows(self):
        for key in self.context.states["modbus_variables"]:
            state = self.context.states["modbus_forms"][key]["show"]
            if state == "1" or state == 1:
                self.show_row(key)
            else:
                self.hide_row(key)

    def show_row(self, key: str):
        row = self.rows[key]
        if not row.winfo_ismapped():
            return
        row.grid_remove()  

    def hide_row(self, key: str):
        row = self.forms[key]
        if row.winfo_ismapped():
            return
        row.grid()

    def update(self):
        for key in self.rows:
            this_row = self.rows[key]
            in_str = "-"
            out_str = "-"
            command = "-"
            # TODO switch to a get dump type of thing where it dumps all the changed values

            in_value = self.buffer.get_single(key, "in")
            if not in_value == "-":
                in_str = f"{in_value:.2f}"

            out_value = self.buffer.get_single(key, "out")
            if not out_value == "-":
                out_str = f"{out_value:.2f}"

            command = self.buffer.get_command(key)


            this_row["incoming"].configure(text=in_str)
            this_row["outgoing"].configure(text=out_str)
            this_row["source"].configure(text=command)