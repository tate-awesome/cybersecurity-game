from ...app_core import Context
from ..page import Page
from ...widgets import TitleMenu


class SelectMode(Page):
    '''
    Page constructor for title/select_mode. Inherits CTkFrame
    '''

    def __init__(self, context: Context):
        super().__init__(context)

        panel = TitleMenu(self, context, "select_mode")
        panel.button("hardware_attacker", lambda:self.router.show("attacker/v0"))
        panel.button("hardware_defender", lambda:self.router.show("defender/v0"))
        panel.button("select_demo", lambda:self.router.show("title/select_demo"))
        panel.button("generic_page", lambda:self.router.show("generic"))
        panel.button("back", self.router.go_back)
        panel.button("quit", self.router.quit)