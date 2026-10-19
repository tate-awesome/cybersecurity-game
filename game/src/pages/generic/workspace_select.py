import re
from pathlib import Path

from PySide6.QtCore import QEasingCurve, QPropertyAnimation, Qt, QUrl, QVariantAnimation, Signal
from PySide6.QtGui import QColor, QImage, QPainter, QTextDocument
from PySide6.QtWidgets import (QButtonGroup, QFrame, QGraphicsOpacityEffect, QHBoxLayout, QPushButton, QSizePolicy,
                               QTextBrowser, QVBoxLayout, QWidget)

from ...app_core import Context
from ...app_core.context.style import PANEL_BORDER_WIDTH
from ...widgets import Scrollable
from ...widgets.panels.panel import paint_panel
from ...widgets.frame_widgets.important_buttons import PAGE_MARK, POPOUT_MARK
from ..page import Page


class NoteBrowser(QTextBrowser):
    '''
    Read-only markdown view for a workspace's _note. Relative image paths
    (e.g. "screenshot.png") resolve against the workspace's own folder via
    searchPaths, and images are scaled down to fit the viewport so a
    full-size screenshot doesn't force horizontal scrolling.

    Links that open the browser (http/https) get the POPOUT_MARK after
    their text, like every other way out of the app.
    '''

    # A markdown link to the web - not an image (![...](...))
    WEB_LINK = re.compile(r"(?<!!)\[([^\]]+)\]\((https?://[^)\s]+)\)")

    def setMarkdown(self, markdown: str):
        def mark(match: re.Match) -> str:
            text = match.group(1)
            if not text.rstrip().endswith(POPOUT_MARK):
                text = f"{text} {POPOUT_MARK}"
            return f"[{text}]({match.group(2)})"
        super().setMarkdown(self.WEB_LINK.sub(mark, markdown))

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


class SummaryCard(QFrame):
    '''
    The workspace summary's box: dressed like a panel - the theme's panel
    material, outline, corners and shadow (see Style.panel_shadow) - but
    painted by hand, so it can fade in and out (see reveal). Its content
    sits inside the room the shadow needs, so revealing it never moves the
    text.
    '''

    REVEAL_MS = 220

    def __init__(self, context: Context):
        super().__init__()
        self.context = context
        self.style = context.style
        # 0 = not there (the page's own note shows on the bare background), 1 = fully there
        self.shown = 0.0
        self.animation = QVariantAnimation(self)
        self.animation.setDuration(self.REVEAL_MS)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation.valueChanged.connect(self._set_shown)
        self.setLayout(QVBoxLayout())
        self.fit()
        self.style.signals.changed.connect(self.fit)

    def fit(self):
        '''After a theme change: room for its shadow, then its padding.'''
        left, top, right, bottom = self.style.panel_margins()
        pad = self.style.igap + PANEL_BORDER_WIDTH
        self.layout().setContentsMargins(left + pad, top + pad, right + pad, bottom + pad)
        self.update()

    def reveal(self, show: bool):
        '''Fades in (or out) - at once with page transitions off (see Performance.page_transitions).'''
        target = 1.0 if show else 0.0
        self.animation.stop()
        if not self.context.performance.page_transitions or self.shown == target:
            self._set_shown(target)
            return
        self.animation.setStartValue(self.shown)
        self.animation.setEndValue(target)
        self.animation.start()

    def _set_shown(self, value):
        self.shown = float(value)
        self.update()

    def paintEvent(self, event):
        if self.shown <= 0:
            return
        painter = QPainter(self)
        painter.setOpacity(self.shown)
        paint_panel(painter, self.style, self.width(), self.height())
        painter.end()


def fade_in(widget: QWidget, context: Context, duration: int = 200):
    '''
    Fades widget in from transparent - its new content arriving - then
    drops the effect, so it costs nothing once it's in. At once with page
    transitions off (see Performance.page_transitions).
    '''
    if not context.performance.page_transitions:
        return
    effect = QGraphicsOpacityEffect(widget)
    effect.setOpacity(0.0)
    widget.setGraphicsEffect(effect)
    animation = QPropertyAnimation(effect, b"opacity", effect)
    animation.setDuration(duration)
    animation.setStartValue(0.0)
    animation.setEndValue(1.0)
    animation.setEasingCurve(QEasingCurve.Type.OutCubic)
    # The effect is the widget's - setting None deletes it, and the animation with it
    animation.finished.connect(lambda: widget.setGraphicsEffect(None))
    animation.start()


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
        their "order". A section with "hidden": true isn't shown at all
      - the summary area filling the rest

    With nothing selected, the summary area shows this page's own "_note"
    straight on the background. Clicking a workspace shows that
    workspace's config.json "_note" (markdown) on a card dressed like a
    panel instead (see SummaryCard), which fades in - and switching
    workspaces fades the new summary in over it. Under the summary, the
    card's bottom row has Open Workspace (and, in developer mode, Edit This
    Workspace, which opens it in the workspace editor) - out of the
    summary's way, so it never covers it. Double-clicking a workspace opens it
    immediately, and clicking any dead space - the background, empty
    sidebar, the box's margins - deselects it, back to this page's note.

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

        self.add_background(config, menu=True)

        self.build_menu_bar(config.get("title", "_default"), config.get("menu_bar", []))

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
        self.style.set_material(self.scrollable, "none")
        self.scrollable.viewport().setAutoFillBackground(False)
        self.style.set_material(self.scrollable.inner, "none")

        self.build_summary(body)

        self.workspace_group = QButtonGroup(self)
        self.workspace_group.setExclusive(True)
        row = 0
        for section in config.get("sections", []):
            if not section.get("hidden", False):
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
        self.style.live_style(header, lambda: (
            # A header, not a button - whatever a theme's buttons look like (see themes.BUTTON_KINDS)
            f"QPushButton {{ text-align: left; background-color: transparent; color: {self.style.color('text')};"
            f" border-color: transparent; }}"
            f"QPushButton:hover, QPushButton:pressed {{ background-color: {self.translucent(self.style.color('widget'), 0.6)}; }}"
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
            # A menu button - the selected one (checked) looks hovered (see Style.mark_menu_button)
            self.style.mark_menu_button(button)
            button.setStyleSheet("QPushButton { text-align: left; }")
            button.clicked.connect(lambda checked=False, target=target: self.select(target))
            button.doubleClicked.connect(lambda target=target: self.start(target))
            self.workspace_group.addButton(button)
            content_layout.addWidget(button)

        def update(expanded: bool, title=title, header=header, content=content):
            header.setText(f"{self.style.icon('chevron-down' if expanded else 'chevron-right')}  {title}")
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
        The summary card (see SummaryCard): the markdown browser, and under
        it a row of action buttons - Edit This Workspace in developer mode,
        then Open Workspace - shown while a workspace is selected. The
        browser and the row fade in together whenever the summary changes
        (see show_note).
        '''
        self.summary_box = SummaryCard(self.context)
        body.addWidget(self.summary_box, 1)

        self.summary = QWidget()
        summary_layout = QVBoxLayout(self.summary)
        summary_layout.setContentsMargins(0, 0, 0, 0)
        summary_layout.setSpacing(self.style.igap)
        self.summary_box.layout().addWidget(self.summary)

        self.browser = NoteBrowser()
        self.browser.setOpenExternalLinks(True)
        self.browser.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.browser.setFont(self.style.get_font("default"))
        self.browser.setStyleSheet("QTextBrowser { background-color: transparent; border: none; }")
        self.browser.viewport().setAutoFillBackground(False)
        summary_layout.addWidget(self.browser, 1)

        self.actions = QWidget()
        actions_layout = QHBoxLayout(self.actions)
        actions_layout.setContentsMargins(0, 0, 0, 0)
        actions_layout.setSpacing(self.style.igap)
        actions_layout.addStretch(1)

        self.edit_button = None
        if self.context.preferences.is_developer():
            from ...widgets.frame_widgets.important_buttons import developer_text
            self.edit_button = QPushButton(developer_text(f"{self.labels.get('title_buttons_edit_workspace')} {PAGE_MARK}"))
            self.edit_button.setFont(self.style.get_font("title_btn"))
            self.edit_button.clicked.connect(lambda checked=False: self.edit(self.selected_target))
            actions_layout.addWidget(self.edit_button)

        self.start_button = QPushButton(f"{self.labels.get('title_buttons_open_workspace')} {PAGE_MARK}")
        self.start_button.setFont(self.style.get_font("title_btn"))
        self.start_button.clicked.connect(lambda checked=False: self.start(self.selected_target))
        actions_layout.addWidget(self.start_button)
        self.actions.hide()
        summary_layout.addWidget(self.actions)

    def select(self, target: str):
        if target == self.selected_target:
            return
        self.selected_target = target
        config = self.context.pages.load_page_config(target)
        self.actions.show()
        self.summary_box.reveal(True)
        self.show_note(self.join_note(config.get("_note", "")), self.context.paths.pages / target)

    def deselect(self):
        '''Back to nothing selected - this page's own note, on the bare background.'''
        if self.selected_target is None:
            return
        self.selected_target = None
        # An exclusive group won't let its checked button be unchecked directly
        self.workspace_group.setExclusive(False)
        for button in self.workspace_group.buttons():
            button.setChecked(False)
        self.workspace_group.setExclusive(True)
        self.actions.hide()
        self.summary_box.reveal(False)
        self.show_note(self.default_note, self.default_folder)

    def mousePressEvent(self, event):
        # Only clicks nothing else took reach the page: the background,
        # empty sidebar and the card's margins, the menu bar's empty stretch
        if event.button() == Qt.MouseButton.LeftButton:
            self.deselect()
        super().mousePressEvent(event)

    def show_note(self, markdown: str, folder: Path):
        self.browser.setSearchPaths([str(folder)])
        self.browser.document().clear()
        self.browser.setMarkdown(markdown)
        self.browser.verticalScrollBar().setValue(0)
        fade_in(self.summary, self.context)

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

    def edit(self, target: str | None):
        '''Opens the workspace editor on this workspace (developer mode only - see build_summary).'''
        if target is None:
            return
        # Imported here: the editor's module imports this one
        from ..demo.config_editor import ConfigEditor
        ConfigEditor.selected_key = target
        self.router.show("demo/config_editor")
