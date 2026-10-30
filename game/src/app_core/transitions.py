from collections.abc import Callable

from PySide6.QtCore import QEasingCurve, QPoint, QPointF, QRect, QSize, Qt, QTimer, QVariantAnimation
from PySide6.QtGui import QColor, QGuiApplication, QPainter, QPixmap, QRegion
from PySide6.QtWidgets import QGraphicsEffect, QWidget


class HideEffect(QGraphicsEffect):
    '''
    Draws nothing - keeps a new page's item off screen while
    PageTransition draws a picture of it in its place. Never asks for the
    source pixmap, so it costs no offscreen pass.
    '''

    def draw(self, painter: QPainter):
        pass


class Layer:
    '''One picture on a TransitionOverlay, and its current pose.'''

    def __init__(self, pixmap: QPixmap | None, origin: QPoint, opacity: float = 0.0):
        # None until it's taken (see PageTransition.capture)
        self.pixmap = pixmap
        # Where its content sits in the window, at rest
        self.origin = QPointF(origin)
        self.opacity = opacity
        self.dx = self.dy = 0.0


class TransitionOverlay(QWidget):
    '''
    Pictures of page content - the page being left, the new page's items -
    drawn over the window while they fade and drift. One widget paints
    them all, so each frame is a single pass of plain pixmap draws rather
    than an offscreen render of every widget that's moving.
    '''

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.layers: list[Layer] = []
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)

    def paintEvent(self, event):
        painter = QPainter(self)
        for layer in self.layers:
            if layer.pixmap is None or layer.opacity <= 0.0:
                continue
            painter.setOpacity(layer.opacity)
            painter.drawPixmap(layer.origin + QPointF(layer.dx, layer.dy), layer.pixmap)
        painter.end()


class PageTransition:
    '''
    Animates a page change. Navigating (direction +1 deeper, -1 back) the
    old page's content slides out against the direction of travel and
    fades while the new page's items (Page.appear_targets) fade in one
    after another, sliding in from the direction of travel and rising
    slightly into place. The shared background isn't in the snapshot or
    the targets, so it carries on underneath untouched.

    direction 0 (refresh - a theme or language change, say) just
    crossfades from a picture of the whole old page, since nothing moved.

    Nothing live moves: the old content and each new item are pictures on
    one TransitionOverlay, and the real items stay hidden (HideEffect)
    until their picture lands, then take its place. A new item is pictured
    as its own entrance begins - the page has been laid out and shown by
    then, which it hasn't when this is made.

    One animation drives everything. stop() jumps straight to the end
    state, for when another page change interrupts this one.
    '''

    OUT_MS = 200        # old content fading out
    IN_DELAY_MS = 70    # new content starts while the old is still fading
    IN_MS = 340         # each new item's own fade/slide
    STAGGER_MS = 45     # between consecutive new items
    REFRESH_MS = 260    # whole-page crossfade on a refresh
    SLIDE = 28.0        # px of horizontal travel
    RISE = 10.0         # px new items rise into place

    OUT_CURVE = QEasingCurve(QEasingCurve.Type.InOutQuad)
    IN_CURVE = QEasingCurve(QEasingCurve.Type.OutCubic)

    @staticmethod
    def blank(widget: QWidget, size: QSize) -> QPixmap:
        '''A transparent pixmap of size (logical px) at widget's screen's pixel ratio.'''
        ratio = widget.devicePixelRatioF()
        pixmap = QPixmap(size * ratio)
        pixmap.setDevicePixelRatio(ratio)
        pixmap.fill(Qt.GlobalColor.transparent)
        return pixmap

    @staticmethod
    def draw_content(target: QWidget, pixmap: QPixmap, offset: QPoint):
        # DrawChildren only - the default also fills each target with
        # its palette's window color (near-white in Fusion), which
        # flashed as a light box behind labels and bars. Stylesheet
        # backgrounds still paint, since those come from paintEvent.
        target.render(pixmap, offset, QRegion(), QWidget.RenderFlag.DrawChildren)

    @staticmethod
    def snapshot(page: QWidget | None, direction: int) -> tuple[QPixmap, QPoint] | None:
        '''
        Picture of the outgoing page, and where it sat in the window:
        everything for a refresh, only its content (appear_targets, on a
        transparent pixmap) when navigating. Taken before the page is torn
        down.
        '''
        if page is None or not page.isVisible() or page.width() <= 0:
            return None
        if direction == 0:
            return page.grab(), page.pos()
        targets = page.appear_targets() if hasattr(page, "appear_targets") else []
        pixmap = PageTransition.blank(page, page.size())
        for target in targets:
            PageTransition.draw_content(target, pixmap, target.mapTo(page, QPoint(0, 0)))
        return pixmap, page.pos()

    def __init__(self, page: QWidget, snapshot: tuple[QPixmap, QPoint] | None, direction: int):
        self.direction = direction
        self.page = page
        self.laid_out = False
        # Covers the whole window and draws each picture where its content
        # sits - the new page isn't laid out yet, so its own geometry can't
        # be trusted here
        window = page.parentWidget()
        self.overlay: TransitionOverlay | None = TransitionOverlay(window)
        self.overlay.setGeometry(window.rect())

        self.outgoing: Layer | None = None
        if snapshot is not None:
            self.outgoing = Layer(*snapshot, opacity=1.0)
            self.overlay.layers.append(self.outgoing)

        # (stagger index, item, its HideEffect, its picture) for each new
        # item still entering - the effect is held here too, or Python
        # collects it out from under the item
        self.entering: list[tuple[int, QWidget, HideEffect, Layer]] = []
        if direction != 0 and hasattr(page, "appear_targets"):
            for index, target in enumerate(page.appear_targets()):
                effect = HideEffect()
                target.setGraphicsEffect(effect)
                layer = Layer(None, QPoint())
                self.entering.append((index, target, effect, layer))
                self.overlay.layers.append(layer)
        self.overlay.show()
        self.overlay.raise_()

        if direction == 0:
            total = self.REFRESH_MS
        else:
            total = max(self.OUT_MS, self.IN_DELAY_MS + self.IN_MS + self.STAGGER_MS * max(0, len(self.entering) - 1))
        self.animation = QVariantAnimation()
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(float(total))
        self.animation.setDuration(total)
        self.animation.valueChanged.connect(self.step)
        self.animation.finished.connect(self.stop)
        self.step(0.0)
        self.animation.start()

    def capture(self, target: QWidget, effect: HideEffect, layer: Layer):
        '''Pictures a new item, at rest, for its entrance.'''
        window = self.overlay.parentWidget()
        if not self.laid_out:
            # Settle any geometry still pending, so the pictures match
            # where the items will be once they're handed back
            self.laid_out = True
            for widget in (window, self.page):
                if widget.layout() is not None:
                    widget.layout().activate()
        layer.pixmap = self.blank(target, target.size())
        # Its HideEffect would otherwise blank the picture too
        effect.setEnabled(False)
        self.draw_content(target, layer.pixmap, QPoint(0, 0))
        effect.setEnabled(True)
        layer.origin = QPointF(target.mapTo(window, QPoint(0, 0)))

    def step(self, elapsed: float):
        try:
            if self.outgoing is not None:
                span = self.REFRESH_MS if self.direction == 0 else self.OUT_MS
                progress = self.OUT_CURVE.valueForProgress(min(1.0, elapsed / span))
                self.outgoing.opacity = 1.0 - progress
                self.outgoing.dx = -self.direction * self.SLIDE * progress
            landed = []
            for entry in self.entering:
                index, target, effect, layer = entry
                local = (elapsed - self.IN_DELAY_MS - index * self.STAGGER_MS) / self.IN_MS
                if local <= 0.0 or not self.page.isVisible():
                    continue
                if local >= 1.0:
                    landed.append(entry)
                    continue
                if layer.pixmap is None:
                    self.capture(target, effect, layer)
                progress = self.IN_CURVE.valueForProgress(local)
                remaining = 1.0 - progress
                layer.opacity = progress
                layer.dx = self.direction * self.SLIDE * remaining
                layer.dy = self.RISE * remaining
            for entry in landed:
                # In place - the real item takes over from its picture
                self.entering.remove(entry)
                self.overlay.layers.remove(entry[3])
                entry[1].setGraphicsEffect(None)
            self.overlay.update()
        except RuntimeError:
            # A widget went away mid-transition (its page was torn down)
            self.stop()

    def stop(self):
        if self.animation is None:
            return
        animation, self.animation = self.animation, None
        animation.stop()
        try:
            if self.overlay is not None:
                self.overlay.deleteLater()
        except RuntimeError:
            pass
        self.overlay = None
        self.outgoing = None
        for _index, target, _effect, _layer in self.entering:
            try:
                # Drop the effect entirely so the finished page paints
                # directly again
                target.setGraphicsEffect(None)
            except RuntimeError:
                pass
        self.entering = []


class PopupEntrance:
    '''
    Animates a popup window (an Overlay) opening, as one piece: the window
    glides SLIDE px out from its trigger button into place while fading in.

    The fade needs the platform to support window opacity (Windows, macOS,
    X11 with a compositor) - elsewhere, e.g. Wayland, just the glide plays.

    stop() snaps the window to its final state - called when the popup
    hides mid-animation.
    '''

    DURATION_MS = 200
    SLIDE = 10.0

    def __init__(self, window: QWidget, away: tuple[float, float]):
        '''away is the unit direction from the trigger button toward where the popup sits.'''
        self.window = window
        self.final = QPointF(window.pos())
        self.away = away
        self.fade_window = self.supports_fade()
        self.curve = QEasingCurve(QEasingCurve.Type.OutCubic)

        self.animation = QVariantAnimation()
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setDuration(self.DURATION_MS)
        self.animation.valueChanged.connect(self.step)
        self.animation.finished.connect(self.stop)
        self.step(0.0)
        self.animation.start()

    @staticmethod
    def supports_fade() -> bool:
        return QGuiApplication.platformName() in ("windows", "cocoa", "xcb")

    def step(self, progress: float):
        eased = self.curve.valueForProgress(progress)
        remaining = (1.0 - eased) * self.SLIDE
        try:
            self.window.move((self.final - QPointF(self.away[0] * remaining, self.away[1] * remaining)).toPoint())
            if self.fade_window:
                self.window.setWindowOpacity(eased)
        except RuntimeError:
            # The popup was deleted mid-animation
            self.stop()

    def stop(self):
        if self.animation is None:
            return
        animation, self.animation = self.animation, None
        try:
            animation.stop()
            self.window.move(self.final.toPoint())
            if self.fade_window:
                self.window.setWindowOpacity(1.0)
        except RuntimeError:
            pass


class WindowReveal:
    '''
    Fades the main window in at startup. Windows shows a new window as a
    blank white surface until Qt paints its first frame - a flash on a dark
    theme - so the window is shown fully transparent (hide(), before it's
    shown) and fades in once the first page has had time to paint
    (reveal(), once the event loop is running).

    Only where window opacity works (see PopupEntrance) - elsewhere the
    window just appears as it would without this.
    '''

    DELAY_MS = 50
    DURATION_MS = 180

    @staticmethod
    def hide(window: QWidget):
        if PopupEntrance.supports_fade():
            window.setWindowOpacity(0.0)

    @classmethod
    def reveal(cls, window: QWidget):
        if not PopupEntrance.supports_fade():
            return
        # Parented to the window, so it lives as long as it needs to
        animation = QVariantAnimation(window)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setDuration(cls.DURATION_MS)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        animation.valueChanged.connect(window.setWindowOpacity)
        # Exactly 1.0 at the end - Qt then drops the layered window opacity needs
        animation.finished.connect(lambda: window.setWindowOpacity(1.0))
        animation.finished.connect(animation.deleteLater)
        QTimer.singleShot(cls.DELAY_MS, animation.start)


class DesktopFade(QWidget):
    '''
    A borderless, click-through window over where the main window is (or
    will be), fading something in or out straight on the desktop - for
    FadeIn and FadeOut. It's see-through per pixel from the start
    (WA_TranslucentBackground) and paints its own opacity, rather than
    using window opacity: switching a window in and out of opacity mode
    redraws it on Windows, which flashes the desktop.
    '''

    def __init__(self, area: QRect):
        super().__init__(None, Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint
                         | Qt.WindowType.Tool | Qt.WindowType.WindowTransparentForInput)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating, True)
        self.setGeometry(area)
        self.opacity = 0.0

    def fade(self, duration: int, start: float, end: float, curve: QEasingCurve.Type, finished: Callable[[], None]):
        self.opacity = start
        animation = QVariantAnimation(self)
        animation.setStartValue(start)
        animation.setEndValue(end)
        animation.setDuration(duration)
        animation.setEasingCurve(curve)
        animation.valueChanged.connect(self.set_opacity)
        animation.finished.connect(finished)
        animation.finished.connect(animation.deleteLater)
        animation.start()

    def set_opacity(self, opacity: float):
        self.opacity = opacity
        self.update()


class FadeIn(DesktopFade):
    '''
    Startup with the "fade_in" preference: the theme's background color
    fades in on the desktop where the window will be, then the window
    shows underneath it (just that color) and this goes - see App.
    '''

    DURATION_MS = 900
    # Time for the window's painted frame to reach the screen before it's uncovered
    WINDOW_PAINT_MS = 50
    # How often to check whether the window has settled, and the longest to wait for it
    SETTLE_POLL_MS = 16
    SETTLE_MAX_MS = 1000

    def __init__(self, area: QRect, color: str):
        super().__init__(area)
        self.color = QColor(color)

    def play(self, window: QWidget, show_window: Callable[[], None], done: Callable[[], None]):
        '''
        Fades in, calls show_window, and once window has settled and painted
        closes and calls done. Settled is shown on screen with the same
        geometry two checks running - on Linux the window manager maps the
        window and only then maximizes it, so a fixed delay can uncover it
        unpainted or mid-resize.
        '''
        self.show()
        last_geometry = None
        waited = 0

        def covered():
            show_window()
            QTimer.singleShot(self.SETTLE_POLL_MS, settle)

        def settle():
            nonlocal last_geometry, waited
            waited += self.SETTLE_POLL_MS
            handle = window.windowHandle()
            exposed = handle is not None and handle.isExposed()
            geometry = window.geometry()
            if (exposed and geometry == last_geometry) or waited >= self.SETTLE_MAX_MS:
                # Painted at its final size before the cover goes
                window.repaint()
                QTimer.singleShot(self.WINDOW_PAINT_MS, uncovered)
                return
            last_geometry = geometry if exposed else None
            QTimer.singleShot(self.SETTLE_POLL_MS, settle)

        def uncovered():
            self.close()
            done()
        self.fade(self.DURATION_MS, 0.0, 1.0, QEasingCurve.Type.InOutCubic, covered)

    def paintEvent(self, event):
        color = QColor(self.color)
        color.setAlphaF(max(0.0, min(1.0, self.opacity)))
        painter = QPainter(self)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Source)
        painter.fillRect(self.rect(), color)
        painter.end()


class FadeOut(DesktopFade):
    '''
    Quitting with the "fade_out" preference: a screenshot of the window
    takes its place on the desktop and fades out, then the app quits - see
    Router.quit.
    '''

    DURATION_MS = 350

    def __init__(self, window: QWidget):
        super().__init__(window.geometry())
        self.screenshot = window.grab()
        self.opacity = 1.0

    def play(self, window: QWidget, done: Callable[[], None]):
        '''Covers window with its screenshot, hides it, fades out, and calls done.'''
        self.show()
        # Once this has painted over it, so the desktop never shows between them
        QTimer.singleShot(30, window.hide)
        self.fade(self.DURATION_MS, 1.0, 0.0, QEasingCurve.Type.InCubic, done)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Source)
        painter.fillRect(self.rect(), Qt.GlobalColor.transparent)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)
        painter.setOpacity(max(0.0, min(1.0, self.opacity)))
        painter.drawPixmap(self.rect(), self.screenshot)
        painter.end()
