import math

import numpy as np
from PySide6.QtCore import QLineF, QPointF, Qt
from PySide6.QtGui import QPainter, QPen

from .base import Visual, VisualPalette


class Constellation(Visual):
    '''
    A constellation diagram, like a QAM receiver's: a grid of clusters,
    each a cloud of short-lived points blinking in and out, normally
    scattered around the cluster's center - received symbols around their
    ideal spots.

    Detailed: dense clusters with a little phase-noise wobble in each
    center. Simple: sparser, steadier clusters.

    Startup: points blink in around the middle of the screen - about half
    the screen's height across - faster and faster. Once that one cluster
    is full, its focal point splits in two, then four, eight... gliding
    apart each time, until the screen is covered in a grid of clusters.
    '''

    KEY = "constellation"
    SPACING_BUTTONS = 4.0     # grid spacing between cluster centers, in button heights
    SPREAD = 0.13             # each cluster's scatter (sigma), as a fraction of its cell
    LIFE = (1.0, 2.2)         # s a point lives, blinking in and out
    PER_CLUSTER = {"detailed": 26, "simple": 12}   # points alive per cluster, steady state
    WOBBLE = 0.07             # detailed: cluster centers drift by this fraction of a cell
    # Startup
    FIRST_CLUSTER = 320       # points in the single cluster before it starts splitting
    GROWTH_START = 4.0        # births per second when the startup begins...
    GROWTH_DOUBLING = 0.45    # ...doubling every this many seconds
    FULL_HOLD = 0.5           # s the full single cluster holds before the first split
    SPLIT_EVERY = 0.85        # s between splits
    SPLIT_GLIDE = 0.7         # s a split takes to glide apart
    ALPHA_LEVELS = 5

    def on_resize(self, first: bool):
        self.spacing = max(40.0, self.SPACING_BUTTONS * self.button_height())
        self.clock = getattr(self, "clock", 0.0)
        self.empty_points()
        self.birth_due = 0.0
        if first and self.claim_intro():
            self.cells = [self.cell(self.width / 2, self.height / 2, self.width, self.height)]
            self.intro = {"stage": "grow", "timer": 0.0}
        else:
            self.settle()

    # Cells - each a cluster's region of the screen
    def cell(self, cx: float, cy: float, w: float, h: float, start: tuple[float, float] | None = None) -> dict:
        x, y = start if start is not None else (cx, cy)
        return {"cx": cx, "cy": cy, "w": w, "h": h, "x": x, "y": y, "from": (x, y), "glide": 0.0 if start else 1.0,
                "phase": self.rng.uniform(0, math.tau)}

    def can_split(self) -> bool:
        cell = self.cells[0]
        return max(cell["w"], cell["h"]) > self.spacing * 1.3

    def split(self):
        '''Every cluster splits in two along its cell's longer side, the halves gliding apart from where it was.'''
        children = []
        for cell in self.cells:
            w, h = cell["w"], cell["h"]
            if w >= h:
                halves = [(cell["cx"] - w / 4, cell["cy"], w / 2, h), (cell["cx"] + w / 4, cell["cy"], w / 2, h)]
            else:
                halves = [(cell["cx"], cell["cy"] - h / 4, w, h / 2), (cell["cx"], cell["cy"] + h / 4, w, h / 2)]
            children += [self.cell(*half, start=(cell["x"], cell["y"])) for half in halves]
        self.cells = children

    def final_cells(self) -> list[dict]:
        self.cells = [self.cell(self.width / 2, self.height / 2, self.width, self.height)]
        while self.can_split():
            self.split()
        for cell in self.cells:
            cell["x"], cell["y"], cell["glide"] = cell["cx"], cell["cy"], 1.0
        return self.cells

    def settle(self):
        '''Straight to the finished grid, already populated.'''
        self.intro = None
        self.final_cells()
        self.empty_points()
        # A full steady population, each point partway through its life
        self.birth(self.steady_target())
        self.age[:] = self.np_rng().uniform(0, 1, len(self.age)) * self.life

    # Points
    def np_rng(self) -> np.random.Generator:
        if not hasattr(self, "_np_rng"):
            self._np_rng = np.random.default_rng(self.rng.randrange(2 ** 32))
        return self._np_rng

    def empty_points(self):
        self.px, self.py, self.age, self.life = (np.zeros(0) for _ in range(4))

    def steady_target(self) -> int:
        return self.PER_CLUSTER["detailed" if self.detailed else "simple"] * len(self.cells)

    def birth(self, count: int):
        if count <= 0:
            return
        rng = self.np_rng()
        which = rng.integers(0, len(self.cells), count)
        cx = np.array([cell["x"] for cell in self.cells])[which]
        cy = np.array([cell["y"] for cell in self.cells])[which]
        sigma = self.SPREAD * min(self.cells[0]["w"], self.cells[0]["h"])
        self.px = np.concatenate([self.px, cx + rng.normal(0, sigma, count)])
        self.py = np.concatenate([self.py, cy + rng.normal(0, sigma, count)])
        self.age = np.concatenate([self.age, np.zeros(count)])
        self.life = np.concatenate([self.life, rng.uniform(*self.LIFE, count)])

    # Simulation
    def update(self, dt: float):
        self.clock += dt
        self.age += dt
        alive = self.age < self.life
        self.px, self.py, self.age, self.life = self.px[alive], self.py[alive], self.age[alive], self.life[alive]

        for cell in self.cells:
            if cell["glide"] < 1.0:
                cell["glide"] = min(1.0, cell["glide"] + dt / self.SPLIT_GLIDE)
                eased = 1 - (1 - cell["glide"]) ** 3
                fx, fy = cell["from"]
                cell["x"], cell["y"] = fx + (cell["cx"] - fx) * eased, fy + (cell["cy"] - fy) * eased
            elif self.detailed:
                # Phase noise: each center drifts in a small slow loop
                wobble = self.WOBBLE * min(cell["w"], cell["h"])
                t = self.clock * 0.9 + cell["phase"]
                cell["x"] = cell["cx"] + wobble * math.cos(t) * math.sin(t * 0.61)
                cell["y"] = cell["cy"] + wobble * math.sin(t * 1.3)
            else:
                cell["x"], cell["y"] = cell["cx"], cell["cy"]

        mean_life = sum(self.LIFE) / 2
        if self.intro is None:
            rate = self.steady_target() / mean_life
        else:
            rate = self.update_intro(dt, mean_life)
        self.birth_due += rate * dt
        count = int(self.birth_due)
        self.birth_due -= count
        self.birth(count)

    def update_intro(self, dt: float, mean_life: float) -> float:
        '''Advances the startup and returns the birth rate it wants right now.'''
        intro = self.intro
        intro["timer"] += dt
        if intro["stage"] == "grow":
            rate = self.GROWTH_START * 2 ** (intro["timer"] / self.GROWTH_DOUBLING)
            if len(self.px) >= self.FIRST_CLUSTER:
                intro.update(stage="hold", timer=0.0)
            return min(rate, self.FIRST_CLUSTER / mean_life * 1.5)
        if intro["timer"] >= (self.FULL_HOLD if intro["stage"] == "hold" else self.SPLIT_EVERY):
            if self.can_split():
                self.split()
                intro.update(stage="split", timer=0.0)
            else:
                self.intro = None
        return max(self.FIRST_CLUSTER, self.steady_target()) / mean_life

    # Drawing
    def paint(self, painter: QPainter, palette: VisualPalette):
        # The I/Q axes through the middle, as on a real constellation plot
        painter.setPen(QPen(palette.color("foreground", 0.12), 1.0))
        painter.drawLines([QLineF(0, self.height / 2, self.width, self.height / 2),
                           QLineF(self.width / 2, 0, self.width / 2, self.height)])

        if not len(self.px):
            return
        # Each point blinks: fades in, holds, fades out over its life
        progress = self.age / self.life
        brightness = np.clip(np.minimum(progress / 0.15, (1 - progress) / 0.35), 0.0, 1.0)
        levels = np.minimum((brightness * self.ALPHA_LEVELS).astype(int), self.ALPHA_LEVELS - 1)
        for level in range(self.ALPHA_LEVELS):
            index = np.flatnonzero(levels == level)
            if not len(index):
                continue
            pen = QPen(palette.color("accent", 0.25 + 0.75 * (level + 1) / self.ALPHA_LEVELS), 3.6)
            pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)
            painter.drawPoints([QPointF(self.px[i], self.py[i]) for i in index])
