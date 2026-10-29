import ctypes, sys

from PySide6.QtCore import QEvent, Qt, QTimer, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow

from .router import Router
from .transitions import FadeIn, WindowReveal
from ..widgets import VisualBackground

# Names the app to the OS for its taskbar entry (see App.set_icon) - the
# Windows AppUserModelID, and on Linux the .desktop file's name
APP_ID = "cybergame"


class MainWindow(QMainWindow):
    '''
    QMainWindow can't have its closeEvent overridden by simply assigning an
    instance attribute (Qt dispatches virtual methods like closeEvent
    through the class, not the instance), so this thin subclass exists
    purely to forward the close event to whatever callable is set as
    on_close - KeyBinds wires this up to Router.quit.

    fullscreen_changed is emitted with whether it's fullscreen now, however
    that changed (F11, the settings checkbox, deleting user data) - for
    controls that show it. window_state_changed is emitted on any change
    of state (maximized, minimized, fullscreen, normal).

    The window is borderless in and out of fullscreen, so pages meet the
    top of the window the same way in both: the app draws its own window
    controls and title bar dragging (see window_chrome), and WindowEdges
    gives back resizing by the edges.
    '''

    fullscreen_changed = Signal(bool)
    window_state_changed = Signal()

    # Frameless, but still with a system menu and minimize/maximize boxes -
    # on Windows those are what let clicking the taskbar button minimize it
    WINDOW_FLAGS = (Qt.WindowType.Window | Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowSystemMenuHint
                    | Qt.WindowType.WindowMinimizeButtonHint | Qt.WindowType.WindowMaximizeButtonHint)

    def __init__(self):
        super().__init__()
        self.on_close = None
        self.setWindowFlags(self.WINDOW_FLAGS)
        # Where leaving fullscreen goes back to (see set_fullscreen) - maximized,
        # unless it was a normal window when fullscreen came on
        self.maximized_before_fullscreen = True
        self.edges = None  # WindowEdges, once the native window exists (see showEvent)
        from ..widgets.frame_widgets.window_chrome import NativeFrame
        self.native_frame = NativeFrame.make()

    def showEvent(self, event):
        if self.edges is None:
            from ..widgets.frame_widgets.window_chrome import WindowEdges
            self.edges = WindowEdges(self)
        self.apply_native_frame()
        super().showEvent(event)

    def apply_native_frame(self):
        '''
        Gives back the native frame (see NativeFrame) - again after leaving
        fullscreen, which restores the window style from before it.
        '''
        if self.native_frame is not None and not self.isFullScreen():
            self.native_frame.apply(self)

    def nativeEvent(self, event_type, message):
        if self.native_frame is not None:
            handled = self.native_frame.native_event(message)
            if handled is not None:
                return handled
        return super().nativeEvent(event_type, message)

    def set_fullscreen(self, enabled: bool):
        '''Fullscreen, or back to however the window was before it - maximized or not.'''
        if enabled:
            if not self.isFullScreen():
                self.maximized_before_fullscreen = self.isMaximized()
            self.showFullScreen()
        elif self.maximized_before_fullscreen:
            self.showMaximized()
        else:
            self.showNormal()

    def changeEvent(self, event):
        if event.type() == QEvent.Type.WindowStateChange:
            fullscreen = self.isFullScreen()
            if fullscreen != bool(event.oldState() & Qt.WindowState.WindowFullScreen):
                self.fullscreen_changed.emit(fullscreen)
            self.window_state_changed.emit()
            # Once the state change is done with the window style
            QTimer.singleShot(0, self.apply_native_frame)
        super().changeEvent(event)

    def closeEvent(self, event):
        # on_close returns True while it's closing the window itself (FadeOut
        # playing) - kept open until then. Otherwise accepted: Qt 6's quit()
        # closes every window first, and gives up quitting if one refuses
        if self.on_close is not None and self.on_close():
            event.ignore()
        else:
            event.accept()


class App:
    '''
    Creates the Router and starts the GUI main loop
    '''

    def __init__(self, start_page: str | None = None, title="Game"):
        '''
        start_page: page key to open first. If None, the Router opens
        its START_PAGE.
        '''

        # Before any window exists - see set_icon
        if sys.platform == "win32":
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_ID)

        # Start a Qt app
        self.app = QApplication.instance() or QApplication(sys.argv)
        self.app.setDesktopFileName(APP_ID)

        self.root = MainWindow()
        self.root.setWindowTitle(title)
        self.set_geometry()

        # Create the router, which will handle page navigation
        router = Router(self.root)
        context = router.context
        self.set_icon(context)
        if context.preferences.is_fade_in():
            # The background color fades in on the desktop, the window shows
            # under it, then the first page comes in (see FadeIn). The page
            # is built now, while the window is hidden, so it's ready to
            # come in the moment the fade ends
            self.hold_first_page(router, start_page)
            screen = self.app.primaryScreen()
            area = screen.geometry() if context.preferences.is_fullscreen() else screen.availableGeometry()
            # Kept referenced - a window with no parent and no reference is deleted by Python mid-fade
            self.fade_in = FadeIn(area, context.style.color("root"))
            self.fade_in.play(self.root, lambda: self.show_window(context, fade=False),
                              lambda: self.uncovered(router))
        else:
            self.show_window(context)
            router.start(start_page)
            # Once the first page is up and the event loop has come round
            QTimer.singleShot(0, context.performance.app_started)

        # Start the main loop
        sys.exit(self.app.exec())


    def set_icon(self, context):
        '''
        The icon for every window, which is what the taskbar shows. On
        Windows, run from source, the taskbar would group the window under
        python.exe and show its icon instead - the AppUserModelID set before
        the QApplication gives the game its own taskbar entry. On Linux, X11
        takes the window icon as is; Wayland ignores it on most desktops and
        looks up an installed .desktop file named by setDesktopFileName
        instead (APP_ID.desktop), falling back to a generic icon without one.
        '''
        icon = QIcon(str(context.paths.icons / "app.png"))
        if not icon.isNull():
            self.app.setWindowIcon(icon)


    def set_geometry(self):
        '''
        Sizes the window for when it isn't maximized or fullscreen - never
        how it starts (see show_window).
        '''
        f = 3.0/4.0
        screen = self.app.primaryScreen().availableGeometry()
        self.root.resize(int(f*screen.width()), int(f*screen.height()))


    def show_window(self, context, fade: bool = True):
        '''
        Shows the window maximized, or fullscreen if that's the preference,
        and focused - transparent at first, until WindowReveal fades it in
        (see there).
        fade=False shows it straight away and unfocused - for FadeIn, which
        covers it until it's painted (just the background color, see
        hold_first_page) and focuses it once uncovered (see uncovered).
        '''
        if fade:
            WindowReveal.hide(self.root)
        if context.preferences.is_fullscreen():
            self.root.showFullScreen()
        else:
            self.root.showMaximized()
        if fade:
            self.focus_window()
            # Counted from when the event loop is running, not from now
            QTimer.singleShot(0, lambda: WindowReveal.reveal(self.root))


    def focus_window(self):
        '''
        Takes focus, so the fade in plays in front rather than behind
        whatever had it. Not while FadeIn covers the window - a focused
        fullscreen window can go above it on Linux before it's painted.
        '''
        self.root.raise_()
        self.root.activateWindow()


    def uncovered(self, router: Router):
        '''Once FadeIn is gone: the window takes focus and the first page comes in.'''
        self.focus_window()
        self.release_first_page(router)


    def hold_first_page(self, router: Router, start_page: str | None):
        '''
        For FadeIn: builds the first page with everything held back - its
        page transition paused before any widget shows, the footer hidden
        and the background just its color - until release_first_page.
        '''
        router.start(start_page)
        QTimer.singleShot(0, router.context.performance.app_started)
        if router.transition is not None and router.transition.animation is not None:
            router.transition.animation.pause()
        router.footer.hold()
        background = getattr(router.current_frame, "background", None)
        if isinstance(background, VisualBackground):
            background.hold()

    def release_first_page(self, router: Router):
        '''After FadeIn: the first page comes in, and only then does its background animation start.'''
        transition = router.transition
        delay = 0
        if transition is not None and transition.animation is not None:
            transition.animation.resume()
            delay = transition.animation.duration() - transition.animation.currentTime()
        router.footer.release()
        background = getattr(router.current_frame, "background", None)
        if isinstance(background, VisualBackground):
            # Deleted with its page if that's left first - Qt then drops the timer
            QTimer.singleShot(delay, background.release)
