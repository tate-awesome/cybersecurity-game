from PySide6.QtCore import QEvent, QObject, Qt
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout, QWidget

from ...app_core import Context
from .important_buttons import (ImportantButton, OpenSettingsPage, OpenTitlePage, OpenWorkspaceSelect, QuitApplication,
                                ShowHelpMessage, ToggleBookmark)

# How dark the page goes behind the menu (0-255)
DIM_ALPHA = 150


class _Dim(QWidget):
    '''
    The pause menu's backdrop: covers the window and dims it - the page
    keeps running underneath. A click on it (outside the menu) closes the menu.
    '''

    def __init__(self, root: QWidget, close):
        super().__init__(root)
        self.close_menu = close
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, False)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 0, 0, DIM_ALPHA))
        painter.end()

    def mousePressEvent(self, event):
        self.close_menu()


class _FollowResize(QObject):
    def __init__(self, window: QWidget, callback):
        super().__init__(window)
        self.callback = callback
        window.installEventFilter(self)

    def eventFilter(self, watched, event):
        if event.type() == QEvent.Type.Resize:
            self.callback()
        return False


class PauseMenu:
    '''
    The menu Esc (or the menu bar's home button) opens over the page: every
    "leave or jump somewhere" action in one place - the bookmark, the
    page's own links (its config's PAUSE_MENU_GROUPS buttons - see
    MenuBar.page_links), Workspaces, Title, Settings, Help and Quit - and
    what's running right now, so leaving is never blind. Esc closes it
    again, and so does clicking outside it.

    It's only a menu: nothing stops while it's open, the page just dims
    underneath. Never on a page without a menu bar (the title pages, where
    the menu is the page). Belongs to the Router, which closes it whenever
    the page changes.
    '''

    def __init__(self, context: Context):
        self.context = context
        self.root = context.root
        self.dim: _Dim | None = None
        _FollowResize(self.root, self.place)

    def is_open(self) -> bool:
        return self.dim is not None

    def page_bar(self):
        '''The current page's menu bar - None on a page without one.'''
        page = self.root.centralWidget()
        if page is None:
            return None
        from .menu_bar import MenuBar
        return next((child for child in page.findChildren(MenuBar, options=Qt.FindChildOption.FindDirectChildrenOnly)
                     if child.page_bar), None)

    def toggle(self):
        if self.is_open():
            self.close()
        else:
            self.open()

    def open(self):
        bar = self.page_bar()
        if self.is_open() or bar is None:
            return
        self.dim = _Dim(self.root, self.close)
        layout = QVBoxLayout(self.dim)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.build_card(bar), 0, Qt.AlignmentFlag.AlignCenter)
        self.place()
        self.dim.show()
        self.dim.raise_()
        self.dim.setFocus()

    def close(self):
        dim, self.dim = self.dim, None
        if dim is not None:
            try:
                dim.hide()
                dim.deleteLater()
            except RuntimeError:
                pass  # already gone with the window

    def place(self):
        if self.dim is not None:
            self.dim.setGeometry(self.root.rect())

    def label(self, key: str) -> str:
        return self.context.labels.get(f"pause_menu_{key}")

    def build_card(self, bar) -> QFrame:
        context, style = self.context, self.context.style
        card = QFrame()
        style.set_material(card, "overlay", rounded=True, outlined=True)
        rows = QVBoxLayout(card)
        rows.setContentsMargins(style.igap * 3, style.igap * 2, style.igap * 3, style.igap * 2)
        rows.setSpacing(style.igap // 2)

        title = QLabel(self.label("title"))
        title.setFont(style.get_font("page_title"))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        rows.addWidget(title)
        status = QLabel(self.running_text())
        status.setFont(style.get_font("small"))
        status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status.setWordWrap(True)
        rows.addWidget(status)
        rows.addSpacing(style.igap)

        self.row_button(ImportantButton(context, "pause_menu_resume"), rows)
        # The bookmark stays open on click - it's a toggle, not somewhere to go
        bookmark = ToggleBookmark(context)
        bookmark.LABEL, bookmark.ACTIVE_LABEL = "pause_menu_bookmark_off", "pause_menu_bookmark_on"
        bookmark.show_state()
        bookmark.setFont(style.get_font())
        rows.addWidget(bookmark)
        for button_class in bar.page_links:
            self.row_button(button_class(context), rows)
        rows.addSpacing(style.igap // 2)
        for button_class in (OpenWorkspaceSelect, OpenTitlePage, OpenSettingsPage, ShowHelpMessage):
            self.row_button(button_class(context), rows)
        rows.addSpacing(style.igap // 2)
        self.row_button(QuitApplication(context), rows)
        return card

    def row_button(self, button: ImportantButton, rows: QVBoxLayout) -> ImportantButton:
        '''A row of the menu - which closes the menu first, then does what it does.'''
        button.setFont(self.context.style.get_font())
        button.clicked.disconnect()
        button.clicked.connect(lambda checked=False: (self.close(), button.on_click()))
        rows.addWidget(button)
        return button

    def running_text(self) -> str:
        '''What's running right now - "Sniffer running · NFQ running", say - or that nothing is.'''
        running = []
        for name, process in self.context.process_manager.processes.items():
            is_running = getattr(process, "is_running", None)
            try:
                if callable(is_running) and is_running():
                    running.append(self.process_name(name))
            except Exception:
                pass  # a process in a bad state - not worth failing the menu over
        if not running:
            return self.label("nothing_running")
        return " · ".join(self.label("running").replace("{process}", name) for name in running)

    def process_name(self, key: str) -> str:
        '''A process's name: its own pause menu label, else its form's header (see BaseForm.add_header), else its key.'''
        for label in (f"pause_menu_processes_{key}", f"hacking_forms_{key}"):
            try:
                return self.context.labels.get(label)
            except KeyError:
                pass
        return key
