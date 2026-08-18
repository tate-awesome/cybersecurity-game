from ....app_core import Context
from ..panel import Panel

class Builder(Panel):
    def __init__(self, master, context: Context):
        super().__init__(master, context, "network_panel")

        self.menu_bar.minimize_button(None, master)