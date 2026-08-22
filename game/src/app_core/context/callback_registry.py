from customtkinter import CTk
from typing import Callable


class CallbackRegistry:
    '''
    Shared registry logic for AnimationManager and ClickManager: both keep a
    named dict of callbacks, log additions/replacements/removals with a tag,
    and dispatch every registered callback in one pass, isolating each one in
    its own try/except so a single bad callback can't break the rest.
    '''
    def __init__(self, root: CTk, tag: str):
        self.root: CTk = root
        self.callbacks: dict[str, Callable] = {}
        self._tag = tag
        self._add = "+"
        self._replace = "-+"
        self._remove = "-"
        self._error = "error:"

    def add_callback(self, name: str, callback_func: Callable):
        """
        Dynamically adds a callback function.
        """
        if name in self.callbacks:
            print(f"{self._tag} {self._replace} {name}")
        else:
            print(f"{self._tag} {self._add} {name}")
        self.callbacks[name] = callback_func

    def remove_callback(self, name: str):
        """
        Dynamically removes a callback function by its name.
        """
        if name in self.callbacks:
            del self.callbacks[name]
            print(f"{self._tag} {self._remove} {name}")

    def dispatch(self, *args):
        '''
        Runs every registered callback once, in isolation - a raising
        callback is logged and skipped, not allowed to break the rest.
        '''
        # Iterate over a copy of the values to prevent runtime errors
        # if a callback removes a callback mid-execution.
        active_callbacks = list(self.callbacks.values())

        for callback in active_callbacks:
            try:
                callback(*args)
            except Exception as e:
                print(f"{self._tag} {self._error} {e}")

    def delete(self):
        self.callbacks.clear()
