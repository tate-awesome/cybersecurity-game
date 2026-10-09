import math

import numpy as np
from PySide6.QtCore import QLineF, Qt
from PySide6.QtGui import QPainter, QPen

from .base import Visual, VisualPalette


class WaveGrid(Visual):
    '''
    A dense grid of short lines whose thickness shows waves spreading out
    across it - rings that start at random points at random times and
    ripple outward in every direction.

    Each wave grows from a single point: its ring starts tiny and widens as
    it spreads, with its ripples trailing behind the front.

    Detailed: frequent, quick, tightly rippled waves that die away fast -
    a puddle in a drizzle. Any line a wave reaches steps up to a clearly
    thicker, accent-colored minimum, so even a single wave reads as a
    colored band rather than a stray line or two. Simple: broad waves,
    starting at random times, that travel and fade slowly, so monochrome
    patterns drift across the screen - thickness rising smoothly from the
    dead grid.

    Startup: one very strong wave, which never fades, sweeps out from the
    center, and the grid's lines draw themselves in just behind its front
    until they fill the screen.

    The grid itself never moves - only each line's thickness changes - so
    the lines are built once per size and sorted into a few thickness
    levels each frame, one drawLines call per level.
    '''

    KEY = "wave_grid"
    CELL_BUTTONS = 0.75      # grid cell size, in button heights
    LEVELS = 12              # thickness steps a line can be drawn at
    DEAD_WIDTH = 0.6         # px - the grid where no wave is
    PEAK_WIDTH = 14.0        # px - at a wave's peak
    # Detailed: a wave stronger than ACTIVE lifts a line straight to
    # ACTIVE_WIDTH (and the accent color), then on up to PEAK_WIDTH
    ACTIVE = 0.12
    ACTIVE_WIDTH = 2.6
    INTRO_SECONDS = 2.4      # for the startup wave to reach the corners
    # Wave settings by mode - speed px/s, decay 1/s (amplitude e-folds),
    # width px (of the ring's envelope), wavelength px (ripples within it,
    # 0 for none), spread px (distance over which it weakens as it widens)
    DETAILED = {"rate": 4.0, "speed": (120.0, 170.0), "decay": (0.9, 1.3), "width": 24.0, "wavelength": 26.0,
                "amp": (0.8, 1.2), "spread": 260.0}
    SIMPLE = {"rate": 1 / 6, "speed": (20.0, 30.0), "decay": (0.05, 0.08), "width": 340.0, "wavelength": 230.0,
              "amp": (0.8, 1.0), "spread": 1500.0}   # rate: waves per second, at random times

    def on_resize(self, first: bool):
        if not first and hasattr(self, "waves"):
            for wave in self.waves:
                wave["x"] *= self.scale_x
                wave["y"] *= self.scale_y
        self.build_grid()
        if first or not hasattr(self, "waves"):
            self.clock = 0.0
            self.waves: list[dict] = []
            self.spawn_due = 0.0
            self.intro: dict | None = None
            if self.claim_intro():
                self.start_intro()

    def build_grid(self):
        self.cell = max(10.0, self.CELL_BUTTONS * self.button_height())
        cols = int(math.ceil(self.width / self.cell)) + 2
        rows = int(math.ceil(self.height / self.cell)) + 2
        # Centered, so the startup wave's center sits on a grid point
        x0 = self.width / 2 - (cols // 2) * self.cell
        y0 = self.height / 2 - (rows // 2) * self.cell
        xs = x0 + np.arange(cols) * self.cell
        ys = y0 + np.arange(rows) * self.cell
        # Horizontal segments then vertical ones, as endpoint arrays
        hx0, hy = np.meshgrid(xs[:-1], ys)
        vx, vy0 = np.meshgrid(xs, ys[:-1])
        ax = np.concatenate([hx0.ravel(), vx.ravel()])
        ay = np.concatenate([hy.ravel(), vy0.ravel()])
        bx = np.concatenate([hx0.ravel() + self.cell, vx.ravel()])
        by = np.concatenate([hy.ravel(), vy0.ravel() + self.cell])
        self.mid_x, self.mid_y = (ax + bx) / 2, (ay + by) / 2
        self.lines = [QLineF(x1, y1, x2, y2) for x1, y1, x2, y2 in zip(ax, ay, bx, by)]

        # For the startup draw-in: each segment grows from its endpoint
        # nearer the center toward the other one
        cx, cy = self.width / 2, self.height / 2
        a_dist = np.hypot(ax - cx, ay - cy)
        b_dist = np.hypot(bx - cx, by - cy)
        a_near = a_dist <= b_dist
        self.near_x, self.near_y = np.where(a_near, ax, bx), np.where(a_near, ay, by)
        self.far_x, self.far_y = np.where(a_near, bx, ax), np.where(a_near, by, ay)
        self.near_dist = np.minimum(a_dist, b_dist)

    # Waves
    def start_intro(self):
        cx, cy = self.width / 2, self.height / 2
        reach = math.hypot(cx, cy) + 2 * self.cell
        self.intro = {"x": cx, "y": cy, "born": self.clock, "speed": reach / self.INTRO_SECONDS, "amp": 1.0, "decay": 0.0,
                      "width": self.cell * 1.6, "wavelength": 0.0, "spread": 0.0}
        self.intro_reach = reach
        self.waves.append(self.intro)

    def settle(self):
        if self.intro is not None:
            self.waves.remove(self.intro)
            self.intro = None

    def spawn(self, settings: dict):
        self.waves.append({
            "x": self.rng.uniform(0, self.width), "y": self.rng.uniform(0, self.height), "born": self.clock,
            "speed": self.rng.uniform(*settings["speed"]), "amp": self.rng.uniform(*settings["amp"]),
            "decay": self.rng.uniform(*settings["decay"]), "width": settings["width"],
            "wavelength": settings["wavelength"], "spread": settings["spread"],
        })

    def update(self, dt: float):
        self.clock += dt
        if self.intro is not None:
            if self.radius(self.intro) >= self.intro_reach:
                self.intro = None  # its wave carries on off the screen
        elif self.detailed:
            area = self.width * self.height / 1_000_000
            self.spawn_due += dt * self.DETAILED["rate"] * area
            while self.spawn_due >= 1.0:
                self.spawn_due -= 1.0
                self.spawn(self.DETAILED)
        elif self.rng.random() < dt * self.SIMPLE["rate"]:
            # Random arrivals (a Poisson process), so sometimes one wave,
            # sometimes several overlapping, never a fixed rhythm
            self.spawn(self.SIMPLE)

        diagonal = math.hypot(self.width, self.height)
        self.waves = [wave for wave in self.waves
                      if wave is self.intro or (self.strength(wave) > 0.02 and self.radius(wave) - 3 * wave["width"] < diagonal)]

    def radius(self, wave: dict) -> float:
        return wave["speed"] * (self.clock - wave["born"])

    def strength(self, wave: dict) -> float:
        return wave["amp"] * math.exp(-wave["decay"] * (self.clock - wave["born"]))

    def heights(self) -> np.ndarray:
        '''How strongly the waves move each segment, about 0-1.'''
        height = np.zeros_like(self.mid_x)
        sharp = self.cell * 0.6
        for wave in self.waves:
            strength = self.strength(wave)
            radius = self.radius(wave)
            r = np.hypot(self.mid_x - wave["x"], self.mid_y - wave["y"])
            u = r - radius
            # Growing from a point: the ring is only as wide as it is far
            # out, up to its full width, and falls off sharply ahead of its
            # front - the ripples trail behind it
            width = max(sharp, min(wave["width"], radius * 0.6))
            envelope = np.exp(-(np.where(u > 0, u / sharp, u / width)) ** 2)
            if wave["wavelength"]:
                wavelength = max(self.cell, min(wave["wavelength"], radius * 0.5))
                envelope *= 0.55 + 0.45 * np.cos(2 * math.pi * np.minimum(u, 0.0) / wavelength)
            if wave["spread"]:
                envelope /= 1.0 + r / wave["spread"]
            height += strength * envelope
        return height

    # Drawing
    def levels(self) -> np.ndarray:
        '''Each segment's thickness level, 0 (dead grid) to LEVELS - 1 (peak).'''
        height = np.clip(self.heights(), 0.0, 1.0)
        top = self.LEVELS - 1
        if not self.detailed:
            return np.rint(height * top).astype(int)
        # Detailed: a step up out of the dead grid - level 0 below ACTIVE,
        # then 1 (ACTIVE_WIDTH) to top across the rest of the range
        active = height >= self.ACTIVE
        scaled = 1 + np.rint((height - self.ACTIVE) / (1.0 - self.ACTIVE) * (top - 1)).astype(int)
        return np.where(active, np.clip(scaled, 1, top), 0)

    def style(self, level: int, palette: VisualPalette) -> QPen:
        top = self.LEVELS - 1
        if level == 0:
            return QPen(palette.color("foreground", 0.08), self.DEAD_WIDTH)
        if self.detailed:
            t = (level - 1) / (top - 1)
            return QPen(palette.color("accent", 0.45 + 0.45 * t), self.ACTIVE_WIDTH + (self.PEAK_WIDTH - self.ACTIVE_WIDTH) * t)
        t = level / top
        return QPen(palette.color("foreground", 0.08 + 0.42 * t), self.DEAD_WIDTH + (self.PEAK_WIDTH - self.DEAD_WIDTH) * t)

    def paint(self, painter: QPainter, palette: VisualPalette):
        levels = self.levels()
        buckets: list[list[QLineF]] = [[] for _ in range(self.LEVELS)]

        if self.intro is None:
            for level in range(self.LEVELS):
                buckets[level] = [self.lines[i] for i in np.flatnonzero(levels == level)]
        else:
            # Drawn in behind the startup wave's front: whole segments
            # inside it, and the ones it's crossing grown partway out
            front = self.radius(self.intro)
            grown = np.clip((front - self.near_dist) / self.cell, 0.0, 1.0)
            for index in np.flatnonzero(grown >= 1.0):
                buckets[levels[index]].append(self.lines[index])
            for index in np.flatnonzero((grown > 0.0) & (grown < 1.0)):
                f = grown[index]
                nx, ny = self.near_x[index], self.near_y[index]
                buckets[levels[index]].append(QLineF(nx, ny, nx + (self.far_x[index] - nx) * f, ny + (self.far_y[index] - ny) * f))

        # Every line is horizontal or vertical, so antialiasing buys nothing
        # but cost - it more than doubles the time thick lines take
        antialiased = painter.testRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)
        for level, lines in enumerate(buckets):
            if not lines:
                continue
            pen = self.style(level, palette)
            pen.setCapStyle(Qt.PenCapStyle.SquareCap)
            painter.setPen(pen)
            painter.drawLines(lines)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, antialiased)
