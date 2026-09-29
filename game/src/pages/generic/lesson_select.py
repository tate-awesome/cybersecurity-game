from pathlib import Path

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QFont, QImage, QTextDocument
from PySide6.QtWidgets import QButtonGroup, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QTextBrowser, QVBoxLayout, QWidget

from ...app_core import Context
from ...widgets import Scrollable
from ..page import Page


class NoteBrowser(QTextBrowser):
    '''
    Read-only markdown view for a lesson's _note. Relative image paths
    (e.g. "screenshot.png") resolve against the lesson's own folder via
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


class LessonSelectPage(Page):
    '''
    Page constructor for build_type "lesson_select". A scrollable sidebar
    of collapsible sections on the left, one per config["sections"] entry,
    each listing the manifest lessons whose "category" matches it. Clicking
    a lesson shows that lesson's own config.json "_note" (markdown) on the
    right; with nothing selected, this page's own "_note" is shown instead.

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
        self.start_button: QPushButton | None = None

        title = QLabel(self.labels.get("title_text", config.get("title", "_default")))
        # Copy - get_font hands back a shared cached QFont
        title_font = QFont(self.style.get_font("title_btn"))
        title_font.setBold(True)
        title.setFont(title_font)
        self.layout().addWidget(title)

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

        self.browser = NoteBrowser()
        self.browser.setOpenExternalLinks(True)
        self.browser.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.browser.setFont(self.style.get_font("default"))
        self.browser.setStyleSheet(self.style.themed())
        body.addWidget(self.browser, 1)

        self.lesson_group = QButtonGroup(self)
        self.lesson_group.setExclusive(True)
        row = 0
        for section in config.get("sections", []):
            row = self.build_section(section, row)
        self.scrollable.add_deadspace()

        footer = QHBoxLayout()
        footer.setSpacing(self.style.igap)
        self.layout().addLayout(footer)
        for button in config.get("buttons", []):
            self.build_footer_button(button, footer)
            if button.get("action") == "back":
                footer.addStretch(1)

        self.show_note(self.default_note, self.default_folder)

    # Sidebar
    def build_section(self, section: dict, row: int) -> int:
        '''
        Adds one collapsible section (header button + lesson buttons) to
        the sidebar starting at the given grid row, and returns the next
        free row. "numbered" prefixes each lesson with its position, so
        the default note can point students at e.g. "Defender Lesson 1".
        '''
        title = self.labels.get("title_buttons", section.get("label", "_default"))
        lessons = self.lessons_in(section.get("category"))
        numbered = section.get("numbered", False)

        header = QPushButton()
        header.setCheckable(True)
        header.setChecked(section.get("expanded", True))
        header.setFont(self.style.get_font("title_btn"))
        header.setStyleSheet(self.style.themed(
            f"QPushButton {{ text-align: left; background-color: {self.style.color('widget')}; color: {self.style.color('field_text')}; }}"
        ))
        header.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Fixed)
        self.scrollable.grid_layout.addWidget(header, row, 0)

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(self.style.igap, 0, 0, 0)
        content_layout.setSpacing(self.style.cgap * 2)
        self.scrollable.grid_layout.addWidget(content, row + 1, 0)

        for i, (label, target) in enumerate(lessons, start=1):
            # "&" would otherwise be eaten as a keyboard-mnemonic marker
            text = self.labels.get("title_buttons", label).replace("&", "&&")
            if numbered:
                text = f"{i}. {text}"
            button = QPushButton(text)
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
            self.lesson_group.addButton(button)
            content_layout.addWidget(button)

        def update(expanded: bool, title=title, header=header, content=content):
            header.setText(f"{'▼' if expanded else '▶'}  {title}")
            content.setVisible(expanded)
        header.toggled.connect(update)
        update(header.isChecked())

        return row + 2

    def lessons_in(self, category: str | None) -> list[tuple[str, str]]:
        '''
        Every manifest lesson whose "category" matches, in manifest order,
        as (title_label, target page key) pairs.
        '''
        lessons = []
        for key, value in self.context.pages.get("lessons").items():
            if value.get("category") == category:
                lessons.append((value.get("title_label", key), value.get("path", key)))
        return lessons

    # Summary
    def select(self, target: str):
        self.selected_target = target
        if self.start_button is not None:
            self.start_button.setEnabled(True)
        config = self.context.pages.load_page_config(target)
        self.show_note(self.join_note(config.get("_note", "")), self.context.paths.pages / target)

    def show_note(self, markdown: str, folder: Path):
        self.browser.setSearchPaths([str(folder)])
        self.browser.document().clear()
        self.browser.setMarkdown(markdown)
        self.browser.verticalScrollBar().setValue(0)

    @staticmethod
    def join_note(note: str | list) -> str:
        if isinstance(note, list):
            return "\n\n".join(str(block) for block in note)
        return str(note)

    # Footer
    def build_footer_button(self, button: dict, footer: QHBoxLayout):
        action = button.get("action")
        widget = QPushButton(self.labels.get("title_buttons", button.get("label", "_default")))
        widget.setFont(self.style.get_font("title_btn"))
        if action == "back":
            widget.clicked.connect(lambda checked=False: self.router.go_back())
        elif action == "quit":
            widget.clicked.connect(lambda checked=False: self.router.quit())
        elif action == "start":
            self.start_button = widget
            widget.setEnabled(False)
            widget.clicked.connect(lambda checked=False: self.start())
        else:
            print(f"Lesson select button config {button!r} has unknown action {action!r}, skipping")
            return
        footer.addWidget(widget)

    def start(self):
        if self.selected_target is not None:
            self.router.show(self.selected_target)
