from customtkinter import CTk
from .callback_registry import CallbackRegistry


class ClickManager(CallbackRegistry):
    '''
    Global click manager for evil annoying features
    '''
    def __init__(self, root: CTk):
        super().__init__(root, tag="[Click]")

        # Bind the global listener ONCE to the root window
        self.root.bind_all("<Button-1>", self.global_executor, add="+")

        self.add_listener("click_focus", self.click_to_focus)

    def add_listener(self, name: str, callback_func):
        self.add_callback(name, callback_func)

    def remove_listener(self, name: str):
        self.remove_callback(name)

    def global_executor(self, event):
        """
        The single source of truth. Loops through and safely runs all registered
        functions in a single pass whenever a click happens anywhere.
        """
        self.dispatch(event)

    def delete(self):
        super().delete()
        self.root.unbind("<Button-1>")

    def click_to_focus(self, event=None):
        clicked_widget = event.widget
        class_name = type(clicked_widget).__name__

        if class_name == "Canvas" and hasattr(clicked_widget, "master"):
            clicked_widget = clicked_widget.master

        if hasattr(clicked_widget, "focus_set"):
            clicked_widget.focus_set()
