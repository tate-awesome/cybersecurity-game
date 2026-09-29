import math
from collections import deque

from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QPainter, QPainterPath, QPen

from .base import Visual, VisualPalette


class Kalman(Visual):
    '''
    Vessels cruising smooth looping courses over a faint chart grid. Each
    one reports noisy position fixes (scattered dots that fade out), and an
    alpha-beta filter - the fixed-gain cousin of the Kalman filter from the
    submarine defender lesson - turns them into a smooth estimated track.
    The ring around each vessel is the filter's uncertainty, which shrinks
    as fixes agree and swells when one lands far from the prediction.

    The filter itself only runs when a fix arrives (FIX_INTERVAL), but
    everything drawn moves every frame: between fixes the estimate is
    dead-reckoned forward along its velocity, and the drawn vessel eases
    toward that prediction rather than snapping when a fix corrects it.
    '''

    KEY = "kalman"
    FIX_INTERVAL = 0.25
    NOISE = 22.0
    TRAIL_SECONDS = 10.0
    TRACK_INTERVAL = 1 / 30
    ALPHA = 0.25
    BETA = 0.04
    EASE_RATE = 7.0      # 1/s - how quickly the drawn vessel absorbs a correction
    TURN_RATE = 5.0      # 1/s - same for heading
    RING_RATE = 3.0      # 1/s - same for the uncertainty ring

    def on_resize(self, first: bool):
        if first or not hasattr(self, "vessels"):
            self.vessels = [self.new_vessel() for _ in range(self.area_count(2.5, 2, 5))]
            return
        for vessel in self.vessels:
            self.rescale(vessel)

    def rescale(self, vessel: dict):
        sx, sy = self.scale_x, self.scale_y
        vessel["fixes"] = deque((x * sx, y * sy, t) for x, y, t in vessel["fixes"])
        vessel["track"] = deque((x * sx, y * sy, t) for x, y, t in vessel["track"])
        for key in ("estimate", "shown"):
            if vessel[key] is not None:
                vessel[key] = (vessel[key][0] * sx, vessel[key][1] * sy)
        vessel["velocity"] = (vessel["velocity"][0] * sx, vessel["velocity"][1] * sy)

    def new_vessel(self) -> dict:
        return {
            # Lissajous course parameters, normalized to the widget size
            "fx": self.rng.uniform(0.03, 0.07),
            "fy": self.rng.uniform(0.03, 0.07),
            "px": self.rng.uniform(0, math.tau),
            "py": self.rng.uniform(0, math.tau),
            "ax": self.rng.uniform(0.25, 0.42),
            "ay": self.rng.uniform(0.25, 0.42),
            "clock": self.rng.uniform(0, self.FIX_INTERVAL),
            "since_fix": 0.0,
            "estimate": None,          # filter state, updated per fix
            "velocity": (0.0, 0.0),
            "uncertainty": 25.0,
            "shown": None,             # what's drawn, updated per frame
            "shown_heading": None,
            "shown_radius": 25.0,
            "track_clock": 0.0,
            "fixes": deque(),
            "track": deque(),
        }

    def true_position(self, vessel: dict, t: float) -> tuple[float, float]:
        x = 0.5 + vessel["ax"] * math.sin(math.tau * vessel["fx"] * t + vessel["px"])
        y = 0.5 + vessel["ay"] * math.sin(math.tau * vessel["fy"] * t + vessel["py"])
        return x * self.width, y * self.height

    def update(self, dt: float):
        cutoff = self.time - self.TRAIL_SECONDS
        for vessel in self.vessels:
            vessel["clock"] += dt
            vessel["since_fix"] += dt
            while vessel["clock"] >= self.FIX_INTERVAL:
                vessel["clock"] -= self.FIX_INTERVAL
                self.take_fix(vessel)
            self.update_shown(vessel, dt)

            while vessel["fixes"] and vessel["fixes"][0][2] < cutoff:
                vessel["fixes"].popleft()
            while vessel["track"] and vessel["track"][0][2] < cutoff:
                vessel["track"].popleft()

    def take_fix(self, vessel: dict):
        tx, ty = self.true_position(vessel, self.time)
        # Mostly gaussian noise, with the odd wild outlier the filter should shrug off
        spread = self.NOISE * (4.0 if self.rng.random() < 0.05 else 1.0)
        fx, fy = tx + self.rng.gauss(0, spread), ty + self.rng.gauss(0, spread)
        vessel["fixes"].append((fx, fy, self.time))
        vessel["since_fix"] = 0.0

        if vessel["estimate"] is None:
            vessel["estimate"] = (fx, fy)
            vessel["shown"] = (fx, fy)
            return
        dt = self.FIX_INTERVAL
        ex, ey = vessel["estimate"]
        vx, vy = vessel["velocity"]
        # Predict, then correct toward the fix by the residual
        px, py = ex + vx * dt, ey + vy * dt
        rx, ry = fx - px, fy - py
        vessel["estimate"] = (px + self.ALPHA * rx, py + self.ALPHA * ry)
        vessel["velocity"] = (vx + self.BETA * rx / dt, vy + self.BETA * ry / dt)
        residual = math.hypot(rx, ry)
        vessel["uncertainty"] = 0.85 * vessel["uncertainty"] + 0.15 * (10.0 + 0.6 * residual)

    def update_shown(self, vessel: dict, dt: float):
        if vessel["estimate"] is None:
            return
        # Dead-reckon the estimate forward to "now"
        ex, ey = vessel["estimate"]
        vx, vy = vessel["velocity"]
        target_x = ex + vx * vessel["since_fix"]
        target_y = ey + vy * vessel["since_fix"]

        # Frame-rate independent exponential easing toward the target
        ease = 1.0 - math.exp(-self.EASE_RATE * dt)
        sx, sy = vessel["shown"]
        vessel["shown"] = (sx + (target_x - sx) * ease, sy + (target_y - sy) * ease)

        if math.hypot(vx, vy) > 1e-3:
            target_heading = math.atan2(vy, vx)
            if vessel["shown_heading"] is None:
                vessel["shown_heading"] = target_heading
            else:
                # Shortest way around the circle
                delta = (target_heading - vessel["shown_heading"] + math.pi) % math.tau - math.pi
                vessel["shown_heading"] += delta * (1.0 - math.exp(-self.TURN_RATE * dt))

        vessel["shown_radius"] += (vessel["uncertainty"] - vessel["shown_radius"]) * (1.0 - math.exp(-self.RING_RATE * dt))

        vessel["track_clock"] += dt
        if vessel["track_clock"] >= self.TRACK_INTERVAL:
            vessel["track_clock"] = 0.0
            vessel["track"].append((*vessel["shown"], self.time))

    def paint(self, painter: QPainter, palette: VisualPalette):
        grid_pen = QPen(palette.color("foreground", 0.07), 1.0)
        painter.setPen(grid_pen)
        spacing = 80.0
        x = spacing / 2
        while x < self.width:
            painter.drawLine(QPointF(x, 0), QPointF(x, self.height))
            x += spacing
        y = spacing / 2
        while y < self.height:
            painter.drawLine(QPointF(0, y), QPointF(self.width, y))
            y += spacing

        for vessel in self.vessels:
            painter.setPen(Qt.PenStyle.NoPen)
            for fx, fy, stamp in vessel["fixes"]:
                age = (self.time - stamp) / self.TRAIL_SECONDS
                painter.setBrush(palette.color("foreground", 0.5 * (1.0 - age)))
                painter.drawEllipse(QPointF(fx, fy), 2.2, 2.2)

            if vessel["shown"] is None:
                continue
            ex, ey = vessel["shown"]

            # Track, in short runs so older segments can fade out, ending
            # exactly at the vessel so there's no gap between samples
            points = list(vessel["track"]) + [(ex, ey, self.time)]
            pen = QPen()
            pen.setWidthF(2.2)
            pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            for (ax, ay, stamp), (bx, by, _) in zip(points, points[1:]):
                age = (self.time - stamp) / self.TRAIL_SECONDS
                pen.setColor(palette.color("accent", 0.9 * (1.0 - age)))
                painter.setPen(pen)
                painter.drawLine(QPointF(ax, ay), QPointF(bx, by))

            center = QPointF(ex, ey)
            painter.setPen(QPen(palette.color("accent2", 0.5), 1.4))
            painter.setBrush(palette.color("accent2", 0.08))
            radius = vessel["shown_radius"]
            painter.drawEllipse(center, radius, radius)

            if vessel["shown_heading"] is not None:
                ux, uy = math.cos(vessel["shown_heading"]), math.sin(vessel["shown_heading"])
                hull = QPainterPath(QPointF(ex + ux * 10, ey + uy * 10))
                hull.lineTo(QPointF(ex - ux * 6 - uy * 5, ey - uy * 6 + ux * 5))
                hull.lineTo(QPointF(ex - ux * 6 + uy * 5, ey - uy * 6 - ux * 5))
                hull.closeSubpath()
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(palette.color("accent", 1.0))
                painter.drawPath(hull)
