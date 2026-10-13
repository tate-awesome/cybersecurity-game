from PySide6.QtGui import QKeySequence, QShortcut


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .. import Context

# Rebindable actions -> their default key sequence ("" = unbound). Set on the
# settings page's General tab, saved in preferences.json as "keybinds".
DEFAULT_KEYBINDS = {
    "zoom_in": "Ctrl++",
    "zoom_out": "Ctrl+-",
    "zoom_reset": "",
    "fullscreen": "F11",
}

# Extra sequences bound alongside one - Ctrl + is Shift = on most keyboards,
# so Ctrl = (no Shift) works too
ALIASES = {"Ctrl++": ["Ctrl+="]}


class KeyBinds:
    '''
    Adds global keybinds and event handlers to the app.
    Includes the rebindable zoom controls and fullscreen toggle (see
    DEFAULT_KEYBINDS), and the performance overlay (F3).
    Also runs Router.quit() when the window is closed.

    Kept on the context (context.keybinds) - PySide drops a connection to a
    bound method once its object is garbage collected, so an unreferenced
    KeyBinds would leave every shortcut dead.
    '''

    def __init__(self, context: "Context"):
        '''
        Binds all events
        '''
        self.context = context
        self.root = context.root
        self.refresh = context.router.refresh
        self.quit = context.router.quit

        self.handlers = {
            "zoom_in": self.zoom_in,
            "zoom_out": self.zoom_out,
            "zoom_reset": self.zoom_reset,
            "fullscreen": self.toggle_fullscreen,
        }
        self.shortcuts: dict[str, list[QShortcut]] = {action: [] for action in DEFAULT_KEYBINDS}
        self.load()

        # Performance overlay (see Performance)
        self._shortcut("F3", context.performance.toggle_overlay)

        # On close event - MainWindow (see app.py) calls root.on_close
        # instead of exposing a Qt virtual method to override here.
        self.root.on_close = self.quit

        # Whether the window starts fullscreen is App's to apply (see App.show_window)

    def _shortcut(self, sequence: str, handler) -> QShortcut:
        shortcut = QShortcut(QKeySequence(sequence), self.root)
        shortcut.activated.connect(handler)
        return shortcut

    # Rebinding
    def sequence(self, action: str) -> str:
        '''The action's key sequence, in portable text ("" when unbound).'''
        shortcuts = self.shortcuts[action]
        return shortcuts[0].key().toString() if shortcuts else ""

    def bind(self, action: str, sequence: str):
        for shortcut in self.shortcuts[action]:
            shortcut.setParent(None)
            shortcut.deleteLater()
        self.shortcuts[action] = []
        sequence = QKeySequence(sequence).toString()  # normalized, so the same keys always compare equal
        if not sequence:
            return
        for keys in [sequence, *ALIASES.get(sequence, [])]:
            self.shortcuts[action].append(self._shortcut(keys, self.handlers[action]))

    def rebind(self, action: str, sequence: str) -> list[str]:
        '''
        Binds and saves the action's keys. Any other action already on those
        keys is unbound (two shortcuts on one key would both stop working) -
        returns those actions.
        '''
        sequence = QKeySequence(sequence).toString()
        taken = [other for other in DEFAULT_KEYBINDS if other != action and sequence and self.sequence(other) == sequence]
        for other in taken:
            self.bind(other, "")
        self.bind(action, sequence)
        self.save()
        return taken

    def load(self):
        '''Binds every action to its saved keys - its default where none are saved.'''
        saved = self.context.preferences.get("keybinds")
        saved = saved if isinstance(saved, dict) else {}
        for action, default in DEFAULT_KEYBINDS.items():
            sequence = saved.get(action, default)
            self.bind(action, sequence if isinstance(sequence, str) else default)

    def reset(self):
        for action, default in DEFAULT_KEYBINDS.items():
            self.bind(action, default)
        self.save()

    def save(self):
        self.context.preferences.set("keybinds", {action: self.sequence(action) for action in DEFAULT_KEYBINDS})

    def describe(self) -> list[tuple[str, str]]:
        '''(keys as shown to the player, action) for every bound action, then F3.'''
        bound = [(QKeySequence(self.sequence(action)).toString(QKeySequence.SequenceFormat.NativeText), action)
                 for action in DEFAULT_KEYBINDS if self.sequence(action)]
        return [*bound, ("F3", "performance")]

    # Fullscreen
    def set_fullscreen(self, enabled: bool, save: bool = False):
        if save:
            self.context.preferences.set("fullscreen", enabled)
        if enabled:
            self.root.showFullScreen()
        else:
            self.root.showNormal()

    def toggle_fullscreen(self):
        self.set_fullscreen(not self.root.isFullScreen(), save=True)

    # Zoom - context.style, not a copy, since deleting user data replaces it
    def zoom_in(self, event=None):
        style = self.context.style
        next_index = style.ui_scales.index(int(style.ui_scale)) + 1
        if next_index >= len(style.ui_scales):
            return
        style.ui_scale = float(style.ui_scales[next_index])
        self.refresh()


    def zoom_out(self, event=None):
        style = self.context.style
        next_index = style.ui_scales.index(int(style.ui_scale)) - 1
        if next_index < 0:
            return
        style.ui_scale = float(style.ui_scales[next_index])
        self.refresh()


    def zoom_reset(self, event=None):
        self.context.style.ui_scale = 100.0
        self.refresh()
