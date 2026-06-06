from ...app_core.context import Context
from ...widgets import title
from ..demo.v0.main import run


class SelectDemo:

    def __init__(self, context: Context):
        router = context.router
        root = context.root
        style = context.style

        title.title(root, "Select Demo")
        bw = title.buttons_wrapper(root)
        title.button(bw, context, "Boat Motion", lambda:router.show("demo/boat_motion"))
        title.button(bw, context, "Sprites", lambda:router.show("demo/sprites"))
        title.button(bw, context, "Triangle", lambda:router.show("demo/triangle"))
        title.button(bw, context, "Proof of Concept", run)
        title.button(bw, context, "Back", router.go_back)
        title.button(bw, context, "Quit", router.quit)