from ...app_core.context import Context
from ...widgets.panels.title_menu import TitleMenu
from ..demo.v0.main import run


class SelectDemo:

    def __init__(self, context: Context):
        router = context.router
        root = context.root
        style = context.style

        panel = TitleMenu(context.root, context, "Select Demo")

        panel.button("Boat Motion", lambda:router.show("demo/boat_motion"))
        panel.button("Sprites", lambda:router.show("demo/sprites"))
        panel.button("Triangle", lambda:router.show("demo/triangle"))
        panel.button("Proof of Concept", run)
        panel.button("Back", router.go_back)
        panel.button("Quit", router.quit)