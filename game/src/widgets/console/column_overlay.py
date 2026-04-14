from ...network.data_buffer import DataBuffer
from ...app_core.context import Context
from customtkinter import *


class ColumnOverlay:
    def __init__(self, parent, style, button, buffer: DataBuffer, refresh_function):
        self.context = parent
        self.style = style
        self.buffer = buffer
        self.refresh_function = refresh_function

        self.bind_overlay_button(button, self.create_column_overlay, self.destroy_column_overlay)

    def create_column_overlay(self, button: CTkButton):

        # Place overlay just below button
        x = button.winfo_rootx() - self.context.root.winfo_rootx() + button.winfo_width() / 2
        y = button.winfo_rooty() - self.context.root.winfo_rooty() + button.winfo_height() + self.style.igap
        overlay = CTkFrame(self.context.root, border_color=self.style.color("accent"), border_width=2)
        overlay.place(x=x, y=y, anchor="n")
        overlay.lift()
        self.column_overlay = overlay
        
        # Create box filter widgets
        box_slots = self.context.inputs["column_selections"]
        med = self.style.get_font()
        checkbox_frame = CTkFrame(overlay, fg_color=self.style.color("panel"))
        checkbox_frame.pack(side="top", padx=self.style.gap, pady=self.style.gaptop)

        category_frame = CTkFrame(checkbox_frame, fg_color=self.style.color("widget"))
        category_frame.pack(side="left", padx=self.style.gap, pady=self.style.gap, anchor="n")
        category_label = CTkLabel(category_frame, text="Show Columns", font=med)
        category_label.pack(side="top", pady=self.style.gap, anchor="n")
        
        for field in box_slots:
            column_box = CTkCheckBox(category_frame, text=field, font=med)
            column_box.pack(side="top", anchor="w", pady=self.style.gap, padx=self.style.gap)
            # Load previous input
            value = box_slots[field]["state"]
            if value == "1": column_box.select()
            else: column_box.deselect()
            # Configure for autosave
            def autosave(slot=box_slots[field], b=column_box):
                slot["state"] = str(b.get())
            column_box.configure(command=autosave)

        activator_button = CTkButton(category_frame, text="Apply", font=med)
        activator_button.pack(side="bottom", anchor="s", padx=self.style.gap, pady=self.style.gap)

        activator_button.configure(command=self.refresh_function)

    def destroy_column_overlay(self, button: CTkButton):
        try:
            self.column_overlay.destroy()
        finally:
            return

    def bind_overlay_button(self, button: CTkButton, open_func: callable, close_func: callable):
            def configure_opened():
                button.configure(command=close, text=f"Cancel")
            def configure_closed():
                button.configure(command=open, text=f"Columns")
            def close():
                close_func(button)
                configure_closed()
            def open():
                open_func(button)
                configure_opened()
            def event_callback(event=None):
                close()
            self.context.root.bind("<Escape>", event_callback)
            configure_closed()