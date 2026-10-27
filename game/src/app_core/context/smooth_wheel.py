from PySide6.QtCore import QEasingCurve, QEvent, QObject, QPropertyAnimation, Qt
from PySide6.QtGui import QInputDevice
from PySide6.QtWidgets import QAbstractScrollArea, QApplication, QScrollBar

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .. import Context

# One wheel notch's angle delta (see QWheelEvent.angleDelta)
NOTCH = 120
# How long a notch's glide takes - browsers use about the same
DURATION_MS = 220


class SmoothWheel(QObject):
    '''
    Makes the plain wheel glide a scroll area to where it would have
    jumped, everywhere - Qt's own scroll areas jump a notch's three lines
    in one frame, which reads as jumpy (see Performance.smooth_scrolling).

    It takes the wheel on its way to a scroll area's viewport (whatever's
    under the mouse let it pass up to there) or a vertical scroll bar.
    Another notch during a glide adds on to where it's going. Left to Qt
    as before:

      - Shift/ctrl+wheel (see ShiftWheel; ctrl zooms text)
      - Touchpads (and their momentum) - already smooth
      - A scroll area at its end - so an outer one scrolls instead

    Installed once, on the application.
    '''

    def __init__(self, context: "Context"):
        super().__init__()
        self.context = context
        # One glide at a time - the wheel only scrolls one thing at once
        self.animation = QPropertyAnimation()
        self.animation.setPropertyName(b"value")
        self.animation.setDuration(DURATION_MS)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        QApplication.instance().installEventFilter(self)

    def eventFilter(self, watched, event):
        if event.type() != QEvent.Type.Wheel or event.modifiers() != Qt.KeyboardModifier.NoModifier:
            return False
        performance = getattr(self.context, "performance", None)
        if performance is None or not performance.smooth_scrolling:
            return False
        if self.precise(event) or not event.angleDelta().y():
            return False
        bar = self.bar(watched)
        if bar is None:
            return False

        animation = self.animation
        gliding = animation.state() == QPropertyAnimation.State.Running and animation.targetObject() is bar
        start = animation.endValue() if gliding else bar.value()
        step = bar.singleStep() * QApplication.wheelScrollLines()
        # Wheel up counts up, as on a slider - scroll bars invert it by default, so it scrolls up
        notches = event.angleDelta().y() / NOTCH
        if bar.invertedControls():
            notches = -notches
        target = max(bar.minimum(), min(bar.maximum(), round(start + notches * step)))
        if target == start:
            # Already gliding to its end: nothing more to do - Qt would jump
            # the bar ahead of the glide, which then pulls it back. Resting
            # at its end: Qt passes it on to an outer scroll area.
            return gliding

        animation.stop()
        animation.setTargetObject(bar)
        animation.setStartValue(bar.value())
        animation.setEndValue(target)
        animation.start()
        return True

    @staticmethod
    def precise(event) -> bool:
        '''
        Whether event is from a touchpad (or its momentum) - already smooth.
        Not told by pixelDelta: on X11 a plain mouse wheel has one too, a
        notch's worth.
        '''
        return (event.device().type() == QInputDevice.DeviceType.TouchPad
                or event.phase() != Qt.ScrollPhase.NoScrollPhase
                or event.source() == Qt.MouseEventSource.MouseEventSynthesizedBySystem)

    @staticmethod
    def bar(watched) -> QScrollBar | None:
        '''The vertical scroll bar the wheel over watched would move, if it's one this glides.'''
        if isinstance(watched, QScrollBar):
            return watched if watched.orientation() == Qt.Orientation.Vertical else None
        area = watched.parent() if isinstance(watched, QObject) else None
        if isinstance(area, QAbstractScrollArea) and area.viewport() is watched:
            bar = area.verticalScrollBar()
            return bar if bar.maximum() > bar.minimum() else None
        return None
