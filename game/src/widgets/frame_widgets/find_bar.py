from PySide6.QtCore import QEvent, QPoint, QRect, Qt
from PySide6.QtGui import QKeySequence, QShortcut, QTextCursor
from PySide6.QtWidgets import (QCheckBox, QComboBox, QFrame, QHBoxLayout, QLabel, QLineEdit, QPlainTextEdit,
                               QPushButton, QScrollArea, QTabWidget, QTextBrowser, QTreeWidget, QWidget)
import shiboken6

from ...app_core import Context


class FindField(QLineEdit):
    '''
    The find bar's text box. Claims Enter, Shift+Enter and Escape for itself
    while it has focus - otherwise the window-wide Escape shortcut (exit
    fullscreen, see KeyBinds) would take Escape before it got here.
    '''

    def __init__(self, bar: "FindBar"):
        super().__init__()
        self.bar = bar

    def event(self, event):
        if event.type() == QEvent.Type.ShortcutOverride and event.key() in (Qt.Key.Key_Escape, Qt.Key.Key_Return, Qt.Key.Key_Enter):
            event.accept()
            return True
        return super().event(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.bar.close_bar()
        elif event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.bar.step(-1 if event.modifiers() & Qt.KeyboardModifier.ShiftModifier else 1)
        else:
            super().keyPressEvent(event)


class FindBar(QFrame):
    '''
    Ctrl+F search across every tab of a QTabWidget, like a browser's find
    bar: type to jump to the first match, Enter / Shift+Enter (or Next /
    Previous) to step through them, Escape to close. Matches text in labels,
    checkboxes, text boxes (every occurrence), dropdowns and tree items that
    are showing - not buttons. Going to a match switches to its tab, scrolls
    it into view and outlines it (selecting the text, inside a text box).
    '''

    def __init__(self, page: QWidget, context: Context, tabs: QTabWidget):
        super().__init__(page)
        self.context = context
        self.style = context.style
        self.tabs = tabs
        self.matches: list[tuple] = []
        self.index = -1
        self.outline: QFrame | None = None

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(self.style.igap)
        label = QLabel("Find")
        label.setFont(self.style.get_font("default"))
        layout.addWidget(label)
        self.field = FindField(self)
        self.field.setFont(self.style.get_font("default"))
        self.field.setPlaceholderText("Search this page")
        self.field.textChanged.connect(lambda _: self.search(restart=True))
        layout.addWidget(self.field, 1)
        self.count = QLabel()
        self.count.setFont(self.style.get_font("default"))
        self.count.setMinimumWidth(120)
        layout.addWidget(self.count)
        for text, handler in (("Previous", lambda: self.step(-1)), ("Next", lambda: self.step(1)), ("Close", self.close_bar)):
            button = QPushButton(text)
            button.setFont(self.style.get_font("small"))
            button.clicked.connect(lambda checked=False, handler=handler: handler())
            layout.addWidget(button)
        self.hide()

        shortcut = QShortcut(QKeySequence(QKeySequence.StandardKey.Find), page)
        shortcut.setContext(Qt.ShortcutContext.WidgetWithChildrenShortcut)
        shortcut.activated.connect(self.open_bar)

    # Showing and hiding
    def open_bar(self):
        self.show()
        self.field.setFocus()
        self.field.selectAll()
        self.search(restart=True)

    def close_bar(self):
        self.clear_outline()
        self.hide()
        self.tabs.setFocus()

    # Searching
    def search(self, restart: bool = False):
        self.matches = self.collect()
        if restart or not 0 <= self.index < len(self.matches):
            self.index = 0 if self.matches else -1
        self.show_match()

    def step(self, direction: int):
        self.matches = self.collect()
        if not self.matches:
            self.index = -1
        else:
            self.index = (self.index + direction) % len(self.matches)
        self.show_match()

    def collect(self) -> list[tuple]:
        '''
        Every showing match on every tab, in reading order: (tab, widget, where),
        where is a character position in a text box, a tree item, or None.
        '''
        needle = self.field.text().lower()
        if not needle:
            return []
        found = []
        for tab in range(self.tabs.count()):
            page = self.tabs.widget(tab)
            for widget in page.findChildren(QWidget):
                if not widget.isVisibleTo(page) or isinstance(widget, (QPushButton, QTextBrowser)):
                    continue
                corner = widget.mapTo(page, QPoint(0, 0))
                order = (tab, corner.y(), corner.x())
                if isinstance(widget, QTreeWidget):
                    for row, item in enumerate(self.tree_items(widget)):
                        if needle in item.text(0).lower():
                            found.append((order + (row,), tab, widget, item))
                elif isinstance(widget, (QLineEdit, QPlainTextEdit)):
                    if widget.parent() is not None and isinstance(widget.parent(), QComboBox):
                        continue
                    text = (widget.text() if isinstance(widget, QLineEdit) else widget.toPlainText()).lower()
                    start = text.find(needle)
                    while start != -1:
                        found.append((order + (start,), tab, widget, start))
                        start = text.find(needle, start + 1)
                else:
                    text = ""
                    if isinstance(widget, (QLabel, QCheckBox)):
                        text = widget.text()
                    elif isinstance(widget, QComboBox):
                        text = widget.currentText()
                    if needle in text.lower():
                        found.append((order + (0,), tab, widget, None))
        found.sort(key=lambda match: match[0])
        return [match[1:] for match in found]

    @staticmethod
    def tree_items(tree: QTreeWidget) -> list:
        '''Every item in tree, top to bottom.'''
        items = []
        def walk(item):
            items.append(item)
            for index in range(item.childCount()):
                walk(item.child(index))
        for index in range(tree.topLevelItemCount()):
            walk(tree.topLevelItem(index))
        return items

    # Showing a match
    def show_match(self):
        self.clear_outline()
        if not self.field.text():
            self.count.setText("")
            return
        if self.index < 0:
            self.count.setText("No matches")
            self.count.setStyleSheet(f"color: {self.style.color('red')};")
            return
        self.count.setText(f"{self.index + 1} of {len(self.matches)}")
        self.count.setStyleSheet("")
        tab, widget, where = self.matches[self.index]
        self.tabs.setCurrentIndex(tab)
        for scroll in self.scroll_areas(widget):
            scroll.ensureWidgetVisible(widget, 50, 120)
        length = len(self.field.text())

        if isinstance(where, int) and isinstance(widget, QPlainTextEdit):
            cursor = widget.textCursor()
            cursor.setPosition(where)
            cursor.setPosition(where + length, QTextCursor.MoveMode.KeepAnchor)
            widget.setTextCursor(cursor)
            widget.ensureCursorVisible()
            start = widget.textCursor()
            start.setPosition(where)
            rect = widget.cursorRect(start)
            width = widget.fontMetrics().horizontalAdvance(widget.toPlainText()[where:where + length])
            self.draw_outline(widget.viewport(), QRect(rect.left(), rect.top(), width, rect.height()))
        elif isinstance(where, int) and isinstance(widget, QLineEdit):
            widget.setSelection(where, length)
            self.outline_widget(widget)
        elif isinstance(widget, QTreeWidget):
            widget.scrollToItem(where)
            self.draw_outline(widget.viewport(), widget.visualItemRect(where))
        else:
            self.outline_widget(widget)

    @staticmethod
    def scroll_areas(widget: QWidget) -> list[QScrollArea]:
        '''The scroll areas holding widget, innermost first.'''
        areas = []
        parent = widget.parentWidget()
        while parent is not None:
            if isinstance(parent, QScrollArea):
                areas.append(parent)
            parent = parent.parentWidget()
        return areas

    def outline_widget(self, widget: QWidget):
        '''
        Outlines widget from its parent (an outline inside it would have its
        edges clipped). Labels and checkboxes often stretch across a whole
        row, so theirs hugs just their text.
        '''
        rect = widget.geometry()
        if isinstance(widget, (QLabel, QCheckBox)):
            rect.setWidth(min(rect.width(), widget.sizeHint().width()))
        self.draw_outline(widget.parentWidget(), rect)

    def draw_outline(self, parent: QWidget, rect: QRect):
        self.outline = QFrame(parent)
        self.outline.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.outline.setStyleSheet(f"QFrame {{ border: 2px solid {self.style.color('accent')}; background: transparent; border-radius: 3px; }}")
        self.outline.setGeometry(rect.adjusted(-3, -2, 3, 2))
        self.outline.show()
        self.outline.raise_()

    def clear_outline(self):
        if self.outline is not None and shiboken6.isValid(self.outline):
            self.outline.deleteLater()
        self.outline = None
