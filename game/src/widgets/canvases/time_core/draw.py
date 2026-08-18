from customtkinter import CTkCanvas
from....app_core import Context
from .camera import Camera
from . import transforms as t
import math, time

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

    def test_data(self):
        '''
        Visualize the transformations
        '''
        points = []
        for i in range(0, 2000):
            x = i
            y = 100 + 500 * math.sin(time.time() + i / 20.0)
            points.append((x, y))
        transformed_points = self.camera.data_to_strip_chart(points)
        self.background(self.context.style.color("field"))
        self.canvas.create_line(transformed_points, width=2, fill=self.context.style.color("field_text"))


    def line(self, points: list[tuple[float, float]], line_color: str, thickness=2):
        '''
        Draws a line connecting the points
        '''
        if len(points) < 2:
            return
        self.canvas.create_line(points, width=1, fill=line_color)


    def grid_lines(self, lines_color="white", axes_color="red"):
        for i in range(0, 210, 10):
            h_line = [(0, i), (200, i)]
            v_line = t.rotate(h_line, math.pi/2, (i, i))

            h_line = self.camera.world_to_canvas(h_line)
            v_line = self.camera.world_to_canvas(v_line)
            color = lines_color
            if i == 0:
                color = axes_color
            self.canvas.create_line(t.flatten(h_line), width=0.5, fill=color)
            self.canvas.create_line(t.flatten(v_line), width=0.5, fill=color)

            # Draw labels every 20 units using already-transformed coordinates
            if i % 20 == 0:
                # h_line goes from (0,i) to (200,i) — use its left end for the Y axis label
                # v_line goes from (i,0) to (i,200) — use its top end for the X axis label
                x_pixel = v_line[0][0]   # x position of vertical line = X axis label position
                y_pixel = h_line[0][1]   # y position of horizontal line = Y axis label position

                # X axis label — sits above the top of each vertical line
                self.canvas.create_text(x_pixel, v_line[0][1] + 10,
                                        text=str(i), fill="#3a6070", font=("Courier", 7))
                # Y axis label — sits to the left of each horizontal line
                self.canvas.create_text(h_line[0][0] - 16, y_pixel,
                                        text=str(i), fill="#3a6070", font=("Courier", 7))
    
    def strip_chart_axes(self, axes_color="red", bounds=(0, 100)):
        # Draw the axes lines

        self.canvas.create_line([(0, bounds[0]), (0, bounds[1])], fill=axes_color, width=2)  # Y-axis
        self.canvas.create_line([(0, bounds[0]), (100, bounds[0])], axes_color, width=2)  # X-axis
        ...

    def strip_chart_grid(self, grid_color="gray", bounds=(0, 100)):
        # Draw horizontal grid lines
        # for y in range(bounds[0], bounds[1] + 1, 10):
        #     self.line([(0, y), (100, y)], grid_color, thickness=1)
        ...

    def strip_chart_grid_numbers(self, number_color="black"):
        # Draw numbers along the Y-axis
        # for y in range(0, 101, 10):
        #     x_pixel = self.camera.world_to_canvas([(0, y)])[0][0]
        #     y_pixel = self.camera.world_to_canvas([(0, y)])[0][1]
        #     self.canvas.create_text(x_pixel - 10, y_pixel, text=str(y), fill=number_color, font=("Courier", 7))
        ...

    def strip_chart_path(self, path_points: list[tuple[float, float]], path_color="red"):
        if len(path_points) < 2:
            return
        min_y = min(y for _, y in path_points)
        max_y = max(y for _, y in path_points)
        min_x = min(x for x, _ in path_points)
        max_x = max(x for x, _ in path_points)

        time_bounds = [min_x, max_x]
        data_bounds = [min_y, max_y]
        
        path_points = self.camera.data_to_strip_chart(path_points, data_bounds, time_bounds)
        
        self.canvas.create_line(path_points, width=2, fill=path_color)