from ...app_core import Context
from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QPainter, QRegion
from PySide6.QtWidgets import QGridLayout, QScrollArea, QWidget


class _Gaps(QWidget):
    '''
    A scroll area's content in a panel's drawer: the deepest material
    ("field") only where nothing is - between and around its cards - so
    the cards sit straight on the drawer like any other content, rather
    than on top of it, where a see-through card would come out deeper
    than the gaps (see themes' module docstring).
    '''

    def __init__(self, style):
        super().__init__()
        self.style = style
        style.signals.changed.connect(self.update)

    def paintEvent(self, event):
        gaps = QRegion(self.rect())
        for child in self.children():
            if isinstance(child, QWidget) and child.isVisible():
                gaps = gaps.subtracted(QRegion(child.geometry()))
        painter = QPainter(self)
        painter.setClipRegion(gaps)
        painter.fillRect(self.rect(), self.style.brush("field", QRectF(self.rect())))
        painter.end()

class Scrollable(QScrollArea):
    '''
    Vertically scrollable frame. Inherits QScrollArea, which handles mouse
    wheel scrolling natively (including only scrolling when content
    overflows the viewport) - none of the manual wheel-binding customtkinter
    needed applies here.
    '''

    def __init__(self, master: QWidget, context: Context, height: int = -1, fill = "both", expand=True):
        super().__init__(master)
        self.context = context
        style = context.style
        self.style = style

        # Stretch 1 so this claims all leftover space over Panel's trailing
        # filler widget (see panel.py) - Qt distributes leftover strictly by
        # relative stretch factor, so without this a same-stretch (0) filler
        # can end up winning space this should have gotten instead.
        master.layout().addWidget(self, 1)
        # In a panel's drawer, its cards sit edge to edge with the drawer's
        # frame, with the deepest material only between them (see _Gaps).
        # Elsewhere, it's a panel of its own.
        self.in_panel = master.property("material") == "panel"
        style.set_material(self, "none" if self.in_panel else "panel")
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.inner = _Gaps(style) if self.in_panel else QWidget()
        style.set_material(self.inner, "none" if self.in_panel else "panel")
        self.grid_layout = QGridLayout(self.inner)
        # Without explicit values here, stacked rows (forms, strip charts,
        # etc.) fall back to Qt's default layout spacing, which is roughly
        # zero once each row is its own full-width widget - they end up
        # welded edge-to-edge with no gap to separate them.
        margin = 0 if self.in_panel else style.igap
        self.grid_layout.setContentsMargins(margin, margin, margin, margin)
        self.grid_layout.setVerticalSpacing(style.igap)
        self.grid_layout.setHorizontalSpacing(style.igap)
        self.setWidget(self.inner)

        # The vertical scrollbar (ScrollBarAsNeeded, the default we don't
        # override) already reads as its own bit of right-edge padding once
        # it's showing, so the full igap margin on top of it looks like too
        # much space - 2px instead keeps content from sitting flush against
        # the scrollbar. Without a scrollbar there's nothing providing that
        # separation, so it falls back to the normal igap. rangeChanged
        # fires exactly when scrolling becomes possible/impossible (its
        # min/max span is what ScrollBarAsNeeded itself keys visibility off
        # of), which covers content being added/removed/hidden/shown after
        # construction, not just this initial layout.
        self.verticalScrollBar().rangeChanged.connect(self._update_right_margin)
        self._update_right_margin(self.verticalScrollBar().minimum(), self.verticalScrollBar().maximum())

        if not height == -1:
            self.setFixedHeight(height)

    def _update_right_margin(self, min_value: int, max_value: int):
        margins = self.grid_layout.contentsMargins()
        right = 0 if max_value > min_value else self.style.igap
        self.grid_layout.setContentsMargins(margins.left(), margins.top(), right, margins.bottom())

    def columnconfigure(self, index: int, weight: int):
        self.grid_layout.setColumnStretch(index, weight)

    def add_deadspace(self, type: str = "grid", height: float | int = 100):
        '''
        Reserves empty space below the last row of content so it doesn't
        sit flush against the bottom of the scroll area. Only "grid" is
        used by anything converted so far - giving a trailing row a
        stretch factor achieves the same thing a spacer frame did, without
        needing to know how many rows are already in use.
        '''
        self.grid_layout.setRowStretch(999, 1)

    def top(self):
        self.verticalScrollBar().setValue(0)
