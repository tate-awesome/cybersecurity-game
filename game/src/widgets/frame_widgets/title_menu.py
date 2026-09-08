from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QLabel, QPushButton, QWidget
from ...app_core import Context
from typing import Callable

class TitleMenu(QWidget):
    '''
    The main Widget for the title menu.
    Comes with a title and has a button maker.
    '''

    def __init__(self, master: QWidget, context: Context, title_label: str = "_default"):
        super().__init__(master)
        self.context = context
        self.style = context.style
        title_text = self.context.labels.get("title_text", title_label)

        master.layout().addWidget(self)

        self.grid = QGridLayout(self)
        self.setLayout(self.grid)

        self.current_row = 1

        title_widget = QLabel(title_text)
        title_widget.setFont(self.style.get_font("title"))
        title_widget.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.grid.addWidget(title_widget, self.current_row, 1)
        self.grid.setRowMinimumHeight(self.current_row, self.style.gap2[1])
        self.current_row = self.current_row + 1

        self.grid.setColumnStretch(0, 1)
        self.grid.setColumnStretch(1, 0)
        self.grid.setColumnStretch(2, 1)

        self.grid.setRowStretch(0, 1)
        self.grid.setRowStretch(1, 0)
        self.grid.setRowStretch(2, 1)

    def button(self, label: str = "_default", function: Callable | None = None):
        button = QPushButton(self.context.labels.get("title_buttons", label))
        button.setFont(self.style.get_font("title_btn"))
        if function is not None:
            # clicked emits a "checked" bool that callers here don't expect
            # (they're all zero-arg callables) - dropping it here means a
            # navigate callback's own default-valued "target" argument
            # doesn't get silently clobbered by it.
            button.clicked.connect(lambda checked=False, function=function: function())
        # No alignment flag here means "fill" - QGridLayout stretches the
        # button to the column's width, and since the title label shares
        # that same column, every button ends up as wide as the title text.
        # AlignHCenter switches to the button's own sizeHint width (title
        # text plus QPushButton's padding: 6px 12px from style.py), centered
        # in the column instead of stretched across it.
        self.grid.addWidget(button, self.current_row, 1, Qt.AlignmentFlag.AlignHCenter)
        self.grid.setRowStretch(self.current_row, 0)
        self.current_row = self.current_row + 1
        self.grid.setRowStretch(self.current_row, 1)