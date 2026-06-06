from ...app_core.context import Context
from ..page import Page
from ...widgets.frame_widgets.title_menu import TitleMenu


class SelectMode(Page):
    '''
    Page constructor for title/select_mode. Inherits CTkFrame
    '''

    def __init__(self, context: Context):
        super().__init__(context)

        panel = TitleMenu(self, context, "Select Mode")
        panel.button("Hardware Attacker", lambda:self.router.show("attacker/v0"))
        panel.button("Hardware Defender", lambda:self.router.show("defender/v0"))
        panel.button("Select a Demo", lambda:self.router.show("title/select_demo"))
        panel.button("Back", self.router.go_back)
        panel.button("Quit", self.router.quit)