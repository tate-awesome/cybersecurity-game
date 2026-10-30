from collections.abc import Callable
from math import ceil

from PySide6.QtCore import QMargins, QPoint, QRect, QSize, Qt
from PySide6.QtWidgets import QLayout, QLayoutItem, QSizePolicy, QWidget, QWidgetItem


QWIDGETSIZE_MAX = (1 << 24) - 1  # Qt's "no maximum" sentinel for widget sizes


class FlowLayout(QLayout):
    '''
    Lays its widgets out on a grid of uniform cells, left to right and
    wrapping to a new row - so a panel of cards reflows to fill however wide
    it currently is, one column when narrow and more as it widens. Hidden
    widgets are skipped and take up no space (the network action panel
    shows/hides forms in place - see its Builder), so a hidden card leaves no
    gap.

    A cell is unit_height tall (the height of a card with just its header
    and button). A taller card spans as many cells down as it needs and is
    stretched to fill them exactly, so every card's top and bottom land on
    the grid instead of leaving ragged gaps. Cards are placed in order, each
    in the next free cell reading left to right then top to bottom - a row
    is filled before moving on to the next, skipping cells that a tall card
    from the row above still covers.

    All columns share one width that fills the panel edge to edge (each
    between the cards' minimum and maximum width); a trailing gap is avoided
    as long as the maximum width is about twice the minimum.

    The width-dependent height is reported through heightForWidth, which a
    vertical scroll area honours.
    '''

    def __init__(self, parent: QWidget | None = None, margin: int = 0, hspacing: int = -1, vspacing: int = -1,
                 unit_height: Callable[[], int] | None = None):
        '''
        unit_height returns the grid's cell height - asked on every layout,
        since it follows the theme's fonts. Without it (or when it returns 0)
        the shortest visible card sets the cell height.
        '''
        super().__init__(parent)
        self._items: list[QLayoutItem] = []
        self._hspacing = hspacing
        self._vspacing = vspacing
        self._unit_height = unit_height
        self.setContentsMargins(QMargins(margin, margin, margin, margin))

    def addItem(self, item: QLayoutItem):
        self._items.append(item)

    def set_order(self, widgets: list[QWidget]):
        '''
        Reorders the laid-out items to match `widgets` (any item whose widget
        isn't listed keeps its relative place at the end), then relays out.
        Lets a panel reflow its cards to a new order without rebuilding them.
        '''
        rank = {id(w): i for i, w in enumerate(widgets)}
        self._items.sort(key=lambda item: rank.get(id(item.widget()), len(rank)))
        self.invalidate()

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

    def _unit(self, items: list[QLayoutItem]) -> int:
        unit = self._unit_height() if self._unit_height is not None else 0
        if unit <= 0:
            unit = min(item.sizeHint().height() for item in items)
        return max(unit, 1)

    def _span(self, item: QLayoutItem, unit: int, vspace: int) -> int:
        '''How many cells down a card needs to fit its natural height.'''
        return max(1, ceil((item.sizeHint().height() + vspace) / (unit + vspace)))

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
        unit = self._unit(items)

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
        col_x = []
        x = effective.x()
        for col in range(cols):
            col_x.append(x)
            x += width + (1 if col < remainder else 0) + hspace

        # Each card takes the next free cell after the previous card's,
        # reading left to right then top to bottom, and claims the cells
        # below it that its span covers. Nothing placed later sits above the
        # cursor, so a tall card always has room to extend down.
        occupied: set[tuple[int, int]] = set()
        row = col = 0
        rows_used = 0
        for item in items:
            while (row, col) in occupied:
                col += 1
                if col == cols:
                    col, row = 0, row + 1
            span = self._span(item, unit, vspace)
            occupied.update((r, col) for r in range(row, row + span))
            rows_used = max(rows_used, row + span)
            if not test_only:
                col_width = width + (1 if col < remainder else 0)
                y = effective.y() + row * (unit + vspace)
                item.setGeometry(QRect(col_x[col], y, col_width, span * unit + (span - 1) * vspace))

        bottom = effective.y() + rows_used * (unit + vspace) - vspace
        return bottom - rect.y() + margins.bottom()

    def _smart_spacing(self) -> int:
        parent = self.parent()
        if parent is None:
            return 0
        if parent.isWidgetType():
            return parent.style().pixelMetric(parent.style().PixelMetric.PM_LayoutHorizontalSpacing, None, parent)
        return 0


class WrapLayout(QLayout):
    '''
    Lays its widgets out left to right at their own size, wrapping to a new
    row when the next one wouldn't fit - like words in a paragraph, for rows
    of chips. Unlike FlowLayout, nothing is stretched and the order reads
    across, then down.

    Its height depends on its width (heightForWidth). Its size hint uses
    its widget's fixed width when it has one, so a popup that sizes itself
    to its contents (an Overlay) gets the wrapped height up front.
    '''

    def __init__(self, parent: QWidget | None = None, spacing: int = 0):
        super().__init__(parent)
        self._items: list[QLayoutItem] = []
        self.setSpacing(spacing)
        self.setContentsMargins(QMargins(0, 0, 0, 0))

    def addItem(self, item: QLayoutItem):
        self._items.append(item)

    def insertWidget(self, index: int, widget: QWidget):
        '''Like QBoxLayout.insertWidget - so a DropZone can lay its items out with this.'''
        self.addChildWidget(widget)
        self._items.insert(max(0, min(index, len(self._items))), QWidgetItem(widget))
        self.invalidate()

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
        for item in self._items:
            size = size.expandedTo(item.minimumSize())
        parent = self.parentWidget()
        if parent is not None and parent.minimumWidth() == parent.maximumWidth():
            # The widget's own margins (padding) aren't the layout's to fill
            margins = parent.contentsMargins()
            width = parent.maximumWidth() - margins.left() - margins.right()
            size = QSize(width, self.heightForWidth(width))
        return size

    def _do_layout(self, rect: QRect, test_only: bool) -> int:
        space = self.spacing()
        x, y, row_height = rect.x(), rect.y(), 0
        for item in self._items:
            hint = item.sizeHint()
            if x > rect.x() and x + hint.width() > rect.right() + 1:
                x, y, row_height = rect.x(), y + row_height + space, 0
            if not test_only:
                item.setGeometry(QRect(QPoint(x, y), hint))
            x += hint.width() + space
            row_height = max(row_height, hint.height())
        return y + row_height - rect.y()
