from ....network.data_buffer import DataBuffer
from ....app_core.context import Context
from ... import Overlay
from customtkinter import *
from typing import cast


class ColumnOverlay:
    '''
    Binds a button to open and close an overlay with checkboxes for each column, which are saved in the context states for persistence.
    The refresh function is called when the "Apply" button is pressed, which should trigger a refresh of the console to show/hide columns based on the new states.
    '''
    def __init__(self, button, context: Context, refresh_function):
        self.context = context
        self.style = context.style
        self.buffer = cast(DataBuffer, context.net.data_buffer)
        self.refresh_function = refresh_function
        self.overlay = Overlay(self.context.root, context, button, self.populate_column_overlay)

        

    def populate_column_overlay(self, overlay):
        
        box_slots = self.context.states["packet_columns"]
        med = self.style.get_font()

        # Create box filter widgets
        checkbox_frame = CTkFrame(overlay, fg_color=self.style.color("panel"))
        checkbox_frame.pack(side="top", padx=self.style.gap, pady=self.style.gaptop)

        category_frame = CTkFrame(checkbox_frame, fg_color=self.style.color("widget"))
        category_frame.pack(side="left", padx=self.style.gap, pady=self.style.gap, anchor="n")
        category_label = CTkLabel(category_frame, text="Show Columns", font=med)
        category_label.pack(side="top", pady=self.style.gap, anchor="n")

        for key in self.context.states["packet_columns"]:
            column_box = CTkCheckBox(category_frame, text=self.context.labels["packet_columns"][key], font=med)
            column_box.pack(side="top", anchor="w", pady=self.style.gap, padx=self.style.gap)
            # Load previous input
            value = box_slots[key]
            if value == "1" or value == 1: column_box.select()
            else: column_box.deselect()
            # Configure for autosave (give it a function with a value container, its key, and itself)
            def autosave(value=box_slots, key=key, b=column_box):
                value[key] = str(b.get())
                self.refresh_function()
            column_box.configure(command=autosave)