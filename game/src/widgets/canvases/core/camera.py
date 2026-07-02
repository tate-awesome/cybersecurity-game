from customtkinter import CTkCanvas
from ....app_core.context import Context
from . import transforms as t

class Camera:

    def __init__(self, canvas: CTkCanvas, context: Context, world_bounds: tuple[tuple[float,float],tuple[float,float]] = ((0.0, 0.0), (0.0, 0.0))):
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

        # Bind events
        self.canvas.bind("<ButtonPress-1>", self.click_callback)
        self.canvas.bind("<B1-Motion>", self.do_pan)
            # Windows / Mac
        self.canvas.bind("<MouseWheel>", self.zoom)
            # Linux
        self.canvas.bind("<Button-4>", self.zoom)
        self.canvas.bind("<Button-5>", self.zoom)
        # canvas.scale("all", x_zoom, y_zoom, factor, factor)  # <--- only useful for already drawn canvases
        self.canvas.bind("<Button-2>", self.reset_scale)      # Windows/Linux
        self.canvas.bind("<Button-3>", self.reset_scale)      # Mac sometimes uses Button-3

    def update_padding(self):
        base = min(self.canvas.winfo_width(), self.canvas.winfo_height())
        self.padding = max(base * 0.025, 10)

# --------------------------------------------------------------------------------------------------------------------------
#                                                       TRANSFORMERS
# --------------------------------------------------------------------------------------------------------------------------

    def world_to_canvas(self, points_in: list[tuple[float, float]]) -> list[tuple[float, float]]:
        canvas_fit = t.padded_fit_uniform(points_in, self.world_bounds[0], self.world_bounds[1], self.canvas, self.padding)
        camera_transformed = t.zoom_and_pan(canvas_fit, self.scale, self.offset)
        return camera_transformed

    def canvas_to_world(self, points_in: list[tuple[float, float]]) -> list[tuple[float, float]]:
        camera_undone = t.zoom_and_pan_reverse(points_in, self.scale, self.offset)
        canvas_undone = t.padded_fit_uniform_reverse(camera_undone, self.world_bounds[0], self.world_bounds[1], self.canvas, self.padding)
        return canvas_undone

    def data_to_strip_chart(self, points_in: list[tuple[float, float]]) -> list[tuple[float, float]]:
        chart_fit = t.padded_fit_vertical_snap_right(points_in, self.canvas, self.padding)
        time_scaled = t.zoom_and_pan_horizontal(chart_fit, self.scale, self.offset)
        return time_scaled

# --------------------------------------------------------------------------------------------------------------------------
#                                                       EVENT CALLBACKS
# --------------------------------------------------------------------------------------------------------------------------

    def click_callback(self, event=None):
        print(f"Raw: {event.x}, {event.y}")
        raw_points = [(event.x, event.y)]
        world_points = self.canvas_to_world(raw_points)
        x = world_points[0][0]
        y = world_points[0][1]
        print(f"World: {x}, {y}")
        self.pan_start = [event.x, event.y]

    def do_pan(self, event=None):
        # Calculate movement
        dx = event.x - self.pan_start[0]
        dy = event.y - self.pan_start[1]

        self.offset[0] += dx
        self.offset[1] += dy

        self.pan_start = [event.x, event.y]

        # Redraw for each mouse position
        if self.canvas.frame_callback is not None:
            self.canvas.frame_callback()

    def apply_scale_about(self, C: tuple[float, float], k: float):
        # Changes scale and offset based on zoom event and direction
        cx, cy = C
        tx, ty = self.offset

        self.scale = k * self.scale
        self.offset = [
        cx + k * (tx - cx),
        cy + k * (ty - cy),
        ]

    # Zoom
    def zoom(self, event):
        # Determine zoom direction
        if event.delta > 0:
            factor = 1.1
        else:
            factor = 0.9
        if hasattr(event, "num"):
            if event.num == 4:
                factor = 1.1
            elif event.num == 5:
                factor = 0.9

        # Clamp scale?
        # if not (0.2 <= new_scale <= 5.0):
        #     return

        x_focus = self.canvas.canvasx(event.x)
        y_focus = self.canvas.canvasy(event.y)
        self.apply_scale_about((x_focus,y_focus), factor)

        # Redraw for each zoom scroll
        if self.canvas.frame_callback is not None:
            self.canvas.frame_callback()

    def reset_scale(self, event=None):
        self.scale = 1.0
        self.offset = [0, 0]
        # Redraw on reset scale
        if self.canvas.frame_callback is not None:
            self.canvas.frame_callback()  