import sys

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QMainWindow

from .router import Router
from .transitions import WindowReveal


class MainWindow(QMainWindow):
    '''
    QMainWindow can't have its closeEvent overridden by simply assigning an
    instance attribute (Qt dispatches virtual methods like closeEvent
    through the class, not the instance), so this thin subclass exists
    purely to forward the close event to whatever callable is set as
    on_close - KeyBinds wires this up to Router.quit.
    '''

    def __init__(self):
        super().__init__()
        self.on_close = None

    def closeEvent(self, event):
        if self.on_close is not None:
            self.on_close()
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
        router = Router(self.root, start_page)
        # Once the first page is up and the event loop has come round
        QTimer.singleShot(0, router.context.performance.app_started)
        QTimer.singleShot(0, lambda: WindowReveal.reveal(self.root))

        # Start the main loop
        sys.exit(self.app.exec())


    def set_geometry(self):
        '''
        Shows the window maximized, but transparent until WindowReveal fades
        it in. KeyBinds then makes it fullscreen, if that's the preference,
        before the event loop starts - so neither shows as a step on screen.
        '''
        # Only the size it restores to if un-maximized - never shown at startup
        f = 3.0/4.0
        screen = self.app.primaryScreen().availableGeometry()
        self.root.resize(int(f*screen.width()), int(f*screen.height()))
        WindowReveal.hide(self.root)
        self.root.showMaximized()