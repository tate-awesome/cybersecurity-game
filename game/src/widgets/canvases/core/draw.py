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

    def ocean(self):
        self.background("#003459")
    
    def bbox(self):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        o = 3
        self.canvas.create_rectangle(0,0,w-o/2,h-o/2,fill="",outline="black", width=o)

    def test_triangle(self):
        '''
        Visualize the transformations
        '''

        # Gridlines
        for i in range(-5, 6):
            h_line = [ (-1, i), (1, i) ]
            h_line = t.scale(h_line, 5)
            v_line = t.rotate(h_line, math.pi/2, (0, 0))

            h_line = self.camera.world_to_canvas(h_line)
            v_line = self.camera.world_to_canvas(v_line)
            color = "black"
            if i == 0:
                color = "red"

            self.canvas.create_line(t.flatten(h_line), width=2, fill=color)
            self.canvas.create_line(t.flatten(v_line), width=2, fill=color)

        # Triangle
        triangle = [ (-1,0), (0,2), (1,0) ]          #   /.\  centered on a 10x10 plane with origin at 0
        triangle = t.scale(triangle, 2.0, (0,0))
        angle = (time.time() % 20.0) * math.pi / 10.0
        triangle = t.rotate(triangle, angle, (0,0))  #   <.   
        triangle = self.camera.world_to_canvas(triangle)
        self.canvas.create_polygon(triangle, fill="green", width="5", outline="blue")

        # Inscribed circle
        circle_box = [ (-2,-2), (2,2) ]
        circle_box = t.scale(circle_box, 2.0, (0,0)) 
        circle_box = self.camera.world_to_canvas(circle_box)
        self.canvas.create_oval(circle_box, fill="", outline="blue", width="3")


    def line(self, points: list[tuple[float, float]], line_color: str, thickness=2):
        '''
        Draws the path of the points 
        '''
        if len(points) < 2:
            return
        points = self.camera.world_to_canvas(points)
        self.canvas.create_line(points, width=1, fill=line_color)

    def arrow(self, points: list[tuple[float, float]], line_color: str, thickness=2):
        '''
        Draws the path of the points with an arrowhead at the middle point
        '''
        if len(points) < 2:
            return
        points = self.camera.world_to_canvas(points)
        self.canvas.create_line(points, width=thickness, fill=line_color, arrow="last")

    def visible_arrow(self, points: list[tuple[float, float]], line_color: str, thickness=2):
        '''
        Draws an arrow most of the way between points, leaving space for a visible arrowhead and gap
        '''
        if len(points) < 2:
            return
        short = t.shorten_line((points[0], points[1]), 0.8)
        self.arrow(short, line_color, thickness)

    def arc(self, center: tuple[float, float], radius: float, start_angle: float, end_angle: float, line_color: str, thickness=2):
        '''
        Draws an arc with the given parameters. Angles are in radians, 0 is to the right, and positive is counterclockwise.
        '''
        num_points = int(radius * abs(end_angle - start_angle) + 5)
        points = t.get_arc_points(center, radius, start_angle, end_angle, num_points)
        points = self.camera.world_to_canvas(points)
        self.canvas.create_line(points, width=2, fill=line_color)


    def grid_lines(self, lines_color="white", axes_color="red", numbers_color="#3a6070"):
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
                font = self.context.style.get_font("chart_numbers")
                self.canvas.create_text(x_pixel, v_line[0][1] + 10,
                                        text=str(i), fill=numbers_color, font=font)
                # Y axis label — sits to the left of each horizontal line
                self.canvas.create_text(h_line[0][0] - 16, y_pixel,
                                        text=str(i), fill=numbers_color, font=font)

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

    # --------------------------------------------------------------------------------------------------------------------------
    #                                                       HVAC House
    # --------------------------------------------------------------------------------------------------------------------------

    def rect(self, bl: tuple[float, float], tr: tuple[float, float], fill_color="", outline_color="", thickness=2):
        '''
        Draws an axis-aligned rectangle from world-space corners bl (bottom-left) to tr (top-right)
        '''
        points = self.camera.world_to_canvas([bl, tr])
        (x0, y0), (x1, y1) = points
        self.canvas.create_rectangle(x0, y0, x1, y1, fill=fill_color, outline=outline_color, width=thickness)

    def circle(self, center: tuple[float, float], radius: float, fill_color="", outline_color="", thickness=2):
        '''
        Draws a circle in world space, centered at `center` with the given world-space radius
        '''
        bl = (center[0] - radius, center[1] - radius)
        tr = (center[0] + radius, center[1] + radius)
        points = self.camera.world_to_canvas([bl, tr])
        (x0, y0), (x1, y1) = points
        self.canvas.create_oval(x0, y0, x1, y1, fill=fill_color, outline=outline_color, width=thickness)

    def label(self, position: tuple[float, float], text: str, text_color="black", font_name="chart_label"):
        '''
        Draws centered text at a world-space position
        '''
        point = self.camera.world_to_canvas([position])[0]
        font = self.context.style.get_font(font_name)
        self.canvas.create_text(point[0], point[1], text=text, fill=text_color, font=font)

    def wall_point(self, bl: tuple[float, float], tr: tuple[float, float], wall: str, t=0.5) -> tuple[float, float]:
        '''
        Returns a point on the given wall ("top", "bottom", "left", or "right") of a bl/tr box,
        t in [0,1] parameterizes position along the wall
        '''
        x0, y0 = bl
        x1, y1 = tr
        if wall == "top":
            return (x0 + t * (x1 - x0), y1)
        if wall == "bottom":
            return (x0 + t * (x1 - x0), y0)
        if wall == "left":
            return (x0, y0 + t * (y1 - y0))
        return (x1, y0 + t * (y1 - y0))

    def inward_normal(self, wall: str) -> tuple[float, float]:
        '''
        Returns the unit vector pointing from the given wall into the room's interior
        '''
        return {"top": (0, -1), "bottom": (0, 1), "left": (1, 0), "right": (-1, 0)}[wall]

    def hvac_room(self, bl: tuple[float, float], tr: tuple[float, float], fill_color: str, outline_color: str):
        '''
        Draws the room's outer wall as a filled rectangle
        '''
        self.rect(bl, tr, fill_color, outline_color, thickness=3)

    def hvac_controller_box(self, bl: tuple[float, float], tr: tuple[float, float], fill_color: str, outline_color: str):
        '''
        Draws the hvac controller as a filled rectangle
        '''
        self.rect(bl, tr, fill_color, outline_color, thickness=3)

    def hvac_thermostat(self, position: tuple[float, float], temperature: float | None,
                         fill_color: str, outline_color: str, text_color: str, radius=4,
                         status: str | None = None, status_color: str | None = None):
        '''
        Draws a round thermostat readout at a world-space position, showing the given temperature
        (or "--" if None). If status is given (e.g. "too cold!"/"too hot!"), the dial is filled with
        status_color and the status text is drawn above the dial in that color, splitting label
        space above and below the dial instead of stacking both on one side.
        '''
        self.circle(position, radius, status_color if status else fill_color, outline_color, thickness=2)
        reading = "--" if temperature is None else f"{temperature:.0f}°F"
        self.label((position[0], position[1] - radius - 4), reading, text_color, "chart_numbers")
        if status:
            self.label((position[0], position[1] + radius + 4), status, text_color, "chart_label")

    def hvac_indicator(self, position: tuple[float, float], is_open: bool,
                        open_color: str, closed_color: str, text_color: str, radius=4):
        '''
        Draws the controller's commanded-state light: open_color/"OPEN" when commanding the vent
        open, closed_color/"CLOSED" otherwise
        '''
        color = open_color if is_open else closed_color
        state = "OPEN" if is_open else "CLOSED"
        self.circle(position, radius, color, text_color, thickness=2)
        self.label((position[0], position[1] - radius - 4), state, text_color, "chart_label")

    def hvac_window(self, bl: tuple[float, float], tr: tuple[float, float], wall: str, t: float,
                     frame_color: str, glass_color: str, size=16, depth=3):
        '''
        Draws an open window embedded in the given wall ("top", "bottom", "left", or "right") of a room,
        set just inside the wall so it doesn't get covered by whatever sits against the outside of it
        '''
        wx, wy = self.wall_point(bl, tr, wall, t)
        nx, ny = self.inward_normal(wall)
        cx, cy = wx + nx * depth / 2, wy + ny * depth / 2
        if wall in ("top", "bottom"):
            w_bl, w_tr = (cx - size / 2, cy - depth / 2), (cx + size / 2, cy + depth / 2)
        else:
            w_bl, w_tr = (cx - depth / 2, cy - size / 2), (cx + depth / 2, cy + size / 2)
        self.rect(w_bl, w_tr, glass_color, frame_color, thickness=2)

    def hvac_vent(self, bl: tuple[float, float], tr: tuple[float, float], wall: str, t: float,
                  frame_color: str, fill_color="", size=16, depth=3, louvers=4):
        '''
        Draws a vent grate embedded in the given wall of a room, set just inside the wall so it
        doesn't get covered by whatever sits against the outside of it. Pass fill_color (e.g. the
        hotness color) to show the vent as actively blowing.
        '''
        wx, wy = self.wall_point(bl, tr, wall, t)
        nx, ny = self.inward_normal(wall)
        cx, cy = wx + nx * depth / 2, wy + ny * depth / 2
        if wall in ("top", "bottom"):
            v_bl, v_tr = (cx - size / 2, cy - depth / 2), (cx + size / 2, cy + depth / 2)
        else:
            v_bl, v_tr = (cx - depth / 2, cy - size / 2), (cx + depth / 2, cy + size / 2)
        self.rect(v_bl, v_tr, fill_color, frame_color, thickness=2)
        for i in range(1, louvers):
            f = i / louvers
            if wall in ("top", "bottom"):
                x = v_bl[0] + f * size
                self.line([(x, v_bl[1]), (x, v_tr[1])], frame_color, thickness=1)
            else:
                y = v_bl[1] + f * size
                self.line([(v_bl[0], y), (v_tr[0], y)], frame_color, thickness=1)

    def hvac_flow_arrows(self, bl: tuple[float, float], tr: tuple[float, float], wall: str, t: float,
                          color: str, count=3, length=20, spread=10, amplitude=1.6, wavelength=9,
                          cycles_per_sec=1.0, thickness=2, samples=18):
        '''
        Draws animated sine-wave streaks flowing inward through the given wall of a room, e.g. cold
        air from a window or hot air from a vent. The wave crests travel along the flow direction
        (using the current wall clock time) so the motion reads as flowing rather than static, and
        each streak ends in an arrowhead pointing straight along the flow direction regardless of
        the wave's local wiggle.
        '''
        cx, cy = self.wall_point(bl, tr, wall, t)
        nx, ny = self.inward_normal(wall)
        ax, ay = {"top": (1, 0), "bottom": (1, 0), "left": (0, 1), "right": (0, 1)}[wall]
        now = time.time()
        k = 2 * math.pi / wavelength
        w = 2 * math.pi * cycles_per_sec
        for i in range(count):
            offset = (i - (count - 1) / 2) * (spread / max(count - 1, 1)) if count > 1 else 0
            start = (cx + ax * offset, cy + ay * offset)
            points = []
            for s in range(samples + 1):
                along = length * s / samples
                wobble = amplitude * math.sin(k * along - w * now)
                points.append((
                    start[0] + nx * along + ax * wobble,
                    start[1] + ny * along + ay * wobble,
                ))
            canvas_points = self.camera.world_to_canvas(points)
            self.canvas.create_line(canvas_points, width=thickness, fill=color, smooth=True)
            self._hvac_arrowhead(points[-1], (nx, ny), color)

    def _hvac_arrowhead(self, tip: tuple[float, float], direction: tuple[float, float], color: str, size=2.5):
        '''
        Draws a filled triangular arrowhead in world space at `tip`, pointing along `direction`
        '''
        dx, dy = direction
        px, py = -dy, dx
        back = (tip[0] - dx * size, tip[1] - dy * size)
        left = (back[0] + px * size * 0.5, back[1] + py * size * 0.5)
        right = (back[0] - px * size * 0.5, back[1] - py * size * 0.5)
        points = self.camera.world_to_canvas([tip, left, right])
        self.canvas.create_polygon(points, fill=color, outline=color)