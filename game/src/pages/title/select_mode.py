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
        title.button(style, bw, "Live Network", lambda:router.show("attacker/v0"))
        title.button(style, bw, "Peer Network", None)
        title.button(style, bw, "Local Simulation", None)
        title.button(style, bw, "Packet Replay", None)
        title.button(style, bw, "Synthetic Data", None)
        title.button(style, bw, "Play Demos", lambda:router.show("title/select_demo"))
        title.button(style, bw, "Back", lambda:router.show("title"))
        title.button(style, bw, "Quit", router.quit)