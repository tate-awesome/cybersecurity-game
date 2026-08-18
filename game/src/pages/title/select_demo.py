from ...app_core import Context
from ...widgets import TitleMenu
from ..page import Page
from ..demo.v0.main import run


class SelectDemo(Page):
    '''
    Page constructor for title/select_demo. Inherits CTkFrame
    '''

    def __init__(self, context: Context):
        super().__init__(context)

        panel = TitleMenu(self, context, "select_demo")
        panel.button("boat_motion", lambda:self.router.show("demo/boat_motion"))
        panel.button("sprites", lambda:self.router.show("demo/sprites"))
        panel.button("triangle", lambda:self.router.show("demo/triangle"))
        panel.button("proof", run)
        panel.button("back", self.router.go_back)
        panel.button("quit", self.router.quit)