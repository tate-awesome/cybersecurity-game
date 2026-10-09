import random

from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QColor, QPainter, QRadialGradient


class VisualPalette:
    '''
    Theme colors handed to a Visual each frame. Every color a visual draws
    with goes through color(), which scales its alpha by intensity - so one
    visual reads as a bold demo at intensity 1.0 and a quiet title-page
    background at ~0.3 without the visual itself knowing which it is.
    '''

    def __init__(self, background: str, foreground: str, accent: str, intensity: float = 1.0):
        self.background = QColor(background)
        self.foreground = QColor(foreground)
        self.accent = QColor(accent)
        # Complementary hue of the accent, for a second highlight color
        # that still belongs to the active theme family.
        h, s, v, _ = self.accent.getHsvF()
        self.accent2 = QColor.fromHsvF((max(h, 0.0) + 0.5) % 1.0, s, v)
        self.intensity = intensity

    def color(self, name: str, alpha: float = 1.0) -> QColor:
        '''
        name: "foreground", "accent", "accent2" or "background".
        alpha: 0-1 opacity before intensity scaling.
        '''
        return self.faded(getattr(self, name), alpha)

    def hue(self, offset: float, alpha: float = 1.0) -> QColor:
        '''
        The accent color rotated around the color wheel by offset (0-1), for
        visuals that need more distinct colors than accent/accent2 while
        keeping the theme's saturation and brightness.
        '''
        h, s, v, _ = self.accent.getHsvF()
        return self.faded(QColor.fromHsvF((max(h, 0.0) + offset) % 1.0, s, v), alpha)

    def faded(self, color: QColor, alpha: float) -> QColor:
        color = QColor(color)
        color.setAlphaF(max(0.0, min(1.0, alpha * self.intensity)))
        return color


def draw_glow(painter: QPainter, center: QPointF, radius: float, color: QColor):
    '''
    A soft glowing spot: a radial gradient from a bright, nearly white-hot
    core through color out to fully transparent at radius.
    '''
    core = QColor(color).lighter(160)
    core.setAlphaF(color.alphaF())
    edge = QColor(color)
    edge.setAlphaF(0.0)
    mid = QColor(color)
    mid.setAlphaF(color.alphaF() * 0.45)
    gradient = QRadialGradient(center, radius)
    gradient.setColorAt(0.0, core)
    gradient.setColorAt(0.18, color)
    gradient.setColorAt(0.45, mid)
    gradient.setColorAt(1.0, edge)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(gradient)
    painter.drawEllipse(center, radius, radius)


class Visual:
    '''
    Superclass for procedural visuals drawn by VisualBackground. Works in
    plain widget pixels (no Camera/world space - a background has no reason
    to pan or zoom) and advances by real elapsed seconds, so motion speed
    doesn't depend on frame rate.

    Subclasses override update(dt) to advance their simulation and
    paint(painter, palette) to draw it; on_resize() is called whenever the
    drawing area changes size (including the first time), and should keep
    state in normalized or resize-tolerant coordinates where it can.
    '''

    KEY = ""

    def __init__(self, seed: int | None = None):
        self.rng = random.Random(seed)
        self.width = 0
        self.height = 0
        self.time = 0.0
        # Mouse position in this visual's pixels (None when the cursor isn't
        # over it) and whether the left/right buttons are held - kept
        # current by VisualBackground before each step
        self.pointer: tuple[float, float] | None = None
        self.pressed = False
        self.pulling = False
        # Per-render drawing options from whichever VisualBackground is
        # painting this visual right now (e.g. {"packets": False})
        self.paint_options: dict = {}

    def resize(self, width: int, height: int):
        first = self.width == 0 or self.height == 0
        self.scale_x = 1.0 if first else width / self.width
        self.scale_y = 1.0 if first else height / self.height
        self.width, self.height = width, height
        self.on_resize(first)

    def on_resize(self, first: bool):
        '''
        scale_x/scale_y hold new size / old size, for visuals that keep
        pixel positions and need to stretch them to the new area.
        '''
        pass

    def step(self, dt: float):
        self.time += dt
        self.update(dt)

    def update(self, dt: float):
        pass

    def settle(self):
        '''
        Skips straight to the visual's normal running state, past any
        intro (e.g. the network's startup spawn-in) - for a background
        that's shown still, which would otherwise freeze mid-intro.
        '''
        pass

    def paint(self, painter: QPainter, palette: VisualPalette):
        raise NotImplementedError

    # Helpers
    def area_count(self, per_megapixel: float, minimum: int, maximum: int) -> int:
        '''
        How many of something to spawn for the current size, so a visual
        looks equally busy in a small demo pane and a fullscreen title page.
        '''
        count = int(self.width * self.height / 1_000_000 * per_megapixel)
        return max(minimum, min(maximum, count))
