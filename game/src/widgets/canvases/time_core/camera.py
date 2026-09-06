from ....app_core import Context
from . import transforms as t

# Pixels used to draw one second of time when time_scale is at its default (1.0)
PIXELS_PER_SECOND = 20.0

class Camera:

    def __init__(self, canvas, context: Context, time_scale: list[float], time_offset: list[float]):
        '''
        Tracks axis scaling and transforms. Uses a shared time_sync_ptr to synchronize time scaling and offset across multiple canvases.
        '''
        self.canvas = canvas
        self.context = context

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

        # Starting position for each mouse pan event - panning moves the time offset
        self.pan_start = [0.0, 0.0]

    def update_padding(self):
        base = min(self.canvas.width(), self.canvas.height())
        self.padding = max(base * 0.025, 10)

# --------------------------------------------------------------------------------------------------------------------------
#                                                       TRANSFORMERS
# --------------------------------------------------------------------------------------------------------------------------

    def plot_rect(self) -> tuple[float, float, float, float]:
        '''
        Returns (left, top, right, bottom) canvas pixel bounds of the plotting area,
        i.e. the canvas rectangle left over after reserving room for axes/labels.
        '''
        w = self.canvas.width()
        h = self.canvas.height()
        left = self.padding_left
        top = self.padding_top
        right = w - self.padding_right
        bottom = h - self.padding_bottom
        return left, top, right, bottom

    def pixels_per_second(self) -> float:
        return PIXELS_PER_SECOND * self.time_scale[0]

    def is_fit_mode(self) -> bool:
        value = self.context.states.get("fit_stripchart_line")
        return value == 1 or value == "1"

    def time_to_canvas_x(self, time_value: float, now: float, pixels_per_second: float = None, time_offset: float = None) -> float:
        '''
        Maps a data time (seconds) to a canvas x pixel. `now` is right-aligned to the
        right edge of the plot area, offset by any panning done by the user.
        pixels_per_second/time_offset can be overridden (e.g. by fit mode) without
        touching the camera's own pan/zoom state.
        '''
        _, _, right, _ = self.plot_rect()
        pps = self.pixels_per_second() if pixels_per_second is None else pixels_per_second
        offset = self.time_offset[0] if time_offset is None else time_offset
        return right + offset + (time_value - now) * pps

    def canvas_x_to_time(self, x: float, now: float, pixels_per_second: float = None, time_offset: float = None) -> float:
        _, _, right, _ = self.plot_rect()
        pps = self.pixels_per_second() if pixels_per_second is None else pixels_per_second
        if pps == 0:
            return now
        offset = self.time_offset[0] if time_offset is None else time_offset
        return now + (x - right - offset) / pps

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

    def data_to_strip_chart(self, points_in: list[tuple[float, float]], now: float, factor: float, min_unit: float, max_unit: float, pixels_per_second: float = None, time_offset: float = None) -> list[tuple[float, float]]:
        '''
        Transforms (time, raw_value) points into canvas pixel coordinates.
        '''
        out = []
        for time_value, value in points_in:
            x = self.time_to_canvas_x(time_value, now, pixels_per_second, time_offset)
            y = self.value_to_canvas_y(value * factor, min_unit, max_unit)
            out.append((x, y))
        return out

# --------------------------------------------------------------------------------------------------------------------------
#                                                       EVENT CALLBACKS
# --------------------------------------------------------------------------------------------------------------------------
# Called by the owning widget's mouse/wheel event handlers (see
# StripChartBase), which translate Qt's event objects into the plain
# x/delta values these need - unlike the old Tk version, this class no
# longer binds to widget events itself, since Qt widgets own their event
# handling as overridden methods rather than externally bound callbacks.

    def click_callback(self, x: float, y: float):
        if self.is_fit_mode():
            return
        self.pan_start = [x, y]

    def do_pan(self, x: float, y: float):
        if self.is_fit_mode():
            return
        dx = x - self.pan_start[0]
        self.time_offset[0] += dx
        self.pan_start = [x, y]

    def apply_scale_about(self, cx: float, k: float):
        # Changes scale and offset based on zoom event and direction
        tx = self.time_offset[0]
        self.time_scale[0] = k * self.time_scale[0]
        self.time_offset[0] = cx + k * (tx - cx)

    def zoom(self, x: float, delta: float):
        if self.is_fit_mode():
            return
        factor = 1.1 if delta > 0 else 0.9
        self.apply_scale_about(x, factor)

    def reset_camera(self):
        self.time_scale[0] = 1.0
        self.time_offset[0] = 0.0
        self.vertical_scale = 1.0
