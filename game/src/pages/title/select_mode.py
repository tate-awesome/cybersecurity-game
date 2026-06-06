from ...app_core.context import Context
from ...widgets import title


class SelectMode:

    def __init__(self, context: Context):
        router = context.router
        root = context.root
        style = context.style

        title.title(root, "Select Mode")
        bw = title.buttons_wrapper(root)
        title.button(bw, context, "Hardware Attacker", lambda:router.show("attacker/v0"))
        title.button(bw, context, "Hardware Defender", lambda:router.show("defender/v0"))
        title.button(bw, context, "Virtual Attacker", None)
        title.button(bw, context, "Select a Demo", lambda:router.show("title/select_demo"))
        title.button(bw, context, "Back", router.go_back)
        title.button(bw, context, "Quit", router.quit)