from ...app_core.context import Context
from ...widgets.panels.title_menu import TitleMenu


class SelectMode:

    def __init__(self, context: Context):
        router = context.router
        root = context.root
        style = context.style

        panel = TitleMenu(context.root, context, "Select Mode")

        panel.button("Hardware Attacker", lambda:router.show("attacker/v0"))
        panel.button("Hardware Defender", lambda:router.show("defender/v0"))
        panel.button("Virtual Attacker", None)
        panel.button("Select a Demo", lambda:router.show("title/select_demo"))
        panel.button("Back", router.go_back)
        panel.button("Quit", router.quit)