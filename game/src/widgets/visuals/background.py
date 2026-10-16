import math
import time

from PySide6.QtCore import QEvent, QObject, QRectF, Qt, QTimer
from PySide6.QtGui import QColor, QCursor, QImage, QLinearGradient, QPainter
from PySide6.QtWidgets import QApplication, QWidget

from ...app_core import Context
from .base import Visual, VisualPalette
# The package __init__ defines VISUALS before importing this module
from . import VISUALS


def pyramid_blur(image: QImage, levels: int) -> QImage:
    '''
    An image-pyramid blur: halve the image `levels` times, then scale it
    back up one doubling at a time. Each smooth (bilinear) step averages
    neighboring pixels, so the round trip spreads shapes out like a
    gaussian of roughly 2^(levels + 1) px, cheaply.
    '''
    sizes = [image.size()]
    for _ in range(levels):
        image = image.scaled(max(1, image.width() // 2), max(1, image.height() // 2),
                             Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
        sizes.append(image.size())
    for size in reversed(sizes[:-1]):
        image = image.scaled(size, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
    return image


# How many columns wide the northern lights are drawn, whatever the window's
# size - soft shapes lose nothing scaled up, and it keeps them cheap enough for every frame
AURORA_COLUMNS = 120


def paint_aurora(painter: QPainter, width: int, height: int, colors: list[str], t: float, glow: bool = True):
    '''
    Northern lights across the top of a width x height area: a curtain of
    light per color, each a band with a wavy lower edge that fades upward,
    swaying slowly and shimmering in vertical rays as t (seconds) passes.
    glow adds the light (on a dark sky); otherwise it's laid over (a light one).
    '''
    if width <= 0 or height <= 0:
        return
    w = AURORA_COLUMNS
    h = max(8, round(w * height / width))
    image = QImage(w, h, QImage.Format.Format_ARGB32_Premultiplied)
    image.fill(Qt.GlobalColor.transparent)
    p = QPainter(image)
    p.setCompositionMode(QPainter.CompositionMode.CompositionMode_Plus if glow else QPainter.CompositionMode.CompositionMode_SourceOver)
    strength = 0.55 if glow else 0.32
    for i, hex_color in enumerate(colors):
        # One curtain's light, top to bottom of each column it's drawn in -
        # faint at the top, brightest just above its lower edge
        gradient = QLinearGradient(0, 0, 0, 1)
        gradient.setCoordinateMode(QLinearGradient.CoordinateMode.ObjectMode)
        for stop, a in ((0.0, 0.0), (0.7, 0.55), (0.93, 1.0), (1.0, 0.0)):
            c = QColor(hex_color)
            c.setAlphaF(a)
            gradient.setColorAt(stop, c)
        phase = i * 2.1
        base = 0.22 + 0.13 * i  # each curtain a little lower down the sky
        for x in range(w):
            u = x / w
            # The lower edge sways, and the curtain's height breathes along it
            edge = base + 0.07 * math.sin(u * 5.3 + t * 0.21 + phase) + 0.035 * math.sin(u * 11.7 - t * 0.37 + phase * 1.7)
            reach = 0.16 + 0.07 * math.sin(u * 3.1 + t * 0.15 + phase)
            # Rays: brightness rippling sideways along the curtain
            ray = 0.45 + 0.55 * math.sin(u * 37.0 + t * 0.9 + phase + math.sin(t * 0.3 + u * 7)) ** 2
            # Fading out toward the sides, so no curtain ends at an edge
            ends = min(1.0, 4 * u, 4 * (1 - u))
            top = (edge - reach * 1.5) * h
            p.setOpacity(min(1.0, strength * ray * ends))
            p.fillRect(QRectF(x, top, 1, edge * h + 2 - top), gradient)
    p.end()
    painter.save()
    painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
    painter.drawImage(QRectF(0, 0, width, height), image)
    painter.restore()


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

    hold() shows just the theme's background color, with the visual
    paused before its first frame, until release() - so on startup the
    animation (and its intro) only starts once the first page has come in
    (see App.start_first_page).

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
        # Drawn in the theme's colors - a cached frame is stale after a change
        self.style.signals.changed.connect(self.invalidate)
        self.intensity = intensity
        self.shared = shared
        self.animate = animate
        # Lower for backgrounds behind busy pages, where each frame also
        # repaints the panels above
        self.frame_ms = max(1, round(1000 / max(1.0, fps)))
        self.paint_options = paint_options or {}
        self.held = False  # see hold
        # Set by follow_preferences - see apply_preferences
        self.follows_preferences = False
        self.page_animate = animate
        self.page_detailed = True
        # Behind a title menu page, which a theme can't turn off (see Style.background_shown)
        self.menu = False
        self.visual_key: str | None = None
        self.frame: QImage | None = None
        # The half-size render a blurred frame is made from (see render_half)
        self.half_frame: QImage | None = None
        # The page's own blur - a theme's "background_blur" replaces it (see apply_preferences)
        self.page_blur = blur
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
        # Precise, like AnimationManager's - a coarse timer made 30 fps ~21 on Windows
        self.timer.setTimerType(Qt.TimerType.PreciseTimer)
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
        '''
        Plays the visual `key` (or "cycle"). Switching from another visual
        starts it fresh, with its startup intro - only a background's first
        visual picks up an already-running shared one (the same network
        carrying on from page to page).
        '''
        if key != "cycle" and key not in VISUALS:
            print(f"No visual named {key!r}, falling back to {next(iter(VISUALS))!r}")
            key = next(iter(VISUALS))
        switching = self.visual_key is not None and key != self.visual_key
        self.cycling = key == "cycle"
        self.visual_key = key
        if switching:
            self.SHARED.pop(key, None)
            Visual.intros_played.discard(next(iter(VISUALS)) if self.cycling else key)

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

    def replay_intro(self):
        '''
        Starts the visual on screen over from scratch, with its startup
        intro unlocked again (see Visual.claim_intro) - for the visuals
        demo's "Replay Startup" button. In "cycle" mode it replays whichever
        visual is showing, without moving the cycle on.
        '''
        current = self.visual
        if current is None:
            return
        Visual.intros_played.discard(current.KEY)
        self.visual = type(current)()
        self.sync_size()
        self.invalidate()

    def follow_preferences(self, page_animate: bool = True, page_detailed: bool = True, menu: bool = False):
        '''
        Makes this background follow the user's background preferences
        (Style.background_*) from now on - a page background, as opposed to
        e.g. the visuals demo's preview. page_animate is whether the page
        allows animation at all (the preference can still turn it off).
        page_detailed=True makes the page always detailed (title and lesson
        select pages); False leaves it to the "Detailed Background"
        preference (workspaces, where detail is off by default since it's
        distracting behind the panels).
        '''
        self.follows_preferences = True
        self.menu = menu
        self.page_animate = page_animate
        self.page_detailed = page_detailed
        self.apply_preferences()

    def apply_preferences(self):
        '''Brings this background in line with Style.background_* - called again whenever they change.'''
        style = self.style
        if style.background_visual != self.visual_key:
            self.set_visual(style.background_visual)
        self.paint_options = {**self.paint_options, "packets": self.page_detailed or style.background_detailed}
        self.animate = self.page_animate and style.background_animate
        self.frame_ms = max(1, round(1000 / style.background_fps))
        if not self.animate and self.visual is not None:
            # A still frame should show the finished picture, not one
            # caught partway through an intro (see Visual.settle) - once
            # it has a size, if it's new and not yet on screen
            self.visual.request_settle()
        # A theme's blur only replaces a page's own - a page drawn sharp (the title) stays sharp
        theme_blur = style.setting("background_blur")
        blur = theme_blur if theme_blur is not None and self.page_blur > 0 else self.page_blur
        if blur != self.blur_radius:
            self.set_blur(blur)
        self.setVisible(style.background_shown(menu=self.menu))
        if self.animate and self.isVisible() and not self.held:
            self.last_tick = time.perf_counter()
            self.timer.start(self.frame_ms)
        else:
            self.timer.stop()
        self.invalidate()

    def set_intensity(self, intensity: float):
        self.intensity = intensity
        self.invalidate()

    def set_blur(self, radius: float):
        '''
        Blurs the whole visual by roughly radius pixels (0 = sharp). No
        visual needs to know it's being blurred - see render_blurred.
        '''
        self.blur_radius = max(0.0, radius)
        self.blur_levels = 0 if radius <= 0 else max(1, round(math.log2(radius)) - 1)
        self.invalidate()

    def next_visual(self):
        keys = list(VISUALS)
        index = (keys.index(self.visual.KEY) + 1) % len(keys) if self.visual else 0
        # Each visual in the cycle arrives with its startup intro
        Visual.intros_played.discard(keys[index])
        self.visual = VISUALS[keys[index]]()
        self.sync_size()

    def hold(self):
        self.held = True
        self.timer.stop()
        self.invalidate()

    def release(self):
        self.held = False
        self.last_tick = time.perf_counter()
        if self.animate and self.isVisible():
            self.timer.start(self.frame_ms)
        self.invalidate()

    def invalidate(self):
        '''Drops the cached frame so the next paint renders a fresh one.'''
        self.frame = None
        self.half_frame = None
        self.update()

    # Loop
    def tick(self):
        now = time.perf_counter()
        # Clamp so a stall (window drag, breakpoint) doesn't teleport everything
        dt = min(0.1, now - self.last_tick)
        self.last_tick = now
        if self.visual is None or not self.visual.sized or self.width() <= 0 or self.height() <= 0:
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
        performance = self.context.performance
        started = time.perf_counter()
        self.visual.paint_options = self.paint_options
        if self.blur_levels > 0:
            image = self.render_blurred(palette)
        else:
            image = QImage(self.width(), self.height(), QImage.Format.Format_RGB32)
            painter = QPainter(image)
            self.fill_base(painter, image.width(), image.height())
            painter.setRenderHint(QPainter.RenderHint.Antialiasing, performance.antialiasing)
            self.visual.paint(painter, palette)
            painter.end()
        # Only page backgrounds - the visuals demo's preview would otherwise mix in
        if performance.measuring and self.follows_preferences:
            performance.record("background", started)
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
        return pyramid_blur(self.render_half(palette), self.blur_levels)

    def render_half(self, palette: VisualPalette) -> QImage:
        '''The visual drawn sharp at half size - cached for the frame.'''
        if self.half_frame is None:
            width, height = max(1, self.width() // 2), max(1, self.height() // 2)
            image = QImage(width, height, QImage.Format.Format_RGB32)
            painter = QPainter(image)
            self.fill_base(painter, width, height)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing, self.context.performance.antialiasing)
            painter.scale(width / self.width(), height / self.height())
            self.visual.paint_options = self.paint_options
            self.visual.paint(painter, palette)
            painter.end()
            self.half_frame = image
        return self.half_frame

    def fill_base(self, painter: QPainter, width: int, height: int):
        '''
        What the visual is drawn over: the theme's window color - or its
        gradient, if it has one (see Style.brush) - and its northern lights,
        if it has those (see paint_aurora).
        '''
        rect = QRectF(0, 0, width, height)
        brush = self.style.brush("window", rect)
        if brush.gradient() is not None:
            painter.fillRect(rect, self.style.color("root", opaque=True))
        painter.fillRect(rect, brush)
        aurora = self.style.setting("aurora")
        if aurora:
            mode = self.style.current_theme.partition("_")[0]
            paint_aurora(painter, width, height, aurora[mode], time.perf_counter(), glow=mode == "dark")

    # Qt events
    def paintEvent(self, event):
        palette = self.palette_for_theme()
        painter = QPainter(self)
        try:
            if self.held or self.visual is None or not self.visual.sized:
                self.fill_base(painter, self.width(), self.height())
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
        if self.animate and not self.held:
            self.timer.start(self.frame_ms)
        super().showEvent(event)
        self.sync_size()

    def hideEvent(self, event):
        self.timer.stop()
        super().hideEvent(event)
