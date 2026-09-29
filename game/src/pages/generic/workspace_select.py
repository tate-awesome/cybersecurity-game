from pathlib import Path

from PySide6.QtCore import QEvent, QObject, Qt, QUrl, Signal
from PySide6.QtGui import QColor, QImage, QTextDocument
from PySide6.QtWidgets import QButtonGroup, QFrame, QHBoxLayout, QPushButton, QSizePolicy, QTextBrowser, QVBoxLayout, QWidget

from ...app_core import Context
from ...widgets import Scrollable, popup
from ..page import Page


class NoteBrowser(QTextBrowser):
    '''
    Read-only markdown view for a workspace's _note. Relative image paths
    (e.g. "screenshot.png") resolve against the workspace's own folder via
    searchPaths, and images are scaled down to fit the viewport so a
    full-size screenshot doesn't force horizontal scrolling.
    '''

    def loadResource(self, type: int, name: QUrl):
        resource = super().loadResource(type, name)
        if type == QTextDocument.ResourceType.ImageResource.value and resource is not None:
            image = QImage.fromData(resource) if not isinstance(resource, QImage) else resource
            # Leave room for the margins and a vertical scrollbar that may
            # only appear once the image itself is laid out.
            max_width = self.viewport().width() - 4 * int(self.document().documentMargin()) - self.verticalScrollBar().sizeHint().width()
            if not image.isNull() and max_width > 0 and image.width() > max_width:
                return image.scaledToWidth(max_width, Qt.TransformationMode.SmoothTransformation)
            return image
        return resource


class WorkspaceButton(QPushButton):
    '''A sidebar workspace button that also reports double-clicks, to open a workspace directly.'''

    doubleClicked = Signal()

    def mouseDoubleClickEvent(self, event):
        self.doubleClicked.emit()
        event.accept()


class WorkspaceSelectPage(Page):
    '''
    Page constructor for build_type "workspace_select". Everything floats on
    the page's (optional) procedural background:

      - a transparent MenuBar on top, titled by config["title"] with
        config["menu_bar"]'s buttons
      - a transparent scrollable sidebar on the left of collapsible
        sections, one per config["sections"] entry, each listing the
        workspaces whose "category" matches it - every page directly inside
        the config["link_folder"] folder with "include": 1, sorted by
        their "order"
      - the summary area filling the rest

    With nothing selected, the summary area shows this page's own "_note"
    straight on the background. Clicking a workspace shows that
    workspace's config.json "_note" (markdown) on an opaque box instead,
    with Delete Saved Data and Open Workspace buttons pinned to the box's
    bottom-right corner - they stay put while the summary scrolls under
    them. Double-clicking a workspace opens it immediately.

    A _note can be one string or a list of markdown blocks, joined with
    blank lines between them.
    '''

    SIDEBAR_WIDTH = 380

    def __init__(self, context: Context):
        super().__init__(context)
        self.labels = context.labels

        key = context.router.current_page
        config = context.pages.load_page_config(key)
        self.default_note = self.join_note(config.get("_note", ""))
        self.default_folder = context.paths.pages / key
        self.selected_target: str | None = None
        self.workspaces = context.pages.pages_in(config.get("link_folder", "workspaces"))

        self.add_background(config)

        menu_bar = self.build_menu_bar(config.get("title", "_default"), config.get("menu_bar", []))
        menu_bar.setStyleSheet(self.style.themed("background-color: transparent;", menu_bar))

        body = QHBoxLayout()
        body.setSpacing(self.style.igap)
        self.layout().addLayout(body, 1)

        sidebar = QWidget()
        sidebar.setFixedWidth(self.SIDEBAR_WIDTH)
        sidebar.setLayout(QVBoxLayout())
        sidebar.layout().setContentsMargins(0, 0, 0, 0)
        body.addWidget(sidebar)
        self.scrollable = Scrollable(sidebar, context)
        self.scrollable.columnconfigure(0, 1)
        self.scrollable.setStyleSheet("QScrollArea { background-color: transparent; border: none; }")
        self.scrollable.viewport().setAutoFillBackground(False)
        self.scrollable.inner.setStyleSheet(self.style.themed("background-color: transparent;", self.scrollable.inner))

        self.build_summary(body)

        self.workspace_group = QButtonGroup(self)
        self.workspace_group.setExclusive(True)
        row = 0
        for section in config.get("sections", []):
            row = self.build_section(section, row)
        self.scrollable.add_deadspace()

        self.show_note(self.default_note, self.default_folder)

    # Sidebar
    def build_section(self, section: dict, row: int) -> int:
        '''
        Adds one collapsible section (header button + workspace buttons) to
        the sidebar starting at the given grid row, and returns the next
        free row. "numbered" prefixes each workspace with its position, so
        the default note can point students at e.g. "Defender Lesson 1".
        '''
        title = self.labels.get(f'title_buttons_{section.get("label", "_default")}')
        workspaces = self.workspaces_in(section.get("category"))
        numbered = section.get("numbered", False)

        header = QPushButton()
        header.setCheckable(True)
        header.setChecked(section.get("expanded", True))
        header.setFont(self.style.get_font("title_btn"))
        hover = self.translucent(self.style.color("widget"), 0.6)
        header.setStyleSheet(self.style.themed(
            f"QPushButton {{ text-align: left; background-color: transparent; color: {self.style.color('text')}; }}"
            f"QPushButton:hover, QPushButton:pressed {{ background-color: {hover}; }}"
        ))
        header.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Fixed)
        self.scrollable.grid_layout.addWidget(header, row, 0)

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(self.style.igap, 0, 0, 0)
        content_layout.setSpacing(self.style.cgap * 2)
        self.scrollable.grid_layout.addWidget(content, row + 1, 0)

        for i, (label, target) in enumerate(workspaces, start=1):
            # "&" would otherwise be eaten as a keyboard-mnemonic marker
            text = self.labels.get(label).replace("&", "&&")
            if numbered:
                text = f"{i}. {text}"
            button = WorkspaceButton(text)
            button.setToolTip(text.replace("&&", "&"))
            button.setCheckable(True)
            # Let long titles clip inside the sidebar instead of widening it past its fixed width
            button.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Fixed)
            button.setFont(self.style.get_font("default"))
            button.setStyleSheet(self.style.themed(
                f"QPushButton {{ text-align: left; }}"
                f"QPushButton:checked {{ border: 2px solid {self.style.color('field_text')}; }}"
            ))
            button.clicked.connect(lambda checked=False, target=target: self.select(target))
            button.doubleClicked.connect(lambda target=target: self.start(target))
            self.workspace_group.addButton(button)
            content_layout.addWidget(button)

        def update(expanded: bool, title=title, header=header, content=content):
            header.setText(f"{'▼' if expanded else '▶'}  {title}")
            content.setVisible(expanded)
        header.toggled.connect(update)
        update(header.isChecked())

        return row + 2

    def workspaces_in(self, category: str | None) -> list[tuple[str, str]]:
        '''
        Every included workspace whose "category" matches, sorted by "order"
        (then page key), as (link_label, target page key) pairs.
        '''
        matches = [
            (config.get("order", 0), key, config)
            for key, config in self.workspaces.items()
            if config.get("include") == 1 and config.get("category") == category
        ]
        matches.sort(key=lambda match: match[:2])
        return [(self.context.pages.link_label(key), key) for _, key, _ in matches]

    # Summary
    def build_summary(self, body: QHBoxLayout):
        '''
        The summary box: a frame holding the markdown browser, transparent
        until a workspace is selected (see set_summary_opaque), plus a row
        of action buttons (Delete Saved Data, Open Workspace) that isn't in
        any layout - it's placed by hand in the box's bottom-right corner on
        every resize (see eventFilter), so it floats over the browser and
        stays put while the summary scrolls.
        '''
        self.summary_box = QFrame()
        box_layout = QVBoxLayout(self.summary_box)
        box_layout.setContentsMargins(self.style.igap, self.style.igap, self.style.igap, self.style.igap)
        body.addWidget(self.summary_box, 1)

        self.browser = NoteBrowser()
        self.browser.setOpenExternalLinks(True)
        self.browser.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.browser.setFont(self.style.get_font("default"))
        self.browser.setStyleSheet(self.style.themed("QTextBrowser { background-color: transparent; border: none; }"))
        self.browser.viewport().setAutoFillBackground(False)
        box_layout.addWidget(self.browser)

        self.actions = QWidget(self.summary_box)
        actions_layout = QHBoxLayout(self.actions)
        actions_layout.setContentsMargins(0, 0, 0, 0)
        actions_layout.setSpacing(self.style.igap)

        self.delete_button = QPushButton(self.labels.get("title_buttons_delete_workspace_data"))
        self.delete_button.setFont(self.style.get_font("title_btn"))
        self.delete_button.clicked.connect(lambda checked=False: self.delete_saved_data(self.selected_target))
        actions_layout.addWidget(self.delete_button)

        self.start_button = QPushButton(self.labels.get("title_buttons_open_workspace"))
        self.start_button.setFont(self.style.get_font("title_btn"))
        self.start_button.clicked.connect(lambda checked=False: self.start(self.selected_target))
        actions_layout.addWidget(self.start_button)
        self.actions.hide()

        self.summary_box.installEventFilter(self)
        # The scrollbar appearing/disappearing changes where the corner is
        self.browser.verticalScrollBar().rangeChanged.connect(lambda *_: self.place_actions())
        self.set_summary_opaque(False)

    def set_summary_opaque(self, opaque: bool):
        color = self.style.color("field") if opaque else "transparent"
        self.summary_box.setStyleSheet(self.style.themed(
            f"background-color: {color}; border-radius: {self.style.PANEL_RADIUS}px;", self.summary_box
        ))
        self.actions.setVisible(opaque)
        self.place_actions()

    def place_actions(self):
        padding = self.style.igap * 2
        scrollbar = self.browser.verticalScrollBar()
        scrollbar_width = scrollbar.width() if scrollbar.isVisible() else 0
        size = self.actions.sizeHint()
        self.actions.resize(size)
        self.actions.move(
            self.summary_box.width() - size.width() - padding - scrollbar_width,
            self.summary_box.height() - size.height() - padding,
        )
        self.actions.raise_()

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if watched is self.summary_box and event.type() == QEvent.Type.Resize:
            self.place_actions()
        return False

    def select(self, target: str):
        self.selected_target = target
        config = self.context.pages.load_page_config(target)
        self.set_summary_opaque(True)
        self.refresh_delete_button()
        self.show_note(self.join_note(config.get("_note", "")), self.context.paths.pages / target)

    def show_note(self, markdown: str, folder: Path):
        self.browser.setSearchPaths([str(folder)])
        self.browser.document().clear()
        self.browser.setMarkdown(markdown)
        if self.actions.isVisible():
            # Room at the bottom so the last lines can scroll up past the pinned buttons
            root = self.browser.document().rootFrame()
            frame_format = root.frameFormat()
            frame_format.setBottomMargin(self.actions.sizeHint().height() + self.style.igap * 2)
            root.setFrameFormat(frame_format)
        self.browser.verticalScrollBar().setValue(0)

    @staticmethod
    def join_note(note: str | list) -> str:
        if isinstance(note, list):
            return "\n\n".join(str(block) for block in note)
        return str(note)

    @staticmethod
    def translucent(hex_color: str, opacity: float) -> str:
        color = QColor(hex_color)
        return f"rgba({color.red()}, {color.green()}, {color.blue()}, {int(opacity * 255)})"

    def start(self, target: str | None):
        if target is not None:
            self.router.show(target)

    # Saved data
    def refresh_delete_button(self):
        '''Only lets the selected workspace's saved data be deleted if it has any.'''
        has_data = self.selected_target is not None and self.context.pages.has_saved_page(self.selected_target)
        self.delete_button.setEnabled(has_data)
        self.delete_button.setToolTip("" if has_data else "Nothing saved for this workspace yet")

    def delete_saved_data(self, target: str | None):
        if target is None:
            return
        name = self.labels.get(self.context.pages.link_label(target))
        def delete():
            self.context.pages.delete_saved_page(target)
            self.refresh_delete_button()
        popup.delete_workspace_data_dialog(self, self.context, name, delete)
