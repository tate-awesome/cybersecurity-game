from ....app_core import Context
from ...canvases.world_map import WorldMap
from ..panel import Panel
from typing import cast

class Builder(Panel):
    KEY = "submarine_panel"
    def __init__(self, master, context: Context):
        super().__init__(master, context, self.KEY)

        map = WorldMap(self, context)

        self.menu_bar.minimize_button(map, master)