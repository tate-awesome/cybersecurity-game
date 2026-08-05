from ....app_core.context import Context
from ..panel import Panel

class Builder(Panel):
    def __init__(self, master, context: Context):
        super().__init__(master, context, "Network Diagram")

        self.menu_bar.minimize_button(None, master)
        self.menu_bar.add_button("Freeze Time")
        self.menu_bar.add_button("Show Less")
        self.menu_bar.add_button("Show More")