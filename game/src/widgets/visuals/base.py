import random
import zlib

import numpy as np
from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QColor, QPainter, QRadialGradient


# Which of a theme's visual colors each thing gets (see VisualPalette.pick) -
# new every run, so they land differently each time the app opens
COLOR_SEED = random.getrandbits(32)


class VisualPalette:
    '''
    Theme colors handed to a Visual each frame. Every color a visual draws
    with goes through color(), which scales its alpha by intensity - so one
    visual reads as a bold demo at intensity 1.0 and a quiet title-page
    background at ~0.3 without the visual itself knowing which it is.

    A theme can hand it colors of its own ("visual_colors" - see
    themes.py): each thing a visual highlights then gets one of them at
    random, the same one for as long as it lives (see pick and split).
    '''

    def __init__(self, background: str, foreground: str, accent: str, intensity: float = 1.0, colors: list[str] | None = None):
        self.background = QColor(background)
        self.foreground = QColor(foreground)
        self.accent = QColor(accent)
        # Complementary hue of the accent, for a second highlight color
        # that still belongs to the active theme family.
        h, s, v, _ = self.accent.getHsvF()
        self.accent2 = QColor.fromHsvF((max(h, 0.0) + 0.5) % 1.0, s, v)
        self.intensity = intensity
        self.colors = [QColor(color) for color in colors or ()]

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
        keeping the theme's saturation and brightness. In a theme with
        visual colors, one of those instead - the same one for each offset.
        '''
        if self.colors:
            return self.pick(("hue", offset), alpha)
        h, s, v, _ = self.accent.getHsvF()
        return self.faded(QColor.fromHsvF((max(h, 0.0) + offset) % 1.0, s, v), alpha)

    def pick(self, key, alpha: float = 1.0, name: str = "accent") -> QColor:
        '''
        The highlight for one thing, by a key that stays the same for as
        long as it lives (an index, an id): one of the theme's visual
        colors at random - or name's color, in a theme without them.
        '''
        if not self.colors:
            return self.color(name, alpha)
        return self.faded(self.colors[zlib.crc32(f"{COLOR_SEED}:{key}".encode()) % len(self.colors)], alpha)

    def split(self, indices) -> list[tuple[int, np.ndarray]]:
        '''
        indices (of things drawn together - points, lines) grouped by which
        of the theme's visual colors each gets, as (slot for slot_color,
        the group's indices) - all in one group, in a theme without them.
        '''
        indices = np.asarray(indices, dtype=np.int64)
        if not self.colors:
            return [(0, indices)]
        # A multiplicative hash's high bits, so neighbours don't take turns
        slots = (((indices.astype(np.uint64) * np.uint64(2654435761) + np.uint64(COLOR_SEED)) & np.uint64(0xFFFFFFFF))
                 >> np.uint64(16)) % np.uint64(len(self.colors))
        return [(slot, indices[slots == slot]) for slot in range(len(self.colors)) if (slots == slot).any()]

    def slot_color(self, slot: int, alpha: float = 1.0, name: str = "accent") -> QColor:
        '''The color of one of split's groups - name's color, in a theme without visual colors.'''
        return self.faded(self.colors[slot], alpha) if self.colors else self.color(name, alpha)

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

    Most visuals build their state in on_resize, so nothing runs until the
    first resize: step does nothing before it, and settle waits for it
    (see request_settle) - VisualBackground only paints a sized visual.
    '''

    KEY = ""
    # Visual KEYs whose startup intro has already played this session (see claim_intro)
    intros_played: set[str] = set()

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
        # settle asked for before the first resize - done right after it (see request_settle)
        self.settle_pending = False

    @property
    def sized(self) -> bool:
        '''Whether it's been given a size yet - and so built its state (see on_resize).'''
        return self.width > 0 and self.height > 0

    def resize(self, width: int, height: int):
        first = self.width == 0 or self.height == 0
        self.scale_x = 1.0 if first else width / self.width
        self.scale_y = 1.0 if first else height / self.height
        self.width, self.height = width, height
        self.on_resize(first)
        if self.settle_pending and self.sized:
            self.settle_pending = False
            self.settle()

    def on_resize(self, first: bool):
        '''
        scale_x/scale_y hold new size / old size, for visuals that keep
        pixel positions and need to stretch them to the new area.
        '''
        pass

    def step(self, dt: float):
        if not self.sized:
            return  # nothing built yet to move (see on_resize)
        self.time += dt
        self.update(dt)

    def update(self, dt: float):
        pass

    @property
    def detailed(self) -> bool:
        '''
        Whether to draw the detailed version - from the "packets" paint
        option, which title pages always set and workspaces leave to the
        "Detailed Background" preference (see VisualBackground.apply_preferences).
        '''
        return self.paint_options.get("packets", True)

    def claim_intro(self) -> bool:
        '''
        True the first time a visual of this kind is built this session -
        so its startup animation plays once, when it's first seen (at app
        start, or when it's first picked as the background), and later
        rebuilds (a resize, another page) appear straight away.
        '''
        if self.KEY in Visual.intros_played:
            return False
        Visual.intros_played.add(self.KEY)
        return True

    @staticmethod
    def button_height() -> float:
        '''Roughly how tall a standard button is (font height plus style.py's 6px padding), for sizing to the UI.'''
        from PySide6.QtGui import QFontMetricsF
        from PySide6.QtWidgets import QApplication
        return QFontMetricsF(QApplication.font()).height() + 12

    def settle(self):
        '''
        Skips straight to the visual's normal running state, past any
        intro (e.g. the network's startup spawn-in) - for a background
        that's shown still, which would otherwise freeze mid-intro. Only
        called on a sized visual - see request_settle.
        '''
        pass

    def request_settle(self):
        '''settle - now if it's sized, else as soon as it is (see resize), since there's nothing to settle before then.'''
        if self.sized:
            self.settle()
        else:
            self.settle_pending = True

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
