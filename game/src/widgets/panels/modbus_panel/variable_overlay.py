from ....app_core import Context
from ....widgets import Overlay
from customtkinter import CTkEntry, CTkCheckBox, CTkLabel, CTkFrame, CTkButton
from typing import cast


class VariableOverlay:
    '''
    Binds a button to open and close an overlay with checkboxes for each form, which are saved in the context states for persistence.
    The refresh function is called when any checkbox is clicked
    '''
    def __init__(self, button, context: Context, refresh_rows, refresh_nicknames):
        self.context = context
        self.style = context.style
        self.refresh_rows = refresh_rows
        self.refresh_nicknames = refresh_nicknames
        self.overlay = Overlay(self.context.root, context, button, self.populate_overlay, "east")



    def populate_overlay(self, overlay):
        med = self.style.get_font()
        frame = CTkFrame(overlay, fg_color=self.style.color("panel"))
        frame.pack(side="top", padx=self.style.gap, pady=self.style.gap)


        row = 0
        col = 0

        # Top Row
        top_labels = self.context.labels["modbus_settings"]
        for key, text in top_labels.items():
            top_label = CTkLabel(frame, text=text, font=med)
            top_label.grid(row=row, column=col, padx=self.style.gap, pady=self.style.gap)
            col += 1
        col = 0
        row += 1


        show_checkboxes = []
        nick_entries = []
        factor_entries = []
        units_entries = []
        modify_checkboxes = []

        # Variable Rows

        for slot in self.context.states.get_registers().values():
            # "label": "hreg_8",
            variable_name = self.context.labels["modbus_variables"][slot["label"]]
            var_label = CTkLabel(frame, text=variable_name, font=med)
            var_label.grid(row=row, column=col, sticky="", pady=self.style.gap)
            col += 1
            # "show": 1.0,
            show_checkbox = CTkCheckBox(frame, text="")
            show_checkbox.grid(row=row, column=col, sticky="e", padx=self.style.gap, pady=self.style.gapbot)
            self.enrich_checkbox(show_checkbox, slot, "show")
            show_checkboxes.append(show_checkbox)
            col += 1
            # "nickname": "",
            nick_entry = CTkEntry(frame, font=med)
            nick_entry.grid(row=row, column=col, sticky="ew", padx=self.style.gap, pady=self.style.gapbot)
            self.enrich_entry(nick_entry, slot, "nickname")
            nick_entries.append(nick_entry)
            col += 1
            # "factor": 1.0,
            factor_entry = CTkEntry(frame, font=med)
            factor_entry.grid(row=row, column=col, sticky="", padx=self.style.gap, pady=self.style.gapbot)
            self.enrich_entry(factor_entry, slot, "factor")
            factor_entries.append(factor_entry)
            col += 1
            # "units": "",
            units_entry = CTkEntry(frame, font=med)
            units_entry.grid(row=row, column=col, sticky="ew", padx=self.style.gap, pady=self.style.gapbot)
            self.enrich_entry(units_entry, slot, "units")
            units_entries.append(units_entry)
            col += 1
            # "modify": 0
            modify_checkbox = CTkCheckBox(frame, text="")
            modify_checkbox.grid(row=row, column=col, sticky="e", padx=self.style.gap, pady=self.style.gapbot)
            self.enrich_checkbox(modify_checkbox, slot, "modify")
            modify_checkboxes.append(modify_checkbox)

            col = 0
            row += 1

        # Do All buttons
        # Reset All
        def reset_all():
            self.select_all(show_checkboxes)
            self.clear_entries(nick_entries)
            self.set_entries(factor_entries, "1.0")
            self.clear_entries(units_entries)
            self.deselect_all(modify_checkboxes)
        button = CTkButton(frame, font=med, text="Reset All", command=reset_all)
        button.grid(row = row+1, column = col, padx = self.style.gap, pady=self.style.gapbot, sticky="e")
        col += 1
        # Show
        button = CTkButton(frame, font=med, text="Select All", command=lambda: self.select_all(show_checkboxes))
        button.grid(row = row, column = col, padx = self.style.gap, pady=self.style.gapbot)
        button = CTkButton(frame, font=med, text="Deselect All", command=lambda: self.deselect_all(show_checkboxes))
        button.grid(row = row+1, column = col, padx = self.style.gap, pady=self.style.gapbot)
        col += 1
        # Nicknames
        button = CTkButton(frame, font=med, text="Clear All", command=lambda: self.clear_entries(nick_entries))
        button.grid(row = row+1, column = col, padx = self.style.gap, pady=self.style.gapbot)
        col += 1
        # Factors
        button = CTkButton(frame, font=med, text="Reset All", command=lambda: self.set_entries(factor_entries, "1.0"))
        button.grid(row = row+1, column = col, padx = self.style.gap, pady=self.style.gapbot)
        col += 1
        # Units
        button = CTkButton(frame, font=med, text="Clear All", command=lambda: self.clear_entries(units_entries))
        button.grid(row = row+1, column = col, padx = self.style.gap, pady=self.style.gapbot)
        col += 1
        # Modify
        button = CTkButton(frame, font=med, text="Select All", command=lambda: self.select_all(modify_checkboxes))
        button.grid(row = row, column = col, padx = self.style.gap, pady=self.style.gapbot)
        button = CTkButton(frame, font=med, text="Deselect All", command=lambda: self.deselect_all(modify_checkboxes))
        button.grid(row = row+1, column = col, padx = self.style.gap, pady=self.style.gapbot)
        col += 1


        col = 0
        row += 1

    def enrich_entry(self, entry: CTkEntry, slot: dict, key: str):
        # Bind autosave
        def autosave(event=None, e=entry, key=key):
            slot[key] = e.get()
            self.refresh_nicknames()
        entry.bind("<KeyRelease>", autosave)

        # Load saved entry input
        entry.delete(0, "end")
        entry.insert(0, slot[key])

    def enrich_checkbox(self, checkbox: CTkCheckBox, slot: dict, key: str):
        # Configure for autosave (give it a function with a value container, its key, and itself)
        def autosave(event=None, slot=slot, key=key, b=checkbox):
            slot[key] = str(b.get())
            self.refresh_rows()
        checkbox.configure(command=autosave)

        # Load previous input
        value = slot[key]
        if value == "1" or value == 1: checkbox.select()
        else: checkbox.deselect()

    def select_all(self, checkboxes: list[CTkCheckBox]):
        for checkbox in checkboxes:
            checkbox.deselect()
            checkbox.toggle()

    def deselect_all(self, checkboxes: list[CTkCheckBox]):
        for checkbox in checkboxes:
            checkbox.select()
            checkbox.toggle()

    def clear_entries(self, entries: list[CTkEntry]):
        self.set_entries(entries, "")

    def set_entries(self, entries: list[CTkEntry], text: str):
        for entry in entries:
            entry.delete(0, "end")
            entry.insert(0, text)
            entry.focus_set()
            entry.event_generate("<KeyRelease>")
        self.context.root.focus_set()