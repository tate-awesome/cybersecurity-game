from customtkinter import CTkFrame

class ClickManager:
    '''
    Global click manager for evil annoying features
    '''
    def __init__(self, root):
        self.root = root
        self.listeners = {}  # Stores identifier: callback_function
        self.tag = "[Click]"
        self.add = "+"
        self.replace = "-+"
        self.remove = "-"
        self.error = "error:"
        
        # Bind the global listener ONCE to the root window
        self.root.bind_all("<Button-1>", self.global_executor, add="+")

        self.add_listener("click_focus", self.click_to_focus)

    def add_listener(self, name: str, callback_func):
        """
        Dynamically a click callback function.
        """
        if name in self.listeners.keys():
            print(f"{self.tag} {self.replace} {name}")
        else:
            print(f"{self.tag} {self.add} {name}")
        self.listeners[name] = callback_func

    def remove_listener(self, name: str):
        """
        Dynamically remove a click callback function by its name.
        """
        if name in self.listeners:
            del self.listeners[name]
            print(f"{self.tag} {self.remove} {name}")

    def global_executor(self, event):
        """
        The single source of truth. Loops through and safely runs all registered 
        functions in a single pass whenever a click happens anywhere.
        """
        # Iterate over a copy of the values to prevent runtime errors 
        # if a callback removes a listener mid-execution.
        active_callbacks = list(self.listeners.values())
        
        for callback in active_callbacks:
            try:
                callback(event)
            except Exception as e:
                print(f"{self.tag} {self.error} {e}")

    def delete(self):
        self.listeners.clear()
        self.root.unbind("<Button-1>")

    def click_to_focus(self, event=None):
        clicked_widget = event.widget
        class_name = type(clicked_widget).__name__
    
        if class_name == "Canvas" and hasattr(clicked_widget, "master"):
            clicked_widget = clicked_widget.master

        if hasattr(clicked_widget, "focus_set"):
            clicked_widget.focus_set()