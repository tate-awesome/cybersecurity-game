from PySide6.QtCore import QEvent, QObject, Qt
from PySide6.QtWidgets import QAbstractScrollArea, QAbstractSlider, QApplication, QScrollBar, QWidget

# One wheel notch's angle delta (see QWheelEvent.angleDelta)
NOTCH = 120


class ShiftWheel(QObject):
    '''
    Makes shift+wheel mean "sideways" everywhere, on its way to any widget:

      - A widget whose class sets SHIFT_WHEEL = True (a strip chart's zoom)
        takes it itself, as is.
      - A horizontal slider or scroll bar steps along, and a scroll area
        that can scroll sideways scrolls sideways - wheel up going left,
        like the plain wheel going up.
      - Anything else under the mouse leaves it alone - Qt's own scroll
        areas and sliders would take shift as "a page at a time" and jump
        up or down.

    Whichever of those is nearest the widget under the mouse (it, or a
    parent) gets it, and nothing else. Its delta is read off whichever
    axis has one - some systems already turn shift+wheel sideways.
    Installed once, on the application.
    '''

    def __init__(self):
        super().__init__()
        # Partial notches (trackpads), carried over to the next event
        self.remainder = 0.0
        QApplication.instance().installEventFilter(self)

    def eventFilter(self, watched, event):
        if event.type() != QEvent.Type.Wheel or not event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
            return False
        if not isinstance(watched, QWidget):
            return False
        for widget in self.chain(watched):
            if getattr(widget, "SHIFT_WHEEL", False):
                # Passed up to it by Qt - or the widget under the mouse is it
                return False
            if self.scroll(widget, event):
                return True
        return True  # nothing takes it sideways - and nothing's let take it up or down

    @staticmethod
    def chain(widget: QWidget):
        while widget is not None:
            yield widget
            if widget.isWindow():
                return
            widget = widget.parentWidget()

    def scroll(self, widget: QWidget, event) -> bool:
        '''Moves widget sideways for event, if it moves that way - whether it took it.'''
        if isinstance(widget, QAbstractScrollArea):
            bar = widget.horizontalScrollBar()
            if bar.maximum() <= bar.minimum():
                return False
            self.step(bar, event, -QApplication.wheelScrollLines())
            return True
        if isinstance(widget, QAbstractSlider) and widget.orientation() == Qt.Orientation.Horizontal:
            # A scroll bar scrolls, wheel up going left; a slider counts up, as on the plain wheel
            lines = -QApplication.wheelScrollLines() if isinstance(widget, QScrollBar) else 1
            if widget.isEnabled():
                self.step(widget, event, lines)
            return True
        return False

    def step(self, slider: QAbstractSlider, event, lines: int):
        delta = event.angleDelta()
        notches = (delta.y() or delta.x()) / NOTCH + self.remainder
        whole = int(notches)
        self.remainder = notches - whole
        if slider.invertedControls():
            whole = -whole
        slider.setValue(slider.value() + whole * lines * slider.singleStep())
