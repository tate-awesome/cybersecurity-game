from collections.abc import Callable

from PySide6.QtCore import QEasingCurve, QEvent, QPoint, Qt, QTimer, QVariantAnimation
from PySide6.QtGui import QColor, QPainter, QTextFrameFormat, QTextTable
from PySide6.QtWidgets import QDialog, QFrame, QHBoxLayout, QLabel, QPushButton, QTextBrowser, QVBoxLayout, QWidget
from ..app_core import Context
from ..app_core.transitions import PopupEntrance


class Scrim(QWidget):
    '''
    A dim veil over a whole window while a ModalWindow is open over it - so
    the modal stands out on any theme, however much its panel looks like
    the ones behind it. Follows the window's size. strength fades it in
    (0 to 1), along with its modal (see ModalWindow.reveal).
    '''
    COLOR = QColor(0, 0, 0, 110)

    def __init__(self, window: QWidget):
        super().__init__(window)
        self.strength = 1.0
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        window.installEventFilter(self)
        self.setGeometry(window.rect())
        self.raise_()
        self.show()

    def eventFilter(self, watched, event):
        if event.type() == QEvent.Type.Resize:
            self.setGeometry(watched.rect())
        return False

    def set_strength(self, strength: float):
        self.strength = strength
        self.update()

    def paintEvent(self, event):
        color = QColor(self.COLOR)
        color.setAlphaF(color.alphaF() * self.strength)
        painter = QPainter(self)
        painter.fillRect(self.rect(), color)
        painter.end()


class PopupWindow(QDialog):
    '''
    A window drawn like a panel instead of in the system's window frame:
    the theme's shadow and corners, a drawer with the title along its top
    (drag it to move the window), and a card inside with the message (add
    to body) and a row of buttons (see add_button) - see themes' module
    docstring. Escape closes it, like any dialog. The app stays usable
    behind it - see ModalWindow for one that blocks it.
    '''

    MIN_WIDTH = 420

    def __init__(self, master: QWidget, context: Context, title: str):
        super().__init__(master, Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        self.context = context
        self.style = context.style
        style = self.style
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
        '''After a theme change: room for its shadow (see Style.popup_shadows), then its frame (see Panel.fit_frame), and the title's padding.'''
        style = self.style
        left, top, right, bottom = style.shadow_margins(style.popup_shadows())
        frame = style.setting("panel_frame") + style.PANEL_BORDER_WIDTH
        self.drawer.setContentsMargins(left + frame, top + style.PANEL_BORDER_WIDTH, right + frame, bottom + frame)
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
        # Outlined like an overlay, so it stands apart from the page under it (see Style.floating_outline)
        paint_panel(painter, self.style, self.width(), self.height(), on_window=True, outline=self.style.floating_outline(),
                    shadows=self.style.popup_shadows())
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


class ModalWindow(PopupWindow):
    '''
    A PopupWindow that blocks the window behind it, and dims it (see Scrim)
    while it's open. A button opening one shows MODAL_MARK
    (ImportantButton.OPENS = "modal").

    It arrives as one thing, with its dimming (see reveal) - not the
    dimming at once, then the window coming in after it.
    '''

    # Like WindowReveal's: how long it stays see-through, until it's
    # painted and done sizing itself (an editor may again, just after
    # it's shown), then how long it fades in for
    REVEAL_DELAY_MS = 50
    REVEAL_MS = 160

    def __init__(self, master: QWidget, context: Context, title: str):
        super().__init__(master, context, title)
        self.setModal(True)  # block interactions with the main window
        self._scrim: Scrim | None = None
        self._reveal: QVariantAnimation | None = None

    def showEvent(self, event):
        # Sent before it's on screen, so its first frame is already see-through
        if self._scrim is None and self.parentWidget() is not None:
            self._scrim = Scrim(self.parentWidget().window())
        self.reveal()
        super().showEvent(event)

    def reveal(self):
        '''
        Keeps it and its dimming see-through for a moment, then fades them
        in together. Windows shows a new window blank, and animates it
        opening, before Qt paints it - both happen out of sight this way.
        Where window opacity doesn't work (see PopupEntrance), it just shows.
        '''
        if not PopupEntrance.supports_fade():
            return
        self.setWindowOpacity(0.0)
        if self._scrim is not None:
            self._scrim.set_strength(0.0)
        if self._reveal is not None:
            self._reveal.stop()
        animation = QVariantAnimation(self)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        # Animations off (see Performance.page_transitions) - all at once, still out of sight at first
        animation.setDuration(self.REVEAL_MS if self.context.performance.page_transitions else 0)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        animation.valueChanged.connect(self._reveal_step)
        animation.finished.connect(lambda: self._reveal_step(1.0))
        self._reveal = animation
        QTimer.singleShot(self.REVEAL_DELAY_MS, animation, animation.start)

    def _reveal_step(self, value: float):
        self.setWindowOpacity(value)
        if self._scrim is not None:
            self._scrim.set_strength(value)

    def hideEvent(self, event):
        if self._reveal is not None:
            self._reveal.stop()
            self._reveal = None
        if self._scrim is not None:
            self._scrim.deleteLater()
            self._scrim = None
        super().hideEvent(event)


class ButtonModal(ModalWindow):
    '''
    A modal for an editor too big for an Overlay, which drops out of its
    button and can run off the screen: centered over the main window
    instead, with a Close button. Made afresh by its button's click - fill
    body, then show it - and deleted once closed.
    '''

    def __init__(self, context: Context, title: str):
        super().__init__(context.root, context, title)
        self.add_button(context.labels.get("modal_close"), self.accept)
        self.finished.connect(lambda *_: self.deleteLater())

    def show(self):
        self.fit_contents()  # first - or show() would adjustSize (see fit_contents)
        super().show()

    def fit_contents(self):
        '''
        Sizes it to its contents, as far as the screen goes - after they
        change, too, around the same middle (so it doesn't jump to one
        side), back onto the screen if that grew it past an edge. Not
        adjustSize, which caps a window at 2/3 of the screen, cutting a
        wide editor off.
        '''
        screen = self.screen().availableGeometry()
        width = min(self.sizeHint().width(), screen.width())
        height = self.heightForWidth(width) if self.hasHeightForWidth() else self.sizeHint().height()
        middle = self.geometry().center()
        self.resize(width, min(max(height, self.minimumSizeHint().height()), screen.height()))
        if self.isVisible():
            x, y = middle.x() - self.width() // 2, middle.y() - self.height() // 2
            self.move(max(screen.left(), min(x, screen.right() - self.width())),
                      max(screen.top(), min(y, screen.bottom() - self.height())))


class MarkdownModal(ButtonModal):
    '''
    A ButtonModal reading out a markdown document - a status toast's report,
    or an error's fix (see toasts.open_notice) - scrolling past
    HEIGHT of the window. Its links open in the browser.
    '''

    WIDTH = 620
    HEIGHT = 0.7
    # Room around a table's cells - Qt's markdown leaves them touching
    CELL_PADDING = 6

    def __init__(self, context: Context, title: str, markdown: str):
        super().__init__(context, title)
        style = context.style
        browser = QTextBrowser()
        browser.setOpenExternalLinks(True)
        browser.setFont(style.get_font())
        browser.setFrameShape(QFrame.Shape.NoFrame)
        style.live_style(browser, lambda: f"QTextBrowser {{ background: transparent; border: none; color: {style.color('text')}; }}")
        browser.setMarkdown(markdown)
        for frame in browser.document().rootFrame().childFrames():
            if isinstance(frame, QTextTable):
                table = frame.format()
                table.setCellPadding(self.CELL_PADDING)
                table.setCellSpacing(0)
                table.setBorderStyle(QTextFrameFormat.BorderStyle.BorderStyle_None)
                frame.setFormat(table)
        document = browser.document()
        document.setTextWidth(self.WIDTH)
        height = int(document.size().height()) + 2 * int(document.documentMargin())
        browser.setFixedSize(self.WIDTH + browser.verticalScrollBar().sizeHint().width(),
                             min(height, int(context.root.height() * self.HEIGHT)))
        self.body.addWidget(browser)


def message(master: QWidget, context: Context, message: str):
        window = ModalWindow(master, context, "Help")
        window.add_text(message)
        window.add_button("Dismiss", window.accept)
        window.show()
        return window

def confirm_dialog(master: QWidget, context: Context, message: str, confirm_text: str, cancel_text: str, confirm_func):
        '''
        A modal yes/no dialog: shows message, and calls confirm_func only if
        the user presses the confirm_text button.
        '''
        window = ModalWindow(master, context, "Confirm")
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
