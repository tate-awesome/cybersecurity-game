from PySide6.QtCore import QTimer
from .callback_registry import CallbackRegistry


class AnimationManager(CallbackRegistry):
    '''
    Global manager for animation loops. A single QTimer is more performant than a timer for every canvas.
    '''
    def __init__(self, root, frame_time_ms: int = 100):
        super().__init__(root, tag="[Animation]")
        self.time = frame_time_ms
        self.timer = QTimer()
        self.timer.timeout.connect(self.do_loop)

        self.start_loop()

    def start_loop(self):
        self.timer.start(self.time)

    def do_loop(self):
        """
        The single source of truth. Loops through and safely runs all registered
        functions in a single pass.
        """
        self.dispatch()

    def stop_loop(self):
        self.timer.stop()

    def delete(self):
        self.stop_loop()
        super().delete()
