from ...app_core import Context
from .overlay import Overlay
from customtkinter import CTkFrame, CTkLabel, CTkCheckBox, CTkButton
from typing import Callable


class CheckboxOverlay:
    '''
    Binds a button to open and close an overlay with one checkbox per key in
    a context.states settings category, persisted there, with a translated
    label per checkbox (via context.labels) and a category title above them.
    refresh_function is called whenever a checkbox is toggled.

    Used for hacking-panel form visibility, modbus-panel form visibility, and
    packet-console column visibility - those only ever differed in which
    settings category to read/write (state_key) and what to title the column
    (category_label).
    '''
    def __init__(self, button: CTkButton, context: Context, refresh_function: Callable,
                 state_key: str, category_label: str, visibility_key: str | None = None):
        self.context = context
        self.style = context.style
        self.refresh_function = refresh_function
        self.state_key = state_key
        self.category_label = category_label
        self.visibility_key = visibility_key
        self.overlay = Overlay(self.context.root, context, button, self.populate_overlay)

    def populate_overlay(self, overlay: Overlay):
        box_slots = self.context.states.get(self.state_key)
        med = self.style.get_font()

        # Create box filter widgets
        checkbox_frame = CTkFrame(overlay, fg_color=self.style.color("panel"))
        checkbox_frame.pack(side="top", padx=self.style.gap, pady=self.style.gaptop)

        category_frame = CTkFrame(checkbox_frame, fg_color=self.style.color("widget"))
        category_frame.pack(side="left", padx=self.style.gap, pady=self.style.gap, anchor="n")
        category_label = CTkLabel(category_frame, text=self.category_label, font=med)
        category_label.pack(side="top", pady=self.style.gap, anchor="n")


        available_forms: dict[str, int] = self.context.states.get(self.visibility_key) if self.visibility_key else None
        for key in self.context.states.get(self.state_key):
            if available_forms and (key not in available_forms or available_forms[key] == 0 or available_forms[key] == "0"):
                print(f"Form is invisible: {key!r}")
                continue

            checkbox = CTkCheckBox(category_frame, text=self.context.labels.get(self.state_key, key), font=med)
            checkbox.pack(side="top", anchor="w", pady=self.style.gap, padx=self.style.gap)
            # Load previous input
            value = box_slots[key]
            if value == "1" or value == 1: checkbox.select()
            else: checkbox.deselect()
            # Configure for autosave (give it a function with a value container, its key, and itself)
            def autosave(value=box_slots, key=key, b=checkbox):
                value[key] = str(b.get())
                self.refresh_function()
            checkbox.configure(command=autosave)
