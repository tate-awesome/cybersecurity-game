from customtkinter import CTkCanvas
from....app_core import Context
from .camera import Camera
from . import transforms as t
import math, time

# Layout constants for strip chart axes
TICK_LENGTH = 5
LABEL_GAP = 4
MIN_TIME_LABEL_SPACING_PX = 60
Y_TARGET_TICK_COUNT = 5
TIME_STEP_CANDIDATES = [0.1, 0.25, 0.5, 1, 2, 5, 10, 15, 30, 60, 120, 300, 600, 900, 1800, 3600, 7200, 14400]

class StripChartLayout:
    '''
    Everything needed to draw one frame of a strip chart, computed once per frame
    so the axes, ticks, numbers, labels, and data lines all agree on where things go.
    '''
    def __init__(self, now, t_min, t_max, min_unit, max_unit, x_ticks, y_ticks, left, top, right, bottom):
        self.now = now
        self.t_min = t_min
        self.t_max = t_max
        self.min_unit = min_unit
        self.max_unit = max_unit
        self.x_ticks = x_ticks  # list of (canvas_x, label)
        self.y_ticks = y_ticks  # list of (canvas_y, label)
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

class Draw:
    '''
    Contains helper functions for drawing objects in world space.
    Has access to the canvas and camera
    '''
    def __init__(self, canvas: CTkCanvas, context: Context, camera: Camera):
        self.canvas = canvas
        self.camera = camera
        self.context = context

    def background(self, color: str):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        self.canvas.create_rectangle(0, 0, w, h, fill=color)

    def line(self, points: list[tuple[float, float]], line_color: str, thickness=2):
        '''
        Draws a line connecting the points
        '''
        if len(points) < 2:
            return
        self.canvas.create_line(points, width=1, fill=line_color)

# --------------------------------------------------------------------------------------------------------------------------
#                                                       STRIP CHART AXES
# --------------------------------------------------------------------------------------------------------------------------

    def strip_chart_layout(self, history_lists: list[list[tuple[float, float]]], factor: float) -> StripChartLayout:
        '''
        Computes the plot area, x (time) ticks, and y (value) ticks for this frame.
        Time scaling/offset are resolved first to find the visible time window, then
        the value axis is autoscaled to whatever data falls inside that window.
        '''
        camera = self.camera

        # History timestamps are seconds since the first captured packet (see
        # MetaPacket), not wall-clock epoch time - convert "now" into that same
        # coordinate space so it lines up with the data.
        first_packet_time = self.context.net.buffer.packets.first_packet_time
        now = 0.0 if first_packet_time is None else time.time() - first_packet_time

        number_font = self.context.style.get_font("chart_numbers")
        label_font = self.context.style.get_font("chart_label")
        title_font = self.context.style.get_font("chart_title")

        number_height = number_font.metrics("linespace")
        label_height = label_font.metrics("linespace")
        title_height = title_font.metrics("linespace")

        w = self.canvas.winfo_width()

        # Top/right/bottom padding only depend on font metrics, so they can be set directly.
        camera.padding_top = title_height + LABEL_GAP + label_height + LABEL_GAP
        camera.padding_bottom = TICK_LENGTH + LABEL_GAP + number_height + LABEL_GAP + label_height + LABEL_GAP
        camera.padding_right = max(w * 0.025, 10)

        # Left padding depends on the width of the widest visible number, which isn't
        # known until the value axis below is computed - so this frame uses last
        # frame's padding_left, and refreshes it at the end for the next frame.
        left, top, right, bottom = camera.plot_rect()

        # --- Time (x) axis ---
        pps = camera.pixels_per_second()
        step = t.choose_time_step(pps, MIN_TIME_LABEL_SPACING_PX, TIME_STEP_CANDIDATES)
        decimals = t.decimals_for_step(step)

        rel_left = camera.canvas_x_to_time(left, now) - now
        rel_right = camera.canvas_x_to_time(right, now) - now

        x_ticks = []
        first_tick = math.ceil(rel_left / step) * step
        tick_count = int((rel_right - first_tick) / step) + 2
        for i in range(max(tick_count, 0)):
            rel = first_tick + i * step
            if rel > rel_right + step * 0.5:
                break
            cx = camera.time_to_canvas_x(now + rel, now)
            x_ticks.append((cx, t.format_tick(rel, decimals)))

        t_min, t_max = now + rel_left, now + rel_right

        # --- Value (y) axis: autoscale using only points visible in the time window ---
        visible_units = []
        for points in history_lists:
            for point_time, value in points:
                if t_min <= point_time <= t_max:
                    visible_units.append(value * factor)

        if visible_units:
            y_tick_values, y_step = t.nice_ticks(min(visible_units), max(visible_units), Y_TARGET_TICK_COUNT)
        else:
            y_tick_values, y_step = t.nice_ticks(0.0, 1.0, Y_TARGET_TICK_COUNT)

        y_decimals = t.decimals_for_step(y_step)
        min_unit, max_unit = y_tick_values[0], y_tick_values[-1]

        y_labels = [t.format_tick(v, y_decimals) for v in y_tick_values]
        max_label_width = max((number_font.measure(s) for s in y_labels), default=0)
        camera.padding_left = LABEL_GAP + max_label_width + LABEL_GAP + TICK_LENGTH

        y_ticks = [(camera.value_to_canvas_y(v, min_unit, max_unit), s) for v, s in zip(y_tick_values, y_labels)]

        return StripChartLayout(now, t_min, t_max, min_unit, max_unit, x_ticks, y_ticks, left, top, right, bottom)

    def strip_chart_ticks(self, layout: StripChartLayout, tick_color="gray", gridlines: bool = False):
        '''
        Draws tick marks pointing from the axes to each number. If gridlines is True,
        the ticks are extended into full lines spanning the plot area instead.
        '''
        for cx, _ in layout.x_ticks:
            y_far = layout.top if gridlines else layout.bottom + TICK_LENGTH
            self.canvas.create_line(cx, layout.bottom, cx, y_far, fill=tick_color, width=1)

        for cy, _ in layout.y_ticks:
            x_far = layout.right if gridlines else layout.left - TICK_LENGTH
            self.canvas.create_line(layout.left, cy, x_far, cy, fill=tick_color, width=1)

    def strip_chart_axes(self, layout: StripChartLayout, axes_color="red"):
        # X-axis sits along the bottom of the plot area, Y-axis along the left
        self.canvas.create_line(layout.left, layout.bottom, layout.right, layout.bottom, fill=axes_color, width=2)
        self.canvas.create_line(layout.left, layout.top, layout.left, layout.bottom, fill=axes_color, width=2)

    def strip_chart_numbers(self, layout: StripChartLayout, number_color="black"):
        number_font = self.context.style.get_font("chart_numbers")

        for cx, label in layout.x_ticks:
            self.canvas.create_text(cx, layout.bottom + TICK_LENGTH + LABEL_GAP, text=label,
                                     fill=number_color, font=number_font, anchor="n")

        for cy, label in layout.y_ticks:
            # Left-aligned on the canvas edge, regardless of individual label width
            self.canvas.create_text(LABEL_GAP, cy, text=label,
                                     fill=number_color, font=number_font, anchor="w")

    def strip_chart_title(self, title: str, text_color="black"):
        title_font = self.context.style.get_font("chart_title")
        self.canvas.create_text(LABEL_GAP, LABEL_GAP, text=title, fill=text_color, font=title_font, anchor="nw")

    def strip_chart_axis_labels(self, layout: StripChartLayout, x_label: str, y_label: str, text_color="black"):
        label_font = self.context.style.get_font("chart_label")
        title_font = self.context.style.get_font("chart_title")
        number_font = self.context.style.get_font("chart_numbers")

        # Y-axis label sits below the title, still clear of the axis line/numbers below it
        title_height = title_font.metrics("linespace")
        self.canvas.create_text(LABEL_GAP, LABEL_GAP + title_height + LABEL_GAP, text=y_label,
                                 fill=text_color, font=label_font, anchor="nw")

        # X-axis label is centered under the plot area, below the tick numbers
        number_height = number_font.metrics("linespace")
        x_label_y = layout.bottom + TICK_LENGTH + LABEL_GAP + number_height + LABEL_GAP
        cx = (layout.left + layout.right) / 2
        self.canvas.create_text(cx, x_label_y, text=x_label, fill=text_color, font=label_font, anchor="n")

    def strip_chart_path(self, path_points: list[tuple[float, float]], layout: StripChartLayout, factor: float, path_color="red"):
        visible = [(pt, v) for pt, v in path_points if layout.t_min <= pt <= layout.t_max]
        if len(visible) < 2:
            return
        canvas_points = self.camera.data_to_strip_chart(visible, layout.now, factor, layout.min_unit, layout.max_unit)
        self.canvas.create_line(canvas_points, width=2, fill=path_color)