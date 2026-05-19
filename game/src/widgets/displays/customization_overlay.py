from ...app_core.context import Context

from customtkinter import *
from tkinter import ttk
import tkinter as tk

class CustomizationOverlay:
    def __init__(self, context, style, button):
        self.context = context
        self.style = style

        self.bind_overlay_button(button, self.create_filter_overlay, self.destroy_filter_overlay)

    # Filter overlay

    def add_customization_options(self, parent: CTkFrame):
        '''
        Create filter menu widgets, load filter options from context and configure inputs for autosave
        '''
        # Create box filter widgets
        box_slots = self.context.inputs["map_settings"]["customization"]
        med = self.style.get_font()
        checkbox_frame = CTkFrame(parent, fg_color=self.style.color("panel"))
        checkbox_frame.pack(side="top", padx=self.style.gap, pady=self.style.gaptop)

        for category in box_slots:

            category_frame = CTkFrame(checkbox_frame, fg_color=self.style.color("widget"))
            category_frame.pack(side="left", padx=self.style.gap, pady=self.style.gap, anchor="n")
            category_label = CTkLabel(category_frame, text=category, font=med)
            category_label.pack(side="top", pady=self.style.gap, anchor="n")

            for box_name in box_slots[category]:

                # Load previous input
                value = box_slots[category][box_name]
                if value == "1" or value == "0": 
                    filter_box = CTkCheckBox(category_frame, text=box_name, font=med)
                    filter_box.pack(side="top", anchor="w", pady=self.style.gap, padx=self.style.gap)
                    filter_box.select()
                    if value == "0":
                        filter_box.deselect()
                else:
                    filter_frame = CTkFrame(category_frame)
                    filter_frame.pack(side="top", fill="x", pady=self.style.gap, padx=self.style.gap)
                    filter_frame.configure(fg_color=self.style.color("widget"))
                    filter_label = CTkLabel(filter_frame, text=box_name, font=med, bg_color=self.style.color("widget"), fg_color=self.style.color("widget"))
                    filter_label.pack(side="left")
                    filter_box = CTkEntry(filter_frame, font=med)
                    filter_box.insert(0, value)
                    filter_box.pack(side="right", fill="x", expand=False, padx=self.style.igap)
                # Configure for autosave
                def autosave(slot=box_slots[category][box_name], b=filter_box):
                    slot = str(b.get())
                if isinstance(filter_box, CTkCheckBox):
                    filter_box.configure(command=autosave)
                if isinstance(filter_box, CTkEntry):
                    filter_box.bind("<KeyRelease>", lambda event: autosave())
        

    def create_filter_overlay(self, button: CTkButton):

        # Place overlay just below button
        x = button.winfo_rootx() - self.context.root.winfo_rootx() + button.winfo_width() / 2
        y = button.winfo_rooty() - self.context.root.winfo_rooty() + button.winfo_height() + self.style.igap
        overlay = CTkFrame(self.context.root, border_color=self.style.color("accent"), border_width=2)
        overlay.place(x=x, y=y, anchor="n")
        overlay.lift()
        self.filter_overlay = overlay
        self.add_customization_options(overlay)

    def destroy_filter_overlay(self, button: CTkButton):
        try:
            self.filter_overlay.destroy()
        finally:
            return

    def bind_overlay_button(self, button: CTkButton, open_func: callable, close_func: callable):
            def configure_opened():
                button.configure(command=close, text=f"Close")
            def configure_closed():
                button.configure(command=open, text=f"Customize")
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