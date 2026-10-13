import time

from PySide6.QtCore import Qt, QTimer
from .callback_registry import CallbackRegistry

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .performance import Performance


class AnimationManager(CallbackRegistry):
    '''
    Global manager for animation loops. A single QTimer is more performant than a timer for every canvas.
    Its rate is the UI framerate setting (see Performance.ui_fps), and
    while Performance is measuring, each pass is timed - see do_loop.
    '''
    def __init__(self, root, frame_time_ms: int = 100, performance: "Performance | None" = None):
        super().__init__(root, tag="[Animation]")
        self.time = frame_time_ms
        self.performance = performance
        self.last_tick: float | None = None
        self.timer = QTimer()
        # Qt's default coarse timer rounds to the OS timer step (~15.6 ms on
        # Windows), so every frame ran late - 30 fps came out at ~21
        self.timer.setTimerType(Qt.TimerType.PreciseTimer)
        self.timer.timeout.connect(self.do_loop)

        self.start_loop()

    def start_loop(self):
        self.timer.start(self.time)

    def set_frame_time(self, frame_time_ms: int):
        '''Changes the tick rate - takes effect at once if the loop is running.'''
        self.time = frame_time_ms
        if self.timer.isActive():
            self.timer.start(self.time)

    def do_loop(self):
        """
        The single source of truth. Loops through and safely runs all registered
        functions in a single pass.
        """
        performance = self.performance
        if performance is None or not performance.measuring:
            self.last_tick = None
            self.dispatch()
            return
        started = time.perf_counter()
        if self.last_tick is not None:
            performance.record_value("late", max(0.0, (started - self.last_tick) * 1000 - self.time), started)
        self.last_tick = started

        def timed(name: str, callback_started: float):
            performance.record(f"callback:{performance.group(name)}", callback_started)
        self.dispatch(timed=timed)
        performance.record("tick", started)

    def stop_loop(self):
        self.timer.stop()

    def delete(self):
        self.stop_loop()
        super().delete()
