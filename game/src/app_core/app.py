import sys

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QMainWindow

from .router import Router


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


class App():
    '''
    Creates the Router and starts the GUI main loop
    '''

    def __init__(self, start_page: str | None = None, title="Game", start_fullscreen = False):
        '''
        start_page: page key to open first. If None, the Router reads it
        from the manifest's "startup_page" instead.
        '''

        # Start a Qt app
        self.app = QApplication.instance() or QApplication(sys.argv)

        self.root = MainWindow()
        self.root.setWindowTitle(title)
        self.set_geometry(start_fullscreen)
        self.root.show()

        # Create the router, which will handle page navigation
        Router(self.root, start_page)

        # Start the main loop
        sys.exit(self.app.exec())


    def set_geometry(self, start_fullscreen):
        '''
        Sets the size and position of the window, then starts maximized or fullscreen
        '''
        f = 3.0/4.0
        screen = self.app.primaryScreen().availableGeometry()
        w = int(f*screen.width())
        h = int(f*screen.height())
        self.root.resize(w, h)

        if start_fullscreen:
            self.root.showFullScreen()
        else:
            QTimer.singleShot(
                50,
                self.maximize
            )


    def maximize(self):
        self.root.showMaximized()