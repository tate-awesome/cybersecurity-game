import sys

from PySide6.QtCore import QEvent, QObject, QPoint, QPointF, Qt
from PySide6.QtGui import QColor, QCursor, QMouseEvent, QPainter
from PySide6.QtWidgets import QApplication, QHBoxLayout, QPushButton, QSizePolicy, QStyle, QWidget

from ...app_core import Context

# How far in from the window's edge a press resizes it rather than reaching
# the page, and how far along an edge from a corner it still takes the corner
EDGE = 6
CORNER = 16

# The close button's hover color - the same red whatever the theme, since
# it's the one control that ends the app
CLOSE_HOVER = "#c42b1c"


class NativeFrame:
    '''
    Windows only: gives the borderless window its native resizable frame
    back, then has the window's content cover it (WM_NCCALCSIZE) - so it
    still looks borderless, but Windows treats it as an ordinary resizable
    window: dragging it to the top of the screen maximizes it, to a side
    snaps it, and minimizing/restoring animate. A frameless window without
    the frame (Qt's FramelessWindowHint alone) gets none of that.

    Maximized, Windows hangs the frame off the screen's edges - the content
    is pulled in by that much, or its edges would be cut off.
    '''

    WM_NCCALCSIZE = 0x0083
    GWL_STYLE = -16
    WS_THICKFRAME = 0x00040000
    WS_CAPTION = 0x00C00000
    # SetWindowPos: NOSIZE | NOMOVE | NOZORDER | NOACTIVATE | FRAMECHANGED
    SWP_REFRAME = 0x0001 | 0x0002 | 0x0004 | 0x0010 | 0x0020
    # GetSystemMetricsForDpi: SM_CXSIZEFRAME, SM_CYSIZEFRAME, SM_CXPADDEDBORDER
    SM_CXSIZEFRAME, SM_CYSIZEFRAME, SM_CXPADDEDBORDER = 32, 33, 92

    def __init__(self):
        import ctypes
        from ctypes import wintypes

        class NCCALCSIZE_PARAMS(ctypes.Structure):
            _fields_ = [("rgrc", wintypes.RECT * 3), ("lppos", ctypes.c_void_p)]

        self.user32 = ctypes.windll.user32
        self.MSG = wintypes.MSG
        self.NCCALCSIZE_PARAMS = NCCALCSIZE_PARAMS

    @staticmethod
    def make() -> "NativeFrame | None":
        '''A NativeFrame on Windows, None anywhere else.'''
        if sys.platform != "win32":
            return None
        try:
            return NativeFrame()
        except Exception as error:
            print(f"Native window frame unavailable: {error}")
            return None

    def apply(self, window: QWidget):
        '''Adds the frame back to window's native window. Harmless to repeat.'''
        hwnd = int(window.winId())
        style = self.user32.GetWindowLongW(hwnd, self.GWL_STYLE)
        wanted = style | self.WS_THICKFRAME | self.WS_CAPTION
        if wanted != style:
            self.user32.SetWindowLongW(hwnd, self.GWL_STYLE, wanted)
            self.user32.SetWindowPos(hwnd, 0, 0, 0, 0, 0, self.SWP_REFRAME)

    def native_event(self, message) -> tuple[bool, int] | None:
        '''For QWidget.nativeEvent - the result for a message handled here, None for the rest.'''
        msg = self.MSG.from_address(int(message))
        if msg.message != self.WM_NCCALCSIZE or not msg.wParam:
            return None
        if self.user32.IsZoomed(msg.hWnd):
            params = self.NCCALCSIZE_PARAMS.from_address(msg.lParam)
            dpi = self.user32.GetDpiForWindow(msg.hWnd)
            padding = self.user32.GetSystemMetricsForDpi(self.SM_CXPADDEDBORDER, dpi)
            x = self.user32.GetSystemMetricsForDpi(self.SM_CXSIZEFRAME, dpi) + padding
            y = self.user32.GetSystemMetricsForDpi(self.SM_CYSIZEFRAME, dpi) + padding
            rect = params.rgrc[0]
            rect.left += x
            rect.right -= x
            rect.top += y
            rect.bottom -= y
            params.rgrc[0] = rect
        # The whole window is content - no frame or title bar drawn
        return True, 0


class WindowEdges(QObject):
    '''
    Resizing for the borderless window (see MainWindow): pressing within
    EDGE of a side, or CORNER of a corner, hands the drag to the system
    (QWindow.startSystemResize), with the matching resize cursor while
    hovering there. Only while the window is neither maximized nor
    fullscreen - then there's nothing to resize.

    Watches the window itself rather than its widgets: the window sees
    every mouse move, where a widget only does with mouse tracking on.

    Also pulls the mouse back onto the window's last pixel at its right
    and bottom edges (see clamped). At a fractional display scale (150%,
    say) the screen's last physical pixel is a fraction past the window's
    last logical one - 2559.33 in a 2560-wide window - and Qt hands
    widgets nothing there, so the close button, which runs to the corner,
    stopped being hovered or clickable right at the screen's edge.
    '''

    MOUSE_EVENTS = (QEvent.Type.MouseMove, QEvent.Type.MouseButtonPress,
                    QEvent.Type.MouseButtonRelease, QEvent.Type.MouseButtonDblClick)

    def __init__(self, root: QWidget):
        super().__init__(root)
        self.root = root
        # Whether our resize cursor is the one showing (an override cursor)
        self.cursor_shown = False
        root.windowHandle().installEventFilter(self)

    def edges_at(self, pos: QPoint) -> Qt.Edge:
        '''The window edges a point (in window coordinates) is on, none if it's inside.'''
        edges = Qt.Edge(0)
        root = self.root
        if root.isMaximized() or root.isFullScreen() or root.isMinimized():
            return edges
        x, y, w, h = pos.x(), pos.y(), root.width(), root.height()
        near_left, near_right = x < CORNER, x >= w - CORNER
        near_top, near_bottom = y < CORNER, y >= h - CORNER
        if x < EDGE or (near_left and (y < EDGE or y >= h - EDGE)):
            edges |= Qt.Edge.LeftEdge
        if x >= w - EDGE or (near_right and (y < EDGE or y >= h - EDGE)):
            edges |= Qt.Edge.RightEdge
        if y < EDGE or (near_top and (x < EDGE or x >= w - EDGE)):
            edges |= Qt.Edge.TopEdge
        if y >= h - EDGE or (near_bottom and (x < EDGE or x >= w - EDGE)):
            edges |= Qt.Edge.BottomEdge
        return edges

    @staticmethod
    def cursor_for(edges: Qt.Edge) -> Qt.CursorShape | None:
        left, right = bool(edges & Qt.Edge.LeftEdge), bool(edges & Qt.Edge.RightEdge)
        top, bottom = bool(edges & Qt.Edge.TopEdge), bool(edges & Qt.Edge.BottomEdge)
        if (left and top) or (right and bottom):
            return Qt.CursorShape.SizeFDiagCursor
        if (right and top) or (left and bottom):
            return Qt.CursorShape.SizeBDiagCursor
        if left or right:
            return Qt.CursorShape.SizeHorCursor
        if top or bottom:
            return Qt.CursorShape.SizeVerCursor
        return None

    def show_cursor(self, shape: Qt.CursorShape | None):
        if shape is None:
            if self.cursor_shown:
                QApplication.restoreOverrideCursor()
                self.cursor_shown = False
            return
        if self.cursor_shown:
            QApplication.changeOverrideCursor(QCursor(shape))
        else:
            QApplication.setOverrideCursor(QCursor(shape))
            self.cursor_shown = True

    def clamped(self, event: QMouseEvent) -> QMouseEvent | None:
        '''
        The event moved onto the window's last whole pixel if it's past it
        (but still in the window - see above), None if it doesn't need to be.
        '''
        pos = event.position()
        right, bottom = self.root.width() - 1, self.root.height() - 1
        if not (right < pos.x() < right + 1 or bottom < pos.y() < bottom + 1):
            return None
        pos = QPointF(min(pos.x(), right), min(pos.y(), bottom))
        return QMouseEvent(event.type(), pos, event.globalPosition(), event.button(), event.buttons(),
                           event.modifiers(), event.pointingDevice())

    def eventFilter(self, watched, event):
        kind = event.type()
        if kind in self.MOUSE_EVENTS and isinstance(event, QMouseEvent):
            clamped = self.clamped(event)
            if clamped is not None:
                QApplication.sendEvent(watched, clamped)
                return True
        if kind == QEvent.Type.MouseMove and isinstance(event, QMouseEvent):
            if event.buttons() == Qt.MouseButton.NoButton:
                self.show_cursor(self.cursor_for(self.edges_at(event.position().toPoint())))
        elif kind == QEvent.Type.MouseButtonPress and isinstance(event, QMouseEvent):
            if event.button() == Qt.MouseButton.LeftButton:
                edges = self.edges_at(event.position().toPoint())
                if edges:
                    self.show_cursor(None)
                    self.root.windowHandle().startSystemResize(edges)
                    return True
        elif kind in (QEvent.Type.Leave, QEvent.Type.WindowStateChange):
            self.show_cursor(None)
        return False


class WindowDrag(QObject):
    '''
    Makes a widget's empty space move the window, like a title bar: drag
    to move it (the system's own move, so Windows' snapping works),
    double-click to maximize or restore it. Presses on its buttons stay
    theirs - only presses the widget itself gets (its own empty space, and
    children that let the mouse through) start a move. A label has to be
    made transparent for mouse events: it passes a press on, but keeps the
    moves after it.

    Dragging a maximized window restores it first, keeping the same part
    of the bar under the cursor. Nothing moves while fullscreen.
    '''

    def __init__(self, widget: QWidget, root: QWidget):
        super().__init__(widget)
        self.root = root
        self.pressed_at: QPoint | None = None
        widget.installEventFilter(self)

    def eventFilter(self, watched, event):
        kind = event.type()
        if not isinstance(event, QMouseEvent) or self.root.isFullScreen():
            return False
        if kind == QEvent.Type.MouseButtonPress and event.button() == Qt.MouseButton.LeftButton:
            self.pressed_at = event.globalPosition().toPoint()
            return True
        if kind == QEvent.Type.MouseMove and self.pressed_at is not None:
            now = event.globalPosition().toPoint()
            if (now - self.pressed_at).manhattanLength() >= QApplication.startDragDistance():
                self.start_move(self.pressed_at, now)
                self.pressed_at = None
            return True
        if kind == QEvent.Type.MouseButtonRelease and event.button() == Qt.MouseButton.LeftButton:
            self.pressed_at = None
            return True
        if kind == QEvent.Type.MouseButtonDblClick and event.button() == Qt.MouseButton.LeftButton:
            self.pressed_at = None
            toggle_maximized(self.root)
            return True
        return False

    def start_move(self, pressed_at: QPoint, now: QPoint):
        '''
        Hands the drag to the system once it's past the drag distance - with
        the window first caught up to the cursor, so the part of the bar
        that was pressed stays under it.
        '''
        root = self.root
        if root.isMaximized():
            if getattr(root, "native_frame", None) is None:
                # Restore under the cursor: the same fraction across the
                # window, the same distance down from its top. (With a
                # NativeFrame, Windows' own move restores it like this.)
                frame = root.frameGeometry()
                across = (pressed_at.x() - frame.x()) / max(1, frame.width())
                down = pressed_at.y() - frame.y()
                root.showNormal()
                QApplication.processEvents()
                normal = root.frameGeometry()
                root.move(round(now.x() - across * normal.width()), now.y() - down)
        else:
            root.move(root.pos() + (now - pressed_at))
        root.windowHandle().startSystemMove()


def window_bar_height(context: Context) -> int:
    '''
    The height of the bar along the top of the window - a page's menu bar
    (see MenuBar.bar_height), or the strip around CornerControls on a page
    without one - so it's the same on every page: a menu bar button's
    height (the tallest thing a bar always has - its dropdowns), with a
    little room above and below.
    '''
    style = context.style
    sample = QPushButton("Ag")
    sample.setFont(style.get_font())
    sample.ensurePolished()
    height = sample.sizeHint().height()
    sample.deleteLater()
    return height + 4 * style.cgap


def window_bar_has_line(context: Context) -> bool:
    '''
    Whether the window bar is underlined on the current page (see
    draw_window_bar_line) - everywhere but workspaces, whose panels already
    start their own row below it.
    '''
    return context.pages.get_build_type(context.router.current_page) != "workspace"


def draw_window_bar_line(widget: QWidget, context: Context):
    '''Underlines the window bar along widget's bottom edge, in the footer's divider color (the text, faint).'''
    line = QColor(context.style.color("text"))
    line.setAlpha(70)
    painter = QPainter(widget)
    painter.setPen(line)
    painter.drawLine(0, widget.height() - 1, widget.width(), widget.height() - 1)
    painter.end()


class _Strip(QWidget):
    '''CornerControls' strip across the top of the window - see-through, but underlined where the window bar is (see window_bar_has_line).'''

    def __init__(self, context: Context):
        super().__init__(context.root)
        self.context = context
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

    def paintEvent(self, event):
        if window_bar_has_line(self.context):
            draw_window_bar_line(self, self.context)


def toggle_maximized(root: QWidget):
    '''Maximizes the window, or restores it if it already is - never while fullscreen.'''
    if root.isFullScreen():
        return
    if root.isMaximized():
        root.showNormal()
    else:
        root.showMaximized()


class WindowControls(QWidget):
    '''
    Minimize, maximize/restore and close, for the borderless window - at
    the right end of a page's menu bar (see MenuBar), or by themselves in
    the corner of a page that has no menu bar (see CornerControls).
    Hidden while fullscreen, where the window has nothing to minimize to
    or restore from - F11 or the settings page leave fullscreen.

    Each shows one of style.ICONS (see ICONS here), with its name as a
    labels key tooltip ("window_controls_tooltips_<name>").
    '''

    # Each control's icon (see style.ICONS) - close is a power symbol, since
    # closing the window quits the game
    ICONS = {"minimize": "minus", "maximize": "square", "restore": "copy", "close": "power"}

    def __init__(self, context: Context, parent: QWidget | None = None):
        super().__init__(parent)
        self.context = context
        self.style = context.style
        self.root = context.root
        self.setObjectName(f"_window_controls_{id(self)}")
        row = QHBoxLayout(self)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(0)

        self.minimize = self._button("minimize", self.root.showMinimized)
        self.maximize = self._button("maximize", lambda: toggle_maximized(self.root))
        self.close_button = self._button("close", self.root.close)
        self.close_button.setProperty("close", True)
        for button in (self.minimize, self.maximize, self.close_button):
            row.addWidget(button)

        self.style.live_style(self, self.sheet)
        self.root.fullscreen_changed.connect(self.follow_window)
        self.root.window_state_changed.connect(self.follow_window)
        self.follow_window()

    def _button(self, name: str, action) -> QPushButton:
        button = QPushButton(self.style.icon(self.ICONS[name]))
        button.setFont(self.style.get_font("icon"))
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        button.setToolTip(self.label(f"tooltips_{name}"))
        # As tall as whatever holds them - in a menu bar, its whole height
        button.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        button.clicked.connect(lambda checked=False: action())
        return button

    def label(self, key: str) -> str:
        return self.context.labels.get(f"window_controls_{key}")

    def sheet(self) -> str:
        name = self.objectName()
        text = self.style.color("text")
        return (f"QWidget#{name} QPushButton {{ background: transparent; border: none; color: {text}; {self.style.icon_css()}"
                f" padding: 0px {self.style.igap}px; }}"
                f" QWidget#{name} QPushButton:hover {{ background: {self.style.css('card')}; color: {self.style.color('accent')}; }}"
                f" QWidget#{name} QPushButton[close=\"true\"]:hover {{ background: {CLOSE_HOVER}; color: white; }}"
                f" QWidget#{name} QPushButton:pressed {{ color: {text}; }}")

    def follow_window(self, *args):
        '''Hidden while fullscreen; the maximize button says restore while maximized.'''
        try:
            # Never shown while parentless - it would open as a window of its own
            if self.parentWidget() is not None:
                self.setVisible(not self.root.isFullScreen())
            maximized = self.root.isMaximized()
            self.maximize.setText(self.style.icon(self.ICONS["restore" if maximized else "maximize"]))
            self.maximize.setToolTip(self.label("tooltips_restore" if maximized else "tooltips_maximize"))
        except RuntimeError:
            pass  # deleted with its page, with the signal still connected


class CornerControls(WindowControls):
    '''
    WindowControls floating over the top right of the window, for pages
    without a menu bar to hold them (the title pages) - with the buttons
    every page has beside them (see menu_bar.global_buttons), and the strip
    across the top of the window around them moving it, as a title bar
    would. Belongs to the window, like the Footer: Router calls
    page_changed after each page is built.
    '''

    def __init__(self, context: Context):
        super().__init__(context, context.root)
        self.strip = _Strip(context)
        WindowDrag(self.strip, context.root)
        # Debug, Appearance, Settings and Help - built afresh for each page
        # without a menu bar (see page_changed), so they follow the theme,
        # zoom, labels and developer mode like a menu bar's do
        self.buttons: QWidget | None = None
        context.root.installEventFilter(self)
        self.page_changed()

    def eventFilter(self, watched, event):
        if event.type() == QEvent.Type.Resize:
            self.place()
        return False

    def page_has_menu_bar(self) -> bool:
        page = self.root.centralWidget()
        if page is None:
            return False
        from .menu_bar import MenuBar
        return any(isinstance(child, MenuBar) for child in page.findChildren(QWidget, options=Qt.FindChildOption.FindDirectChildrenOnly))

    @staticmethod
    def spacing() -> int:
        '''The space between these buttons - a menu bar row's (the style's), so they sit just where a menu bar's do.'''
        return QApplication.style().pixelMetric(QStyle.PixelMetric.PM_LayoutHorizontalSpacing)

    def wanted(self) -> bool:
        '''Whether the page showing has no menu bar of its own, so these stand in for one.'''
        return self.root.centralWidget() is not None and not self.page_has_menu_bar()

    def page_changed(self):
        if self.buttons is not None:
            self.buttons.hide()
            self.buttons.deleteLater()
            self.buttons = None
        if self.wanted():
            from .menu_bar import global_buttons
            self.buttons = global_buttons(self.context, self.spacing())
            self.buttons.setParent(self.root)
        self.place()

    def place(self):
        '''
        Across the top of the window, over the page, as tall as a menu bar
        (see window_bar_height) - unless the page's own menu bar has these.
        The window controls hide while fullscreen, like a menu bar's; the
        other buttons and the strip stay.
        '''
        try:
            wanted = self.wanted()
            controls = wanted and not self.root.isFullScreen()
            width = self.sizeHint().width() if controls else 0
            height = window_bar_height(self.context)
            self.setGeometry(self.root.width() - width, 0, width, height)
            # The whole width, under the controls too, so its line runs to the edge
            self.strip.setGeometry(0, 0, self.root.width(), height)
            self.strip.update()
            self.setVisible(controls)
            self.strip.setVisible(wanted)
            if self.buttons is not None:
                buttons_width = self.buttons.sizeHint().width()
                gap = self.spacing() if controls else 0
                self.buttons.setGeometry(self.root.width() - width - gap - buttons_width, 0, buttons_width, height)
                self.buttons.setVisible(wanted)
            if wanted:
                self.strip.raise_()
                if self.buttons is not None:
                    self.buttons.raise_()
                self.raise_()
        except RuntimeError:
            pass

    def follow_window(self, *args):
        super().follow_window(*args)
        if hasattr(self, "strip"):
            self.place()
