from PySide6.QtCore import QEvent, QObject
from PySide6.QtWidgets import QApplication
from .callback_registry import CallbackRegistry


class _GlobalClickFilter(QObject):
    '''
    Installing an event filter requires a QObject; ClickManager isn't one
    (it's a plain CallbackRegistry, like AnimationManager), so this tiny
    helper just forwards every mouse press back to it.
    '''
    def __init__(self, manager: "ClickManager"):
        super().__init__()
        self.manager = manager

    def eventFilter(self, watched, event):
        if event.type() == QEvent.Type.MouseButtonPress:
            self.manager.dispatch(watched, event)
        return False


class ClickManager(CallbackRegistry):
    '''
    Global click manager for evil annoying features
    '''
    def __init__(self, root):
        super().__init__(root, tag="[Click]")

        # Install the global listener ONCE on the application, so it sees
        # every mouse press regardless of which widget it lands on.
        self.app = QApplication.instance()
        self._filter = _GlobalClickFilter(self)
        self.app.installEventFilter(self._filter)

        self.add_listener("click_focus", self.click_to_focus)

    def add_listener(self, name: str, callback_func):
        self.add_callback(name, callback_func)

    def remove_listener(self, name: str):
        self.remove_callback(name)

    def delete(self):
        super().delete()
        self.app.removeEventFilter(self._filter)

    def click_to_focus(self, widget=None, event=None):
        if widget is not None and hasattr(widget, "setFocus"):
            widget.setFocus()
