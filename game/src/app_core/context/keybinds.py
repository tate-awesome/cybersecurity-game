from PySide6.QtCore import QTimer
from PySide6.QtGui import QKeySequence, QShortcut

from .style import Style

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .. import Context

class KeyBinds:
    '''
    Adds global keybinds and event handlers to the app.
    Includes zoom controls (Ctrl +, Ctrl -, Ctrl 0), fullscreen toggle (F11), and exit fullscreen (Escape).
    Also runs Router.quit() when the window is closed.
    '''

    def __init__(self, context: "Context"):
        '''
        Binds all events
        '''
        self.context = context
        self.root = context.root
        self.style = context.style
        self.refresh = context.router.refresh
        self.quit = context.router.quit

        # Page zoom control
        self._shortcut("Ctrl++", self.zoom_in)
        self._shortcut("Ctrl+=", self.zoom_in)  # (linux) Ctrl = also works as Ctrl +
        self._shortcut("Ctrl+-", self.zoom_out)
        self._shortcut("Ctrl+0", self.zoom_default)

        # Fullscreen control
        self._shortcut("F11", self.toggle_fullscreen)
        self._shortcut("Esc", self.exit_fullscreen)

        # On close event - MainWindow (see app.py) calls root.on_close
        # instead of exposing a Qt virtual method to override here.
        self.root.on_close = self.quit

        # Stored as a string ("True"/"False") like the rest of preferences.json.
        if self.context.preferences.get("fullscreen") == "True":
            QTimer.singleShot(50, lambda: self.set_fullscreen(True))

    def _shortcut(self, sequence: str, handler):
        shortcut = QShortcut(QKeySequence(sequence), self.root)
        shortcut.activated.connect(handler)

    def set_fullscreen(self, enabled: bool):
        if enabled:
            self.root.showFullScreen()
        else:
            self.root.showNormal()

    def toggle_fullscreen(self):
        switch_fullscreen = not self.root.isFullScreen()
        self.context.preferences.set("fullscreen", str(switch_fullscreen))
        self.set_fullscreen(switch_fullscreen)

    def exit_fullscreen(self):
        self.set_fullscreen(False)


    def zoom_in(self, event=None):
        next_index = self.style.ui_scales.index(int(self.style.ui_scale)) + 1
        if next_index >= len(self.style.ui_scales):
            return
        self.style.ui_scale = float(self.style.ui_scales[next_index])
        self.refresh()


    def zoom_out(self, event=None):
        next_index = self.style.ui_scales.index(int(self.style.ui_scale)) - 1
        if next_index < 0:
            return
        self.style.ui_scale = float(self.style.ui_scales[next_index])
        self.refresh()


    def zoom_default(self, event=None):
        self.style.ui_scale = 100.0
        self.refresh()

    
    def print_key(self, e):
        print(e.keysym, e.state)