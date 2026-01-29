'''
Draw to canvas from here
'''
from . import transformations as t
from customtkinter import CTkCanvas
from math import pi as PI
import time

def test_triangle(canvas: CTkCanvas, scale: float, offset: tuple[float, float]):
    '''
    Visualize the transformations
    '''
    padding = 20

    # Gridlines
    for i in range(-5, 6):
        h_line = [ (-1, i), (1, i) ]
        h_line = t.scale(h_line, 5)

        v_line = t.rotate(h_line, PI/2, (0, 0))

        h_line = t.padded_fit(h_line, (-5, -5), (5, 5), canvas, padding)
        v_line = t.padded_fit(v_line, (-5, -5), (5, 5), canvas, padding)

        h_line = t.zoom_and_pan(h_line, scale, offset)
        v_line = t.zoom_and_pan(v_line, scale, offset)

        color = "black"
        if i == 0:
            color = "red"

        canvas.create_line(t.flatten(h_line), width=2, fill=color)
        canvas.create_line(t.flatten(v_line), width=2, fill=color)

    triangle = [ (-1,0), (0,2), (1,0) ]          #   /.\  centered on a 10x10 plane with origin at 0
    triangle = t.scale(triangle, 2.0, (0,0))
    angle = (time.time() % 20.0) * PI / 10.0
    triangle = t.rotate(triangle, angle, (0,0))  #   <.   
    triangle = t.padded_fit(triangle, (-5, -5), (5, 5), canvas, padding)
    triangle = t.zoom_and_pan(triangle, scale, offset)
    canvas.create_polygon(triangle, fill="green", width="5", outline="blue")

    circle_box = [ (-2,-2), (2,2) ]
    circle_box = t.scale(circle_box, 2.0, (0,0)) 
    circle_box = t.padded_fit(circle_box, (-5, -5), (5, 5), canvas, padding)
    circle_box = t.zoom_and_pan(circle_box, scale, offset)
    canvas.create_oval(circle_box, fill="", outline="blue", width="3")


class boat:


    def poly_line(canvas: CTkCanvas, points: list, scale: float, offset: tuple[float, float], line_color: str):
        '''
        Draws the path of the points 
        '''
        if len(points) < 2:
            return
        points = t.padded_fit(points, (0,0), (200,200), canvas, 20)
        points = t.zoom_and_pan(points, scale, offset)
        canvas.create_line(points, width=2, fill=line_color)


    def grid_lines(canvas: CTkCanvas, scale: float, offset: tuple[float, float]):
        for i in range(0, 210, 10):
            h_line = [ (0, i), (200, i) ]

            v_line = t.rotate(h_line, PI/2, (i, i))

            h_line = t.padded_fit(h_line, (0,0), (200,200), canvas, 20)
            v_line = t.padded_fit(v_line, (0,0), (200,200), canvas, 20)

            h_line = t.zoom_and_pan(h_line, scale, offset)
            v_line = t.zoom_and_pan(v_line, scale, offset)

            color = "black"
            if i == 0:
                color = "red"

            canvas.create_line(t.flatten(h_line), width=2, fill=color)
            canvas.create_line(t.flatten(v_line), width=2, fill=color)

# def ocean(canvas, color):
#     w = canvas.winfo_width()
#     h = canvas.winfo_height()
#     canvas.create_rectangle(0, 0, w, h, fill=color)

# def point(canvas: CTkCanvas, coords: list, color: str):
#     canvas.create_oval(coords[0] - 5, coords[1] - 5, coords[0] + 5, coords[1] + 5, fill=color)

# def boat(canvas: CTkCanvas, position: list, bearing_radians: float, line_color: str, fill_color: str, size=7.5):
#     boat_vertices = [
#                     -2, 1,
#                     -2, -1,
#                     1, -1,
#                     3, 0,
#                     1, 1
#                     ]
#     w = canvas.winfo_width()
#     h = canvas.winfo_height()
#     oriented_boat = rotate(boat_vertices, bearing_radians, scale=size)
#     canvas_position = padding_transform(range_transform(position, 200, 200, w, h), w, h)
#     vertices = []
#     for i in range(0, len(boat_vertices), 2):
#         vertices.append(canvas_position[0] + oriented_boat[i])
#         vertices.append(canvas_position[1] - oriented_boat[i+1])
    
#     canvas.create_polygon(scale(vertices), fill=fill_color, outline=line_color)

# def coordinate_plane(canvas: CTkCanvas, step_size = 20):
#     w = canvas.winfo_width()
#     h = canvas.winfo_height()

#     for i in range(0, 220, step_size):
#         line_horizontal = [0, i, 200, i]
#         line_vertical = [i, 0, i, 200]
#         canvas.create_line(scale(padding_transform(range_transform(line_horizontal, 200, 200, w, h), w, h)), width=1, fill="white")
#         canvas.create_line(scale(padding_transform(range_transform(line_vertical, 200, 200, w, h), w, h)), width=1, fill="white")

# def ticks(canvas, path, step, width, color="black"):
#     # if len(path) < 4 or len(path)%2 != 0:
#     #     return
#     # tracks = coordinates_transform(path, canvas.winfo_height())
#     # startpoint = [tracks[0], tracks[1]]
#     # endpoint = [tracks[-2], tracks[-1]]
#     # line_vector = [endpoint[0]-startpoint[0], endpoint[1]-startpoint[1]]
#     # length = math.sqrt(line_vector[0]**2 + line_vector[1]**2)
#     # norm_line_vector = [line_vector[0]/length, line_vector[1]]
#     # stepsize = coordinates_transform([step], canvas.winfo_height())[0]
#     # num_ticks = math.floor(length/stepsize)
#     # orth = [norm_line_vector[1], norm_line_vector[0]]
#     # for i in range(0, num_ticks):
#     #     points = [
#     #         startpoint[0] - orth[0]*5 + norm_line_vector[0]*stepsize*i,
#     #         startpoint[1] - orth[1]*5 + norm_line_vector[1]*stepsize*i,
#     #         startpoint[0] + orth[0]*5 + norm_line_vector[0]*stepsize*i,
#     #         startpoint[1] + orth[1]*5 + norm_line_vector[1]*stepsize*i,
#     #     ]
#     #     canvas.create_line(points, fill=color, width=1)
#     # canvas.create_line([startpoint,endpoint], fill=color, width=3)

#     # Get canvas dimensions
#     w = canvas.winfo_width()
#     h = canvas.winfo_height()
#     scale_x = w / 1000
#     scale_y = h / 1000

#     # Helper to scale grid coords to canvas coords
#     def sx(x): return x * scale_x
#     def sy(y): return h - y * scale_y  # flip Y so (0,0) = bottom-left

#     # Draw main line path
#     for i in range_transform(0, len(path) - 2, 2):
#         x0, y0 = path[i], path[i+1]
#         x1, y1 = path[i+2], path[i+3]
#         canvas.create_line(sx(x0), sy(y0), sx(x1), sy(y1), fill=color, width=2)

#         # Compute vector and segment length
#         dx, dy = x1 - x0, y1 - y0
#         length = math.hypot(dx, dy)
#         if length == 0:
#             continue

#         # Unit direction vector
#         ux, uy = dx / length, dy / length

#         # Perpendicular unit vector (for tick direction)
#         px, py = -uy, ux

#         # Place ticks every "step" distance
#         n_ticks = int(length // step)
#         for t in range_transform(1, n_ticks):
#             tx = x0 + ux * t * step
#             ty = y0 + uy * t * step

#             tick_len = width  # tick length in grid units
#             xA = tx + px * tick_len / 2
#             yA = ty + py * tick_len / 2
#             xB = tx - px * tick_len / 2
#             yB = ty - py * tick_len / 2

#             canvas.create_line(sx(xA), sy(yA), sx(xB), sy(yB),
#                             fill=color, width=3)