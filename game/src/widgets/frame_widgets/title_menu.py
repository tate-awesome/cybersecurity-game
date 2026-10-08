from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QLabel, QWidget
from ...app_core import Context
from .important_buttons import ImportantButton

class TitleMenu(QWidget):
    '''
    The main Widget for the title menu.
    Comes with a title and has a button maker.
    '''

    def __init__(self, master: QWidget, context: Context, title_label: str = "_default"):
        super().__init__(master)
        self.context = context
        self.style = context.style
        title_text = self.context.labels.get(f"title_text_{title_label}")

        master.layout().addWidget(self)

        self.grid = QGridLayout(self)
        self.setLayout(self.grid)

        self.current_row = 1
        # The title, then each button - in order, for the page's entrance (see TitlePage.appear_targets)
        self.items: list[QWidget] = []

        title_widget = QLabel(title_text)
        title_widget.setFont(self.style.get_font("title"))
        title_widget.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.grid.addWidget(title_widget, self.current_row, 1)
        self.items.append(title_widget)
        self.grid.setRowMinimumHeight(self.current_row, self.style.gap2[1])
        self.current_row = self.current_row + 1

        self.grid.setColumnStretch(0, 1)
        self.grid.setColumnStretch(1, 0)
        self.grid.setColumnStretch(2, 1)

        self.grid.setRowStretch(0, 1)
        self.grid.setRowStretch(1, 0)
        self.grid.setRowStretch(2, 1)

    def add_important(self, button_class: type[ImportantButton], *args) -> ImportantButton | None:
        '''
        Adds an important button (see important_buttons) as the next row -
        args are passed through to its constructor after context. Returns
        the button, or None if it isn't available right now (see is_available).
        '''
        if not button_class.is_available(self.context):
            return None
        button = button_class(self.context, *args)
        button.setFont(self.style.get_font("title_btn"))
        # No alignment flag here means "fill" - QGridLayout stretches the
        # button to the column's width, and since the title label shares
        # that same column, every button ends up as wide as the title text.
        # AlignHCenter switches to the button's own sizeHint width (title
        # text plus QPushButton's padding: 6px 12px from style.py), centered
        # in the column instead of stretched across it.
        self.grid.addWidget(button, self.current_row, 1, Qt.AlignmentFlag.AlignHCenter)
        self.items.append(button)
        self.grid.setRowStretch(self.current_row, 0)
        self.current_row = self.current_row + 1
        self.grid.setRowStretch(self.current_row, 1)
        return button
