from ....app_core import Context
from . import transforms as t
from ....geometry import apply_scale_about

class Camera:

    def __init__(self, canvas, context: Context, world_bounds: tuple[tuple[float,float],tuple[float,float]] = ((0.0, 0.0), (0.0, 0.0))):
        '''
        Tracks virtual camera movement: zoom and pan
        '''
        self.canvas = canvas
        self.world_bounds = world_bounds
        self.padding = 0
        self.update_padding()

        # Current Camera zoom (accessed by Draw)
        self.scale = 1.0

        # Current "Camera" offset (accessed by Draw)
        self.offset = [0.0, 0.0]

        # Starting position for each mouse pan event
        self.pan_start = [0.0, 0.0]

    def update_padding(self):
        base = min(self.canvas.width(), self.canvas.height())
        self.padding = max(base * 0.025, 10)

# --------------------------------------------------------------------------------------------------------------------------
#                                                       TRANSFORMERS
# --------------------------------------------------------------------------------------------------------------------------

    def world_to_canvas(self, points_in: list[tuple[float, float]]) -> list[tuple[float, float]]:
        canvas_fit = t.padded_fit_uniform(points_in, self.world_bounds[0], self.world_bounds[1], self.canvas, self.padding)
        camera_transformed = t.zoom_and_pan(canvas_fit, self.scale, (self.offset[0], self.offset[1]))
        return camera_transformed

    def canvas_to_world(self, points_in: list[tuple[float, float]]) -> list[tuple[float, float]]:
        camera_undone = t.zoom_and_pan_reverse(points_in, self.scale, (self.offset[0], self.offset[1]))
        canvas_undone = t.padded_fit_uniform_reverse(camera_undone, self.world_bounds[0], self.world_bounds[1], self.canvas, self.padding)
        return canvas_undone

# --------------------------------------------------------------------------------------------------------------------------
#                                                       EVENT CALLBACKS
# --------------------------------------------------------------------------------------------------------------------------
# Called by the owning widget's mouse/wheel event handlers (see Canvas),
# which translate Qt's event objects into the plain x/y/delta values these
# need - unlike the old Tk version, this class no longer binds to widget
# events itself, since Qt widgets own their event handling as overridden
# methods rather than externally bound callbacks.

    def click_callback(self, x: float, y: float):
        self.pan_start = [x, y]

    def do_pan(self, x: float, y: float):
        dx = x - self.pan_start[0]
        dy = y - self.pan_start[1]

        self.offset[0] += dx
        self.offset[1] += dy

        self.pan_start = [x, y]

    def apply_scale_about(self, C: tuple[float, float], k: float):
        # Changes scale and offset based on zoom event and direction
        new_scale, new_offset = apply_scale_about(self.scale, (self.offset[0], self.offset[1]), C, k)
        self.scale = new_scale
        self.offset = list(new_offset)

    def zoom(self, x: float, y: float, delta: float):
        factor = 1.1 if delta > 0 else 0.9
        self.apply_scale_about((x, y), factor)

    def reset_scale(self):
        self.scale = 1.0
        self.offset = [0, 0]
