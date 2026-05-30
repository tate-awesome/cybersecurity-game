from ...network.data_buffer import DataBuffer
from ...app_core.context import Context
from customtkinter import *


class ColumnOverlay:
    '''
    Binds a button to open and close an overlay with checkboxes for each column, which are saved in the context states for persistence.
    The refresh function is called when the "Apply" button is pressed, which should trigger a refresh of the console to show/hide columns based on the new states.
    '''
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
        overlay.place(x=x/self.style.get_scale_correction(), y=y/self.style.get_scale_correction(), anchor="n")
        overlay.lift()
        self.column_overlay = overlay
        
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
            column_box.configure(command=autosave)

        activator_button = CTkButton(category_frame, text="Apply", font=med, command=self.refresh_function)
        activator_button.pack(side="bottom", anchor="s", padx=self.style.gap, pady=self.style.gap)


    def destroy_column_overlay(self, button: CTkButton):
        try:
            self.column_overlay.destroy()
        finally:
            return

    def bind_overlay_button(self, button: CTkButton, open_func: callable, close_func: callable):
            def configure_opened():
                button.configure(command=close, text=f"Close")
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