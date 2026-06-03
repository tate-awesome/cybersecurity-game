from ...app_core.context import Context
from ...widgets.style import Style
from ...widgets import title
from ..demo.v0.main import run


class SelectDemo:

    def __init__(self, context: Context):
        router = context.router
        root = context.root
        style = Style(context)

        title.title(root, "Select Demo")
        bw = title.buttons_wrapper(root)
        title.button(style, bw, "Boat Motion", lambda:router.show("demo/boat_motion"))
        title.button(style, bw, "Sprites", lambda:router.show("demo/sprites"))
        title.button(style, bw, "Triangle", lambda:router.show("demo/triangle"))
        title.button(style, bw, "Proof of Concept", run)
        title.button(style, bw, "Back", router.go_back)
        title.button(style, bw, "Quit", router.quit)