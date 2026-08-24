from ....app_core import Context
from ...canvases.house import House
from ..panel import Panel
from typing import cast

class Builder(Panel):
    def __init__(self, master, context: Context):
        super().__init__(master, context, "hvac_panel")

        model = House(self, context)

        self.menu_bar.minimize_button(model, master)