from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QWidget

from ....app_core import Context
from .draw import Draw
from .camera import Camera
from typing import Callable

class StripChartBase(QWidget):
    '''
    Base class for specialized canvas widgets with stripchart-type sizing and camera rules.
    Special behavior is defined here, then activated in the specialized canvas.

    Draws fresh every frame via paintEvent - unlike the old CTkCanvas version,
    there's no item-pooling optimization here (see time_core/draw.py's
    docstring): QPainter has none of Tcl's per-item creation overhead that
    made reusing drawn items across frames worthwhile.
    '''

    def __init__(self, master: QWidget, context: Context, grid_position: tuple[int, int], time_scale: list[float] | None = None, time_offset: list[float] | None = None):
        # Each caller that doesn't explicitly want to share a time reference
        # with other strip charts needs its own fresh list here - a mutable
        # default argument would instead be the one list object shared by
        # every StripChartBase built without an explicit time_scale/time_offset,
        # silently coupling their pan/zoom state together.
        if time_scale is None:
            time_scale = [0.0]
        if time_offset is None:
            time_offset = [0.0]

        super().__init__()
        self.context = context
        master.grid_layout.addWidget(self, grid_position[0], grid_position[1])

        # Make a Camera that tracks time scaling and offset. Mouse/wheel event
        # handlers below (this widget's, not the camera's own - see Camera's
        # docstring) change the values, Draw methods use the values in transform functions
        self.camera = Camera(self, context, time_scale, time_offset)

        # Make a drawing object for this canvas - will be used in child canvases
        self.do_animation_loop = False
        self.frame_callback = None
        self.draw = Draw(self, context, self.camera)
        self.painter: QPainter | None = None  # live only during paintEvent

        # Track the cursor for the crosshairs hover effect. This only records the
        # position - it does NOT trigger a redraw itself. Mouse movement can fire many
        # times per second, and a full canvas redraw (axes/ticks/labels/lines) on
        # every one of those would be wasted work between animation ticks - the
        # existing ~10fps animation loop picks up the latest position on its next tick.
        self.hover_pos = None
        self.setMouseTracking(True)

        # A bare QWidget has no natural size of its own, unlike the old
        # CTkCanvas - without this, stacking several of these in an
        # unweighted grid row (see defender_stripchart_panel) collapses
        # them to near-zero height.
        self.setMinimumHeight(200)

# --------------------------------------------------------------------------------------------------------------------------
#                                                       Animation Controls
# --------------------------------------------------------------------------------------------------------------------------

    def set_frame_callback(self, frame_callback: Callable[[], None]):
        self.frame_callback = frame_callback


    def run_frame(self):
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

    def resizeEvent(self, event):
        if self.frame_callback is not None and self.do_animation_loop:
            self.camera.reset_camera()
            self.camera.update_padding()
        super().resizeEvent(event)

    def start_animation(self, framerate_ms: float = 100):
        self.framerate_ms = framerate_ms
        self.do_animation_loop = True
        # id(self) keeps this key unique per widget instance - a grid row/position
        # is only unique within one panel, and different panels (e.g. the variable
        # monitor and the network diagram) both start numbering their charts at row 0,
        # which previously made their callbacks silently overwrite each other.
        self.context.animation_manager.add_callback(f"{self.__class__.__name__}_{id(self)}", self.update)



    def stop_animation(self):
        self.do_animation_loop = False
        self.context.animation_manager.remove_callback(f"{self.__class__.__name__}_{id(self)}")

# --------------------------------------------------------------------------------------------------------------------------
#                                                       Mouse / wheel
# --------------------------------------------------------------------------------------------------------------------------
# Left-drag pans, shift+wheel zooms, middle/right click resets. Qt widgets
# own their event handling as overridden methods (rather than externally
# bound callbacks the way Tk's .bind() worked), so this is where Camera's
# pan/zoom/reset get called from now, translating Qt's event objects into
# the plain x/delta values Camera needs.

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.position()
            self.camera.click_callback(pos.x(), pos.y())
        elif event.button() in (Qt.MouseButton.MiddleButton, Qt.MouseButton.RightButton):
            self.camera.reset_camera()
            self.update()

    def mouseMoveEvent(self, event):
        pos = event.position()
        self.hover_pos = (pos.x(), pos.y())
        if event.buttons() & Qt.MouseButton.LeftButton:
            self.camera.do_pan(pos.x(), pos.y())
            self.update()

    def leaveEvent(self, event):
        self.hover_pos = None

    def wheelEvent(self, event):
        if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
            pos = event.position()
            self.camera.zoom(pos.x(), event.angleDelta().y())
            self.update()
        else:
            event.ignore()
