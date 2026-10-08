from PySide6.QtCore import QEasingCurve, QPoint, QPointF, QRectF, Qt, QVariantAnimation
from PySide6.QtGui import QPainter, QPixmap, QRegion
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
