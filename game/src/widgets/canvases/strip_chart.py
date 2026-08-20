from .time_core.stripchart import StripChartBase
from customtkinter import CTkFrame
from ...app_core import Context
from typing import Callable


class StripChart(StripChartBase):
    '''
    Canvas that displays a running value of the provided getter.
    The getter must return list[tuple[time: float, value: float]].
    Its time axis is synchronized with other strip charts in the same context.
    '''

    def __init__(self, master: CTkFrame, context: Context, grid_position: tuple[int, int], 
                 title_getter, units_getter, factor_getter, 
                 history_getters: list[Callable[[None], list[tuple[float, float]]]], 
                 time_scale: list[float] = [0.0], time_offset: list[float] = [0.0]):

        # Create the canvas widget
        super().__init__(master, context, grid_position, time_scale, time_offset)

        def frame_callback():
            self.delete("all")
            def color(key):
                return self.context.style.color(self.context.states.get("strip_chart_colors", key))
            self.draw.background(color("background"))

            if self.winfo_width() <= 1 or self.winfo_height() <= 1:
                return

            histories = [history() for history in history_getters]
            # The factor is raw * factor = units, so the y-axis is scaled/labeled in units
            if float(factor_getter()):
                factor = float(factor_getter())
            else:
                factor = 1.0

            # Time scaling/offset are resolved first (the visible time window), then
            # the value axis autoscales to whatever data falls inside that window.
            layout = self.draw.strip_chart_layout(histories, factor)

            grid_color = color("grid_lines")
            axes_color = color("grid_axes")
            text_color = color("grid_numbers")

            self.draw.strip_chart_ticks(layout, grid_color, gridlines=False)
            self.draw.strip_chart_axes(layout, axes_color)
            self.draw.strip_chart_numbers(layout, text_color)

            time_text = self.context.labels.get("stripcharts", "time")
            self.draw.strip_chart_axis_labels(layout, time_text, units_getter(), text_color)
            self.draw.strip_chart_title(title_getter(), text_color)

            line_colors = context.states.get("strip_chart_colors", "paths")
            for i, history in enumerate(histories):
                line_color = line_colors[i%len(line_colors)]
                self.draw.strip_chart_path(history, layout, factor, line_color)

        self.set_frame_callback(frame_callback)