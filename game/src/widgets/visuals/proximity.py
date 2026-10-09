import math

import numpy as np
from PySide6.QtCore import QLineF, QPointF, Qt
from PySide6.QtGui import QPainter, QPen

from .base import Visual, VisualPalette


class Proximity(Visual):
    '''
    A proximity graph: points drifting slowly across the screen, with a
    line between every two that come within reach of each other - fainter
    the further apart - so links form and break as they wander.

    Detailed: more points, and the mouse is a node too - points near it
    link to it in the accent color and light up. Simple: fewer points,
    paying the mouse no attention. Points beyond the simple count fade out
    (and back in) rather than vanishing when the mode changes.

    Startup: the points appear in a ring spreading out from the center,
    links forming between them as they arrive.
    '''

    KEY = "proximity"
    DENSITY = {"detailed": 110, "simple": 65}   # points per megapixel
    REACH_BUTTONS = 4.6       # link distance, in button heights
    MOUSE_REACH = 1.5         # detailed: the mouse links this many times further
    SPEED = (6.0, 20.0)       # px/s drift
    FADE_RATE = 1.5           # 1/s - points fading in or out on a mode change
    INTRO_SECONDS = 2.2       # for the ring of arriving points to reach the corners
    GROW_SECONDS = 0.5        # each arriving point's fade-in
    ALPHA_LEVELS = 6
    MARGIN = 60.0             # px beyond the edges points can drift before wrapping

    def on_resize(self, first: bool):
        self.reach = max(40.0, self.REACH_BUTTONS * self.button_height())
        count = max(12, int(self.width * self.height / 1_000_000 * self.DENSITY["detailed"]))
        rng = self.np_rng()
        self.x = rng.uniform(0, self.width, count)
        self.y = rng.uniform(0, self.height, count)
        heading = rng.uniform(0, math.tau, count)
        speed = rng.uniform(*self.SPEED, count)
        self.vx, self.vy = np.cos(heading) * speed, np.sin(heading) * speed
        # How present each point is (0-1) - the simple mode's extras fade to 0
        self.weight = np.ones(count)
        self.clock = 0.0
        self.born = np.zeros(count)
        self.intro = False
        if first and self.claim_intro():
            self.intro = True
            # Arrival time grows with distance from the center
            distance = np.hypot(self.x - self.width / 2, self.y - self.height / 2)
            self.born = distance / max(1.0, distance.max()) * self.INTRO_SECONDS + rng.uniform(0, 0.25, count)

    def np_rng(self) -> np.random.Generator:
        if not hasattr(self, "_np_rng"):
            self._np_rng = np.random.default_rng(self.rng.randrange(2 ** 32))
        return self._np_rng

    def settle(self):
        self.intro = False

    def growth(self) -> np.ndarray:
        if not self.intro:
            return np.ones_like(self.x)
        return np.clip((self.clock - self.born) / self.GROW_SECONDS, 0.0, 1.0)

    def update(self, dt: float):
        self.clock += dt
        if self.intro and self.clock > self.born.max() + self.GROW_SECONDS:
            self.intro = False
        self.x += self.vx * dt
        self.y += self.vy * dt
        # Wrap around just off screen, so points drift out of view before reappearing
        span_x, span_y = self.width + 2 * self.MARGIN, self.height + 2 * self.MARGIN
        self.x = (self.x + self.MARGIN) % span_x - self.MARGIN
        self.y = (self.y + self.MARGIN) % span_y - self.MARGIN

        active = int(len(self.x) * self.DENSITY["simple"] / self.DENSITY["detailed"]) if not self.detailed else len(self.x)
        target = np.zeros_like(self.weight)
        target[:active] = 1.0
        step = self.FADE_RATE * dt
        self.weight += np.clip(target - self.weight, -step, step)

    def paint(self, painter: QPainter, palette: VisualPalette):
        presence = self.weight * self.growth()
        shown = np.flatnonzero(presence > 0.01)
        x, y, presence = self.x[shown], self.y[shown], presence[shown]

        # Links: every pair within reach, fainter with distance and with
        # either end's presence
        dx = x[:, None] - x[None, :]
        dy = y[:, None] - y[None, :]
        distance = np.hypot(dx, dy)
        i, j = np.nonzero(np.triu(distance < self.reach, k=1))
        strength = (1.0 - distance[i, j] / self.reach) ** 1.5 * np.minimum(presence[i], presence[j])
        levels = np.minimum((strength * self.ALPHA_LEVELS).astype(int), self.ALPHA_LEVELS - 1)
        for level in range(self.ALPHA_LEVELS):
            pick = np.flatnonzero(levels == level)
            if not len(pick):
                continue
            pen = QPen(palette.color("foreground", 0.05 + 0.4 * (level + 1) / self.ALPHA_LEVELS), 1.0)
            painter.setPen(pen)
            painter.drawLines([QLineF(x[i[k]], y[i[k]], x[j[k]], y[j[k]]) for k in pick])

        # The mouse as a node, in detailed mode
        near = np.zeros(len(x), dtype=bool)
        if self.detailed and self.pointer is not None:
            mx, my = self.pointer
            mouse_reach = self.reach * self.MOUSE_REACH
            to_mouse = np.hypot(x - mx, y - my)
            near = to_mouse < mouse_reach
            pen = QPen(palette.color("accent", 0.5), 1.0)
            painter.setPen(pen)
            painter.drawLines([QLineF(mx, my, x[k], y[k]) for k in np.flatnonzero(near)])

        # Points
        dim = [QPointF(x[k], y[k]) for k in np.flatnonzero(~near)]
        node_pen = QPen(palette.color("foreground", 0.6), 3.0)
        node_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(node_pen)
        painter.drawPoints(dim)
        if near.any():
            lit_pen = QPen(palette.color("accent", 0.95), 4.0)
            lit_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            painter.setPen(lit_pen)
            painter.drawPoints([QPointF(x[k], y[k]) for k in np.flatnonzero(near)])
