from .core.canvas import Canvas
from PySide6.QtWidgets import QWidget
from ...app_core import Context


class TriangleCanvas(Canvas):
    '''
    Canvas that demonstrates/tests the canvas, camera, drawing, and transforms classes
    '''

    def __init__(self, master: QWidget, context: Context):

        # Create the canvas widget
        super().__init__(master, context, ((-5,-5),(5,5)))

        def frame_callback():
            self.draw.test_triangle()
        self.set_frame_callback(frame_callback)
        self.start_animation()