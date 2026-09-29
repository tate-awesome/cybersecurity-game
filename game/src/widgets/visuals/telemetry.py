from collections import deque

from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QPainter, QPainterPath, QPen

from .base import Visual, VisualPalette, draw_glow


class Telemetry(Visual):
    '''
    Stacked strip-chart traces scrolling right to left, each one a simulated
    second-order control loop chasing a setpoint that steps every few
    seconds - overshoot, ringing, and settling included - plus a little
    sensor noise. The dashed line is the setpoint; the grid scrolls with
    the data like the Defender Monitors charts.
    '''

    KEY = "telemetry"
    # Samples per second - also the point count per trace, so this is the
    # main paint-cost knob (15 keeps a fullscreen chart well under a frame)
    SAMPLE_RATE = 15.0
    PIXELS_PER_SECOND = 70.0
    GRID_SPACING = 70.0

    def on_resize(self, first: bool):
        count = max(3, min(7, self.height // 150))
        capacity = int(self.width / self.PIXELS_PER_SECOND * self.SAMPLE_RATE) + 4
        if first or not hasattr(self, "traces") or len(self.traces) != count:
            self.traces = [self.new_trace() for _ in range(count)]
            self.sample_clock = 0.0
        for trace in self.traces:
            trace["history"] = deque(trace["history"], maxlen=capacity)
            # Pre-run the loop so the chart starts full instead of drawing
            # in from the right edge - matters most as a page background.
            while len(trace["history"]) < capacity:
                self.sample(trace, 1.0 / self.SAMPLE_RATE)

    def new_trace(self) -> dict:
        return {
            # Natural frequency and damping ratio of the simulated loop -
            # low damping rings, high damping creeps.
            "wn": self.rng.uniform(1.5, 4.0),
            "zeta": self.rng.uniform(0.15, 0.7),
            "x": 0.0,
            "v": 0.0,
            "setpoint": self.rng.uniform(-0.6, 0.6),
            "next_step": self.rng.uniform(1.0, 4.0),
            "noise": self.rng.uniform(0.01, 0.05),
            "history": deque(),
        }

    def update(self, dt: float):
        self.sample_clock += dt
        sample_dt = 1.0 / self.SAMPLE_RATE
        while self.sample_clock >= sample_dt:
            self.sample_clock -= sample_dt
            for trace in self.traces:
                self.sample(trace, sample_dt)

    def sample(self, trace: dict, dt: float):
        trace["next_step"] -= dt
        if trace["next_step"] <= 0:
            trace["setpoint"] = self.rng.uniform(-0.75, 0.75)
            trace["next_step"] = self.rng.uniform(2.5, 6.0)
        wn, zeta = trace["wn"], trace["zeta"]
        acceleration = wn * wn * (trace["setpoint"] - trace["x"]) - 2 * zeta * wn * trace["v"]
        trace["v"] += acceleration * dt
        trace["x"] += trace["v"] * dt
        measured = trace["x"] + self.rng.gauss(0, trace["noise"])
        trace["history"].append((measured, trace["setpoint"]))

    def paint(self, painter: QPainter, palette: VisualPalette):
        band = self.height / len(self.traces)
        scroll = (self.time * self.PIXELS_PER_SECOND) % self.GRID_SPACING

        grid_pen = QPen(palette.color("foreground", 0.08))
        grid_pen.setWidthF(1.0)
        painter.setPen(grid_pen)
        x = self.width - scroll
        while x > 0:
            painter.drawLine(QPointF(x, 0), QPointF(x, self.height))
            x -= self.GRID_SPACING

        step = self.PIXELS_PER_SECOND / self.SAMPLE_RATE
        for index, trace in enumerate(self.traces):
            top = index * band
            middle = top + band / 2
            amplitude = band * 0.4
            history = trace["history"]
            if len(history) < 2:
                continue

            painter.setPen(QPen(palette.color("foreground", 0.12), 1.0))
            painter.drawLine(QPointF(0, top + band), QPointF(self.width, top + band))

            setpoint_pen = QPen(palette.color("accent2", 0.55), 1.4)
            setpoint_pen.setStyle(Qt.PenStyle.DashLine)
            value_path = QPainterPath()
            setpoint_path = QPainterPath()
            count = len(history)
            # Samples land only SAMPLE_RATE times a second - shift them left
            # by the time since the last one so the chart scrolls every
            # frame, in step with the grid, instead of in sample-sized jumps.
            newest_x = self.width - self.sample_clock * self.PIXELS_PER_SECOND
            for i, (value, setpoint) in enumerate(history):
                px = newest_x - (count - 1 - i) * step
                value_point = QPointF(px, middle - value * amplitude)
                setpoint_point = QPointF(px, middle - setpoint * amplitude)
                if i == 0:
                    value_path.moveTo(value_point)
                    setpoint_path.moveTo(setpoint_point)
                else:
                    value_path.lineTo(value_point)
                    setpoint_path.lineTo(setpoint_point)

            # Close the gap to the right edge with the loop's live state
            live = trace["x"] + trace["v"] * self.sample_clock
            live_point = QPointF(self.width, middle - live * amplitude)
            value_path.lineTo(live_point)
            setpoint_path.lineTo(QPointF(self.width, middle - trace["setpoint"] * amplitude))

            painter.setPen(setpoint_pen)
            painter.drawPath(setpoint_path)
            painter.setPen(QPen(palette.color("accent", 0.9), 2.0))
            painter.drawPath(value_path)

            # Glowing "pen head" at the live value
            draw_glow(painter, QPointF(self.width - 2, live_point.y()), 10.0, palette.color("accent", 1.0))
            painter.setBrush(Qt.BrushStyle.NoBrush)
