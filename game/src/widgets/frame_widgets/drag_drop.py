'''
Drag and drop between zones, independent of what's being dragged.

Three pieces, each knowing nothing about the others' contents:

  - DragPayload: what a drag carries - its kind ("workspace", "section",
    later e.g. "panel"), the dragged item's id, and the zone it left.
  - DragHandle: makes any widget start a drag - a chip by itself, or a
    card by its header - with a picture of whatever it drags following
    the mouse.
  - DropZone: a widget that takes drops of the kinds it accepts, draws
    where one would land, and reports it as `dropped(payload, slot)`. It
    never moves anything itself - whoever owns the zones decides what a
    drop means, so the same zones can back any model.

The drag never leaves the app: it's plain mouse events and a picture
floating over the window, not the system's drag and drop, so it works the
same on every platform and window system (and as root under sudo, where
the system's can't reach the window).

ListZone (a column, by index) is the zone so far. A "slot" is whatever a
zone's slot_at returns, so a zone that docks - say, by which edge of a
pane the drop is near - only needs its own slot_at and indicator_rect, and
its owner reads that slot.
'''
from dataclasses import dataclass
from typing import Callable

from PySide6.QtCore import QEvent, QObject, QPoint, QRect, Qt, QTimer, Signal
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import (QAbstractButton, QAbstractScrollArea, QAbstractSpinBox, QApplication, QComboBox, QFrame,
                               QGraphicsOpacityEffect, QLabel, QLineEdit, QVBoxLayout, QWidget)

from ...app_core import Context

# How thick the line showing where a drop lands is, the soft glow around it, and the dots capping its ends
INDICATOR_WIDTH = 4
INDICATOR_GLOW = 12
INDICATOR_CAP = 10
# Dragging this close to a scroll area's top or bottom edge scrolls it - faster the closer
AUTO_SCROLL_MARGIN = 60
AUTO_SCROLL_MAX_STEP = 24
AUTO_SCROLL_MS = 16
# Children of a handle that take clicks themselves - pressing one never starts a drag
INTERACTIVE = (QAbstractButton, QLineEdit, QComboBox, QAbstractSpinBox)


@dataclass(frozen=True)
class DragPayload:
    kind: str
    item_id: str
    source: str


class DragHandle(QObject):
    '''
    Lets handle start a drag once the mouse is pressed on it (or anything in
    it but INTERACTIVE children) and moved past the platform's drag
    distance - carrying payload(), with a picture of preview (handle
    itself by default) following the mouse while preview fades in place.
    Releasing over a DropZone that accepts the payload's kind drops it
    there; anywhere else, or Esc, cancels. Holding it near the top or
    bottom of a scroll area scrolls it, to reach zones out of view.

    It watches handle and every child of it directly, since a child that
    takes mouse moves itself (a QLabel does) never passes them on.
    '''

    def __init__(self, handle: QWidget, payload: Callable[[], DragPayload], preview: QWidget | None = None):
        super().__init__(handle)
        self.handle = handle
        self.payload = payload
        self.preview = preview or handle
        self.pressed_at: QPoint | None = None
        # While dragging: what's dragged, its floating picture, where the mouse holds it, the zone it's over
        self.dragging: DragPayload | None = None
        self.ghost: QLabel | None = None
        self.grip = QPoint()
        self.zone: "DropZone | None" = None
        self.at = QPoint()
        self.scroller = QTimer(self)
        self.scroller.setInterval(AUTO_SCROLL_MS)
        self.scroller.timeout.connect(self.auto_scroll)
        for widget in [handle, *handle.findChildren(QWidget)]:
            if not isinstance(widget, INTERACTIVE):
                widget.setCursor(Qt.CursorShape.OpenHandCursor)
                widget.installEventFilter(self)

    def eventFilter(self, watched, event):
        kind = event.type()
        if kind == QEvent.Type.MouseButtonPress and event.button() == Qt.MouseButton.LeftButton:
            self.pressed_at = event.globalPosition().toPoint()
        elif kind == QEvent.Type.MouseMove and event.buttons() & Qt.MouseButton.LeftButton:
            at = event.globalPosition().toPoint()
            if self.dragging is not None:
                self.move_to(at)
                return True
            if self.pressed_at is not None and (at - self.pressed_at).manhattanLength() >= QApplication.startDragDistance():
                self.begin(self.pressed_at)
                self.move_to(at)
                return True
        elif kind == QEvent.Type.MouseButtonRelease and event.button() == Qt.MouseButton.LeftButton:
            self.pressed_at = None
            if self.dragging is not None:
                self.finish(drop=True)
                return True
        elif kind == QEvent.Type.KeyPress and event.key() == Qt.Key.Key_Escape and self.dragging is not None:
            self.finish(drop=False)
            return True
        return False

    def begin(self, at: QPoint):
        self.dragging = self.payload()
        window = self.handle.window()
        self.grip = self.preview.mapFromGlobal(at)
        self.ghost = QLabel(window)
        self.ghost.setPixmap(self.preview.grab())
        self.ghost.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.ghost.adjustSize()
        self.ghost.show()
        self.ghost.raise_()
        # Left in place, faded, so its old spot still reads while it's dragged
        effect = QGraphicsOpacityEffect(self.preview)
        effect.setOpacity(0.35)
        self.preview.setGraphicsEffect(effect)
        self.handle.setCursor(Qt.CursorShape.ClosedHandCursor)
        # For Esc, which goes to whatever has focus
        self.handle.setFocus()
        self.scroller.start()

    def move_to(self, at: QPoint):
        self.at = at
        self.ghost.move(self.ghost.parentWidget().mapFromGlobal(at) - self.grip)
        zone = self.zone_at(at)
        if zone is not self.zone:
            if self.zone is not None:
                self.zone.clear_indicator()
            self.zone = zone
        if zone is not None:
            zone.hover(zone.mapFromGlobal(at))

    def auto_scroll(self):
        '''While dragging: scrolls the scroll area under the mouse if it's near its top or bottom edge.'''
        widget = QApplication.widgetAt(self.at)
        while widget is not None and not isinstance(widget, QAbstractScrollArea):
            widget = widget.parentWidget()
        if widget is None:
            return
        viewport = widget.viewport()
        y = viewport.mapFromGlobal(self.at).y()
        if y < AUTO_SCROLL_MARGIN:
            step = -AUTO_SCROLL_MAX_STEP * (AUTO_SCROLL_MARGIN - max(y, 0)) // AUTO_SCROLL_MARGIN
        elif y > viewport.height() - AUTO_SCROLL_MARGIN:
            step = AUTO_SCROLL_MAX_STEP * (min(y, viewport.height()) - viewport.height() + AUTO_SCROLL_MARGIN) // AUTO_SCROLL_MARGIN
        else:
            return
        bar = widget.verticalScrollBar()
        before = bar.value()
        bar.setValue(before + step)
        if bar.value() != before:
            self.move_to(self.at)  # what's under the mouse moved

    def zone_at(self, at: QPoint) -> "DropZone | None":
        '''The innermost DropZone under the mouse that accepts what's dragged.'''
        widget = QApplication.widgetAt(at)
        while widget is not None:
            if isinstance(widget, DropZone) and self.dragging.kind in widget.accepts:
                return widget
            widget = widget.parentWidget()
        return None

    def finish(self, drop: bool):
        self.scroller.stop()
        payload, zone, at = self.dragging, self.zone, self.at
        self.dragging, self.zone = None, None
        self.ghost.hide()
        self.ghost.deleteLater()
        self.ghost = None
        # Setting None deletes the effect
        self.preview.setGraphicsEffect(None)
        self.handle.setCursor(Qt.CursorShape.OpenHandCursor)
        if zone is not None:
            zone.clear_indicator()
            if drop:
                zone.dropped.emit(payload, zone.slot_at(zone.mapFromGlobal(at)))


class _Indicator(QWidget):
    '''
    The line showing where a drop lands, floating over a zone's items so
    none of them can cover it: an accent line in a soft glow, with a dot
    at each end. Its line runs along its middle, end to end.
    '''

    def __init__(self, zone: "DropZone"):
        super().__init__(zone)
        self.style = zone.style
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.style.set_material(self, "none")
        self.hide()

    def place(self, line: QRect):
        '''Covers line, with room around it for the glow and the dots.'''
        pad = max(INDICATOR_GLOW, INDICATOR_CAP) // 2
        self.setGeometry(line.adjusted(0, -pad, 0, pad))
        self.show()
        self.raise_()
        self.update()

    def paintEvent(self, event):
        color = QColor(self.style.color("accent"))
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        y = self.height() / 2
        r = INDICATOR_CAP / 2
        left, right = r, self.width() - r
        glow = QColor(color)
        glow.setAlpha(70)
        for line_color, width in ((glow, INDICATOR_GLOW), (color, INDICATOR_WIDTH)):
            pen = QPen(line_color, width)
            pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)
            painter.drawLine(int(left), int(y), int(right), int(y))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(color)
        for x in (left, right):
            painter.drawEllipse(int(x - r), int(y - r), INDICATOR_CAP, INDICATOR_CAP)
        painter.end()


class DropZone(QFrame):
    '''
    A widget that takes drops of the kinds it accepts (see DragPayload.kind)
    and emits dropped(payload, slot) - moving anything is up to whoever
    connects to it. Holds its items (widgets) in order; subclasses lay
    them out and say where a drop at a point lands (slot_at) and where to
    draw that (indicator_rect).

    Zones can nest - cards in a ListZone, each holding a ListZone - and a
    drag goes to the innermost one under the mouse that accepts its kind.
    '''

    dropped = Signal(object, object)

    def __init__(self, context: Context, zone_id: str, accepts: set[str]):
        super().__init__()
        self.context = context
        self.style = context.style
        self.zone_id = zone_id
        self.accepts = accepts
        self.items: list[QWidget] = []
        self.indicator: QRect | None = None
        self.indicator_line = _Indicator(self)

    # Items
    def insert(self, widget: QWidget, index: int):
        index = max(0, min(index, len(self.items)))
        self.items.insert(index, widget)
        self.layout().insertWidget(index, widget)

    def take(self, widget: QWidget):
        '''Takes widget out of this zone (without deleting it), so another zone can insert it.'''
        self.items.remove(widget)
        self.layout().removeWidget(widget)

    def index_of(self, widget: QWidget) -> int:
        return self.items.index(widget)

    # Subclasses
    def slot_at(self, pos: QPoint):
        raise NotImplementedError

    def indicator_rect(self, slot) -> QRect | None:
        raise NotImplementedError

    # Dragging over it (see DragHandle)
    def hover(self, pos: QPoint):
        indicator = self.indicator_rect(self.slot_at(pos))
        if indicator != self.indicator:
            self.indicator = indicator
            if indicator is None:
                self.indicator_line.hide()
            else:
                self.indicator_line.place(indicator)

    def clear_indicator(self):
        self.indicator = None
        self.indicator_line.hide()


class ListZone(DropZone):
    '''
    Items stacked top to bottom. A slot is the index a drop would insert at;
    the indicator is a line in the gap above that item (or below the last).
    Empty, it keeps a row's height, so there's still somewhere to drop.
    '''

    def __init__(self, context: Context, zone_id: str, accepts: set[str], spacing: int | None = None):
        super().__init__(context, zone_id, accepts)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(context.style.igap if spacing is None else spacing)
        self.setMinimumHeight(self.fontMetrics().height() * 2)

    def slot_at(self, pos: QPoint) -> int:
        for index, widget in enumerate(self.items):
            if pos.y() < widget.geometry().center().y():
                return index
        return len(self.items)

    def indicator_rect(self, slot: int) -> QRect:
        if not self.items:
            return QRect(0, (self.height() - INDICATOR_WIDTH) // 2, self.width(), INDICATOR_WIDTH)
        gap = self.layout().spacing()
        if slot < len(self.items):
            y = self.items[slot].geometry().top() - (gap + INDICATOR_WIDTH) // 2
        else:
            y = self.items[-1].geometry().bottom() + (gap - INDICATOR_WIDTH) // 2 + 1
        return QRect(0, max(0, min(y, self.height() - INDICATOR_WIDTH)), self.width(), INDICATOR_WIDTH)
