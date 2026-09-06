'''
Handles drawing to the map.
'''

from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QWidget
from threading import Lock
from typing import Callable
from ..app_core import Context
from ..geometry import apply_scale_about
import time


class _MapCanvas(QWidget):
    '''
    Draws fresh every frame via paintEvent - see core/draw.py's docstring
    for why the old CTkCanvas/PooledCanvasMixin item-pooling optimization
    isn't needed under Qt.
    '''

    def __init__(self, owner: "Map"):
        super().__init__()
        self._owner = owner
        self.painter: QPainter | None = None
        self.setMouseTracking(True)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        self.painter = painter
        try:
            self._owner.run_frame()
        finally:
            painter.end()
            self.painter = None

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.position()
            self._owner.start_pan(pos.x(), pos.y())
        elif event.button() in (Qt.MouseButton.MiddleButton, Qt.MouseButton.RightButton):
            self._owner.reset_view()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            pos = event.position()
            self._owner.do_pan(pos.x(), pos.y())

    def wheelEvent(self, event):
        pos = event.position()
        self._owner.zoom(pos.x(), pos.y(), event.angleDelta().y())


class Map:

    def __init__(self, parent: QWidget, context: Context, draw_callback: Callable, framerate_ms: float, padding: float=20, margin: float=40):
        # zoom/pan persistent values
        self.scale = 1.0
        self.offset = [0.0, 0.0]
        self.x_pan_start = 0.0
        self.y_pan_start = 0.0

        # Padding for world plane
        self.padding = padding
        self.margin = margin

        # Assign variables
        self.context = context
        self.parent = parent
        self.draw_callback = draw_callback
        self.framerate_ms = framerate_ms
        self.draw_lock = Lock()

        # Create canvas
        self.canvas = _MapCanvas(self)
        parent.layout().addWidget(self.canvas)

        # Start animation loop - registered with the shared animation_manager
        # (instead of a raw self-rescheduling canvas.after() loop) so a
        # destroyed frame or a raising draw_callback can't leave an unguarded,
        # un-stoppable loop running, and so it's cleaned up automatically on
        # page exit/refresh like every other canvas's animation. The manager
        # ticks every callback at its own fixed rate, so this throttles itself
        # internally to still only actually redraw every framerate_ms.
        self._last_draw_time = 0.0
        def frame_callback():
            now = time.monotonic()
            if now - self._last_draw_time < self.framerate_ms / 1000.0:
                return
            self._last_draw_time = now
            self.canvas.update()
        self.frame_callback = frame_callback
        self.context.animation_manager.add_callback(f"Map_{id(self)}", frame_callback)

    def run_frame(self):
        '''
        Runs draw_callback once. Called from the canvas's paintEvent, which
        gives it a live QPainter (canvas.painter) to draw through.
        '''
        self.draw_callback(self.canvas, self.draw_lock, self.scale, self.offset)

    def start_pan(self, x: float, y: float):
        self.x_pan_start = x
        self.y_pan_start = y

    def do_pan(self, x: float, y: float):
        dx = x - self.x_pan_start
        dy = y - self.y_pan_start

        self.offset[0] += dx
        self.offset[1] += dy

        self.x_pan_start = x
        self.y_pan_start = y

        self.canvas.update()

    def apply_scale_about(self, C: tuple[float, float], k: float):
        # Changes scale and offset based on zoom event and direction
        new_scale, new_offset = apply_scale_about(self.scale, (self.offset[0], self.offset[1]), C, k)
        self.scale = new_scale
        self.offset = list(new_offset)

    # Zoom
    def zoom(self, x: float, y: float, delta: float):
        factor = 1.1 if delta > 0 else 0.9
        self.apply_scale_about((x, y), factor)
        self.canvas.update()

    def reset_scale(self):
        self.scale = 1.0
        self.offset = [0, 0]

    def reset_view(self):
        self.reset_scale()
        self.canvas.update()
