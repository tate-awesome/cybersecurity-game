from customtkinter import CTkCanvas, CTkFrame
from ....app_core.context import Context
from .draw import Draw
from .camera import Camera
from typing import Callable

class Canvas(CTkCanvas):
    '''
    Base class for specialized canvas widgets with cameras and events stuff.
    Special behavior is defined here, then activated in the specialized canvas.
    Canvases
    '''

    def __init__(self, master: CTkFrame, context: Context, world_bounds: tuple[tuple[float,float],tuple[float,float]] = ((0.0, 0.0), (0.0, 0.0))):
        '''
        world_bounds defines the world-space domain that the frame_callback will try to draw stuff in.
        Consider the range of values from the context.net.data_buffer
        The world position should be relatable to canvas position
        For example:    the frame_callback will draw every boat inside [(0, 0), (200, 200)] - world coordinates
        and:            the frame_callback will draw the past theta values inside [(0, -180), (100, 180)] - graph domains
        and:            the frame_callback will draw the network picture inside [(0, 0), (100, 100)] - arbitrary drawing space
        '''

        # Create and pack the canvas to fill its frame
        super().__init__(master)
        self.pack(side="top", fill="both", expand=True, pady=context.style.gap, padx=context.style.gap)

        # Make a Camera that tracks panning and zooming and maps. Canvas events change the values, Draw methods use the values
        self.camera = Camera(self, context, world_bounds)

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


    def start_animation(self, framerate_ms: float = 50):
        self.framerate_ms = framerate_ms
        self.do_animation_loop = True
        self.animation_loop()

    
    def animation_loop(self):
        if self.frame_callback is not None:
            self.frame_callback()
            if self.do_animation_loop:
                self.after_id = self.after(self.framerate_ms, self.animation_loop)


    def stop_animation(self):
        self.do_animation_loop = False
        if self.after_id is not None:
            self.after_cancel(self.after_id)
            self.after_id = None


    def resize_handler(self, event=None):
        if self.frame_callback is not None and self.do_animation_loop:
            self.camera.reset_scale()
            self.camera.update_padding()
            self.frame_callback()