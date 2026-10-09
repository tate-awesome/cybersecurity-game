import math

import numpy as np
from PySide6.QtCore import QLineF, QPointF, Qt
from PySide6.QtGui import QPainter, QPen

from .base import Visual, VisualPalette


class VectorField(Visual):
    '''
    A grid of vectors across the screen, like a field plot.

    Detailed: devoted to the mouse - every vector points at it, longer the
    further away it is, while a drifting noise pattern bends the far ones
    a little off target, so the field looks blown by the wind but still
    turned toward the mouse. Simple: the wind alone - a slowly turning
    prevailing direction with gusts rippling through it.

    Startup: a cloud of points flies out from the mouse to the field. The
    vectors are already there, invisibly - each point heads for its
    vector's tip, and from the tip runs down to the base, drawing the
    vector in behind it as it goes.

    Vectors ease toward where they should point instead of snapping, so
    changing mode or a jumpy mouse turns the field smoothly.
    '''

    KEY = "vector_field"
    SPACING_BUTTONS = 1.6    # grid spacing, in button heights
    MAX_LENGTH = 0.85        # longest vector, as a fraction of spacing
    TURN_RATE = 6.0          # 1/s - how fast vectors ease toward their target
    REACH = 0.08             # detailed: vector length per px of distance to the mouse
    MAX_BEND = 0.9           # detailed: radians the wind can bend the farthest vectors
    # Startup flight
    LAUNCH_SPREAD = 0.35     # s over which the points leave the mouse
    FLY_SPEED = (650.0, 950.0)   # px/s to the tip
    DRAW_SPEED = 140.0       # px/s tracing tip to base

    def on_resize(self, first: bool):
        self.spacing = max(16.0, self.SPACING_BUTTONS * self.button_height())
        self.max_length = self.spacing * self.MAX_LENGTH
        cols = int(self.width / self.spacing) + 1
        rows = int(self.height / self.spacing) + 1
        xs = (self.width - (cols - 1) * self.spacing) / 2 + np.arange(cols) * self.spacing
        ys = (self.height - (rows - 1) * self.spacing) / 2 + np.arange(rows) * self.spacing
        grid_x, grid_y = np.meshgrid(xs, ys)
        self.base_x, self.base_y = grid_x.ravel(), grid_y.ravel()
        if first or not hasattr(self, "vec_x"):
            self.clock = 0.0
            self.target = (self.width / 2, self.height / 2)
            self.intro = None
            self.vec_x, self.vec_y = self.aim()
            if self.claim_intro():
                self.start_intro()
        else:
            # A new grid: its vectors start where they should point, and an
            # intro in progress (sized to the old grid) just finishes
            self.vec_x, self.vec_y = self.aim()
            self.intro = None

    # The field
    def wind(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        '''Smooth drifting noise in about -1..1 - a few crossed sine waves sliding at different speeds.'''
        t = self.clock
        return (np.sin(x * 0.0061 + t * 0.53) + np.sin(y * 0.0083 - t * 0.41)
                + np.sin((x + y) * 0.0037 + t * 0.29) + np.sin((x - 1.7 * y) * 0.0049 - t * 0.37)) / 4

    def aim(self) -> tuple[np.ndarray, np.ndarray]:
        '''Where every vector should point right now, as (x, y) components.'''
        x, y = self.base_x, self.base_y
        noise = self.wind(x, y)
        if self.detailed:
            tx, ty = self.target
            dx, dy = tx - x, ty - y
            distance = np.hypot(dx, dy)
            far = np.clip(distance / (0.6 * math.hypot(self.width, self.height)), 0.0, 1.0)
            angle = np.arctan2(dy, dx) + noise * self.MAX_BEND * far
            length = np.clip(distance * self.REACH, self.max_length * 0.15, self.max_length)
        else:
            prevailing = 0.6 * math.sin(self.clock * 0.05) + 0.35 * math.sin(self.clock * 0.13 + 1.0)
            angle = prevailing + noise * 1.1
            gust = self.wind(x * 0.7 + 400, y * 0.7 - 300)
            length = self.max_length * np.clip(0.55 + 0.4 * gust, 0.15, 1.0)
        return np.cos(angle) * length, np.sin(angle) * length

    def update(self, dt: float):
        self.clock += dt
        if self.pointer is not None:
            self.target = self.pointer
        aim_x, aim_y = self.aim()
        ease = 1.0 - math.exp(-self.TURN_RATE * dt)
        self.vec_x += (aim_x - self.vec_x) * ease
        self.vec_y += (aim_y - self.vec_y) * ease
        if self.intro is not None:
            self.update_intro(dt)

    # Startup
    def start_intro(self):
        count = len(self.base_x)
        launch_x, launch_y = self.pointer if self.pointer is not None else self.target
        self.intro = {
            "x": np.full(count, float(launch_x)), "y": np.full(count, float(launch_y)),
            "delay": self.np_rng().uniform(0.0, self.LAUNCH_SPREAD, count),
            "speed": self.np_rng().uniform(*self.FLY_SPEED, count),
            # 0 flying to the tip, 1 tracing tip to base (drawn fraction in "drawn"), 2 done
            "phase": np.zeros(count, dtype=int),
            "drawn": np.zeros(count),
        }

    def np_rng(self) -> np.random.Generator:
        if not hasattr(self, "_np_rng"):
            self._np_rng = np.random.default_rng(self.rng.randrange(2 ** 32))
        return self._np_rng

    def update_intro(self, dt: float):
        intro = self.intro
        intro["delay"] -= dt
        flying = (intro["phase"] == 0) & (intro["delay"] <= 0)
        tip_x, tip_y = self.base_x + self.vec_x, self.base_y + self.vec_y
        dx, dy = tip_x - intro["x"], tip_y - intro["y"]
        distance = np.hypot(dx, dy)
        step = intro["speed"] * dt
        arrived = flying & (distance <= step)
        moving = flying & ~arrived
        scale = np.where(moving, step / np.maximum(distance, 1e-6), 0.0)
        intro["x"] += dx * scale
        intro["y"] += dy * scale
        intro["phase"][arrived] = 1

        tracing = intro["phase"] == 1
        length = np.maximum(np.hypot(self.vec_x, self.vec_y), 1.0)
        intro["drawn"][tracing] += self.DRAW_SPEED * dt / length[tracing]
        intro["phase"][tracing & (intro["drawn"] >= 1.0)] = 2
        np.clip(intro["drawn"], 0.0, 1.0, out=intro["drawn"])
        if np.all(intro["phase"] == 2):
            self.intro = None

    def settle(self):
        self.intro = None

    # Drawing
    def paint(self, painter: QPainter, palette: VisualPalette):
        tip_x, tip_y = self.base_x + self.vec_x, self.base_y + self.vec_y
        if self.intro is None:
            shown = np.arange(len(self.base_x))
            start_x, start_y = self.base_x, self.base_y
        else:
            phase, drawn = self.intro["phase"], self.intro["drawn"]
            shown = np.flatnonzero(phase >= 1)
            # A traced vector runs from its tip back to how far its point has got
            start_x = tip_x - self.vec_x * drawn
            start_y = tip_y - self.vec_y * drawn

        lines = [QLineF(start_x[i], start_y[i], tip_x[i], tip_y[i]) for i in shown]
        pen = QPen(palette.color("foreground", 0.45), 1.5)
        # Flat caps: round ones on lines wider than 1px are several times
        # slower to draw, and at this size look no different
        pen.setCapStyle(Qt.PenCapStyle.FlatCap)
        painter.setPen(pen)
        painter.drawLines(lines)

        # Tips, so each line reads as a vector with a direction
        tips = [QPointF(tip_x[i], tip_y[i]) for i in shown if self.intro is None or self.intro["phase"][i] == 2]
        tip_pen = QPen(palette.color("accent", 0.75), 3.2)
        tip_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(tip_pen)
        painter.drawPoints(tips)

        if self.intro is not None:
            # The flying points, and the heads still tracing their vectors
            phase = self.intro["phase"]
            flying = np.flatnonzero((phase == 0) & (self.intro["delay"] <= 0))
            tracing = np.flatnonzero(phase == 1)
            heads = [QPointF(self.intro["x"][i], self.intro["y"][i]) for i in flying]
            heads += [QPointF(start_x[i], start_y[i]) for i in tracing]
            head_pen = QPen(palette.color("accent", 0.95), 4.0)
            head_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            painter.setPen(head_pen)
            painter.drawPoints(heads)
