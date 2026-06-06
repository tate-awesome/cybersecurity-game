from ...app_core.context import Context
from ...widgets import title


class Title:

    def __init__(self, context: Context):
        router = context.router
        root = context.root
        style = context.style

        title.title(root, "The Game")
        bw = title.buttons_wrapper(root)
        title.button(bw, context, "Play", lambda:router.show("title/select_mode"))
        title.button(bw, context, "Settings", None)
        title.button(bw, context, "Quit", router.quit)