from ...app_core.context import Context
from ...widgets import TitleMenu
from ..page import Page
from ..demo.v0.main import run


class SelectDemo(Page):
    '''
    Page constructor for title/select_demo. Inherits CTkFrame
    '''

    def __init__(self, context: Context):
        super().__init__(context)

        panel = TitleMenu(self, context, "Select Demo")
        panel.button("Boat Motion", lambda:self.router.show("demo/boat_motion"))
        panel.button("Sprites", lambda:self.router.show("demo/sprites"))
        panel.button("Triangle", lambda:self.router.show("demo/triangle"))
        panel.button("Proof of Concept", run)
        panel.button("Back", self.router.go_back)
        panel.button("Quit", self.router.quit)