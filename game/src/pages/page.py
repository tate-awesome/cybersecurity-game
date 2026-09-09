from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QWidget
from ..app_core import Context

class Page(QWidget):
    '''
    Superclass for pages. Inherits QWidget. Router places the built page as
    the root window's central widget, so a page doesn't place itself the
    way a CTkFrame used to pack itself into its parent - it just needs a
    layout of its own for whatever it adds as children.
    '''

    def __init__(self, context: Context):
        super().__init__()
        self.context = context
        self.router = context.router
        self.style = context.style

        # A plain QWidget doesn't paint a stylesheet background at all by
        # default (unlike QFrame/QScrollArea, which do) - see Panel/
        # BaseForm for the same fix and the full explanation.
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet(self.style.themed(f"background-color: {self.style.color('root')};", self))
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        # A page's own MenuBar and its Panes content are both typically
        # "widget"-colored - with no gap between them they read as one
        # fused bar instead of two distinct regions (global page toolbar vs.
        # the panel grid below it).
        self.layout().setSpacing(self.style.igap)
