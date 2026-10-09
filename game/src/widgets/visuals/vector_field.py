import math

import numpy as np
from PySide6.QtCore import QLineF, QPointF, Qt
from PySide6.QtGui import QPainter, QPen

from .base import Visual, VisualPalette


class VectorField(Visual):
    '''
    A grid of vectors across the screen, like a field plot.

    Detailed: devoted to the mouse but out in real weather - every vector
    points at the mouse, longer the further away it is, while the wind
    bends the far ones off target and gusts swell and shrink them as they
    blow through (a moving noise map scales every vector's length). The
    wind has moods (see gust): calmer spells and wild ones where it churns
    faster still and bends hard. A few big translucent discs ride the
    field in to the mouse, then blow back in from the edge for another run.
    Simple: steady wind alone, paying the mouse no attention - longer
    vectors, moving briskly but without the gusts, all in the foreground
    color, with no discs.

    Startup: a cloud of points flies out from the mouse to the field. The
    vectors are already there, invisibly - each point heads for its
    vector's tip, and from the tip runs down to the base, drawing the
    vector in behind it as it goes.

    Vectors ease toward where they should point instead of snapping, so
    changing mode or a jumpy mouse turns the field smoothly.
    '''

    KEY = "vector_field"
    SPACING_BUTTONS = 1.6    # grid spacing, in button heights
    MAX_LENGTH = {"detailed": 0.85, "simple": 1.35}   # longest vector, as a fraction of spacing
    TURN_RATE = 10.0         # 1/s - how fast vectors ease toward their target
    REACH = 0.08             # detailed: vector length per px of distance to the mouse
    MAX_BEND = 1.8           # detailed: radians the wildest wind bends the farthest vectors
    WIND_PACE = {"calm": 2.8, "wild": 8.4, "simple": 2.8}   # how fast the wind pattern moves, by mood
    GUST_SHRINK = 0.75       # detailed: how far a lull in the gust map can shrink a vector (0-1)
    # Discs riding the field (detailed only)
    BALLS = 3
    BALL_SPEED = 4.0         # px/s of disc speed per px of vector length
    BALL_GRIP = 2.5          # 1/s - how quickly a disc takes up the field's velocity
    BALL_RADIUS = 1.5        # in grid spacings
    # Startup flight
    LAUNCH_SPREAD = 0.35     # s over which the points leave the mouse
    FLY_SPEED = (650.0, 950.0)   # px/s to the tip
    DRAW_SPEED = 140.0       # px/s tracing tip to base

    def on_resize(self, first: bool):
        self.spacing = max(16.0, self.SPACING_BUTTONS * self.button_height())
        cols = int(self.width / self.spacing) + 1
        rows = int(self.height / self.spacing) + 1
        xs = (self.width - (cols - 1) * self.spacing) / 2 + np.arange(cols) * self.spacing
        ys = (self.height - (rows - 1) * self.spacing) / 2 + np.arange(rows) * self.spacing
        grid_x, grid_y = np.meshgrid(xs, ys)
        self.base_x, self.base_y = grid_x.ravel(), grid_y.ravel()
        if first or not hasattr(self, "vec_x"):
            self.clock = 0.0
            self.wind_clock = 0.0
            self.target = (self.width / 2, self.height / 2)
            self.intro = None
            self.vec_x, self.vec_y = self.aim(self.base_x, self.base_y)
            self.balls = [self.new_ball() for _ in range(self.BALLS)]
            if self.claim_intro():
                self.start_intro()
        else:
            # A new grid: its vectors start where they should point, and an
            # intro in progress (sized to the old grid) just finishes
            self.vec_x, self.vec_y = self.aim(self.base_x, self.base_y)
            self.intro = None
            for ball in self.balls:
                ball["x"] *= self.scale_x
                ball["y"] *= self.scale_y

    def max_length(self) -> float:
        return self.spacing * self.MAX_LENGTH["detailed" if self.detailed else "simple"]

    # The wind
    def gust(self) -> float:
        '''
        The wind's mood, 0 (dead calm) to 1 (wild): a slow wander built
        from long, unrelated periods, squared so calm spells last longer
        than the wild ones.
        '''
        t = self.clock
        mood = (math.sin(t * 0.21) + math.sin(t * 0.137 + 2.0) + math.sin(t * 0.083 + 4.1)) / 3
        return (0.5 + 0.5 * mood) ** 2

    def wind(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        '''Smooth drifting noise in about -1..1 - a few crossed sine waves sliding at different speeds.'''
        t = self.wind_clock
        return (np.sin(x * 0.0061 + t * 0.53) + np.sin(y * 0.0083 - t * 0.41)
                + np.sin((x + y) * 0.0037 + t * 0.29) + np.sin((x - 1.7 * y) * 0.0049 - t * 0.37)) / 4

    def aim(self, x: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        '''Where the field points at (x, y) right now, as (x, y) components.'''
        noise = self.wind(x, y)
        longest = self.max_length()
        if self.detailed:
            tx, ty = self.target
            dx, dy = tx - x, ty - y
            distance = np.hypot(dx, dy)
            far = np.clip(distance / (0.6 * math.hypot(self.width, self.height)), 0.0, 1.0)
            bend = self.MAX_BEND * (0.3 + 0.7 * self.gust())
            angle = np.arctan2(dy, dx) + noise * bend * far
            # Gusts: a second, offset noise map swells and shrinks the
            # vectors as it sweeps through, so the wind visibly blows
            swell = 0.5 + 0.5 * self.wind(x * 0.6 - 230, y * 0.6 + 170)
            length = np.clip(distance * self.REACH, longest * 0.15, longest) * (1.0 - self.GUST_SHRINK * (1.0 - swell))
        else:
            prevailing = 0.6 * math.sin(self.wind_clock * 0.05) + 0.35 * math.sin(self.wind_clock * 0.13 + 1.0)
            angle = prevailing + noise * 1.1
            length = longest * np.clip(0.55 + 0.4 * self.wind(x * 0.7 + 400, y * 0.7 - 300), 0.15, 1.0)
        return np.cos(angle) * length, np.sin(angle) * length

    def update(self, dt: float):
        self.clock += dt
        if self.detailed:
            pace = self.WIND_PACE["calm"] + (self.WIND_PACE["wild"] - self.WIND_PACE["calm"]) * self.gust()
        else:
            pace = self.WIND_PACE["simple"]
        self.wind_clock += dt * pace
        if self.pointer is not None:
            self.target = self.pointer
        aim_x, aim_y = self.aim(self.base_x, self.base_y)
        ease = 1.0 - math.exp(-self.TURN_RATE * dt)
        self.vec_x += (aim_x - self.vec_x) * ease
        self.vec_y += (aim_y - self.vec_y) * ease
        if self.intro is not None:
            self.update_intro(dt)
        elif self.detailed:
            self.update_balls(dt)

    # Balls
    def new_ball(self) -> dict:
        return {"x": self.rng.uniform(0, self.width), "y": self.rng.uniform(0, self.height), "vx": 0.0, "vy": 0.0}

    def update_balls(self, dt: float):
        grip = 1.0 - math.exp(-self.BALL_GRIP * dt)
        xs = np.array([ball["x"] for ball in self.balls])
        ys = np.array([ball["y"] for ball in self.balls])
        fx, fy = self.aim(xs, ys)
        margin = self.spacing
        for ball, field_x, field_y in zip(self.balls, fx, fy):
            ball["vx"] += (field_x * self.BALL_SPEED - ball["vx"]) * grip
            ball["vy"] += (field_y * self.BALL_SPEED - ball["vy"]) * grip
            ball["x"] += ball["vx"] * dt
            ball["y"] += ball["vy"] * dt
            if self.detailed and math.hypot(ball["x"] - self.target[0], ball["y"] - self.target[1]) < self.spacing * 0.6:
                # Reached the mouse, where the field dies away - blow it
                # back in from somewhere along the edge for another run
                self.enter_from_edge(ball)
                continue
            # Blown off one edge, it comes back in at the opposite one
            if not -margin <= ball["x"] <= self.width + margin or not -margin <= ball["y"] <= self.height + margin:
                ball["x"] = (ball["x"] + margin) % (self.width + 2 * margin) - margin
                ball["y"] = (ball["y"] + margin) % (self.height + 2 * margin) - margin

    def enter_from_edge(self, ball: dict):
        side = self.rng.randrange(4)
        along = self.rng.random()
        ball["x"] = (along * self.width, self.width, along * self.width, 0.0)[side]
        ball["y"] = (0.0, along * self.height, self.height, along * self.height)[side]
        ball["vx"] = ball["vy"] = 0.0

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
        # The discs set off from the mouse too, once the field is drawn
        for ball in self.balls:
            ball["x"], ball["y"] = float(launch_x), float(launch_y)

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
        tint = "accent" if self.detailed else "foreground"
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
        tip_pen = QPen(palette.color(tint, 0.75), 3.2)
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
            head_pen = QPen(palette.color(tint, 0.95), 4.0)
            head_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            painter.setPen(head_pen)
            painter.drawPoints(heads)
            return

        if not self.detailed:
            return
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(palette.color("accent", 0.18))
        radius = self.spacing * self.BALL_RADIUS
        for ball in self.balls:
            painter.drawEllipse(QPointF(ball["x"], ball["y"]), radius, radius)
