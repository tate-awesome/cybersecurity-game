from ...app_core import Context
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QScrollArea, QWidget

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
        self.setStyleSheet(f"QScrollArea {{ background-color: {style.color('panel')}; border: none; }}")
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.inner = QWidget()
        # A plain QWidget doesn't paint a stylesheet background at all by
        # default (unlike QFrame/QScrollArea, which do) - see Panel/
        # BaseForm for the same fix and the full explanation.
        self.inner.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.inner.setStyleSheet(style.themed(f"background-color: {style.color('panel')};", self.inner))
        self.grid_layout = QGridLayout(self.inner)
        # Without explicit values here, stacked rows (forms, strip charts,
        # etc.) fall back to Qt's default layout spacing, which is roughly
        # zero once each row is its own full-width widget - they end up
        # welded edge-to-edge with no panel-colored gap to separate them.
        self.grid_layout.setContentsMargins(style.igap, style.igap, style.igap, style.igap)
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
