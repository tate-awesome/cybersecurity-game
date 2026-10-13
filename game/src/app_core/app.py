import sys

from PySide6.QtCore import QEvent, Qt, QTimer, Signal
from PySide6.QtWidgets import QApplication, QMainWindow

from .router import Router
from .transitions import FadeIn, WindowReveal
from ..widgets import VisualBackground


class MainWindow(QMainWindow):
    '''
    QMainWindow can't have its closeEvent overridden by simply assigning an
    instance attribute (Qt dispatches virtual methods like closeEvent
    through the class, not the instance), so this thin subclass exists
    purely to forward the close event to whatever callable is set as
    on_close - KeyBinds wires this up to Router.quit.

    fullscreen_changed is emitted with whether it's fullscreen now, however
    that changed (F11, the settings checkbox, deleting user data) - for
    controls that show it.
    '''

    fullscreen_changed = Signal(bool)

    def __init__(self):
        super().__init__()
        self.on_close = None

    def changeEvent(self, event):
        if event.type() == QEvent.Type.WindowStateChange:
            fullscreen = self.isFullScreen()
            if fullscreen != bool(event.oldState() & Qt.WindowState.WindowFullScreen):
                self.fullscreen_changed.emit(fullscreen)
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

        # Start a Qt app
        self.app = QApplication.instance() or QApplication(sys.argv)

        self.root = MainWindow()
        self.root.setWindowTitle(title)
        self.set_geometry()

        # Create the router, which will handle page navigation
        router = Router(self.root)
        context = router.context
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
            self.fade_in.play(lambda: self.show_window(context, fade=False),
                              lambda: self.release_first_page(router))
        else:
            self.show_window(context)
            router.start(start_page)
            # Once the first page is up and the event loop has come round
            QTimer.singleShot(0, context.performance.app_started)

        # Start the main loop
        sys.exit(self.app.exec())


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
        Shows the window maximized, or fullscreen if that's the preference -
        transparent at first, until WindowReveal fades it in (see there).
        fade=False shows it straight away - for FadeIn, which covers it
        until it's painted (just the background color, see hold_first_page).
        '''
        if fade:
            WindowReveal.hide(self.root)
        if context.preferences.is_fullscreen():
            self.root.showFullScreen()
        else:
            self.root.showMaximized()
        if fade:
            # Counted from when the event loop is running, not from now
            QTimer.singleShot(0, lambda: WindowReveal.reveal(self.root))


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
