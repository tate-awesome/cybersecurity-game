from .core.canvas import Canvas
from customtkinter import CTkFrame
from ...app_core.context import Context
from typing import Callable


class StripChart(Canvas):
    '''
    Canvas that displays a running value of the provided getter.
    The getter must return list[tuple[time: float, value: float]].
    It can grow to fit the variable but a provided bounds helps display more cleanly.
    '''

    def __init__(self, master: CTkFrame, context: Context, getter: Callable[None, list[tuple[float, float]]], name: "Variable", bounds: tuple[float, float] = (0, 100)):

        # Create the canvas widget
        super().__init__(master, context, ((0,0),(100,100)))

        def frame_callback():
            sprites = context.states["strip_chart_sprites"]
            colors = context.states["strip_chart_colors"]
            
            self.delete("all")
            
            self.draw.background(colors["background"])

            if int(sprites["grid_axes"]) == 1:
                self.draw.strip_chart_axes(colors["grid_axes"], bounds)

            if int(sprites["grid_numbers"]) == 1:
                self.draw.strip_chart_grid_numbers(colors["grid_numbers"])

            if int(sprites["grid_lines"]) == 1:
                self.draw.strip_chart_grid(colors["grid_lines"])

            if int(sprites["path_in"]) == 1:
                
                data = getter()
                if data:
                    self.draw.strip_chart_path(data, colors["path_in"])
                
            # "strip_chart_sprites": {
            #     "grid_lines": 1,
            #     "grid_axes": 1,
            #     "grid_numbers": 1,
            #     "head_in": 1,
            #     "head_out": 1,
            #     "path_in": 1,
            #     "path_out": 1,
            #     "head_in_label": 1,
            #     "head_out_label": 1
            # },

            # "strip_chart_colors": {
            #     "background": "white",
            #     "grid_lines": "black",
            #     "grid_axes": "red",
            #     "grid_numbers": "black",
            #     "path_in": "blue",
            #     "path_out": "green",
            #     "head_in": "blue",
            #     "head_out": "green"
            # }
        self.set_frame_callback(frame_callback)
        self.start_animation()