from PySide6.QtCore import QEasingCurve, QPoint, QPointF, QRectF, Qt, QVariantAnimation
from PySide6.QtGui import QGuiApplication, QPainter, QPixmap, QRegion
from PySide6.QtWidgets import QGraphicsEffect, QWidget


class AppearEffect(QGraphicsEffect):
    '''
    Draws its widget faded and shifted by (dx, dy) - an entrance pose that
    PageTransition eases back to fully opaque and in place.
    '''

    def __init__(self, dx: float, dy: float):
        super().__init__()
        self.opacity = 0.0
        self.dx, self.dy = dx, dy

    def set_pose(self, opacity: float, dx: float, dy: float):
        self.opacity, self.dx, self.dy = opacity, dx, dy
        self.updateBoundingRect()
        self.update()

    def boundingRectFor(self, rect: QRectF) -> QRectF:
        return rect.united(rect.translated(self.dx, self.dy))

    def draw(self, painter: QPainter):
        if self.opacity <= 0.0:
            return
        if self.opacity >= 1.0 and not self.dx and not self.dy:
            self.drawSource(painter)
            return
        # PySide6 drops sourcePixmap's offset out-parameter, so place the
        # pixmap by the source's own bounding rect (logical coordinates,
        # no padding - the two then line up exactly)
        pixmap = self.sourcePixmap(Qt.CoordinateSystem.LogicalCoordinates, mode=QGraphicsEffect.PixmapPadMode.NoPad)
        origin = self.sourceBoundingRect(Qt.CoordinateSystem.LogicalCoordinates).topLeft()
        painter.save()
        painter.setOpacity(self.opacity)
        painter.drawPixmap(origin + QPointF(self.dx, self.dy), pixmap)
        painter.restore()


class SnapshotOverlay(QWidget):
    '''A picture of the page being left, drawn over the new one while it fades and drifts away.'''

    def __init__(self, parent: QWidget, pixmap: QPixmap, origin: QPoint):
        super().__init__(parent)
        self.pixmap = pixmap
        # Where the old page sat in the window
        self.origin = QPointF(origin)
        self.opacity = 1.0
        self.dx = 0.0
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)

    def paintEvent(self, event):
        if self.opacity <= 0.0:
            return
        painter = QPainter(self)
        painter.setOpacity(self.opacity)
        painter.drawPixmap(self.origin + QPointF(self.dx, 0.0), self.pixmap)
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
        ratio = page.devicePixelRatioF()
        pixmap = QPixmap(page.size() * ratio)
        pixmap.setDevicePixelRatio(ratio)
        pixmap.fill(Qt.GlobalColor.transparent)
        for target in targets:
            # DrawChildren only - the default also fills each target with
            # its palette's window color (near-white in Fusion), which
            # flashed as a light box behind labels and bars. Stylesheet
            # backgrounds still paint, since those come from paintEvent.
            target.render(pixmap, target.mapTo(page, QPoint(0, 0)), QRegion(), QWidget.RenderFlag.DrawChildren)
        return pixmap, page.pos()

    def __init__(self, page: QWidget, snapshot: tuple[QPixmap, QPoint] | None, direction: int):
        self.direction = direction
        self.overlay = None
        if snapshot is not None:
            # Covers the whole window and draws the picture where the old
            # page was - the new page isn't laid out yet, so its own
            # geometry can't be trusted here
            window = page.parentWidget()
            self.overlay = SnapshotOverlay(window, *snapshot)
            self.overlay.setGeometry(window.rect())
            self.overlay.show()
            self.overlay.raise_()

        self.effects: list[tuple[QWidget, AppearEffect]] = []
        if direction != 0 and hasattr(page, "appear_targets"):
            for target in page.appear_targets():
                effect = AppearEffect(direction * self.SLIDE, self.RISE)
                target.setGraphicsEffect(effect)
                self.effects.append((target, effect))

        if direction == 0:
            total = self.REFRESH_MS
        else:
            total = max(self.OUT_MS, self.IN_DELAY_MS + self.IN_MS + self.STAGGER_MS * max(0, len(self.effects) - 1))
        self.animation = QVariantAnimation()
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(float(total))
        self.animation.setDuration(total)
        self.animation.valueChanged.connect(self.step)
        self.animation.finished.connect(self.stop)
        self.step(0.0)
        self.animation.start()

    def step(self, elapsed: float):
        out_curve = QEasingCurve(QEasingCurve.Type.InOutQuad)
        in_curve = QEasingCurve(QEasingCurve.Type.OutCubic)
        try:
            if self.overlay is not None:
                span = self.REFRESH_MS if self.direction == 0 else self.OUT_MS
                progress = out_curve.valueForProgress(min(1.0, elapsed / span))
                self.overlay.opacity = 1.0 - progress
                self.overlay.dx = -self.direction * self.SLIDE * progress
                self.overlay.update()
            for index, (_target, effect) in enumerate(self.effects):
                local = (elapsed - self.IN_DELAY_MS - index * self.STAGGER_MS) / self.IN_MS
                progress = in_curve.valueForProgress(min(1.0, max(0.0, local)))
                remaining = 1.0 - progress
                effect.set_pose(progress, self.direction * self.SLIDE * remaining, self.RISE * remaining)
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
        for target, _effect in self.effects:
            try:
                # Drop the effect entirely so the finished page paints
                # directly again, with no offscreen pass
                target.setGraphicsEffect(None)
            except RuntimeError:
                pass
        self.effects = []


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


class PopupExit(QWidget):
    '''
    A popup's fade-out. The popup itself hides at once (its open/close
    bookkeeping stays instant and untouched); this click-through window
    takes its place, showing a picture of it, and fades out while gliding
    SLIDE px back toward the trigger button, then deletes itself.

    Only played where window opacity works (see PopupEntrance) - elsewhere
    the popup just vanishes, as it would without this.
    '''

    DURATION_MS = 150
    SLIDE = 6.0

    @classmethod
    def play(cls, popup: QWidget, away: tuple[float, float]):
        if not PopupEntrance.supports_fade() or popup.width() <= 0:
            return
        cls(popup.parentWidget(), popup.grab(), popup.pos(), away)

    def __init__(self, parent: QWidget | None, pixmap: QPixmap, pos: QPoint, away: tuple[float, float]):
        super().__init__(parent, Qt.WindowType.ToolTip | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating, True)
        self.pixmap = pixmap
        self.start = QPointF(pos)
        self.away = away
        self.curve = QEasingCurve(QEasingCurve.Type.InCubic)
        self.resize(pixmap.deviceIndependentSize().toSize())
        self.move(pos)

        self.animation = QVariantAnimation(self)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setDuration(self.DURATION_MS)
        self.animation.valueChanged.connect(self.step)
        self.animation.finished.connect(self.deleteLater)
        self.step(0.0)
        self.show()
        self.animation.start()

    def step(self, progress: float):
        eased = self.curve.valueForProgress(progress)
        self.setWindowOpacity(1.0 - eased)
        offset = eased * self.SLIDE
        self.move((self.start - QPointF(self.away[0] * offset, self.away[1] * offset)).toPoint())

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.pixmap)
        painter.end()
