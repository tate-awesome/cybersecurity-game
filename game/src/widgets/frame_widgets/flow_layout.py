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

    Within a row the cards are stretched to fill its full width (each between
    its own minimum and maximum width), so a full row never leaves a trailing
    gap - which holds as long as the cards' maximum width is about twice their
    minimum (then whatever space is left when no more cards fit is always
    less than the room the row's cards have left to grow). Every card in a row
    is also given the row's tallest card's height, so a row reads as one band.
    Only the last row, if it can't be filled, is left ragged.

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

        # One uniform card width for the whole panel. The column count is
        # how many cards fit at their minimum width, so a wide panel always
        # makes more columns rather than one over-wide card. Every card then
        # takes an even share of the width (so a full row fills edge to edge
        # with no trailing gap) capped at the max - which, being about twice
        # the min, is always enough room to swallow the leftover, so the cap
        # only bites when there's a single column wider than a card should be.
        unit_min = max(self._card_min(item) for item in items)
        unit_max = min(self._card_max(item) for item in items)
        cols = max(1, (avail + hspace) // (unit_min + hspace))
        inner = avail - (cols - 1) * hspace  # width the cards themselves share
        width = min(inner // cols, unit_max)
        # Spread any rounding remainder one pixel at a time across the row's
        # columns, so a full row's cards reach edge to edge.
        remainder = inner - width * cols if width < unit_max else 0

        x = effective.x()
        y = effective.y()
        col = 0
        row_items: list[tuple[QLayoutItem, int, int]] = []  # (item, x, width)

        def flush_row():
            nonlocal y
            if not row_items:
                return
            row_height = max(it.sizeHint().height() for it, _, _ in row_items)
            if not test_only:
                for it, ix, iw in row_items:
                    it.setGeometry(QRect(ix, y, iw, row_height))
            y += row_height + vspace
            row_items.clear()

        for index, item in enumerate(items):
            if col == cols:
                flush_row()
                x = effective.x()
                col = 0
            w = width + (1 if col < remainder else 0)
            row_items.append((item, x, w))
            x += w + hspace
            col += 1
        flush_row()

        return y - vspace - rect.y() + margins.bottom()

    def _smart_spacing(self) -> int:
        parent = self.parent()
        if parent is None:
            return 0
        if parent.isWidgetType():
            return parent.style().pixelMetric(parent.style().PixelMetric.PM_LayoutHorizontalSpacing, None, parent)
        return 0
