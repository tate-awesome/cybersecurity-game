from ...app_core import Context
from .overlay import Overlay
from PySide6.QtWidgets import QCheckBox, QFrame, QLabel, QPushButton, QVBoxLayout
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
    def __init__(self, button: QPushButton, context: Context, refresh_function: Callable,
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
        category_frame = QFrame()
        category_frame.setStyleSheet(f"background-color: {self.style.color('widget')};")
        category_layout = QVBoxLayout(category_frame)
        overlay.layout().addWidget(category_frame)

        category_label = QLabel(self.category_label)
        category_label.setFont(med)
        category_layout.addWidget(category_label)

        available_forms: dict[str, int] = self.context.states.get(self.visibility_key) if self.visibility_key else None
        for key in self.context.states.get(self.state_key):
            if available_forms and (key not in available_forms or available_forms[key] == 0 or available_forms[key] == "0"):
                print(f"Form is invisible: {key!r}")
                continue

            checkbox = QCheckBox(self.context.labels.get(self.state_key, key))
            checkbox.setFont(med)
            category_layout.addWidget(checkbox)

            # Load previous input before connecting, so restoring it doesn't itself trigger autosave
            value = box_slots[key]
            checkbox.setChecked(value == "1" or value == 1)

            # Configure for autosave (give it a function with a value container and its key).
            # Stored as "1"/"0" - the convention this settings data already uses
            # everywhere else (matching customtkinter's CTkCheckBox.get(), which
            # returned 1/0, not Qt's own True/False).
            def autosave(checked: bool, value=box_slots, key=key):
                value[key] = "1" if checked else "0"
                self.refresh_function()
            checkbox.toggled.connect(autosave)
