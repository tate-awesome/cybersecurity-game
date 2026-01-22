import math

def coords_to_canvas(points: list, input_x, input_y, canvas_x, canvas_y):
    tracks = []
    for i in range(0, len(points)):
        if i%2 == 0:
            tracks.append(points[i] * canvas_x / input_range) # 0-100 becomes 0-canvas_size
        if i%2 == 1:
            tracks.append(canvas_y - points[i] * canvas_y / input_range) # 0-100 becomes canvas-0
        i += 1
    return tracks

def line(canvas, points, line_color):
    w = canvas.winfo_height()
    if len(points)%2 != 0:
        return
    tracks = coordinates_transform(points, w)
    
    canvas.create_line(tracks, width=2, fill=line_color)
    return

def ocean(canvas, color):
    w = canvas.winfo_width()
    h = canvas.winfo_height()
    canvas.create_rectangle(0, 0, w, h, fill=color)

def boat(canvas, x_pos, y_pos, dir_deg_360, line_color, fill_color):
    w = canvas.winfo_width()
    h = canvas.winfo_height()
    boat_vertices = [
                    [-2, 1],
                    [-2, -1],
                    [1, -1],
                    [3, 0],
                    [1, 1]
                    ]
    scale = h/120
    cx = x_pos*100
    cy = y_pos*100
    angle = (dir_deg_360 - 360) *math.pi/180
    vertices = []
    for vx, vy in boat_vertices:
        x = vx * scale
        y = vy * scale

        xr = x * math.cos(angle) - y * math.sin(angle)
        yr = x * math.sin(angle) + y * math.cos(angle)

        xr += cx
        yr += cy

        xt = xr*w/2000
        yt = h - yr*h/2000

        vertices.extend([xt, yt])
    canvas.create_polygon(vertices, fill=fill_color, outline=line_color)
    
def target(canvas, x, y, color):
    center = coordinates_transform([x, y], canvas.winfo_height())
    cx = center[0]
    cy = center[1]
    radius = 12
    side = radius/math.sqrt(2)
    bbox = [
        cx - side,
        cy - side,
        cx + side,
        cy + side
    ]
    canvas.create_oval(bbox, outline=color, width=2, fill="")

def ticks(canvas, path, step, width, color="black"):
    # if len(path) < 4 or len(path)%2 != 0:
    #     return
    # tracks = coordinates_transform(path, canvas.winfo_height())
    # startpoint = [tracks[0], tracks[1]]
    # endpoint = [tracks[-2], tracks[-1]]
    # line_vector = [endpoint[0]-startpoint[0], endpoint[1]-startpoint[1]]
    # length = math.sqrt(line_vector[0]**2 + line_vector[1]**2)
    # norm_line_vector = [line_vector[0]/length, line_vector[1]]
    # stepsize = coordinates_transform([step], canvas.winfo_height())[0]
    # num_ticks = math.floor(length/stepsize)
    # orth = [norm_line_vector[1], norm_line_vector[0]]
    # for i in range(0, num_ticks):
    #     points = [
    #         startpoint[0] - orth[0]*5 + norm_line_vector[0]*stepsize*i,
    #         startpoint[1] - orth[1]*5 + norm_line_vector[1]*stepsize*i,
    #         startpoint[0] + orth[0]*5 + norm_line_vector[0]*stepsize*i,
    #         startpoint[1] + orth[1]*5 + norm_line_vector[1]*stepsize*i,
    #     ]
    #     canvas.create_line(points, fill=color, width=1)
    # canvas.create_line([startpoint,endpoint], fill=color, width=3)

    # Get canvas dimensions
    w = canvas.winfo_width()
    h = canvas.winfo_height()
    scale_x = w / 1000
    scale_y = h / 1000

    # Helper to scale grid coords to canvas coords
    def sx(x): return x * scale_x
    def sy(y): return h - y * scale_y  # flip Y so (0,0) = bottom-left

    # Draw main line path
    for i in range(0, len(path) - 2, 2):
        x0, y0 = path[i], path[i+1]
        x1, y1 = path[i+2], path[i+3]
        canvas.create_line(sx(x0), sy(y0), sx(x1), sy(y1), fill=color, width=2)

        # Compute vector and segment length
        dx, dy = x1 - x0, y1 - y0
        length = math.hypot(dx, dy)
        if length == 0:
            continue

        # Unit direction vector
        ux, uy = dx / length, dy / length

        # Perpendicular unit vector (for tick direction)
        px, py = -uy, ux

        # Place ticks every "step" distance
        n_ticks = int(length // step)
        for t in range(1, n_ticks):
            tx = x0 + ux * t * step
            ty = y0 + uy * t * step

            tick_len = width  # tick length in grid units
            xA = tx + px * tick_len / 2
            yA = ty + py * tick_len / 2
            xB = tx - px * tick_len / 2
            yB = ty - py * tick_len / 2

            canvas.create_line(sx(xA), sy(yA), sx(xB), sy(yB),
                               fill=color, width=3)
    