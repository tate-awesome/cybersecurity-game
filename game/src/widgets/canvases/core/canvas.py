from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QWidget

from ....app_core import Context
from .draw import Draw
from .camera import Camera
from typing import Callable

class Canvas(QWidget):
    '''
    Base class for specialized canvas widgets with worldspace, animations, and cameras.
    Special behavior is defined here, then activated in the specialized canvas.
    Canvases

    Draws fresh every frame via paintEvent - see time_core/draw.py's
    docstring (the strip chart engine, converted first) for why the old
    CTkCanvas item-pooling optimization isn't needed under Qt: QPainter has
    none of Tcl's per-item creation overhead that made reusing drawn items
    across frames worthwhile.
    '''

    def __init__(self, master: QWidget, context: Context, world_bounds: tuple[tuple[float,float],tuple[float,float]] = ((0.0, 0.0), (0.0, 0.0))):
        '''
        world_bounds defines the world-space domain that the frame_callback will try to draw stuff in.
        Consider the range of values from the context.buffer
        The world position should be relatable to canvas position
        For example:    the frame_callback will draw every boat inside [(0, 0), (200, 200)] - world coordinates
        and:            the frame_callback will draw the past theta values inside [(0, -180), (100, 180)] - graph domains
        and:            the frame_callback will draw the network picture inside [(0, 0), (100, 100)] - arbitrary drawing space
        '''
        super().__init__()
        self.context = context
        master.layout().addWidget(self)

        # A bare QWidget has no natural size of its own, unlike the old
        # CTkCanvas - without a floor, one of these stacked alongside other
        # content in an unweighted layout can collapse to near-zero size
        # (see time_core/stripchart.py, where this exact thing happened).
        self.setMinimumSize(200, 200)

        # Make a Camera that tracks panning and zooming and maps. Mouse/wheel
        # event handlers below (this widget's, not the camera's own - Qt
        # widgets own their event handling as overridden methods rather than
        # externally bound callbacks) change the values, Draw methods use them
        self.camera = Camera(self, context, world_bounds)

        # Make a drawing object for this canvas - will be used in child canvases
        self.do_animation_loop = False
        self.frame_callback = None
        self.draw = Draw(self, context, self.camera)
        self.painter: QPainter | None = None  # live only during paintEvent


# --------------------------------------------------------------------------------------------------------------------------
#                                                       Animation Controls
# --------------------------------------------------------------------------------------------------------------------------

    def set_frame_callback(self, frame_callback: Callable[[], None]):
        self.frame_callback = frame_callback


    def run_frame(self):
        '''
        Runs one frame_callback invocation.
        '''
        if self.frame_callback is None:
            return
        self.frame_callback()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        self.painter = painter
        try:
            self.run_frame()
        finally:
            painter.end()
            self.painter = None

    def start_animation(self, framerate_ms: float = 50):
        self.framerate_ms = framerate_ms
        self.do_animation_loop = True
        self.context.animation_manager.add_callback(self.__class__.__name__, self.update)


    def stop_animation(self):
        self.do_animation_loop = False
        self.context.animation_manager.remove_callback(self.__class__.__name__)


    def resizeEvent(self, event):
        self.camera.reset_scale()
        self.camera.update_padding()
        super().resizeEvent(event)

# --------------------------------------------------------------------------------------------------------------------------
#                                                       Mouse / wheel
# --------------------------------------------------------------------------------------------------------------------------
# Left-drag pans, plain wheel zooms, middle/right click resets.

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.position()
            self.camera.click_callback(pos.x(), pos.y())
        elif event.button() in (Qt.MouseButton.MiddleButton, Qt.MouseButton.RightButton):
            self.camera.reset_scale()
            self.update()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            pos = event.position()
            self.camera.do_pan(pos.x(), pos.y())
            self.update()

    def wheelEvent(self, event):
        pos = event.position()
        self.camera.zoom(pos.x(), pos.y(), event.angleDelta().y())
        self.update()
