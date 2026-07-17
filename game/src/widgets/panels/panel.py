from customtkinter import CTkFrame
from ...app_core.context import Context
from .. import MenuBar

class Panel(CTkFrame):
    '''
    Initializes everything a panel should have: context, style, menu bar.
    A panel fills its master with no padding, and has a menu bar.
    This structure parallelizes all the gui elements that fill a pane and have a menu bar.
    '''

    def __init__(self, master, context: Context, menu_bar_text: str = None):
        self.context = context
        self.style = context.style

        super().__init__(master, fg_color=self.style.color("panel"))
        self.pack(**self.style.packing("panel"))

        if menu_bar_text is not None:
            self.menu_bar = MenuBar(self, context, "Attacks")