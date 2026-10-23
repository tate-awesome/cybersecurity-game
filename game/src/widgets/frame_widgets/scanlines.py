from PySide6.QtCore import QEvent, Qt
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QWidget

from ...app_core import Context

# A dark line every this many px
SCANLINE_PERIOD = 3


class Scanlines(QWidget):
    '''
    A theme's scanlines (see themes.STYLE_DEFAULTS) - dark lines across the
    whole window, over everything on it, like an old CRT's. The mouse goes
    straight through. Hidden in a theme without them. Belongs to the window,
    like the Footer: Router calls page_changed after each page is built, to
    put it back on top of the new page.
    '''

    def __init__(self, context: Context):
        super().__init__(context.root)
        self.style = context.style
        self.root = context.root
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        context.root.installEventFilter(self)
        self.style.signals.changed.connect(self.page_changed)
        self.page_changed()

    def eventFilter(self, watched, event):
        if event.type() == QEvent.Type.Resize:
            self.setGeometry(self.root.rect())
        return False

    def page_changed(self):
        strength = self.style.setting("scanlines")
        self.setGeometry(self.root.rect())
        self.setVisible(bool(strength))
        if strength:
            self.raise_()
            self.update()

    def paintEvent(self, event):
        line = QColor("#000000")
        line.setAlphaF(0.5 * self.style.setting("scanlines") / 100)
        area = event.rect()
        painter = QPainter(self)
        for y in range(area.top() - area.top() % SCANLINE_PERIOD, area.bottom() + 1, SCANLINE_PERIOD):
            painter.fillRect(area.left(), y, area.width(), 1, line)
        painter.end()
