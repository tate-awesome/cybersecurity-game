from collections.abc import Callable

from PySide6.QtCore import QPoint, Qt, QTimer
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QDialog, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget
from ..app_core import Context
from ..app_core.context.style import PANEL_BORDER_WIDTH


class PopupWindow(QDialog):
    '''
    A modal popup window drawn like a panel instead of in the system's
    window frame: the theme's shadow and corners, a drawer with the title
    along its top (drag it to move the window), and a card inside with the
    message (add to body) and a row of buttons (see add_button) - see
    themes' module docstring. Escape closes it, like any dialog.
    '''

    MIN_WIDTH = 420

    def __init__(self, master: QWidget, context: Context, title: str):
        super().__init__(master, Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        self.context = context
        self.style = context.style
        style = self.style
        self.setModal(True)  # block interactions with the main window
        self.setWindowTitle(title)
        # Only what paintEvent draws - the shadow's room stays see-through
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("QDialog { background: transparent; border: none; }")
        self.setMinimumWidth(self.MIN_WIDTH)
        self._drag_from: QPoint | None = None

        self.drawer = QVBoxLayout(self)
        self.drawer.setSpacing(0)

        self.title = QLabel(title)
        self.title.setFont(style.get_font("title_btn"))
        style.live_style(self.title, lambda: f"QLabel {{ color: {style.color('menu_bar_text')}; }}")
        self.drawer.addWidget(self.title)

        card = QWidget()
        style.set_material(card, "card")
        self.drawer.addWidget(card, 1)
        inside = QVBoxLayout(card)
        inside.setContentsMargins(style.igap * 2, style.igap * 2, style.igap * 2, style.igap * 2)
        inside.setSpacing(style.igap * 2)
        self.body = QVBoxLayout()
        self.body.setSpacing(style.igap)
        inside.addLayout(self.body, 1)
        self.buttons = QHBoxLayout()
        self.buttons.addStretch(1)
        inside.addLayout(self.buttons)

        self.fit()
        style.signals.changed.connect(self.fit)

    def fit(self):
        '''After a theme change: room for its shadow, then its frame (see Panel.fit_frame), and the title's padding.'''
        style = self.style
        left, top, right, bottom = style.panel_margins()
        frame = style.setting("panel_frame") + PANEL_BORDER_WIDTH
        self.drawer.setContentsMargins(left + frame, top + PANEL_BORDER_WIDTH, right + frame, bottom + frame)
        self.title.setContentsMargins(max(0, style.igap * 2 - frame), style.igap, style.igap, style.igap)
        self.update()

    def add_text(self, text: str) -> QLabel:
        '''A wrapped paragraph in the card.'''
        label = QLabel(text)
        label.setFont(self.style.get_font())
        label.setWordWrap(True)
        self.body.addWidget(label)
        return label

    def add_button(self, text: str, clicked: Callable[[], None]) -> QPushButton:
        '''A button along the card's bottom, right-aligned, in the order added.'''
        button = QPushButton(text)
        button.setFont(self.style.get_font())
        button.clicked.connect(clicked)
        self.buttons.addWidget(button)
        return button

    def paintEvent(self, event):
        from .panels.panel import paint_panel  # here - panels import this package
        painter = QPainter(self)
        paint_panel(painter, self.style, self.width(), self.height(), on_window=True)
        painter.end()

    # Moved by its title, as there's no system frame to drag
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and event.position().y() <= self.title.geometry().bottom():
            self._drag_from = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._drag_from is not None:
            self.move(event.globalPosition().toPoint() - self._drag_from)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self._drag_from = None
        super().mouseReleaseEvent(event)


def message(master: QWidget, context: Context, message: str):
        window = PopupWindow(master, context, "Help")
        window.add_text(message)
        window.add_button("Dismiss", window.accept)
        window.show()
        return window

def confirm_dialog(master: QWidget, context: Context, message: str, confirm_text: str, cancel_text: str, confirm_func):
        '''
        A modal yes/no dialog: shows message, and calls confirm_func only if
        the user presses the confirm_text button.
        '''
        window = PopupWindow(master, context, "Confirm")
        window.add_text(message)

        def confirm():
            # Closed (and the main window unblocked) before the action runs -
            # an action that rebuilds the page, changes the window or raises
            # can't leave this modal dialog blocking the app
            window.accept()
            QTimer.singleShot(0, confirm_func)

        window.add_button(confirm_text, confirm)
        window.add_button(cancel_text, window.reject)
        window.show()
        return window

def quit_dialog(master: QWidget, context: Context, quit_func):
        message = "Are you sure you want to quit?\nNothing will be saved."
        return confirm_dialog(master, context, message, "Yes, quit", "No, continue", quit_func)
