from customtkinter import CTkCanvas, CTkFrame
from ....app_core.context import Context
from .draw import Draw
from .camera import Camera
from typing import Callable

class StripChart(CTkCanvas):
    '''
    Base class for specialized canvas widgets with stripchart-type sizing and camera rules
    Special behavior is defined here, then activated in the specialized canvas.
    It can grow to fit the variable.
    '''

    def __init__(self, master: CTkFrame, context: Context, time_scale: list[float] = [0.0], time_offset: list[float] = [0.0]):

        # Create and pack the canvas to fill its frame
        super().__init__(master)
        self.pack(side="top", fill="both", expand=True, pady=context.style.gap, padx=context.style.gap)

        # Make a Camera that tracks time scaling and offset. Canvas events change the values, Draw methods use the values in transform functions
        self.camera = Camera(self, context, time_scale, time_offset)

        # Make a drawing object for this canvas - will be used in child canvases
        self.do_animation_loop = False
        self.frame_callback = None
        self.draw = Draw(self, context, self.camera)

        # Redraw the canvas when it gets resized
        self.bind("<Configure>", self.resize_handler)


# --------------------------------------------------------------------------------------------------------------------------
#                                                       Animation Controls
# --------------------------------------------------------------------------------------------------------------------------
    
    def set_frame_callback(self, frame_callback: Callable[[], None]):
        self.frame_callback = frame_callback


    def resize_handler(self, event=None):
        if self.frame_callback is not None and self.do_animation_loop:
            self.camera.reset_camera()
            self.camera.update_padding()
            self.frame_callback()