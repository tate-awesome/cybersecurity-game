from ...app_core.context import Context
from ...widgets.style import Style
from ...widgets import title


class Title:

    def __init__(self, context: Context):
        router = context.router
        root = context.root
        style = Style(context)

        title.title(root, "The Game")
        bw = title.buttons_wrapper(root)
        title.button(style, bw, "Play", lambda:router.show("title/select_mode"))
        title.button(style, bw, "Settings", None)
        title.button(style, bw, "Quit", router.quit)