from ..page import Page
from ...app_core import Context
from ...widgets import TitleMenu


class Title(Page):
    '''
    Page constructor for title/title
    Inherits CTkFrame
    '''
    
    def __init__(self, context: Context):
        super().__init__(context)
        
        panel = TitleMenu(self, context, "main_title")
        if self.context.preferences.has("page"):
            page = self.context.preferences.get("page")
            panel.button("resume", lambda: self.router.show(page))
        panel.button("play", lambda: self.router.show("title/select_mode"))
        panel.button("ap_page", self.context.open_ap_config_page)
        panel.button("quit", self.router.quit)