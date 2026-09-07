from PySide6.QtWidgets import QVBoxLayout, QWidget
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

        self.setStyleSheet(self.style.themed(f"background-color: {self.style.color('panel')};", self))
        master.layout().addWidget(self)
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

        if menu_bar_label is not None:
            self.menu_bar = MenuBar(self, context, menu_bar_label)