from customtkinter import CTkCanvas, CTkFrame
from ....app_core import Context
from .draw import Draw
from .camera import Camera
from ..pooled_canvas import PooledCanvasMixin
from typing import Callable

class StripChartBase(PooledCanvasMixin, CTkCanvas):
    '''
    Base class for specialized canvas widgets with stripchart-type sizing and camera rules
    Special behavior is defined here, then activated in the specialized canvas.
    It can grow to fit the variable.
    '''

    def __init__(self, master: CTkFrame, context: Context, grid_position: tuple[int, int], time_scale: list[float] | None = None, time_offset: list[float] | None = None):
        # Each caller that doesn't explicitly want to share a time reference
        # with other strip charts needs its own fresh list here - a mutable
        # default argument would instead be the one list object shared by
        # every StripChartBase built without an explicit time_scale/time_offset,
        # silently coupling their pan/zoom state together.
        if time_scale is None:
            time_scale = [0.0]
        if time_offset is None:
            time_offset = [0.0]

        # Create and pack the canvas to fill its frame
        super().__init__(master)
        self.context = context
        self._pool_setup()
        self.grid(row=grid_position[0], column=grid_position[1], sticky="nsew", pady=context.style.gap, padx=context.style.gap)

        # Make a Camera that tracks time scaling and offset. Canvas events change the values, Draw methods use the values in transform functions
        self.camera = Camera(self, context, time_scale, time_offset)

        # Make a drawing object for this canvas - will be used in child canvases
        self.do_animation_loop = False
        self.frame_callback = None
        self.draw = Draw(self, context, self.camera)

        # Redraw the canvas when it gets resized
        self.bind("<Configure>", self.resize_handler)

        # Track the cursor for the crosshairs hover effect. This only records the
        # position - it does NOT trigger a redraw itself. <Motion> can fire many
        # times per second, and a full canvas redraw (axes/ticks/labels/lines) on
        # every one of those would be far more expensive than just letting the
        # existing ~10fps animation loop pick up the latest position on its next tick.
        self.hover_pos = None
        self.bind("<Motion>", self.hover_handler)
        self.bind("<Leave>", self.leave_handler)

    def hover_handler(self, event=None):
        self.hover_pos = (event.x, event.y)

    def leave_handler(self, event=None):
        self.hover_pos = None


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


    def resize_handler(self, event=None):
        if self.frame_callback is not None and self.do_animation_loop:
            self.camera.reset_camera()
            self.camera.update_padding()
            self.run_frame()

    def start_animation(self, framerate_ms: float = 100):
        self.framerate_ms = framerate_ms
        self.do_animation_loop = True
        # id(self) keeps this key unique per widget instance - a grid row/position
        # is only unique within one panel, and different panels (e.g. the variable
        # monitor and the network diagram) both start numbering their charts at row 0,
        # which previously made their callbacks silently overwrite each other.
        self.context.animation_manager.add_callback(f"{self.__class__.__name__}_{id(self)}", self.run_frame)



    def stop_animation(self):
        self.do_animation_loop = False
        self.context.animation_manager.remove_callback(f"{self.__class__.__name__}_{id(self)}")