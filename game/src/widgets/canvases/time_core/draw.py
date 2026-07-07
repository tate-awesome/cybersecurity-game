from customtkinter import CTkCanvas
from....app_core.context import Context
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
            y = 100 + 500 * math.sin(i / 20.0)
            points.append((x, y))
        transformed_points = self.camera.data_to_strip_chart(points)
        self.canvas.create_line(transformed_points, width=2, fill="red")


    def line(self, points: list[tuple[float, float]], line_color: str, thickness=2):
        '''
        Draws the path of the points 
        '''
        if len(points) < 2:
            return
        points = self.camera.world_to_canvas(points)
        self.canvas.create_line(points, width=1, fill=line_color)

    def arc(self, center: tuple[float, float], radius: float, start_angle: float, end_angle: float, line_color: str, thickness=2):
        '''
        Draws an arc with the given parameters. Angles are in radians, 0 is to the right, and positive is counterclockwise.
        '''
        num_points = int(radius * abs(end_angle - start_angle) + 5)
        points = t.get_arc_points(center, radius, start_angle, end_angle, num_points)
        points = self.camera.world_to_canvas(points)
        self.canvas.create_line(points, width=2, fill=line_color)


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

    def boat(self, position: tuple[float, float], bearing: float, fill_color="gray", line_color="black", scale=2.0):
        the_boat = [
                            (-2, 1),
                            (-2, -1),
                            (1,  -1),
                            (3,  0),
                            (1,  1)
                        ]
        if bearing is None or position is None:
            return
        the_boat = t.rotate(the_boat, bearing)
        the_boat = t.scale(the_boat, scale)

        the_boat = t.translate(the_boat, position)
        
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
    
        the_boat = self.camera.world_to_canvas(the_boat)
        self.canvas.create_polygon(the_boat, fill=fill_color, outline=line_color)

    def random_spline_path(target_points, samples_per_segment):
        import random
        points = []
        for _ in range(target_points):
            x = random.randint(0, 200)
            y = random.randint(0, 200)
            points.append((x,y))
        points.append(points[0])

        spline = []
        for i in range(1, len(points) - 2):
            p0, p1, p2, p3 = points[i-1], points[i], points[i+1], points[i+2]

            for j in range(samples_per_segment):
                t = j / samples_per_segment
                t2 = t * t
                t3 = t2 * t

                x = 0.5 * (
                    (2 * p1[0]) +
                    (-p0[0] + p2[0]) * t +
                    (2*p0[0] - 5*p1[0] + 4*p2[0] - p3[0]) * t2 +
                    (-p0[0] + 3*p1[0] - 3*p2[0] + p3[0]) * t3
                )

                y = 0.5 * (
                    (2 * p1[1]) +
                    (-p0[1] + p2[1]) * t +
                    (2*p0[1] - 5*p1[1] + 4*p2[1] - p3[1]) * t2 +
                    (-p0[1] + 3*p1[1] - 3*p2[1] + p3[1]) * t3
                )

                spline.append((x, y))
        return spline
    
    def strip_chart_axes(self, axes_color="red", bounds=(0, 100)):
        # Draw the axes lines
        # self.line([(0, bounds[0]), (0, bounds[1])], axes_color, thickness=2)  # Y-axis
        # self.line([(0, bounds[0]), (100, bounds[0])], axes_color, thickness=2)  # X-axis
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
        path_points = self.camera.data_to_strip_chart(path_points)
        self.canvas.create_line(path_points, width=2, fill=path_color)