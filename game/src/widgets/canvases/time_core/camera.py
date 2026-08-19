from customtkinter import CTkCanvas
from ....app_core import Context
from . import transforms as t

# Pixels used to draw one second of time when time_scale is at its default (1.0)
PIXELS_PER_SECOND = 20.0

class Camera:

    def __init__(self, canvas: CTkCanvas, context: Context, time_scale: list[float], time_offset: list[float]):
        '''
        Tracks axis scaling and transforms. Uses a shared time_sync_ptr to synchronize time scaling and offset across multiple canvases.
        '''
        self.canvas = canvas

        self.time_scale = time_scale
        self.time_offset = time_offset
        self.vertical_scale = 1.0

        self.time_scale[0] = 1.0
        self.time_offset[0] = 0.0
        self.vertical_scale = 1.0

        self.vertical_offset = 0.0
        self.padding = 0
        self.update_padding() #Set padding based of canvas size

        # Padding reserved on each edge for axes, ticks, numbers, and labels.
        # left/top/bottom are recomputed every frame by Draw (they depend on
        # font metrics and, for the left edge, the widest visible number).
        self.padding_left = self.padding
        self.padding_right = self.padding
        self.padding_top = self.padding
        self.padding_bottom = self.padding

        # Starting position for each mouse pan event - panning moves the time offset and vertical scale
        self.pan_start = [0.0, 0.0]

        # Bind events
        self.canvas.bind("<ButtonPress-1>", self.click_callback)
        self.canvas.bind("<B1-Motion>", self.do_pan)
            # Windows / Mac
        self.canvas.bind("<Shift-MouseWheel>", self.zoom)
            # Linux
        self.canvas.bind("<Shift-Button-4>", self.zoom)
        self.canvas.bind("<Shift-Button-5>", self.zoom)
        # canvas.scale("all", x_zoom, y_zoom, factor, factor)  # <--- only useful for already drawn canvases
        self.canvas.bind("<Button-2>", self.reset_camera)      # Windows/Linux
        self.canvas.bind("<Button-3>", self.reset_camera)      # Mac sometimes uses Button-3

    def update_padding(self):
        base = min(self.canvas.winfo_width(), self.canvas.winfo_height())
        self.padding = max(base * 0.025, 10)

# --------------------------------------------------------------------------------------------------------------------------
#                                                       TRANSFORMERS
# --------------------------------------------------------------------------------------------------------------------------

    def plot_rect(self) -> tuple[float, float, float, float]:
        '''
        Returns (left, top, right, bottom) canvas pixel bounds of the plotting area,
        i.e. the canvas rectangle left over after reserving room for axes/labels.
        '''
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        left = self.padding_left
        top = self.padding_top
        right = w - self.padding_right
        bottom = h - self.padding_bottom
        return left, top, right, bottom

    def pixels_per_second(self) -> float:
        return PIXELS_PER_SECOND * self.time_scale[0]

    def time_to_canvas_x(self, time_value: float, now: float) -> float:
        '''
        Maps a data time (seconds) to a canvas x pixel. `now` is right-aligned to the
        right edge of the plot area, offset by any panning done by the user.
        '''
        _, _, right, _ = self.plot_rect()
        pps = self.pixels_per_second()
        return right + self.time_offset[0] + (time_value - now) * pps

    def canvas_x_to_time(self, x: float, now: float) -> float:
        _, _, right, _ = self.plot_rect()
        pps = self.pixels_per_second()
        if pps == 0:
            return now
        return now + (x - right - self.time_offset[0]) / pps

    def value_to_canvas_y(self, value: float, min_v: float, max_v: float) -> float:
        '''
        Maps a (unit-scaled) data value to a canvas y pixel, min_v at the bottom of
        the plot area and max_v at the top.
        '''
        _, top, _, bottom = self.plot_rect()
        span = max_v - min_v
        if span == 0:
            return (top + bottom) / 2
        fraction = (value - min_v) / span
        return bottom - fraction * (bottom - top)

    def data_to_strip_chart(self, points_in: list[tuple[float, float]], now: float, factor: float, min_unit: float, max_unit: float) -> list[tuple[float, float]]:
        '''
        Transforms (time, raw_value) points into canvas pixel coordinates.
        '''
        out = []
        for time_value, value in points_in:
            x = self.time_to_canvas_x(time_value, now)
            y = self.value_to_canvas_y(value * factor, min_unit, max_unit)
            out.append((x, y))
        return out

# --------------------------------------------------------------------------------------------------------------------------
#                                                       EVENT CALLBACKS
# --------------------------------------------------------------------------------------------------------------------------

    def click_callback(self, event=None):
        self.pan_start = [event.x, event.y]

    def do_pan(self, event=None):
        # Calculate movement
        dx = event.x - self.pan_start[0]
        dy = event.y - self.pan_start[1]

        self.time_offset[0] += dx
        # self.vertical_scale += dy

        self.pan_start = [event.x, event.y]

        # Redraw for each mouse position
        # if self.canvas.frame_callback is not None:
        #     self.canvas.frame_callback()

    def apply_scale_about(self, C: tuple[float, float], k: float):
        # Changes scale and offset based on zoom event and direction
        cx, cy = C
        tx, ty = self.time_offset[0], 0.0

        self.time_scale[0] = k * self.time_scale[0]
        # self.vertical_scale = k * self.vertical_scale
        self.time_offset[0] = cx + k * (tx - cx)

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
        # if self.canvas.frame_callback is not None:
        #     self.canvas.frame_callback()

    def reset_camera(self, event=None):
        self.time_scale[0] = 1.0
        self.time_offset[0] = 0.0
        self.vertical_scale = 1.0
        # Redraw on reset scale
        # if self.canvas.frame_callback:
        #     self.canvas.frame_callback()  