from PySide6.QtCore import QEasingCurve, QEvent, QObject, QRect, Qt, QTimer, QVariantAnimation
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QGridLayout, QLabel, QWidget
from ...app_core import Context
from .important_buttons import ImportantButton

class TitleMenu(QWidget):
    '''
    The main Widget for the title menu.
    Comes with a title and has a button maker.

    Sits against the left edge of the page, vertically centered: column 0
    is a left margin that scales with the width (see resizeEvent), column
    1 holds the title and buttons, and column 2 soaks up the rest.
    '''

    # Left margin as a fraction of the menu's width, and its floor in px
    LEFT_MARGIN = 0.08
    MIN_LEFT_MARGIN = 40

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
        title_widget.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)
        self.grid.addWidget(title_widget, self.current_row, 1)
        self.items.append(title_widget)
        self.grid.setRowMinimumHeight(self.current_row, self.style.gap2[1])
        self.current_row = self.current_row + 1

        self.grid.setColumnStretch(0, 0)
        self.grid.setColumnStretch(1, 0)
        self.grid.setColumnStretch(2, 1)

        self.grid.setRowStretch(0, 1)
        self.grid.setRowStretch(1, 0)
        self.grid.setRowStretch(2, 1)

    def resizeEvent(self, event):
        self.grid.setColumnMinimumWidth(0, max(self.MIN_LEFT_MARGIN, round(self.width() * self.LEFT_MARGIN)))
        super().resizeEvent(event)

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
        # AlignLeft switches to the button's own sizeHint width (title
        # text plus QPushButton's padding: 6px 12px from style.py), lined
        # up under the title's left edge instead of stretched across it.
        self.grid.addWidget(button, self.current_row, 1, Qt.AlignmentFlag.AlignLeft)
        self.items.append(button)
        self.grid.setRowStretch(self.current_row, 0)
        self.current_row = self.current_row + 1
        self.grid.setRowStretch(self.current_row, 1)
        return button

    def add_beside(self, anchor: QWidget, button: QWidget) -> "GrowingButton":
        '''Puts button just right of anchor (the row's button), growing to its full text on hover - see GrowingButton.'''
        button.setFont(self.style.get_font("title_btn"))
        beside = GrowingButton(self, anchor, button)
        # Arrives with its row in the page's entrance
        self.items.insert(self.items.index(anchor) + 1, button)
        return beside


class GrowingButton(QObject):
    '''
    Keeps a button just to the right of another one (its anchor) - short,
    showing button.short_text - and grows it to the right, revealing its
    full text, while the mouse is over the anchor, the button, or the gap
    between them; it shrinks back when the mouse leaves. The text is
    left-aligned, so growing reveals the rest of it rather than sliding
    it around.
    '''

    GAP = 10           # px between the anchor and the button
    GROW_MS = 300

    def __init__(self, menu: QWidget, anchor: QWidget, button: QWidget):
        super().__init__(menu)
        self.menu = menu
        self.anchor = anchor
        self.button = button
        self.short_text = getattr(button, "short_text", button.text())
        self.full_text = button.text()
        button.setParent(menu)
        button.setStyleSheet(menu.style.themed("QPushButton { text-align: left; }"))
        button.setText(self.short_text)
        self.short_width = button.sizeHint().width()
        button.setText(self.full_text)
        self.full_width = button.sizeHint().width()
        button.setText(self.short_text)
        button.show()
        self.amount = 0.0   # 0 short, 1 full
        self.target = 0.0

        self.animation = QVariantAnimation(self)
        # Eases in and out - starts gently, speeds up, settles gently
        self.animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.animation.valueChanged.connect(self.set_amount)
        self.animation.finished.connect(self.settle_text)

        # Hover is judged from the cursor's position whenever it enters or
        # leaves either button - a moment later, so crossing from one into
        # the other (over the gap) doesn't count as leaving
        self.hover_check = QTimer(self)
        self.hover_check.setSingleShot(True)
        self.hover_check.setInterval(30)
        self.hover_check.timeout.connect(self.update_hover)
        for watched in (anchor, button):
            watched.installEventFilter(self)
        self.place()

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        kind = event.type()
        if kind in (QEvent.Type.Enter, QEvent.Type.Leave):
            self.hover_check.start()
        elif watched is self.anchor and kind in (QEvent.Type.Move, QEvent.Type.Resize, QEvent.Type.Show):
            self.place()
        return False

    def place(self):
        anchor = self.anchor.geometry()
        height = self.button.sizeHint().height()
        width = round(self.short_width + (self.full_width - self.short_width) * self.amount)
        self.button.setGeometry(anchor.right() + 1 + self.GAP, anchor.top() + (anchor.height() - height) // 2, width, height)

    def set_amount(self, amount: float):
        self.amount = amount
        self.place()

    def settle_text(self):
        # Fully shrunk, the short text alone - the full one would peek into the padding
        self.button.setText(self.full_text if self.amount > 0 else self.short_text)

    def update_hover(self):
        '''Grown while the cursor is over the anchor, the button, or the gap between them.'''
        cursor = self.menu.mapFromGlobal(QCursor.pos())
        anchor = self.anchor.geometry()
        reach = QRect(anchor.left(), anchor.top(), self.button.geometry().right() - anchor.left() + 1, anchor.height())
        self.grow(1.0 if reach.contains(cursor) or self.button.geometry().contains(cursor) else 0.0)

    def grow(self, target: float):
        if target == self.target:
            return
        self.target = target
        if target > 0:
            self.button.setText(self.full_text)
        start = self.amount
        duration = max(1, round(self.GROW_MS * abs(target - start)))
        # Reconfiguring a finished animation makes it emit its stale end
        # value straight away - which would snap amount to the target (and
        # every grow after the first would be instant) - so set it up silently
        self.animation.stop()
        self.animation.blockSignals(True)
        self.animation.setStartValue(start)
        self.animation.setEndValue(target)
        self.animation.setDuration(duration)
        self.animation.setCurrentTime(0)
        self.animation.blockSignals(False)
        self.animation.start()
