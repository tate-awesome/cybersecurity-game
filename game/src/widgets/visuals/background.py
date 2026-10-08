import math
import time

from PySide6.QtCore import QEvent, QObject, Qt, QTimer
from PySide6.QtGui import QCursor, QImage, QPainter
from PySide6.QtWidgets import QApplication, QWidget

from ...app_core import Context
from .base import Visual, VisualPalette
# The package __init__ defines VISUALS before importing this module
from . import VISUALS


class VisualBackground(QWidget):
    '''
    Plays one procedural Visual (see VISUALS) with theme colors.

    Two placement modes:
      in_layout=True  - adds itself to master's layout with stretch 1, like
                        a Canvas (the visuals demo page).
      in_layout=False - floats behind master's other children, always
                        resized to fill master and transparent to the mouse,
                        so it can sit under a TitleMenu as page background.

    blur softens the whole visual (see set_blur) - the intended look for
    a page background, where it should read as texture, not content.

    animate=False shows a still frame and never ticks - for backgrounds
    behind busy pages (workspaces), where the visual only shows through
    thin gaps and every frame would otherwise force the panels above to
    repaint too. paint_options are handed to the visual at paint time
    (e.g. {"packets": False}) - per background, so one shared simulation
    can look different on different pages.

    Each finished frame is cached as an image, so extra paint events -
    Qt repaints whatever sits behind a panel whenever that panel updates -
    just copy pixels instead of redrawing the visual.

    Runs its own ~30 fps QTimer rather than registering with the shared
    AnimationManager, whose 100 ms tick is fine for data panels but visibly
    choppy for continuous motion. The timer pauses while hidden, so a
    background on a page that's been navigated away from costs nothing.

    The special key "cycle" rotates through every visual, CYCLE_SECONDS each.

    shared=True makes every shared VisualBackground playing the same key
    drive one simulation (see SHARED), so page backgrounds carry on
    seamlessly across navigation instead of restarting on each new page.
    '''

    FRAME_MS = 33
    CYCLE_SECONDS = 20.0

    # visual key -> {"visual": Visual, "cycle_elapsed": float}. Lives for
    # the whole app session; a page being torn down leaves its entry here
    # for the next page's background to pick up.
    SHARED: dict[str, dict] = {}

    def __init__(self, master: QWidget, context: Context, visual_key: str | None = None, intensity: float = 1.0,
                 in_layout: bool = True, blur: float = 0.0, shared: bool = False, animate: bool = True,
                 paint_options: dict | None = None, fps: float = 1000 / FRAME_MS):
        super().__init__(master)
        self.context = context
        self.style = context.style
        self.intensity = intensity
        self.shared = shared
        self.animate = animate
        # Lower for backgrounds behind busy pages, where each frame also
        # repaints the panels above
        self.frame_ms = max(1, round(1000 / max(1.0, fps)))
        self.paint_options = paint_options or {}
        self.frame: QImage | None = None
        self.set_blur(blur)
        self.state: dict = {"visual": None, "cycle_elapsed": 0.0}
        self.cycling = False

        if in_layout:
            master.layout().addWidget(self, 1)
            self.setMinimumSize(200, 200)
        else:
            self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
            self.setGeometry(master.rect())
            master.installEventFilter(self)
            self.lower()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.last_tick = time.perf_counter()

        self.set_visual(visual_key or next(iter(VISUALS)))

    @property
    def visual(self) -> Visual | None:
        return self.state["visual"]

    @visual.setter
    def visual(self, visual: Visual):
        self.state["visual"] = visual

    # Control
    def set_visual(self, key: str):
        if key != "cycle" and key not in VISUALS:
            print(f"No visual named {key!r}, falling back to {next(iter(VISUALS))!r}")
            key = next(iter(VISUALS))
        self.cycling = key == "cycle"

        if self.shared and key in self.SHARED:
            # Pick up the already-running simulation where the last page left it
            self.state = self.SHARED[key]
        else:
            first = next(iter(VISUALS)) if self.cycling else key
            self.state = {"visual": VISUALS[first](), "cycle_elapsed": 0.0}
            if self.shared:
                self.SHARED[key] = self.state
        self.sync_size()
        self.invalidate()

    def set_intensity(self, intensity: float):
        self.intensity = intensity
        self.invalidate()

    def set_blur(self, radius: float):
        '''
        Blurs the whole visual by roughly radius pixels (0 = sharp). No
        visual needs to know it's being blurred - see render_blurred.
        '''
        self.blur_levels = 0 if radius <= 0 else max(1, round(math.log2(radius)) - 1)
        self.invalidate()

    def next_visual(self):
        keys = list(VISUALS)
        index = (keys.index(self.visual.KEY) + 1) % len(keys) if self.visual else 0
        self.visual = VISUALS[keys[index]]()
        self.sync_size()

    def invalidate(self):
        '''Drops the cached frame so the next paint renders a fresh one.'''
        self.frame = None
        self.update()

    # Loop
    def tick(self):
        now = time.perf_counter()
        # Clamp so a stall (window drag, breakpoint) doesn't teleport everything
        dt = min(0.1, now - self.last_tick)
        self.last_tick = now
        if self.visual is None or self.width() <= 0 or self.height() <= 0:
            return
        # Background mode ignores mouse events (so clicks reach the page's
        # own widgets), so read the global cursor and buttons instead of
        # waiting for events - that also keeps working over a button or panel
        local = self.mapFromGlobal(QCursor.pos())
        self.visual.pointer = (float(local.x()), float(local.y())) if self.rect().contains(local) else None
        buttons = QApplication.mouseButtons()
        self.visual.pressed = bool(buttons & Qt.MouseButton.LeftButton)
        self.visual.pulling = bool(buttons & Qt.MouseButton.RightButton)
        # The options also steer the simulation (e.g. {"packets": False}
        # stops traffic), and whichever background is ticking is the one on screen
        self.visual.paint_options = self.paint_options
        if self.cycling:
            self.state["cycle_elapsed"] += dt
            if self.state["cycle_elapsed"] >= self.CYCLE_SECONDS:
                self.state["cycle_elapsed"] = 0.0
                self.next_visual()
        self.visual.step(dt)
        self.invalidate()

    def palette_for_theme(self) -> VisualPalette:
        return VisualPalette(
            self.style.color("root"),
            self.style.color("text"),
            self.style.color("accent"),
            self.intensity,
        )

    # Rendering
    def render_frame(self, palette: VisualPalette) -> QImage:
        '''
        One finished frame: full size when sharp, half size when blurred
        (paintEvent stretches it back up). paint_options are handed to the
        visual for just this render, since a shared visual may be on screen
        with different options elsewhere.
        '''
        self.visual.paint_options = self.paint_options
        if self.blur_levels > 0:
            return self.render_blurred(palette)
        image = QImage(self.width(), self.height(), QImage.Format.Format_RGB32)
        image.fill(palette.background)
        painter = QPainter(image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.visual.paint(painter, palette)
        painter.end()
        return image

    def render_blurred(self, palette: VisualPalette) -> QImage:
        '''
        An image-pyramid blur: render the visual at half size, halve it
        blur_levels more times, then scale back up one doubling at a time.
        Each smooth (bilinear) step averages neighboring pixels, so the
        round trip spreads every shape out like a gaussian - and because
        half the work happens on tiny images, it's cheaper than drawing
        sharp at full size. Qt's own QGraphicsBlurEffect was tried first:
        about 3x slower here, and it leaves faint rectangles around each
        drawn shape's bounding box. Returns half size - the final doubling
        happens in paintEvent.
        '''
        width, height = max(1, self.width() // 2), max(1, self.height() // 2)
        image = QImage(width, height, QImage.Format.Format_RGB32)
        image.fill(palette.background)
        painter = QPainter(image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.scale(width / self.width(), height / self.height())
        self.visual.paint(painter, palette)
        painter.end()

        sizes = [image.size()]
        for _ in range(self.blur_levels):
            image = image.scaled(max(1, image.width() // 2), max(1, image.height() // 2),
                                 Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
            sizes.append(image.size())
        for size in reversed(sizes[:-1]):
            image = image.scaled(size, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
        return image

    # Qt events
    def paintEvent(self, event):
        palette = self.palette_for_theme()
        painter = QPainter(self)
        try:
            if self.visual is None or self.visual.width <= 0:
                painter.fillRect(self.rect(), palette.background)
                return
            if self.frame is None:
                self.frame = self.render_frame(palette)
            # A half-size blurred frame gets stretched back up smoothly
            painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
            painter.drawImage(self.rect(), self.frame)
        finally:
            painter.end()

    def sync_size(self):
        '''
        Hands the visual this widget's size - but only while on screen. A
        page is built at a small default size before the window lays it
        out, and a shared visual (still running from the previous page)
        would take that transient size as a real resize and rebuild itself.
        '''
        if self.visual is None or not self.isVisible() or self.width() <= 0 or self.height() <= 0:
            return
        if (self.visual.width, self.visual.height) != (self.width(), self.height()):
            self.visual.resize(self.width(), self.height())
        self.invalidate()

    def resizeEvent(self, event):
        self.sync_size()
        super().resizeEvent(event)

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        # Background mode: track master's size
        if watched is self.parent() and event.type() == QEvent.Type.Resize:
            self.setGeometry(self.parent().rect())
        return False

    def showEvent(self, event):
        self.last_tick = time.perf_counter()
        if self.animate:
            self.timer.start(self.frame_ms)
        super().showEvent(event)
        self.sync_size()

    def hideEvent(self, event):
        self.timer.stop()
        super().hideEvent(event)
