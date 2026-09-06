from . import transformations as t
from math import pi as PI
import time

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QFont, QFontMetricsF, QPen, QPolygonF

class ViewPort:
    '''
    Holds the current viewport parameters for drawing on the canvas for a single frame.
    Also contains helper functions for drawing objects in world space.
    canvas.painter is a live QPainter, set by the owning widget's paintEvent
    for the duration of one frame (see widgets/map.py) - draws fresh every
    frame rather than reusing items across frames the way the old
    PooledCanvasMixin/CTkCanvas version needed to work around Tcl's
    per-item creation overhead (see core/draw.py's docstring).
    '''
    def __init__(self, canvas, scale: float, offset: tuple[float, float], padding=20, input_range=((0,0),(200,200))):
        self.canvas = canvas
        self.scale = scale
        self.offset = offset
        self.padding = padding
        self.input_range = input_range

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

            v_line = t.rotate(h_line, PI/2, (0, 0))

            h_line = t.padded_fit_uniform(h_line, (-5, -5), (5, 5), self.canvas, self.padding)
            v_line = t.padded_fit_uniform(v_line, (-5, -5), (5, 5), self.canvas, self.padding)

            h_line = t.zoom_and_pan(h_line, self.scale, self.offset)
            v_line = t.zoom_and_pan(v_line, self.scale, self.offset)
            color = "black"
            if i == 0:
                color = "red"

            self._draw_line(h_line, color, 2)
            self._draw_line(v_line, color, 2)

        # Triangle
        triangle = [ (-1,0), (0,2), (1,0) ]          #   /.\  centered on a 10x10 plane with origin at 0
        triangle = t.scale(triangle, 2.0, (0,0))
        angle = (time.time() % 20.0) * PI / 10.0
        triangle = t.rotate(triangle, angle, (0,0))  #   <.
        triangle = t.padded_fit_uniform(triangle, (-5, -5), (5, 5), self.canvas, self.padding)
        triangle = t.zoom_and_pan(triangle, self.scale, self.offset)
        self._draw_polygon(triangle, fill="green", outline="blue", width=5)

        # Inscribed circle
        circle_box = [ (-2,-2), (2,2) ]
        circle_box = t.scale(circle_box, 2.0, (0,0))
        circle_box = t.padded_fit_uniform(circle_box, (-5, -5), (5, 5), self.canvas, self.padding)
        circle_box = t.zoom_and_pan(circle_box, self.scale, self.offset)
        self._draw_oval(t.flatten(circle_box), outline="blue", width=3)

    # ------------------------------------------------------------------
    # QPainter primitives - see core/draw.py, which these mirror
    # ------------------------------------------------------------------

    def _draw_line(self, coords, color: str, width: float = 1):
        painter = self.canvas.painter
        painter.setPen(QPen(QColor(color), width))
        if isinstance(coords[0], (tuple, list)):
            painter.drawPolyline(QPolygonF([QPointF(x, y) for x, y in coords]))
        else:
            x1, y1, x2, y2 = coords
            painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))

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

    def _draw_text(self, x: float, y: float, text: str, font, color: str):
        '''
        Tk's create_text defaults to a "center" anchor when none is given,
        which every text call in this file relies on.
        '''
        metrics = QFontMetricsF(font)
        width = metrics.horizontalAdvance(text)
        height = metrics.height()
        rect = QRectF(x - width / 2, y - height / 2, width, height)
        painter = self.canvas.painter
        painter.setFont(font)
        painter.setPen(QColor(color))
        painter.drawText(rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop, text)

    def line(self, points: list[tuple[float, float]], line_color: str, thickness=2):
        '''
        Draws the path of the points
        '''
        if len(points) < 2:
            return
        points = t.padded_fit_uniform(points, self.input_range[0], self.input_range[1], self.canvas, self.padding)
        points = t.zoom_and_pan(points, self.scale, self.offset)
        self._draw_line(points, line_color, 1)

    def arc(self, center: tuple[float, float], radius: float, start_angle: float, end_angle: float, line_color: str, thickness=2):
        '''
        Draws an arc with the given parameters. Angles are in radians, 0 is to the right, and positive is counterclockwise.
        '''
        num_points = int(radius * abs(end_angle - start_angle) + 5)
        points = t.get_arc_points(center, radius, start_angle, end_angle, num_points)
        points = t.padded_fit_uniform(points, self.input_range[0], self.input_range[1], self.canvas, self.padding)
        points = t.zoom_and_pan(points, self.scale, self.offset)
        self._draw_line(points, line_color, 2)

    def grid_lines(self):
        font = QFont("Courier", 7)
        for i in range(0, 210, 10):
            h_line = [(0, i), (200, i)]
            v_line = t.rotate(h_line, PI/2, (i, i))
            h_line = t.padded_fit_uniform(h_line, self.input_range[0], self.input_range[1], self.canvas, self.padding)
            v_line = t.padded_fit_uniform(v_line, self.input_range[0], self.input_range[1], self.canvas, self.padding)
            h_line = t.zoom_and_pan(h_line, self.scale, self.offset)
            v_line = t.zoom_and_pan(v_line, self.scale, self.offset)
            color = "white"
            if i == 0:
                color = "red"
            self._draw_line(h_line, color, 0.5)
            self._draw_line(v_line, color, 0.5)

            # Draw labels every 20 units using already-transformed coordinates
            if i % 20 == 0:
                # h_line goes from (0,i) to (200,i) — use its left end for the Y axis label
                # v_line goes from (i,0) to (i,200) — use its top end for the X axis label
                x_pixel = v_line[0][0]   # x position of vertical line = X axis label position
                y_pixel = h_line[0][1]   # y position of horizontal line = Y axis label position

                # X axis label — sits above the top of each vertical line
                self._draw_text(x_pixel, v_line[0][1] + 10, str(i), font, "#3a6070")
                # Y axis label — sits to the left of each horizontal line
                self._draw_text(h_line[0][0] - 16, y_pixel, str(i), font, "#3a6070")

    def boat(self, position: tuple[float, float], bearing: float, fill_color="gray", line_color="black", scale=2.0):
        the_boat = [
                            (-2, 1),
                            (-2, -1),
                            (1,  -1),
                            (3,  0),
                            (1,  1)
                        ]
        the_boat = t.rotate(the_boat, bearing)
        the_boat = t.scale(the_boat, scale)

        the_boat = t.translate(the_boat, position)

        the_boat = t.padded_fit_uniform(the_boat, self.input_range[0], self.input_range[1], self.canvas, 20)
        the_boat = t.zoom_and_pan(the_boat, self.scale, self.offset)
        self._draw_polygon(the_boat, fill=fill_color, outline=line_color)
