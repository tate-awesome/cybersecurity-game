from ...app_core.context import Context
from ...widgets.style import Style
from ...widgets import title


class SelectMode:

    def __init__(self, context: Context):
        router = context.router
        root = context.root
        style = Style(context)

        title.title(root, "Select Mode")
        bw = title.buttons_wrapper(root)
        title.button(style, bw, "Hardware Attacker", lambda:router.show("attacker/v0"))
        title.button(style, bw, "Hardware Defender", lambda:router.show("defender/v0"))
        title.button(style, bw, "Virtual Attacker", None)
        title.button(style, bw, "Select a Demo", lambda:router.show("title/select_demo"))
        title.button(style, bw, "Back", router.go_back)
        title.button(style, bw, "Quit", router.quit)