from ...app_core.context import Context
from ...widgets.panels.title_menu import TitleMenu


class Title:
    
    def __init__(self, context: Context):
        self.router = context.router
        
        panel = TitleMenu(context.root, context, "The Game")
        panel.button("Play", lambda: self.router.show("title/select_mode"))
        panel.button("Quit", self.router.quit)