import re
from pathlib import Path

from PySide6.QtCore import (QEasingCurve, QEvent, QPoint, QPointF, QPropertyAnimation, QRectF, QSizeF, Qt, QUrl,
                            QVariantAnimation, Signal)
from PySide6.QtGui import QBrush, QColor, QImage, QLinearGradient, QPainter, QPainterPath, QPixmap, QTextDocument
from PySide6.QtWidgets import (QButtonGroup, QFrame, QGraphicsEffect, QGraphicsOpacityEffect, QHBoxLayout, QLabel,
                               QPushButton, QSizePolicy, QTextBrowser, QVBoxLayout, QWidget)

from ...app_core import Context
from ...widgets import Scrollable
from ...widgets.panels.panel import paint_panel
from ...widgets.frame_widgets.important_buttons import PAGE_MARK, POPOUT_MARK
from ..page import Page


class NoteCache(QGraphicsEffect):
    '''
    Draws its widget from a picture of it, taken once and reused until
    invalidate() - optionally faded through an opacity mask. The note
    sits on a see-through card over the animated background, so every
    background frame repaints it: drawn live (or through a
    QGraphicsOpacityEffect, which Qt doesn't cache for widgets) that was
    most of each frame.

    Qt doesn't tell a widget's effect when the widget changes, so
    whatever changes it has to call invalidate() (see NoteBrowser).
    '''

    def __init__(self):
        super().__init__()
        self.mask: QBrush | None = None
        self.picture: QPixmap | None = None
        self.origin = QPointF()
        # Taking the picture lays the note out, which reports changes of its own
        self.capturing = False

    def invalidate(self):
        if self.capturing:
            return
        self.picture = None
        self.update()

    def set_mask(self, mask: QBrush | None):
        self.mask = mask
        self.invalidate()

    def draw(self, painter: QPainter):
        if self.picture is None:
            self.capturing = True
            try:
                # PySide6 drops sourcePixmap's offset out-parameter, so place
                # it by the source's own bounding rect (logical coordinates,
                # no padding - the two then line up exactly)
                picture = self.sourcePixmap(Qt.CoordinateSystem.LogicalCoordinates,
                                            mode=QGraphicsEffect.PixmapPadMode.NoPad)
                self.origin = self.sourceBoundingRect(Qt.CoordinateSystem.LogicalCoordinates).topLeft()
            finally:
                self.capturing = False
            if self.mask is not None and not picture.isNull():
                masking = QPainter(picture)
                masking.setCompositionMode(QPainter.CompositionMode.CompositionMode_DestinationIn)
                masking.fillRect(QRectF(QPointF(0, 0), picture.deviceIndependentSize()), self.mask)
                masking.end()
            self.picture = picture
        painter.drawPixmap(self.origin, self.picture)


class NoteBrowser(QTextBrowser):
    '''
    Read-only markdown view for a workspace's _note. Relative image paths
    (e.g. "screenshot.png") resolve against the workspace's own folder via
    searchPaths, and images are scaled down to fit the viewport so a
    full-size screenshot doesn't force horizontal scrolling.

    Links that open the browser (http/https) get the POPOUT_MARK after
    their text, like every other way out of the app.

    An edge with more of the note past it fades the text out toward it
    (see show_edges), so a long note never looks like it ends at the
    bottom of the card.

    The text is drawn from a picture (see NoteCache), retaken whenever
    anything here changes how it looks - its content, scrolling, size,
    selection, focus, or the theme.
    '''

    # A markdown link to the web - not an image (![...](...))
    WEB_LINK = re.compile(r"(?<!!)\[([^\]]+)\]\((https?://[^)\s]+)\)")
    # px the fade reaches in from an edge
    FADE_DEPTH = 56
    # Events on the browser or its viewport that change how the text looks
    RESTYLE_EVENTS = {QEvent.Type.FocusIn, QEvent.Type.FocusOut, QEvent.Type.StyleChange, QEvent.Type.PaletteChange,
                      QEvent.Type.FontChange, QEvent.Type.EnabledChange, QEvent.Type.Resize}

    def __init__(self):
        super().__init__()
        # Held here as well, or Python collects it out from under the viewport
        self.cache = NoteCache()
        self.viewport().setGraphicsEffect(self.cache)
        bar = self.verticalScrollBar()
        bar.valueChanged.connect(self.show_edges)
        bar.rangeChanged.connect(self.show_edges)
        self.textChanged.connect(self.cache.invalidate)
        self.selectionChanged.connect(self.cache.invalidate)
        self.cursorPositionChanged.connect(self.cache.invalidate)
        # Images arriving, and any other relayout
        self.document().documentLayout().update.connect(self.cache.invalidate)
        self.installEventFilter(self)
        self.viewport().installEventFilter(self)

    def eventFilter(self, watched, event):
        if event.type() in self.RESTYLE_EVENTS:
            self.cache.invalidate()
        return False

    def show_edges(self, *_):
        '''
        Fades the text out toward each edge with more of the note past it -
        the text itself, through an opacity mask, so it fades into whatever
        is behind it, see-through themes and all. No mask at all while the
        whole note shows.
        '''
        bar = self.verticalScrollBar()
        above, below = bar.value() > bar.minimum(), bar.value() < bar.maximum()
        if not (above or below):
            self.cache.set_mask(None)
            return
        height = self.viewport().height()
        depth = min(self.FADE_DEPTH, height / 3) / max(1, height)
        gradient = QLinearGradient(0, 0, 0, height)
        gradient.setColorAt(0, QColor(0, 0, 0, 0 if above else 255))
        gradient.setColorAt(depth, Qt.GlobalColor.black)
        gradient.setColorAt(1 - depth, Qt.GlobalColor.black)
        gradient.setColorAt(1, QColor(0, 0, 0, 0 if below else 255))
        self.cache.set_mask(QBrush(gradient))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.show_edges()

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


class SummaryDrawer(QFrame):
    '''
    The workspace summary, shaped like a panel's drawer (see themes' module
    docstring): a beefy bar along its top - the workspace's title, big, and
    its action buttons (see add_button) - over a card holding its note, in
    the drawer's frame. The shadow, drawer and card are painted by hand, so
    they fade in and out together (see reveal); inner holds everything on
    them - the bar's title and buttons and the card's content - to fade new
    content in over them.
    '''

    REVEAL_MS = 220

    def __init__(self, context: Context):
        super().__init__()
        self.context = context
        self.style = context.style
        # 0 = not there yet, 1 = fully there
        self.shown = 0.0
        self.animation = QVariantAnimation(self)
        self.animation.setDuration(self.REVEAL_MS)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation.valueChanged.connect(self._set_shown)
        drawer = QVBoxLayout(self)
        drawer.setSpacing(0)

        self.inner = QWidget()
        inner_layout = QVBoxLayout(self.inner)
        inner_layout.setContentsMargins(0, 0, 0, 0)
        inner_layout.setSpacing(0)
        drawer.addWidget(self.inner)

        self.bar = QWidget()
        bar_layout = QHBoxLayout(self.bar)
        bar_layout.setSpacing(self.style.igap)
        self.title = QLabel()
        self.title.setFont(self.style.get_font("page_title"))
        # A title is a name, never markup
        self.title.setTextFormat(Qt.TextFormat.PlainText)
        # A long one clips, rather than pushing the buttons out
        self.title.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)
        self.style.live_style(self.title, lambda: f"QLabel {{ color: {self.style.color('menu_bar_text')}; }}")
        bar_layout.addWidget(self.title, 1)
        self.bar.hide()
        inner_layout.addWidget(self.bar)

        self.content = QWidget()
        content_layout = QVBoxLayout(self.content)
        # Edge to edge with the card - the note scrolls right up to its top and
        # bottom, with its scrollbar along its right (see build_summary)
        content_layout.setContentsMargins(0, 0, 0, 0)
        inner_layout.addWidget(self.content, 1)

        self.fit()
        self.style.signals.changed.connect(self.fit)

    def add_button(self, button: QPushButton):
        '''A button along the bar, right of the title, in the order added - as big as the title.'''
        button.setFont(self.style.get_font("title_btn"))
        self.bar.layout().addWidget(button)

    def show_bar(self, title: str):
        '''The bar, titled.'''
        self.bar.show()
        self.title.setText(title)

    def fit(self):
        '''After a theme change: room for its shadow, then its frame (see Panel.fit_frame), and the bar's padding.'''
        style = self.style
        left, top, right, bottom = style.panel_margins()
        frame = style.setting("panel_frame") + style.PANEL_BORDER_WIDTH
        self.layout().setContentsMargins(left + frame, top + style.PANEL_BORDER_WIDTH, right + frame, bottom + frame)
        # The title lines up with the card's text below it
        self.bar.layout().setContentsMargins(max(0, style.igap * 2 - frame), style.igap, 0, style.igap)
        self.update()

    def body_rect(self) -> QRectF:
        '''Where the drawer itself is drawn - inside the room for its shadow (see Style.panel_margins).'''
        left, top, right, bottom = self.style.panel_margins()
        return QRectF(self.rect()).adjusted(left, top, -right, -bottom)

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
        # The card, clipped to the drawer's rounded shape - with no frame, its corners are the drawer's
        path = QPainterPath()
        path.addRoundedRect(self.body_rect(), self.style.PANEL_RADIUS, self.style.PANEL_RADIUS)
        painter.setClipPath(path)
        card = QRectF(self.content.mapTo(self, QPoint(0, 0)), QSizeF(self.content.size()))
        painter.fillRect(card, self.style.brush("card", card))
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
      - a transparent scrollable sidebar on the left, one entry per
        config["sections"] entry, in order: a collapsible section
        ({"label", "category", ...}) listing the workspaces whose
        "category" matches it - every page directly inside the
        config["link_folder"] folder with "include": 1, sorted by their
        "order" - or a single workspace outside any section
        ({"workspace": its page key}), like Start Here!. A section with
        "hidden": true, or a workspace without "include": 1, isn't shown.
        Sections start collapsed, but for "expanded": true and the one
        holding the selected workspace
      - the summary area filling the rest

    A workspace is always selected, its config.json "_note" (markdown)
    shown in a drawer shaped like a panel's (see SummaryDrawer) - the one
    last selected (the "workspace_description" preference), or the first
    in the list. Switching workspaces fades the new summary in. The
    drawer's bar, where a panel's menu bar is, has the workspace's title
    and its buttons: Open Workspace (and, in developer mode, Edit This
    Workspace, which opens it in the workspace editor). Double-clicking a
    workspace opens it immediately.

    A _note can be one string or a list of markdown blocks, joined with
    blank lines between them.

    key is the page to build (the router's current page, by default);
    preview builds it to show inside another page (see ThemeEditorPage) -
    without the menu bar, which is the window's title bar, and with a
    background of its own.
    '''

    SIDEBAR_WIDTH = 380
    # The preference holding the workspace whose description was read last
    LAST_READ = "workspace_description"

    def __init__(self, context: Context, key: str | None = None, preview: bool = False):
        super().__init__(context)
        self.labels = context.labels

        key = key or context.router.current_page
        config = context.pages.load_page_config(key)
        self.selected_target: str | None = None
        # Each listed workspace's button, and the section header it's under (None outside any), in list order
        self.buttons: dict[str, tuple[WorkspaceButton, QPushButton | None]] = {}
        self.workspaces = context.pages.pages_in(config.get("link_folder", "workspaces"))

        self.add_background(config, menu=True, shared=not preview)

        if not preview:
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
            if not isinstance(section, dict):
                continue
            if "workspace" in section:
                row = self.build_lone_workspace(section["workspace"], row)
            elif not section.get("hidden", False):
                row = self.build_section(section, row)
        self.scrollable.add_deadspace()

        last = context.preferences.get(self.LAST_READ)
        first = last if last in self.buttons else next(iter(self.buttons), None)
        if first is not None:
            button, header = self.buttons[first]
            if header is not None:
                header.setChecked(True)  # its section opened, to show it's the one
            button.setChecked(True)
            self.select(first)

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
        # Collapsed unless the section says otherwise - the last-read workspace's opens anyway (see __init__)
        header.setChecked(section.get("expanded", False))
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
            content_layout.addWidget(self.workspace_button(label, target, header, i if numbered else None))

        def update(expanded: bool, title=title, header=header, content=content):
            header.setText(f"{self.style.icon('chevron-down' if expanded else 'chevron-right')}  {title}")
            content.setVisible(expanded)
        header.toggled.connect(update)
        update(header.isChecked())

        return row + 2

    def build_lone_workspace(self, target: str, row: int) -> int:
        '''Adds a workspace outside any section at the given grid row - if it's there and included - and returns the next free row.'''
        config = self.workspaces.get(target)
        if config is None or config.get("include") != 1 or target in self.buttons:
            return row
        self.scrollable.grid_layout.addWidget(self.workspace_button(self.context.pages.link_label(target), target), row, 0)
        return row + 1

    def workspace_button(self, label: str, target: str, header: QPushButton | None = None,
                         number: int | None = None) -> "WorkspaceButton":
        '''
        A workspace's button in the sidebar - under header's section, or
        outside any - numbered as its section numbers it, if it does.
        '''
        # "&" would otherwise be eaten as a keyboard-mnemonic marker
        text = self.labels.get(label).replace("&", "&&")
        if number is not None:
            text = f"{number}. {text}"
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
        self.buttons.setdefault(target, (button, header))
        return button

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
        The summary drawer (see SummaryDrawer): the markdown browser on its
        card, and on its bar Edit This Workspace in developer mode, then
        Open Workspace. The bar's title and buttons and the browser fade in
        together whenever the summary changes (see show_note).
        '''
        self.summary_box = SummaryDrawer(self.context)
        body.addWidget(self.summary_box, 1)
        self.summary = self.summary_box.inner

        self.browser = NoteBrowser()
        self.browser.setOpenExternalLinks(True)
        self.browser.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.browser.setFont(self.style.get_font("default"))
        self.style.live_style(self.browser, self.browser_sheet)
        self.browser.viewport().setAutoFillBackground(False)
        # The text's padding from the card's sides - around the text only, so
        # the scrollbar still runs along the card's right edge, as in panels
        pad = self.style.igap * 2
        self.browser.setViewportMargins(pad, 0, pad, 0)
        self.summary_box.content.layout().addWidget(self.browser, 1)

        if self.context.preferences.is_developer():
            from ...widgets.frame_widgets.important_buttons import developer_text
            edit_button = QPushButton(developer_text(f"{self.labels.get('title_buttons_edit_workspace')} {PAGE_MARK}"))
            edit_button.clicked.connect(lambda checked=False: self.edit(self.selected_target))
            self.summary_box.add_button(edit_button)

        start_button = QPushButton(f"{self.labels.get('title_buttons_open_workspace')} {PAGE_MARK}")
        start_button.clicked.connect(lambda checked=False: self.start(self.selected_target))
        self.summary_box.add_button(start_button)

    # How much thicker the note's scrollbar is than the theme's others - a long note's is easy to miss
    SCROLLBAR_SCALE = 1.75

    def browser_sheet(self) -> str:
        '''
        The note's own rules: no background or border of its own, and a
        thicker scrollbar - its handle's corners scaled with it, so it keeps
        the theme's shape (see Style's scrollbar rules).
        '''
        style = self.style
        width = int(style.get_scrollbar_size() * self.SCROLLBAR_SCALE)
        thickness = max(2, width - 2 * style.setting("scrollbar_inset"))
        radius = style.setting("scrollbar_radius")
        handle_radius = thickness // 2 if radius is None else min(radius, thickness // 2)
        return (f"QTextBrowser {{ background-color: transparent; border: none; }}"
                f" QScrollBar:vertical {{ width: {width}px; }}"
                f" QScrollBar::handle:vertical {{ border-radius: {handle_radius}px; min-height: {width * 2}px; }}")

    def select(self, target: str):
        '''Shows target's description - and remembers it, for the next time this page opens.'''
        if target == self.selected_target:
            return
        self.selected_target = target
        config = self.context.pages.load_page_config(target)
        self.summary_box.show_bar(self.labels.get(self.context.pages.link_label(target)))
        self.summary_box.reveal(True)
        self.show_note(self.join_note(config.get("_note", "")), self.context.paths.pages / target)
        if self.context.preferences.get(self.LAST_READ) != target:
            self.context.preferences.set(self.LAST_READ, target)

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
