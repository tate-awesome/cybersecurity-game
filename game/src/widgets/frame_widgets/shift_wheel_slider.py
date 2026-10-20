from PySide6.QtWidgets import QSlider


class ShiftWheelSlider(QSlider):
    '''
    A QSlider that only reacts to shift+wheel, like the stripchart's
    shift+wheel-to-zoom (see StripChart.wheelEvent) - QSlider's own
    wheelEvent unconditionally consumes every wheel event, which used to
    make these sliders jump around as an unrelated side effect of the user
    just trying to scroll the panel/form they sit in. A plain wheel event
    is ignored instead of accepted, so it bubbles up to whatever scroll
    area contains this slider; shift+wheel never gets here - it steps
    every horizontal slider along a step at a time (see ShiftWheel).
    '''

    def wheelEvent(self, event):
        event.ignore()
