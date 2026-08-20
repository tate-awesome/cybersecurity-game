from customtkinter import CTkCanvas
from....app_core import Context
from .camera import Camera
from . import transforms as t
import math, time, bisect

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
    def __init__(self, now, wall_now, t_min, t_max, min_unit, max_unit, x_ticks, y_ticks, left, top, right, bottom, value_label, pixels_per_second, time_offset, time_decimals):
        self.now = now
        self.wall_now = wall_now  # real elapsed time, for labels - may differ from `now` (the geometry reference) in fit mode
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
        self.value_label = value_label  # most recent history value, formatted
        self.pixels_per_second = pixels_per_second  # x-axis scale actually used this frame (may be fit-mode's)
        self.time_offset = time_offset  # x-axis pixel offset actually used this frame
        self.time_decimals = time_decimals  # decimal places used for the current time tick resolution

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
        wall_now = 0.0 if first_packet_time is None else time.time() - first_packet_time
        # `now` is the geometry reference (where pixels come from) - normally the
        # same as wall_now, but fit mode freezes it to the latest sample's time so
        # the picture stops moving once data stops arriving. `wall_now` keeps
        # advancing regardless, so labels can still reflect real elapsed time even
        # while the picture is frozen (see the tick loop below).
        now = wall_now

        number_font = self.context.style.get_font("chart_numbers")
        label_font = self.context.style.get_font("chart_label")
        title_font = self.context.style.get_font("chart_title")

        number_height = number_font.metrics("linespace")
        label_height = label_font.metrics("linespace")
        title_height = title_font.metrics("linespace")

        w = self.canvas.winfo_width()

        # Top/right/bottom padding only depend on font metrics, so they can be set directly.
        # The header (units / title / value) is a single row, tall enough for the taller of its fonts.
        camera.padding_top = max(title_height, label_height) + LABEL_GAP * 2
        camera.padding_bottom = TICK_LENGTH + LABEL_GAP + number_height + LABEL_GAP + label_height + LABEL_GAP
        camera.padding_right = max(w * 0.025, 10)

        # Left padding depends on the width of the widest visible number, which isn't
        # known until the value axis below is computed - so this frame uses last
        # frame's padding_left, and refreshes it at the end for the next frame.
        left, top, right, bottom = camera.plot_rect()

        # --- Time (x) axis ---
        # Fit mode overrides the usual zoom/pan-driven time axis: it scales/shifts the
        # x-axis (without touching the camera's own zoom/pan state) so the history
        # exactly fills the plot area, capped to the most recent fitted_stripchart_max_time
        # seconds of data. It only kicks in when there's more than one point to fit to.
        point_count = sum(len(points) for points in history_lists)
        fit_enabled = camera.is_fit_mode() and point_count > 1

        if fit_enabled:
            all_times = [point_time for points in history_lists for point_time, _ in points]
            data_max = max(all_times)
            data_min = min(all_times)
            max_span = float(self.context.states.get("fitted_stripchart_max_time"))
            if data_max - data_min > max_span:
                data_min = data_max - max_span
            span = data_max - data_min
            now = data_max
            pps = (right - left) / span if span > 0 else 1.0
            time_offset = 0.0
        else:
            pps = camera.pixels_per_second()
            time_offset = camera.time_offset[0]

        step = t.choose_time_step(pps, MIN_TIME_LABEL_SPACING_PX, TIME_STEP_CANDIDATES)
        decimals = t.decimals_for_step(step)

        rel_left = camera.canvas_x_to_time(left, now, pps, time_offset) - now
        rel_right = camera.canvas_x_to_time(right, now, pps, time_offset) - now

        # Tick positions come from `rel` (an offset from the frozen geometry reference)
        # so the picture doesn't move, but the label shown is that same instant's
        # offset from wall_now, so labels keep sliding while data isn't arriving.
        x_ticks = []
        first_tick = math.ceil(rel_left / step) * step
        tick_count = int((rel_right - first_tick) / step) + 2
        for i in range(max(tick_count, 0)):
            rel = first_tick + i * step
            if rel > rel_right + step * 0.5:
                break
            t_abs = now + rel
            cx = camera.time_to_canvas_x(t_abs, now, pps, time_offset)
            x_ticks.append((cx, t.format_tick(t_abs - wall_now, decimals)))

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

        # --- Most recent value across all lines, converted by factor ---
        latest_time, latest_value = None, None
        for points in history_lists:
            if points:
                point_time, value = points[-1]
                if latest_time is None or point_time > latest_time:
                    latest_time, latest_value = point_time, value
        value_label = "" if latest_value is None else t.format_max_decimals(latest_value * factor, 2)

        return StripChartLayout(now, wall_now, t_min, t_max, min_unit, max_unit, x_ticks, y_ticks, left, top, right, bottom, value_label, pps, time_offset, decimals)

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
        # Top-middle of the canvas, between the units label and the current value
        title_font = self.context.style.get_font("chart_title")
        w = self.canvas.winfo_width()
        self.canvas.create_text(w / 2, LABEL_GAP, text=title, fill=text_color, font=title_font, anchor="n")

    def strip_chart_units_label(self, units_label: str, text_color="black"):
        # Top-left of the canvas, where the title used to sit
        title_font = self.context.style.get_font("chart_title")
        self.canvas.create_text(LABEL_GAP, LABEL_GAP, text=units_label, fill=text_color, font=title_font, anchor="nw")

    def strip_chart_value_label(self, layout: StripChartLayout, text_color="black"):
        # Top-right of the canvas: the most recent history value, in units
        title_font = self.context.style.get_font("chart_title")
        w = self.canvas.winfo_width()
        self.canvas.create_text(w - LABEL_GAP, LABEL_GAP, text=layout.value_label,
                                 fill=text_color, font=title_font, anchor="ne")

    def strip_chart_x_label(self, layout: StripChartLayout, x_label: str, text_color="black"):
        # Centered under the plot area, below the time tick numbers
        label_font = self.context.style.get_font("chart_label")
        number_font = self.context.style.get_font("chart_numbers")
        number_height = number_font.metrics("linespace")
        x_label_y = layout.bottom + TICK_LENGTH + LABEL_GAP + number_height + LABEL_GAP
        cx = (layout.left + layout.right) / 2
        self.canvas.create_text(cx, x_label_y, text=x_label, fill=text_color, font=label_font, anchor="n")

    def strip_chart_path(self, path_points: list[tuple[float, float]], layout: StripChartLayout, factor: float, path_color="red"):
        visible = [(pt, v) for pt, v in path_points if layout.t_min <= pt <= layout.t_max]
        if len(visible) < 2:
            return
        canvas_points = self.camera.data_to_strip_chart(visible, layout.now, factor, layout.min_unit, layout.max_unit,
                                                          layout.pixels_per_second, layout.time_offset)
        self.canvas.create_line(canvas_points, width=2, fill=path_color)

    def strip_chart_crosshairs(self, layout: StripChartLayout, history_lists: list[list[tuple[float, float]]], factor: float,
                                cursor_pos: tuple[float, float] | None, text_color="black", background_color="white"):
        '''
        Draws a mouse-following crosshair: a horizontal line from the cursor to the
        y-axis and a vertical line from the cursor to the x-axis, with the time under
        the cursor and the most recent data value at-or-before that time labeled beside it.
        '''
        if cursor_pos is None:
            return

        cx, cy = cursor_pos
        if not (layout.left <= cx <= layout.right and layout.top <= cy <= layout.bottom):
            return

        self.canvas.create_line(layout.left, cy, cx, cy, fill=text_color, width=1)
        self.canvas.create_line(cx, layout.bottom, cx, cy, fill=text_color, width=1)

        # Camera transform from canvas position back to world (time) space - this
        # already accounts for fit mode, since pixels_per_second/time_offset/now on
        # the layout are whatever fit mode (or normal zoom/pan) actually used to draw.
        # The label is relative to wall_now (real elapsed time), not the geometry
        # reference, so it keeps sliding along with the x-axis ticks even once fit
        # mode has frozen the picture in place.
        hover_time = self.camera.canvas_x_to_time(cx, layout.now, layout.pixels_per_second, layout.time_offset)
        time_text = t.format_tick(hover_time - layout.wall_now, layout.time_decimals)

        number_font = self.context.style.get_font("chart_numbers")
        self._text_with_background(cx - LABEL_GAP, cy + LABEL_GAP, time_text, "ne",
                                    number_font, text_color, background_color)

        # The value shown is the closest data point at-or-before the hovered time -
        # never a future point - across all lines, matching the top-right "current value".
        point = self._closest_point_before(history_lists, hover_time)
        if point is not None:
            value_text = t.format_max_decimals(point[1] * factor, 2)
            self._text_with_background(cx - LABEL_GAP, cy, value_text, "se",
                                        number_font, text_color, background_color)

    def _closest_point_before(self, history_lists: list[list[tuple[float, float]]], hover_time: float):
        '''
        The most recent (time, value) point at-or-before hover_time, across all lines.
        Points are assumed chronologically ordered within each line.
        '''
        best = None
        for points in history_lists:
            index = bisect.bisect_right(points, hover_time, key=lambda point: point[0]) - 1
            if index < 0:
                continue
            candidate = points[index]
            if best is None or candidate[0] > best[0]:
                best = candidate
        return best

    def _text_with_background(self, x: float, y: float, text: str, anchor: str, font, text_color: str, background_color: str):
        '''
        Draws text with a background-colored box behind it so it doesn't blend into
        whatever else is drawn underneath (axes, gridlines, the data line, ...).
        anchor: "se" pins the text's bottom-right corner to (x, y); "ne" pins its top-right corner.
        '''
        width = font.measure(text)
        height = font.metrics("linespace")
        pad = 2

        if anchor == "se":
            box = (x - width - pad, y - height - pad, x + pad, y + pad)
        elif anchor == "ne":
            box = (x - width - pad, y - pad, x + pad, y + height + pad)
        else:
            raise ValueError(f"Unsupported anchor for _text_with_background: {anchor}")

        self.canvas.create_rectangle(*box, fill=background_color, outline="")
        self.canvas.create_text(x, y, text=text, anchor=anchor, font=font, fill=text_color)