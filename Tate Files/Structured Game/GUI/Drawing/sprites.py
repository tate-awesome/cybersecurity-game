class draw:

    def test_triangle(canvas: CTkCanvas):
        '''
        Visualize the transformations
        '''
        count = 20
        for i in range(1, count):
            r = i*2*math.pi/count

            worldspace_triangle = [ -0.1,0 , 0,2 , 0.1,0]
            rotated_triangle = rotate(worldspace_triangle, r)
            range_triangle = range_transform(rotated_triangle, 20, 20, canvas.winfo_width(), canvas.winfo_height())
            scale_triangle = scale(range_triangle)

            canvas.create_polygon(scale_triangle, fill="green")
        worldspace_triangle = [ -0.1,0 , 0,2 , 0.1,0]
        rotated_triangle = rotate(worldspace_triangle, 0)
        range_triangle = range_transform(rotated_triangle, 2, 2, canvas.winfo_width(), canvas.winfo_height())
        scale_triangle = scale(range_triangle)

        canvas.create_polygon(scale_triangle, fill="red")

    
    def boat_path(canvas: CTkCanvas, points: list, line_color: str):
        '''
        Draws the path of the points 
        '''
        if len(points)%2 > 0 or len(points) < 4:
            return
        w = canvas.winfo_width()
        h = canvas.winfo_height()
        canvas.create_line(scale(padding_transform(range_transform(points, 200, 200, w, h), w, h)), width=2, fill=line_color)

    def ocean(canvas, color):
        w = canvas.winfo_width()
        h = canvas.winfo_height()
        canvas.create_rectangle(0, 0, w, h, fill=color)

    def point(canvas: CTkCanvas, coords: list, color: str):
        canvas.create_oval(coords[0] - 5, coords[1] - 5, coords[0] + 5, coords[1] + 5, fill=color)

    def boat(canvas: CTkCanvas, position: list, bearing_radians: float, line_color: str, fill_color: str, size=7.5):
        boat_vertices = [
                        -2, 1,
                        -2, -1,
                        1, -1,
                        3, 0,
                        1, 1
                        ]
        w = canvas.winfo_width()
        h = canvas.winfo_height()
        oriented_boat = rotate(boat_vertices, bearing_radians, scale=size)
        canvas_position = padding_transform(range_transform(position, 200, 200, w, h), w, h)
        vertices = []
        for i in range(0, len(boat_vertices), 2):
            vertices.append(canvas_position[0] + oriented_boat[i])
            vertices.append(canvas_position[1] - oriented_boat[i+1])
        
        canvas.create_polygon(scale(vertices), fill=fill_color, outline=line_color)

    def coordinate_plane(canvas: CTkCanvas, step_size = 20):
        w = canvas.winfo_width()
        h = canvas.winfo_height()

        for i in range(0, 220, step_size):
            line_horizontal = [0, i, 200, i]
            line_vertical = [i, 0, i, 200]
            canvas.create_line(scale(padding_transform(range_transform(line_horizontal, 200, 200, w, h), w, h)), width=1, fill="white")
            canvas.create_line(scale(padding_transform(range_transform(line_vertical, 200, 200, w, h), w, h)), width=1, fill="white")

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
        for i in range_transform(0, len(path) - 2, 2):
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
            for t in range_transform(1, n_ticks):
                tx = x0 + ux * t * step
                ty = y0 + uy * t * step

                tick_len = width  # tick length in grid units
                xA = tx + px * tick_len / 2
                yA = ty + py * tick_len / 2
                xB = tx - px * tick_len / 2
                yB = ty - py * tick_len / 2

                canvas.create_line(sx(xA), sy(yA), sx(xB), sy(yB),
                                fill=color, width=3)