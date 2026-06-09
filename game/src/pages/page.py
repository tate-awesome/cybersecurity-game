from customtkinter import CTkFrame
from ..app_core.context import Context

class Page(CTkFrame):
    '''
    Superclass for pages. Inherits CTkFrame.
    '''

    def __init__(self, context: Context):
        self.context = context
        self.router = context.router
        self.style = context.style
        
        super().__init__(context.root, fg_color=self.style.color("root"))
        self.pack(expand="True", fill="both")