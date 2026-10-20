from PySide6.QtCore import QEvent, QObject
from PySide6.QtWidgets import QApplication
from .callback_registry import CallbackRegistry


class _GlobalClickFilter(QObject):
    '''
    Installing an event filter requires a QObject; ClickManager isn't one
    (it's a plain CallbackRegistry, like AnimationManager), so this tiny
    helper just forwards every mouse press back to it.

    It also drops a double click whose first click landed on another
    widget: the second click of a double click comes as a double click
    event, which a button takes as a press - so double clicking a link
    clicked whatever the next page put under the mouse (the select
    page's first workspace, from the title page's Workspaces button).
    '''
    def __init__(self, manager: "ClickManager"):
        super().__init__()
        self.manager = manager
        # The widget under the mouse at the last press, and that press's timestamp -
        # an event's filtered again for each parent it's passed up to
        self.pressed_on = None
        self.pressed_at = None

    def eventFilter(self, watched, event):
        kind = event.type()
        if kind == QEvent.Type.MouseButtonPress:
            if event.timestamp() != self.pressed_at:
                self.pressed_at = event.timestamp()
                self.pressed_on = QApplication.widgetAt(event.globalPosition().toPoint())
            self.manager.dispatch(watched, event)
        elif kind == QEvent.Type.MouseButtonDblClick:
            if QApplication.widgetAt(event.globalPosition().toPoint()) is not self.pressed_on:
                return True
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
