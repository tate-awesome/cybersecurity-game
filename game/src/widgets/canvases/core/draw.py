from ....app_core import Context
from .camera import Camera
from . import transforms as t
import math, time

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QFontMetricsF, QPen, QPolygonF

# Pixels between the map's grid and its numbers, and between the cursor and its crosshair labels
GRID_LABEL_GAP = 4

class Draw:
    '''
    Contains helper functions for drawing objects in world space.
    Has access to the canvas and camera. canvas.painter is a live QPainter,
    set by the canvas's paintEvent for the duration of one frame - unlike
    the old pooled-item Tk version, there's no benefit to reusing drawn
    items across frames here (QPainter has none of Tcl's per-item overhead),
    so this just draws everything fresh every frame.
    '''
    def __init__(self, canvas, context: Context, camera: Camera):
        self.canvas = canvas
        self.camera = camera
        self.context = context

    def background(self, color: str):
        w = self.canvas.width()
        h = self.canvas.height()
        self.canvas.painter.fillRect(QRectF(0, 0, w, h), QColor(color))

    def ocean(self):
        self.background("#003459")

    def bbox(self):
        w = self.canvas.width()
        h = self.canvas.height()
        o = 3
        self._draw_rect((0, 0, w - o / 2, h - o / 2), outline="black", width=o)

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

            self._draw_line(h_line, color, 2)
            self._draw_line(v_line, color, 2)

        # Triangle
        triangle = [ (-1,0), (0,2), (1,0) ]          #   /.\  centered on a 10x10 plane with origin at 0
        triangle = t.scale(triangle, 2.0, (0,0))
        angle = (time.time() % 20.0) * math.pi / 10.0
        triangle = t.rotate(triangle, angle, (0,0))  #   <.
        triangle = self.camera.world_to_canvas(triangle)
        self._draw_polygon(triangle, fill="green", outline="blue", width=5)

        # Inscribed circle
        circle_box = [ (-2,-2), (2,2) ]
        circle_box = t.scale(circle_box, 2.0, (0,0))
        circle_box = self.camera.world_to_canvas(circle_box)
        self._draw_oval(t.flatten(circle_box), outline="blue", width=3)

    # ------------------------------------------------------------------
    # QPainter primitives - the direct replacements for pooled_item()
    # ------------------------------------------------------------------

    def _draw_line(self, coords, color: str, width: float = 1, arrow_end: bool = False):
        painter = self.canvas.painter
        painter.setPen(QPen(QColor(color), width))
        if isinstance(coords[0], (tuple, list)):
            points = [(x, y) for x, y in coords]
            painter.drawPolyline(QPolygonF([QPointF(x, y) for x, y in points]))
            if arrow_end and len(points) >= 2:
                self._draw_arrowhead(points[-2], points[-1], color)
        else:
            x1, y1, x2, y2 = coords
            painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))
            if arrow_end:
                self._draw_arrowhead((x1, y1), (x2, y2), color)

    def _draw_arrowhead(self, from_point: tuple[float, float], to_point: tuple[float, float], color: str, size: float = 8):
        '''
        Draws a filled triangular arrowhead at to_point, pointing along the
        from_point -> to_point direction. Tk's arrow="last" line option has
        no QPainter equivalent, so this replicates it by hand.
        '''
        (x1, y1), (x2, y2) = from_point, to_point
        angle = math.atan2(y2 - y1, x2 - x1)
        spread = math.radians(25)
        left = (x2 - size * math.cos(angle - spread), y2 - size * math.sin(angle - spread))
        right = (x2 - size * math.cos(angle + spread), y2 - size * math.sin(angle + spread))
        self._draw_polygon([(x2, y2), left, right], fill=color, outline=color)

    def _draw_rect(self, coords, fill: str | None = None, outline: str | None = None, width: float = 1):
        painter = self.canvas.painter
        x1, y1, x2, y2 = coords
        rect = QRectF(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
        painter.setPen(QPen(QColor(outline), width) if outline else Qt.PenStyle.NoPen)
        painter.setBrush(QColor(fill) if fill else Qt.BrushStyle.NoBrush)
        painter.drawRect(rect)

    def _draw_oval(self, coords, fill: str | None = None, outline: str | None = None, width: float = 1):
        painter = self.canvas.painter
        x1, y1, x2, y2 = coords
        rect = QRectF(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
        painter.setPen(QPen(QColor(outline), width) if outline else Qt.PenStyle.NoPen)
        painter.setBrush(QColor(fill) if fill else Qt.BrushStyle.NoBrush)
        painter.drawEllipse(rect)

    def _draw_polygon(self, points, fill: str | None = None, outline: str | None = None, width: float = 1):
        painter = self.canvas.painter
        painter.setPen(QPen(QColor(outline), width) if outline else Qt.PenStyle.NoPen)
        painter.setBrush(QColor(fill) if fill else Qt.BrushStyle.NoBrush)
        painter.drawPolygon(QPolygonF([QPointF(x, y) for x, y in points]))

    def _draw_text(self, x: float, y: float, text: str, font, color: str, anchor: str = "center"):
        '''
        anchor follows Tk's create_text convention this was ported from -
        "center" (Tk's own default when none is given) pins the text's
        center to (x, y); "n"/"s"/"e"/"w"/"nw"/"ne"/"sw"/"se" pin that
        edge/corner. Text with several lines lines up on its anchored side
        (left for a west one, right for an east one, centered otherwise).
        '''
        rect = self.text_rect(x, y, *self.text_size(text, font), anchor)
        if "w" in anchor and anchor != "center":
            align = Qt.AlignmentFlag.AlignLeft
        elif "e" in anchor and anchor != "center":
            align = Qt.AlignmentFlag.AlignRight
        else:
            align = Qt.AlignmentFlag.AlignHCenter

        painter = self.canvas.painter
        painter.setFont(font)
        painter.setPen(QColor(color))
        # Unclipped - a glyph reaching past the font's metrics (a fallback
        # font's descender) would otherwise lose its bottom
        painter.drawText(rect, align | Qt.AlignmentFlag.AlignTop | Qt.TextFlag.TextDontClip, text)

    @staticmethod
    def text_rect(x: float, y: float, width: float, height: float, anchor: str = "center") -> QRectF:
        '''The box of the given size pinned to (x, y) by anchor, as _draw_text pins text.'''
        if anchor not in ("center", "n", "s", "e", "w", "nw", "ne", "sw", "se"):
            raise ValueError(f"Unsupported text anchor: {anchor}")
        side = "" if anchor == "center" else anchor  # ("center" has an n and an e in it)
        left = x if "w" in side else x - width if "e" in side else x - width / 2
        top = y if "n" in side else y - height if "s" in side else y - height / 2
        return QRectF(left, top, width, height)

    def text_size(self, text: str, font) -> tuple[float, float]:
        '''The (width, height) _draw_text takes up for text - every line of it.'''
        # Laid out as drawText lays it out - lines a lineSpacing apart, not a height
        size = QFontMetricsF(font).size(0, text)
        return size.width(), size.height()

    def _draw_rounded_rect(self, coords, radius: float, fill: str | None = None, outline: str | None = None, width: float = 1):
        painter = self.canvas.painter
        x1, y1, x2, y2 = coords
        rect = QRectF(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
        painter.setPen(QPen(QColor(outline), width) if outline else Qt.PenStyle.NoPen)
        painter.setBrush(QColor(fill) if fill else Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(rect, radius, radius)

    def line(self, points: list[tuple[float, float]], line_color: str, thickness=2):
        '''
        Draws the path of the points
        '''
        if len(points) < 2:
            return
        points = self.camera.world_to_canvas(points)
        self._draw_line(points, line_color, 1)

    def arrow(self, points: list[tuple[float, float]], line_color: str, thickness=2):
        '''
        Draws the path of the points with an arrowhead at the middle point
        '''
        if len(points) < 2:
            return
        points = self.camera.world_to_canvas(points)
        self._draw_line(points, line_color, thickness, arrow_end=True)

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
        self._draw_line(points, line_color, 2)


    def grid_lines(self, lines_color="white", axes_color="red", numbers_color="#3a6070",
                   background_color: str | None = None, numbers: bool = True):
        # Leaves room beside the world for the numbers - set before anything
        # this frame is placed, and only redone when the font changes
        margin = self.grid_label_margin() if numbers else 0.0
        if margin != self.camera.label_margin:
            self.camera.label_margin = margin
            self.camera.update_padding()

        for i in range(0, 210, 10):
            h_line = [(0, i), (200, i)]
            v_line = t.rotate(h_line, math.pi/2, (i, i))

            h_line = self.camera.world_to_canvas(h_line)
            v_line = self.camera.world_to_canvas(v_line)
            color = lines_color
            if i == 0:
                color = axes_color
            self._draw_line(h_line, color, 0.5)
            self._draw_line(v_line, color, 0.5)

        if numbers:
            self.grid_numbers(numbers_color, background_color)

    def grid_label_margin(self) -> float:
        '''
        Room the grid numbers need beside the world (under it and left of it),
        for the camera's padding (see Camera.label_margin) - so the unzoomed
        map's numbers sit wholly inside the canvas.
        '''
        width, height = self.text_size("200", self.context.style.get_font("chart_numbers"))
        return GRID_LABEL_GAP + max(width, height)

    def _grid_number_anchors(self, font) -> tuple[float, float, bool, bool]:
        '''
        (row_y, column_x, row_pinned, column_pinned): the center line of the x
        numbers' row under the grid and the right edge of the y numbers' column
        left of it - each pinned inside the canvas once the grid's edge leaves
        it (zoomed in or panned), so the numbers stay on screen.
        '''
        w, h = self.canvas.width(), self.canvas.height()
        width, height = self.text_size("200", font)
        left, bottom = self.camera.world_to_canvas([(0, 0)])[0]
        row_y = bottom + GRID_LABEL_GAP + height / 2
        column_x = left - GRID_LABEL_GAP
        pinned_row_y = min(max(row_y, GRID_LABEL_GAP + height / 2), h - GRID_LABEL_GAP - height / 2)
        pinned_column_x = min(max(column_x, GRID_LABEL_GAP + width), w - GRID_LABEL_GAP)
        return pinned_row_y, pinned_column_x, pinned_row_y != row_y, pinned_column_x != column_x

    def grid_numbers(self, color: str, background_color: str | None = None):
        '''
        Numbers every 20 units, x under the grid and y left of it (see
        _grid_number_anchors), on a background_color backdrop while pinned
        over the map. One partly off the canvas, or that would land on another
        (the two rows meet in a corner once both are pinned), is skipped.
        '''
        font = self.context.style.get_font("chart_numbers")
        row_y, column_x, row_pinned, column_pinned = self._grid_number_anchors(font)
        canvas_rect = QRectF(0, 0, self.canvas.width(), self.canvas.height())

        drawn = []
        def place(x, y, text, anchor, pinned):
            rect = self.text_rect(x, y, *self.text_size(text, font), anchor)
            if not canvas_rect.contains(rect) or any(rect.intersects(other) for other in drawn):
                return
            drawn.append(rect)
            if pinned and background_color:
                self.canvas.painter.fillRect(rect.adjusted(-2, 0, 2, 0), self._opaque(background_color))
            self._draw_text(x, y, text, font, color, anchor)

        for i in range(0, 210, 20):
            x, y = self.camera.world_to_canvas([(i, i)])[0]
            place(x, row_y, str(i), "center", row_pinned)
            place(column_x, y, str(i), "e", column_pinned)

    def map_crosshairs(self, cursor_pos: tuple[float, float] | None, rows: list[tuple[str, str, str]],
                       text_color: str, background_color: str):
        '''
        Draws a mouse-following crosshair, like the strip charts': over the
        grid, lines from the cursor to the x and y numbers with the cursor's
        coordinates over them; anywhere on the canvas, a legend beside the
        cursor - one row per (legend_text, color, value_text) in rows, reading
        legend name, color square, value. An empty legend_text or value_text
        leaves that part out.
        '''
        if cursor_pos is None:
            return
        cx, cy = cursor_pos
        wx, wy = self.camera.canvas_to_world([cursor_pos])[0]
        (x0, y0), (x1, y1) = self.camera.world_bounds
        font = self.context.style.get_font("chart_numbers")

        if x0 <= wx <= x1 and y0 <= wy <= y1:
            row_y, column_x, _, _ = self._grid_number_anchors(font)
            self._draw_line((column_x, cy, cx, cy), text_color, 1)
            self._draw_line((cx, row_y, cx, cy), text_color, 1)
            # Kept wholly on the canvas - a readout can be wider than the numbers it sits over
            x_text, y_text = f"{wx:.1f}", f"{wy:.1f}"
            x_width = self.text_size(x_text, font)[0]
            x_center = min(max(cx, GRID_LABEL_GAP + x_width / 2), self.canvas.width() - GRID_LABEL_GAP - x_width / 2)
            y_right = max(column_x, GRID_LABEL_GAP + self.text_size(y_text, font)[0])
            self._text_with_background(x_center, row_y, x_text, "center", font, text_color, background_color)
            self._text_with_background(y_right, cy, y_text, "e", font, text_color, background_color)

        if rows:
            self._draw_legend(cx, cy, rows, font, text_color, background_color)

    def _draw_legend(self, cx: float, cy: float, rows: list[tuple[str, str, str]], font,
                     text_color: str, background_color: str):
        '''
        The crosshair legend (see map_crosshairs): up and to the left of the
        cursor like the strip charts', flipped right/down where that would
        leave the canvas.
        '''
        metrics = QFontMetricsF(font)
        row_height = metrics.height()
        pad, gap = 2, 4
        square_size = max(row_height - 6, 6)
        legend_width = max(metrics.horizontalAdvance(legend) for legend, _, _ in rows)
        value_width = max(metrics.horizontalAdvance(value) for _, _, value in rows)
        legend_col = legend_width + gap if legend_width else 0
        value_col = gap + value_width if value_width else 0
        box_width = legend_col + square_size + value_col
        box_height = row_height * len(rows)

        right = cx - GRID_LABEL_GAP - pad
        if right - box_width - pad < 0:
            right = cx + GRID_LABEL_GAP + pad + box_width
        bottom = cy - GRID_LABEL_GAP - pad
        if bottom - box_height - pad < 0:
            bottom = cy + GRID_LABEL_GAP + pad + box_height
        left, top = right - box_width, bottom - box_height

        self.canvas.painter.fillRect(QRectF(left - pad, top - pad, box_width + 2 * pad, box_height + 2 * pad),
                                     self._opaque(background_color))
        square_left = left + legend_col
        for i, (legend, color, value) in enumerate(rows):
            row_center = top + row_height * i + row_height / 2
            if legend:
                self._draw_text(left, row_center, legend, font, text_color, "w")
            square_top = row_center - square_size / 2
            self._draw_rect((square_left, square_top, square_left + square_size, square_top + square_size),
                            fill=color, outline=text_color)
            if value:
                self._draw_text(square_left + square_size + gap, row_center, value, font, text_color, "w")

    def _text_with_background(self, x: float, y: float, text: str, anchor: str, font,
                              text_color: str, background_color: str):
        '''_draw_text on a background_color box, so it reads over whatever is under it.'''
        rect = self.text_rect(x, y, *self.text_size(text, font), anchor)
        self.canvas.painter.fillRect(rect.adjusted(-2, 0, 2, 0), self._opaque(background_color))
        self._draw_text(x, y, text, font, text_color, anchor)

    @staticmethod
    def _opaque(color: str) -> QColor:
        '''
        color made solid, for a backdrop: the map's background is often a
        see-through theme color (e.g. "widget"), which would let whatever is
        under the backdrop show through it.
        '''
        solid = QColor(color)
        solid.setAlpha(255)
        return solid

    @staticmethod
    def coordinates(position: tuple[float, float]) -> str:
        '''A world position as the crosshair legend shows it: "(x, y)".'''
        return f"({position[0]:.1f}, {position[1]:.1f})"

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

        the_boat = self.camera.world_to_canvas(the_boat)
        self._draw_polygon(the_boat, fill=fill_color, outline=line_color)

    # --------------------------------------------------------------------------------------------------------------------------
    #                                                       HVAC House
    # --------------------------------------------------------------------------------------------------------------------------

    def rect(self, bl: tuple[float, float], tr: tuple[float, float], fill_color="", outline_color="", thickness=2):
        '''
        Draws an axis-aligned rectangle from world-space corners bl (bottom-left) to tr (top-right)
        '''
        points = self.camera.world_to_canvas([bl, tr])
        (x0, y0), (x1, y1) = points
        self._draw_rect((x0, y0, x1, y1), fill=fill_color, outline=outline_color, width=thickness)

    def circle(self, center: tuple[float, float], radius: float, fill_color="", outline_color="", thickness=2):
        '''
        Draws a circle in world space, centered at `center` with the given world-space radius
        '''
        bl = (center[0] - radius, center[1] - radius)
        tr = (center[0] + radius, center[1] + radius)
        points = self.camera.world_to_canvas([bl, tr])
        (x0, y0), (x1, y1) = points
        self._draw_oval((x0, y0, x1, y1), fill=fill_color, outline=outline_color, width=thickness)

    def label(self, position: tuple[float, float], text: str, text_color="black", font_name="chart_label"):
        '''
        Draws centered text at a world-space position
        '''
        point = self.camera.world_to_canvas([position])[0]
        font = self.context.style.get_font(font_name)
        self._draw_text(point[0], point[1], text, font, text_color)

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
            self._draw_line(canvas_points, color, thickness)
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
        self._draw_polygon(points, fill=color, outline=color)
