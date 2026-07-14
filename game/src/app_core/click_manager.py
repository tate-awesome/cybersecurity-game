import customtkinter as ctk

class ClickManager:
    '''
    Global click manager for evil annoying features
    '''
    def __init__(self, root):
        self.root = root
        self.listeners = {}  # Stores identifier: callback_function
        
        # Bind the global listener ONCE to the root window
        self.root.bind_all("<Button-1>", self.global_executor, add="+")

    def add_listener(self, name: str, callback_func):
        """
        Dynamically a click callback function.
        """
        if name in self.listeners.keys():
            print(f"[ClickManager] Refused to add duplicate listener: '{name}'")
            return
        self.listeners[name] = callback_func
        print(f"[ClickManager] Added listener: '{name}'")

    def remove_listener(self, name: str):
        """
        Dynamically remove a click callback function by its name.
        """
        if name in self.listeners:
            del self.listeners[name]
            print(f"[ClickManager] Removed listener: '{name}'")

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
                print(f"[ClickManager] Error executing callback: {e}")