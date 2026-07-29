from customtkinter import CTkFrame, CTkLabel
from .....app_core.context import Context
from .....network.mod_table import ModTable
from .....network.meta_packet import MetaPacket
from .....network.data_buffer import DataBuffer
from typing import cast
from .base_form import BaseForm

class MitmTable(BaseForm):
    def __init__(self, master: CTkFrame, context: Context):
        super().__init__(master, context, "mitm2", "MITM Attack")
        # Assign local references
        self.buffer = cast(DataBuffer, context.net.data_buffer)
        
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
            
            in_value = self.buffer.get_latest_value(key,"in")
            out_value = self.buffer.get_latest_value(key,"out")
            source = self.buffer.get_latest_source(key)
            this_row["incoming"].configure(text=f"{in_value:.3f}")
            this_row["outgoing"].configure(text=f"{out_value:.3f}")
            this_row["source"].configure(text=source)
        self.after(100, self.update)