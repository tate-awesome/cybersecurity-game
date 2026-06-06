from ..page import Page
from ...app_core.context import Context
from ...widgets.panels.title_menu import TitleMenu


class Title(Page):
    '''
    Page constructor for title/title
    Inherits CTkFrame
    '''
    
    def __init__(self, context: Context):
        super().__init__(context)
        
        panel = TitleMenu(self, context, "The Game")
        panel.button("Play", lambda: self.router.show("title/select_mode"))
        panel.button("Quit", self.router.quit)