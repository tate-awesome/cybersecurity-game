from customtkinter import CTkCanvas, CTkFrame
from ....app_core import Context
from .draw import Draw
from .camera import Camera
from ..pooled_canvas import PooledCanvasMixin
from typing import Callable

class Canvas(PooledCanvasMixin, CTkCanvas):
    '''
    Base class for specialized canvas widgets with worldspace, animations, and cameras.
    Special behavior is defined here, then activated in the specialized canvas.
    Canvases
    '''

    def __init__(self, master: CTkFrame, context: Context, world_bounds: tuple[tuple[float,float],tuple[float,float]] = ((0.0, 0.0), (0.0, 0.0))):
        '''
        world_bounds defines the world-space domain that the frame_callback will try to draw stuff in.
        Consider the range of values from the context.buffer
        The world position should be relatable to canvas position
        For example:    the frame_callback will draw every boat inside [(0, 0), (200, 200)] - world coordinates
        and:            the frame_callback will draw the past theta values inside [(0, -180), (100, 180)] - graph domains
        and:            the frame_callback will draw the network picture inside [(0, 0), (100, 100)] - arbitrary drawing space
        '''

        # Create and pack the canvas to fill its frame
        super().__init__(master)
        self.pack(side="top", fill="both", expand=True, pady=context.style.gap, padx=context.style.gap)
        self.context = context
        self._pool_setup()

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


    def run_frame(self):
        '''
        Runs one frame_callback invocation, reusing this canvas's existing
        items across the call (see PooledCanvasMixin) instead of the old
        delete("all")-then-recreate-everything pattern. Centralized here
        (rather than in each frame_callback) so every path that can trigger
        a redraw - the animation loop and a manual resize - reconciles the
        item pool the same way.
        '''
        if self.frame_callback is None:
            return
        self.begin_frame()
        try:
            self.frame_callback()
        finally:
            self.end_frame()


    def start_animation(self, framerate_ms: float = 50):
        self.framerate_ms = framerate_ms
        self.do_animation_loop = True
        self.context.animation_manager.add_callback(self.__class__.__name__, self.run_frame)


    def stop_animation(self):
        self.do_animation_loop = False
        self.context.animation_manager.remove_callback(self.__class__.__name__)


    def resize_handler(self, event=None):
        # if self.frame_callback is not None and self.do_animation_loop:
        self.camera.reset_scale()
        self.camera.update_padding()
        self.run_frame()