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

        master.layout().addWidget(self)
        self.setStyleSheet(f"QScrollArea {{ background-color: {style.color('panel')}; border: none; }}")
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.inner = QWidget()
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

        if not height == -1:
            self.setFixedHeight(height)

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
