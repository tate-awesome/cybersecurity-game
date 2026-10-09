import math

from PySide6.QtCore import QEvent, QObject, QPoint, QRectF, Qt
from PySide6.QtGui import QColor, QImage, QPainter, QPainterPath
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QLineEdit, QMainWindow,
                               QPlainTextEdit, QPushButton, QStyle, QStyleOption, QTextEdit, QWidget)

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .style import Style


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


def blur_levels(radius: float) -> list[tuple[int, float]]:
    '''
    Pyramid levels (see pyramid_blur, applied to a half-size image) for a
    blur of `radius` px, with the opacity to draw each at. Levels come in
    doublings, so an in-between radius blends the two nearest - which
    keeps a blur slider smooth.
    '''
    level = max(0.0, math.log2(radius) - 1) if radius > 1 else 0.0
    low = int(level)
    layers = [(low, 1.0)]
    if level - low > 0.02:
        layers.append((low + 1, level - low))
    return layers


class Backdrop(QObject):
    '''
    Frosted glass for surfaces (see style.SURFACE_KINDS): a see-through
    surface with blur paints a blurred crop of the page's background
    visual under itself, then its own translucent color on top - so it
    shows the network behind it softened, like Windows' Acrylic.

    Works as an application event filter that runs just before each
    widget paints. It's only installed while some surface actually has
    blur and is see-through, so it costs nothing otherwise.

    Which surface a widget is: its "surface" property (set by
    Style.themed, Canvas, etc.), else its type - buttons, and text
    inputs/tree views/consoles as fields. A scrolling field gets the
    backdrop across its whole frame, not just its viewport, so its border
    and padding are frosted too; the viewport's tint then lands on top.

    A nested surface (a field on a form on a panel) re-tints its blurred
    crop with every surface it sits inside, outermost first, before its
    own color goes on top - so blur only softens what shows through and
    never changes the color it builds up to (see ancestor_tints).
    '''

    def __init__(self, style: "Style"):
        super().__init__()
        self.style = style
        self.installed = False

    def radius(self, kind: str) -> float:
        if kind in ("button", "field"):
            return 4.0
        if kind == "panel":
            return float(self.style.PANEL_RADIUS)
        return 0.0

    def active_kinds(self) -> set[str]:
        return {kind for kind, blur in self.style.surface_blur.items()
                if blur > 0 and self.style.opacity(kind) < 1.0}

    def sync(self):
        '''Installs or removes the filter to match the settings, and repaints so changes show at once.'''
        app = QApplication.instance()
        active = bool(self.active_kinds())
        if active != self.installed:
            if active:
                app.installEventFilter(self)
            else:
                app.removeEventFilter(self)
            self.installed = active
        for window in app.topLevelWidgets():
            if window.isVisible():
                window.update()

    def kind_of(self, widget: QWidget) -> str | None:
        kind = widget.property("surface")
        if kind:
            return kind
        if isinstance(widget, QPushButton):
            return "button"
        if isinstance(widget, (QLineEdit, QComboBox, QTextEdit, QPlainTextEdit, QAbstractItemView)):
            return "field"
        return None

    def tint(self, kind: str) -> QColor | None:
        '''The see-through color a surface of this kind paints itself in.'''
        if kind in ("panel", "widget", "field"):
            return QColor(self.style.color(kind))
        if kind == "bar":
            color = QColor(self.style.color("widget", opaque=True))
            color.setAlphaF(self.style.opacity("bar"))
            return color
        return None

    def ancestor_tints(self, widget: QWidget, page: QWidget) -> list[QColor]:
        '''The tints of the surfaces widget sits inside, outermost first, stopping at the page.'''
        tints = []
        parent = widget.parentWidget()
        while parent is not None and parent is not page:
            kind = parent.property("surface")
            tint = self.tint(kind) if kind else None
            if tint is not None:
                tints.append(tint)
            parent = parent.parentWidget()
        return tints[::-1]

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if event.type() != QEvent.Type.Paint or not watched.isWidgetType():
            return False
        kind = self.kind_of(watched)
        if kind is None or kind not in self.active_kinds():
            return False
        self.paint(watched, self.style.surface_blur[kind], self.radius(kind))
        return False  # the widget still paints itself, translucent, on top

    def paint(self, widget: QWidget, blur: float, radius: float):
        window = widget.window()
        page = window.centralWidget() if isinstance(window, QMainWindow) else None
        background = getattr(page, "background", None)
        if background is None or not background.isVisible() or background.width() <= 0:
            return
        layers = background.backdrop(blur)
        if not layers:
            return
        origin = widget.mapTo(window, QPoint(0, 0)) - background.mapTo(window, QPoint(0, 0))

        painter = QPainter(widget)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        target = QRectF(widget.rect())
        if radius > 0:
            clip = QPainterPath()
            clip.addRoundedRect(target, radius, radius)
            painter.setClipPath(clip)
        for image, opacity in layers:
            scale = image.width() / background.width()
            source = QRectF(origin.x() * scale, origin.y() * scale, target.width() * scale, target.height() * scale)
            painter.setOpacity(opacity)
            painter.drawImage(target, image, source)
        painter.setOpacity(1.0)
        for tint in self.ancestor_tints(widget, page):
            painter.fillRect(target, tint)

        # A stylesheet background (WA_StyledBackground - panels, forms,
        # menu bars...) is painted by Qt *before* the paint event this runs
        # in, so the backdrop just covered it - paint it again on top.
        # Buttons and inputs paint theirs inside their own paint event,
        # which comes after this anyway.
        if widget.testAttribute(Qt.WidgetAttribute.WA_StyledBackground):
            painter.setOpacity(1.0)
            painter.setClipping(False)
            option = QStyleOption()
            option.initFrom(widget)
            widget.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, option, painter, widget)
        painter.end()
