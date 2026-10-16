from PySide6.QtCore import QEasingCurve, QEvent, QObject, Qt, QVariantAnimation
from PySide6.QtGui import QColor, QCursor, QPainter
from PySide6.QtWidgets import QFrame, QLabel, QPushButton, QScrollArea, QStyle, QVBoxLayout, QWidget

from ...app_core import Context
from .important_buttons import (ButtonGroup, GoBackToPreviousPage, GoForwardToNextPage, ImportantButton, OpenPauseMenu,
                                OpenSettingsPage, QuitApplication, RefreshCurrentPage, ShowHelpMessage, ToggleBookmark)
from .important_buttons.button_group import DEVELOPER_GROUPS, QWIDGETSIZE_MAX
from .overlay import Overlay
from .window_chrome import WindowControls, toggle_maximized

# How dark the page goes behind the menu (0-255), once it's all the way out
DIM_ALPHA = 150
# How long the drawer takes to come all the way out, or go all the way back
SLIDE_MS = 280


class _Dim(QWidget):
    '''
    The pause menu's backdrop: covers the window and dims it - the page
    keeps running underneath - by `amount` (0-1) of DIM_ALPHA. A click on it
    (outside the menu) closes the menu.
    '''

    def __init__(self, root: QWidget, close):
        super().__init__(root)
        self.close_menu = close
        self.amount = 0.0
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, False)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 0, 0, round(DIM_ALPHA * self.amount)))
        painter.end()

    def mousePressEvent(self, event):
        self.close_menu()


class _Drawer(QFrame):
    '''The menu itself - against the window's left edge, full height, with a line down its right edge like the window bar's.'''

    def __init__(self, parent: QWidget, context: Context):
        super().__init__(parent)
        self.context = context
        context.style.set_material(self, "overlay")

    def paintEvent(self, event):
        super().paintEvent(event)
        line = QColor(self.context.style.color("text"))
        line.setAlpha(70)
        painter = QPainter(self)
        painter.setPen(line)
        painter.drawLine(self.width() - 1, 0, self.width() - 1, self.height())
        painter.end()


class _FollowResize(QObject):
    def __init__(self, window: QWidget, callback):
        super().__init__(window)
        self.callback = callback
        window.installEventFilter(self)

    def eventFilter(self, watched, event):
        if event.type() == QEvent.Type.Resize:
            self.callback()
        return False


class _OnHide(QObject):
    '''Calls back whenever a widget hides - an Overlay opened from the menu (see PauseMenu.watch).'''
    def __init__(self, owner: QObject, widget: QWidget, callback):
        super().__init__(owner)
        self.callback = callback
        widget.installEventFilter(self)

    def eventFilter(self, watched, event):
        if event.type() == QEvent.Type.Hide:
            self.callback()
        return False


class PauseMenu:
    '''
    The menu Esc (or the menu bar's home button) slides out of the left
    edge of the window: the window bar's buttons spelled out, for anyone
    who doesn't know its icons yet - each led by its icon on the bar, with
    where it goes (see ImportantButton.OPENS) or its dropdown's caret after
    it. Top to bottom as the bar runs left to right:
      - Resume (the home button), Back, Forward, Bookmark and Refresh
      - the page's own buttons (the bar's center zone), set apart in a card
        under the page's title - they only act on this workspace
      - Debug (developer mode), Appearance, Settings and Help
      - Minimize, Maximize/Restore (not fullscreen) and Quit
    - and what's running right now, so leaving is never blind. Esc closes
    it again, and so does clicking outside it; it slides back out of sight.

    It's only a menu: nothing stops while it's open, the page just dims
    underneath. Never on a page without a menu bar (the title pages, where
    the menu is the page). Belongs to the Router, which closes it whenever
    the page changes.
    '''

    def __init__(self, context: Context):
        self.context = context
        self.root = context.root
        self.dim: _Dim | None = None
        # The menu bar the menu was built from - its page's
        self.bar = None
        self.drawer: _Drawer | None = None
        self.content: QWidget | None = None
        # How far out the drawer is (0 hidden - 1 all the way out), and where it's heading
        self.progress = 0.0
        self.target = 0.0
        # (bar button, its row here) for the page's own buttons - see add_proxy
        self.proxies: list[tuple[QPushButton, QPushButton]] = []
        # Overlays opened from the menu, closed with it (see watch)
        self.watched: list[Overlay] = []
        self.sync_name = f"pause_menu_{id(self)}"

        self.animation = QVariantAnimation()
        self.animation.valueChanged.connect(self.set_progress)
        self.animation.finished.connect(self.settle)
        _FollowResize(self.root, self.place)

    def is_open(self) -> bool:
        '''Open, or on its way out - not while it's going back.'''
        return self.dim is not None and self.target > 0

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
        if self.is_open():
            return
        bar = self.page_bar()
        if self.dim is not None:
            if bar is self.bar:
                # Caught on its way back, on the same page - it turns around
                self.dim.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
                self.context.animation_manager.add_callback(self.sync_name, self.sync_proxies)
                self.animate(1.0)
                return
            # Still going back from the page before - its rows are that page's
            self.close(instant=True)
        if bar is None:
            return
        self.bar = bar
        self.dim = _Dim(self.root, self.close)
        self.drawer = _Drawer(self.dim, self.context)
        self.build(bar)
        self.progress = 0.0
        self.dim.show()
        # A button polished before it had a parent (Debug is - see
        # mark_developer_only) gets its old font back from the stylesheet
        # once it's reparented, whatever setFont said - set again in place
        font = self.context.style.get_font("title_btn")
        for button in self.content.findChildren(QPushButton):
            button.setFont(font)
        self.place()
        self.dim.raise_()
        self.dim.setFocus()
        self.context.animation_manager.add_callback(self.sync_name, self.sync_proxies)
        self.animate(1.0)

    def close(self, instant: bool = False):
        '''Slides the menu back out of sight - or, instant, takes it away at once.'''
        if self.dim is None or (self.target == 0 and not instant):
            return
        # Clicks reach the page again straight away, not once it's gone
        self.dim.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.context.animation_manager.remove_callback(self.sync_name)
        watched, self.watched = self.watched, []
        for overlay in watched:
            try:
                overlay.hide()
            except RuntimeError:
                pass  # gone with its button
        if instant:
            self.animation.stop()
            self.target = 0.0
            self.destroy()
        else:
            self.animate(0.0)

    def animate(self, target: float):
        '''Slides the drawer (and fades the dim) from wherever it is now to target - at once with page transitions off.'''
        self.target = target
        if not self.context.performance.page_transitions:
            self.animation.stop()
            self.set_progress(target)
            self.settle()
            return
        start = self.progress
        # Reconfiguring a finished animation makes it emit its stale end
        # value straight away (see GrowingButton.grow) - so set it up silently
        self.animation.stop()
        self.animation.blockSignals(True)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic if target > start else QEasingCurve.Type.InCubic)
        self.animation.setStartValue(start)
        self.animation.setEndValue(target)
        self.animation.setDuration(max(1, round(SLIDE_MS * abs(target - start))))
        self.animation.setCurrentTime(0)
        self.animation.blockSignals(False)
        self.animation.start()

    def set_progress(self, progress: float):
        self.progress = progress
        if self.dim is None:
            return
        try:
            self.dim.amount = progress
            self.dim.update()
            self.place()
        except RuntimeError:
            self.dim = None  # already gone with the window

    def settle(self):
        if self.target == 0:
            self.destroy()

    def destroy(self):
        dim, self.dim, self.drawer, self.content, self.bar = self.dim, None, None, None, None
        self.proxies = []
        self.progress = 0.0
        if dim is not None:
            try:
                dim.hide()
                dim.deleteLater()
            except RuntimeError:
                pass  # already gone with the window

    def place(self):
        if self.dim is None:
            return
        try:
            self.dim.setGeometry(self.root.rect())
            width = self.drawer_width()
            self.drawer.setGeometry(round(-width * (1.0 - self.progress)), 0, width, self.root.height())
        except RuntimeError:
            pass  # deleted with the window, with the resize still queued

    def drawer_width(self) -> int:
        '''Wide enough for its widest row, and a scrollbar for when the window's too short to show them all.'''
        scrollbar = self.drawer.style().pixelMetric(QStyle.PixelMetric.PM_ScrollBarExtent)
        margins = self.drawer.layout().contentsMargins()
        return min(self.root.width(), self.content.sizeHint().width() + scrollbar + margins.left() + margins.right())

    def label(self, key: str) -> str:
        return self.context.labels.get(f"pause_menu_{key}")

    # Building

    def build(self, bar):
        style = self.context.style
        outer = QVBoxLayout(self.drawer)
        outer.setContentsMargins(style.igap * 4, 0, style.igap * 2, 0)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        outer.addWidget(scroll)
        self.content = QWidget()
        scroll.setWidget(self.content)
        # See-through, down to the drawer's own surface
        scroll.setObjectName("_pause_menu_scroll")
        scroll.viewport().setObjectName("_pause_menu_viewport")
        self.content.setObjectName("_pause_menu_content")
        scroll.setStyleSheet("#_pause_menu_scroll, #_pause_menu_viewport, #_pause_menu_content { background: transparent; border: none; }")
        rows = QVBoxLayout(self.content)
        rows.setContentsMargins(0, style.igap * 3, 0, style.igap * 3)
        rows.setSpacing(style.igap // 2)
        # Vertically centered, like the title menu (see TitleMenu)
        rows.addStretch(1)

        title = QLabel(self.label("title"))
        title.setFont(style.get_font("page_title"))
        rows.addWidget(title)
        status = QLabel(self.running_text())
        status.setFont(style.get_font("small"))
        status.setWordWrap(True)
        rows.addWidget(status)

        self.add_section(rows, self.navigation_rows())
        self.add_page_tools(rows, bar)
        self.add_section(rows, self.global_rows())
        self.add_section(rows, self.window_rows())
        rows.addStretch(1)

    def add_section(self, rows: QVBoxLayout, buttons: list[QPushButton]):
        '''One of the bar's universal groups - set apart from the next by a gap.'''
        if not buttons:
            return
        rows.addSpacing(self.context.style.igap * 2)
        for button in buttons:
            rows.addWidget(button, 0, Qt.AlignmentFlag.AlignLeft)

    def add_page_tools(self, rows: QVBoxLayout, bar):
        '''
        The bar's center zone: the page's own buttons, in a card of their
        own under the page's title - they act on this workspace, where the
        rest of the menu is the same on every page.
        '''
        buttons = bar.tool_buttons()
        if not buttons:
            return
        style = self.context.style
        rows.addSpacing(style.igap * 2)
        header = QLabel(bar.game_label.text())
        header.setFont(style.get_font("small"))
        header.setTextFormat(Qt.TextFormat.PlainText)
        rows.addWidget(header)
        card = QFrame()
        style.set_material(card, "card", rounded=True, outlined=True)
        inside = QVBoxLayout(card)
        inside.setContentsMargins(style.igap, style.igap, style.igap, style.igap)
        inside.setSpacing(style.igap // 2)
        for button in buttons:
            inside.addWidget(self.add_proxy(button), 0, Qt.AlignmentFlag.AlignLeft)
        rows.addWidget(card)

    def navigation_rows(self) -> list[QPushButton]:
        '''The bar's left zone: home (here, Resume), back, forward, the bookmark and refresh.'''
        context, router = self.context, self.context.router
        resume = ImportantButton(context, "pause_menu_resume")
        resume.ICON = OpenPauseMenu.ICON
        back = GoBackToPreviousPage(context)
        forward = GoForwardToNextPage(context)
        stack = router.navigation_stack
        self.where_to(back, stack[-2] if len(stack) >= 2 else None, "back_to")
        self.where_to(forward, router.forward_stack[-1] if router.forward_stack else None, "forward_to")
        # The bookmark stays open on click - it's a toggle, not somewhere to go
        bookmark = ToggleBookmark(context)
        bookmark.LABEL, bookmark.ACTIVE_LABEL = "pause_menu_bookmark_off", "pause_menu_bookmark_on"
        bookmark.show_state()
        return [self.row(resume), self.row(back), self.row(forward), self.row(bookmark, closes=False),
                self.row(RefreshCurrentPage(context))]

    def where_to(self, button: ImportantButton, key: str | None, label: str):
        '''Names the page back/forward leads to (see MenuBar.where_to) - or, with nowhere to go, disables it.'''
        if key is None:
            button.setEnabled(False)
            return
        name = self.context.router.page_name(key)
        button.setText(self.context.labels.get(f"menu_bar_tooltips_{label}").replace("{page}", name))

    def global_rows(self) -> list[QPushButton]:
        '''The bar's right zone, but the window controls: Debug (developer mode), Appearance, Settings and Help - see global_buttons.'''
        from .menu_bar import RIGHT_ZONE_GROUPS, RIGHT_ZONE_ICONS
        context = self.context
        buttons = []
        for group_key, group_sections in RIGHT_ZONE_GROUPS.items():
            if group_key in DEVELOPER_GROUPS and not context.preferences.is_developer():
                continue
            sections = [(header, [button_class for button_class in button_classes if button_class.is_available(context)])
                        for header, button_classes in group_sections]
            group = ButtonGroup(context, group_key, [section for section in sections if section[1]])
            group.ICON = RIGHT_ZONE_ICONS[group_key]
            # Its submenu opens out to the right, beside the menu
            group.overlay.anchor = "east"
            self.watch(group.overlay)
            buttons.append(self.row(group, closes=False))
        for button_class in (OpenSettingsPage, ShowHelpMessage):
            buttons.append(self.row(button_class(context)))
        return buttons

    def window_rows(self) -> list[QPushButton]:
        '''The window controls - minimize, maximize/restore (not while fullscreen, like the bar's) and quit.'''
        root = self.root
        buttons = [self.window_row("minimize", lambda: (self.close(instant=True), root.showMinimized()))]
        if not root.isFullScreen():
            name = "restore" if root.isMaximized() else "maximize"
            buttons.append(self.window_row(name, lambda: (self.close(), toggle_maximized(root))))
        buttons.append(self.row(QuitApplication(self.context)))
        return buttons

    def window_row(self, name: str, action) -> QPushButton:
        '''A window control as a row - its icon on the bar (see WindowControls.ICONS), then its name.'''
        style = self.context.style
        button = QPushButton(f"{style.icon(WindowControls.ICONS[name])} {self.context.labels.get(f'window_controls_tooltips_{name}')}")
        self.style_row(button)
        button.clicked.connect(lambda checked=False: action())
        return button

    def row(self, button: ImportantButton, closes: bool = True) -> ImportantButton:
        '''
        An important button as a row of the menu, led by its icon on the bar
        (see lead_with_icon) - closing the menu first, then doing what it
        does, unless closes is False (a toggle, or a dropdown, whose
        overlay closes the menu - see watch).
        '''
        self.style_row(button)
        if button.developer_only:
            # mark_developer_only fixed its height to the old font's
            button.setMinimumHeight(0)
            button.setMaximumHeight(QWIDGETSIZE_MAX)
        button.lead_with_icon()
        if closes:
            button.clicked.disconnect()
            button.clicked.connect(lambda checked=False: (self.close(), button.on_click()))
        return button

    def style_row(self, button: QPushButton):
        '''Looks like the title menu's buttons (see TitleMenu.add_important).'''
        style = self.context.style
        button.setFont(style.get_font("title_btn"))
        style.mark_menu_button(button)
        button.setCursor(Qt.CursorShape.PointingHandCursor)

    # The page's own buttons

    def add_proxy(self, button: QPushButton) -> QPushButton:
        '''
        A row standing in for one of the page's own buttons on the bar -
        clicking it clicks that button (see replay), so it does exactly what
        the bar's does, however the page set it up. Kept in step with it
        while the menu is open (see sync_proxies).
        '''
        proxy = QPushButton(button.text())
        self.style_row(proxy)
        proxy.setToolTip(button.toolTip())
        proxy.setEnabled(button.isEnabled())
        # Its dropdown opens on hover once another's is open, like the bar's (see Overlay._switch_to_hovered)
        proxy.setProperty("opens_overlay", button.property("opens_overlay"))
        proxy.clicked.connect(lambda checked=False: self.replay(button, proxy))
        self.proxies.append((button, proxy))
        return proxy

    def replay(self, button: QPushButton, proxy: QPushButton):
        '''
        Clicks the bar's button - a dropdown opening beside the menu,
        anchored to the row (see MenuBar._replay_click), and anything else
        after the menu closes.
        '''
        overlay = self.overlay_of(button)
        if overlay is None:
            self.close()
            button.click()
            return
        anchor, overlay.anchor = overlay.anchor, "east"
        button.click_proxy = proxy
        try:
            button.click()
        finally:
            button.click_proxy = None
            overlay.anchor = anchor
        self.watch(overlay)
        proxy.setText(button.text())

    def overlay_of(self, button: QPushButton) -> Overlay | None:
        '''The overlay button opens, if it opens one.'''
        if not button.property("opens_overlay"):
            return None
        return next((overlay for overlay in self.root.findChildren(Overlay) if overlay.button is button), None)

    def sync_proxies(self):
        '''
        The bar's buttons change their text (a toggle, a dropdown's caret)
        and whether they're enabled from anywhere, with no signal to say so
        - so their rows follow them each frame while the menu is open.
        '''
        try:
            for button, proxy in self.proxies:
                if proxy.text() != button.text():
                    proxy.setText(button.text())
                if proxy.isEnabled() != button.isEnabled():
                    proxy.setEnabled(button.isEnabled())
        except RuntimeError:
            # The page (or the menu) was torn down mid-frame
            self.context.animation_manager.remove_callback(self.sync_name)

    def watch(self, overlay: Overlay):
        '''
        A dropdown opened from the menu: once it closes, so does the menu -
        a choice was made - unless the mouse is back over the menu (closing
        it to pick something else).
        '''
        if overlay in self.watched or self.dim is None:
            return
        self.watched.append(overlay)
        _OnHide(self.dim, overlay, self.dropdown_closed)

    def dropdown_closed(self):
        if self.drawer is None or not self.is_open():
            return
        try:
            over_menu = self.drawer.rect().contains(self.drawer.mapFromGlobal(QCursor.pos()))
        except RuntimeError:
            return
        if not over_menu:
            self.close()

    # What's running

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
