from PySide6.QtCore import Qt
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
        self.setStyleSheet(self.style.themed(f"background-color: {self.style.color('panel')};", self))
        master.layout().addWidget(self)
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

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