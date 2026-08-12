from ..page import Page
from ...app_core.context import Context
from ...widgets import TitleMenu


class Title(Page):
    '''
    Page constructor for title/title
    Inherits CTkFrame
    '''
    
    def __init__(self, context: Context):
        super().__init__(context)
        
        panel = TitleMenu(self, context, "The Game")
        if self.context.preferences.has("page"):
            page = self.context.preferences.get("page")
            panel.button("Resume", lambda: self.router.show(page))
        panel.button("Play", lambda: self.router.show("title/select_mode"))
        panel.button("Open AP Config Page", self.router.open_ap_config_page)
        panel.button("Quit", self.router.quit)