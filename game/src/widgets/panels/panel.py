from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QPainterPath, QRegion
from PySide6.QtWidgets import QSizePolicy, QVBoxLayout, QWidget
from ...app_core import Context
from .. import MenuBar

class Panel(QWidget):
    '''
    Initializes everything a panel should have: context, style, menu bar.
    A panel fills its master with no padding, and has a menu bar.
    This structure parallelizes all the gui elements that fill a pane and have a menu bar.
    '''
    KEY = "base_panel"
    BORDER_WIDTH = 2

    def __init__(self, master: QWidget, context: Context, menu_bar_label: str | None = None):
        super().__init__(master)
        self.context = context
        self.style = context.style

        # A plain QWidget doesn't paint a stylesheet background at all by
        # default (unlike QFrame/QScrollArea, which do) - it stays
        # visually transparent and whatever's behind it (its parent pane)
        # shows straight through, regardless of what color this stylesheet
        # says. WA_StyledBackground opts this widget into that painting.
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet(self.style.themed(
            f"background-color: {self.style.color('panel')}; border-radius: {self.style.PANEL_RADIUS}px; "
            f"border: {self.BORDER_WIDTH}px solid {self.style.color('widget')};",
            self
        ))
        master.layout().addWidget(self)

        # The menu bar/body otherwise fill this panel edge-to-edge, which
        # paints straight over the border - the same problem setMask below
        # works around for the menu bar's square corners covering this
        # panel's rounded ones, just for the border instead of the corners.
        # An inset contentsMargins on this widget's own layout would be the
        # obvious fix, but it isn't safe: e.g. Panes.__init__ unconditionally
        # calls master.layout().setContentsMargins(...) on whatever it's
        # given, which would silently clobber it back to 0 the moment a
        # panel's body is a nested Panes split (NetworkDiagram) - and there's
        # no guarantee some other future body constructor won't do the same.
        # Routing the master.layout().addWidget(...) idiom every body
        # constructor already uses (Scrollable/Panes/MenuBar/...) through a
        # separate, actually-installed inner layout instead - via the
        # layout() override below - keeps the border-inset margin on a
        # layout nothing outside this class ever touches.
        self.setLayout(QVBoxLayout())
        real_layout = super().layout()  # not self.layout() - that's overridden below, and self._content_layout doesn't exist yet
        real_layout.setContentsMargins(self.BORDER_WIDTH, self.BORDER_WIDTH, self.BORDER_WIDTH, self.BORDER_WIDTH)
        real_layout.setSpacing(0)

        self._content_area = QWidget()
        self._content_layout = QVBoxLayout(self._content_area)
        self._content_layout.setContentsMargins(0, 0, 0, 0)
        self._content_layout.setSpacing(0)
        real_layout.addWidget(self._content_area)

        if menu_bar_label is not None:
            self.menu_bar = MenuBar(self, context, menu_bar_label)

        # A whole panel's body (whatever gets added below the menu bar via
        # master.layout().addWidget(body, 1) - Scrollable/Panes and the
        # handful of other direct bodies all pass that explicit stretch=1
        # now) claims 100% of any leftover space over this filler as long
        # as it's visible, since Qt's box layout gives leftover strictly by
        # relative stretch factor (1 beats this filler's default 0) - so
        # this stays squeezed to zero height and invisible in the normal
        # case. The one time it matters is a minimized panel, whose body is
        # hidden entirely: with no stretch=1 item left to compete with, this
        # is the sole remaining widget that can grow, so it - not the menu
        # bar - absorbs the leftover instead of Qt centering the lone
        # capped-height menu bar in it (its default behavior for a single
        # item that can't grow to fill the space it's offered).
        #
        # This replaces an earlier attempt that used QLayout.setAlignment on
        # the menu bar item to pin it to the top: that form makes Qt stop
        # stretching *every* item in the layout to fill its cell (using each
        # one's sizeHint instead) the moment *any* item has an explicit
        # alignment, which broke bodies whose sizeHint is naturally smaller
        # than their pane (e.g. NetworkDiagram's nested Panes splitter) -
        # both leaving a gap under the menu bar and shrinking the body away
        # from filling the pane at all, even fully maximized.
        filler = QWidget()
        filler.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        self.layout().addWidget(filler)

    def layout(self):
        '''
        Overrides QWidget.layout() (not virtual on the C++ side, so this
        only affects Python-level callers - Qt's own internals keep using
        the real layout installed via setLayout() in __init__ regardless)
        to hand back the inner, border-padded content layout instead. Every
        body constructor (Scrollable, Panes, MenuBar, ...) adds itself via
        the master.layout().addWidget(...) idiom - routing that through
        here is what keeps their content inset from this panel's own
        border without needing any of them (or anything they in turn call,
        like Panes.__init__ resetting contentsMargins) to know a border
        exists at all.
        '''
        return self._content_layout

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # border-radius alone only rounds *this* widget's own background -
        # it doesn't clip children, and the menu bar plus whatever body sits
        # below it are both opaque, square-cornered widgets that fill this
        # panel edge-to-edge with zero margin, completely covering its
        # corners. A mask clips the whole widget - menu bar, body, and all -
        # to a rounded-rect region instead, which is the only way the
        # rounding actually shows. Recomputed on every resize since the
        # mask is in this widget's own pixel coordinates.
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), self.style.PANEL_RADIUS, self.style.PANEL_RADIUS)
        self.setMask(QRegion(path.toFillPolygon().toPolygon()))