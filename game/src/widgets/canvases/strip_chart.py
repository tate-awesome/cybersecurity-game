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
        super().__init__(master, context, grid_position, title_getter(), time_scale, time_offset)

        def frame_callback():
            self.delete("all")
            def color(key):
                return self.context.style.color(self.context.states.get("strip_chart_colors", key))
            self.draw.background("purple")
            self.draw.background(color("background"))
            # self.draw.strip_chart_axes(data)
            # self.draw.test_data()

            line_colors = context.states.get("strip_chart_colors", "paths")
            for i, history in enumerate(history_getters):
                line_color = line_colors[i%len(line_colors)]
                self.draw.strip_chart_path(history(), line_color)

            # Draw axes
            axes_color = color("grid_axes")
            # Draw labels
            text_color = color("grid_numbers")
            time_text = self.context.labels.get("stripcharts", "time")
            # The factor is raw * factor = units, so align the y-axis numbers accordingly
            
        self.set_frame_callback(frame_callback)