from customtkinter import CTk
from .callback_registry import CallbackRegistry


class AnimationManager(CallbackRegistry):
    '''
    Global manager for animation loops. A single interruptor is more performant than an interruptor for every canvas.
    '''
    def __init__(self, root: CTk, frame_time_ms: int = 50):
        super().__init__(root, tag="[Animation]")
        self.run = True
        self.time = frame_time_ms

        self.start_loop()

    def start_loop(self):
        self.run = True
        self.do_loop()

    def do_loop(self, event=None):
        """
        The single source of truth. Loops through and safely runs all registered
        functions in a single pass.
        """
        self.dispatch()
        if self.run:
            self.root.after(self.time, self.do_loop)

    def stop_loop(self):
        self.run = False

    def delete(self):
        self.stop_loop()
        super().delete()
