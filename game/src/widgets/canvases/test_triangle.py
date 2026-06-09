from .core.canvas import Canvas
from customtkinter import CTkFrame
from ...app_core.context import Context


class TriangleCanvas(Canvas):
    '''
    Canvas that demonstrates/tests the canvas, camera, drawing, and transforms classes
    '''

    def __init__(self, master: CTkFrame, context: Context):

        # Create the canvas widget
        super().__init__(master, context, ((-5,-5),(5,5)))

        def frame_callback():
            self.delete("all")
            self.draw.test_triangle()
        self.set_frame_callback(frame_callback)
        self.start_animation()