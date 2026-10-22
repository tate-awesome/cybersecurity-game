from PySide6.QtCore import QMargins, QRect, QSize, Qt
from PySide6.QtWidgets import QLayout, QLayoutItem, QSizePolicy, QWidget


QWIDGETSIZE_MAX = (1 << 24) - 1  # Qt's "no maximum" sentinel for widget sizes


class FlowLayout(QLayout):
    '''
    Lays its widgets out left to right, wrapping to a new row when the next
    one wouldn't fit the available width - so a panel of cards reflows to
    fill however wide it currently is, one column when narrow and more as it
    widens. Hidden widgets are skipped and take up no space (the network
    action panel shows/hides forms in place - see its Builder), so a hidden
    card leaves no gap.

    The cards are laid out in columns, filling each column top to bottom
    before moving to the next one (so reading order is top-to-bottom then
    left-to-right). Every card keeps its own natural height - nothing is
    stretched to line up with its neighbours - so columns end at ragged but
    honest heights. All columns share one width that fills the panel edge to
    edge (each between the cards' minimum and maximum width); a trailing gap
    is avoided as long as the maximum width is about twice the minimum.

    The width-dependent height is reported through heightForWidth, which a
    vertical scroll area honours.
    '''

    def __init__(self, parent: QWidget | None = None, margin: int = 0, hspacing: int = -1, vspacing: int = -1):
        super().__init__(parent)
        self._items: list[QLayoutItem] = []
        self._hspacing = hspacing
        self._vspacing = vspacing
        self.setContentsMargins(QMargins(margin, margin, margin, margin))

    def addItem(self, item: QLayoutItem):
        self._items.append(item)

    def count(self) -> int:
        return len(self._items)

    def itemAt(self, index: int) -> QLayoutItem | None:
        if 0 <= index < len(self._items):
            return self._items[index]
        return None

    def takeAt(self, index: int) -> QLayoutItem | None:
        if 0 <= index < len(self._items):
            return self._items.pop(index)
        return None

    def horizontalSpacing(self) -> int:
        return self._hspacing if self._hspacing >= 0 else self._smart_spacing()

    def verticalSpacing(self) -> int:
        return self._vspacing if self._vspacing >= 0 else self._smart_spacing()

    def expandingDirections(self) -> Qt.Orientation:
        return Qt.Orientation(0)

    def hasHeightForWidth(self) -> bool:
        return True

    def heightForWidth(self, width: int) -> int:
        return self._do_layout(QRect(0, 0, width, 0), test_only=True)

    def setGeometry(self, rect: QRect):
        super().setGeometry(rect)
        self._do_layout(rect, test_only=False)

    def sizeHint(self) -> QSize:
        return self.minimumSize()

    def minimumSize(self) -> QSize:
        size = QSize()
        for item in self._visible_items():
            size = size.expandedTo(item.minimumSize())
        margins = self.contentsMargins()
        size += QSize(margins.left() + margins.right(), margins.top() + margins.bottom())
        return size

    def _visible_items(self) -> list[QLayoutItem]:
        return [i for i in self._items if not (i.widget() is not None and i.widget().isHidden())]

    def _card_min(self, item: QLayoutItem) -> int:
        widget = item.widget()
        if widget is not None and widget.minimumWidth() > 0:
            return widget.minimumWidth()
        return item.sizeHint().width()

    def _card_max(self, item: QLayoutItem) -> int:
        widget = item.widget()
        if widget is not None and 0 < widget.maximumWidth() < QWIDGETSIZE_MAX:
            return widget.maximumWidth()
        return QWIDGETSIZE_MAX

    def _do_layout(self, rect: QRect, test_only: bool) -> int:
        margins = self.contentsMargins()
        effective = rect.adjusted(margins.left(), margins.top(), -margins.right(), -margins.bottom())
        items = self._visible_items()
        if not items:
            return margins.top() + margins.bottom()

        hspace = self.horizontalSpacing()
        vspace = self.verticalSpacing()
        avail = max(effective.width(), 1)
        count = len(items)

        # One uniform column width for the whole panel. The column count is
        # how many cards fit at their minimum width (never more than there
        # are cards), so a wide panel makes more columns rather than one
        # over-wide card. The columns then share the width evenly (filling it
        # edge to edge with no trailing gap) capped at the max - which, being
        # about twice the min, is always enough room to swallow the leftover,
        # so the cap only bites when a column would be wider than a card
        # should be.
        unit_min = max(self._card_min(item) for item in items)
        unit_max = min(self._card_max(item) for item in items)
        cols = max(1, (avail + hspace) // (unit_min + hspace))
        cols = min(cols, count)
        inner = avail - (cols - 1) * hspace  # width the columns themselves share
        width = min(inner // cols, unit_max)
        # Spread any rounding remainder one pixel at a time across the
        # columns, so a full row of columns reaches edge to edge.
        remainder = inner - width * cols if width < unit_max else 0

        # Fill each column top to bottom before the next: the first `rows`
        # cards go down column 0, the next `rows` down column 1, and so on.
        rows = (count + cols - 1) // cols
        total_height = 0
        x = effective.x()
        for col in range(cols):
            col_width = width + (1 if col < remainder else 0)
            y = effective.y()
            for item in items[col * rows:(col + 1) * rows]:
                h = item.sizeHint().height()
                if not test_only:
                    item.setGeometry(QRect(x, y, col_width, h))
                y += h + vspace
            total_height = max(total_height, y - vspace)
            x += col_width + hspace

        return total_height - rect.y() + margins.bottom()

    def _smart_spacing(self) -> int:
        parent = self.parent()
        if parent is None:
            return 0
        if parent.isWidgetType():
            return parent.style().pixelMetric(parent.style().PixelMetric.PM_LayoutHorizontalSpacing, None, parent)
        return 0
