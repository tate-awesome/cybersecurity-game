from ....app_core import Context
from ...canvases.world_map import WorldMap
from ..panel import Panel

class Builder(Panel):
    KEY = "submarine_panel"
    # The settings keys (see _packages/_default.json) this panel reads or writes -
    # the workspace editor lists it under each of them
    SETTINGS = (
        "submarine_map_sprites",
        "submarine_map_colors",
    )
    def __init__(self, master, context: Context):
        super().__init__(master, context, self.KEY)

        map = WorldMap(self, context)

        self.menu_bar.minimize_button(map, master)