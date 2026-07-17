from ....app_core.context import Context
from ....network.data_buffer import DataBuffer
from ...canvases.world_map import WorldMap
from ..panel import Panel
from typing import cast

class Builder(Panel):
    def __init__(self, master, context: Context):
        super().__init__(master, context, "Submarine System Model")
        self.buffer = cast(DataBuffer, self.context.net.data_buffer)

        map = WorldMap(self, context)

        self.menu_bar.minimize_button(map, master)
        self.menu_bar.add_button("Customize")
        self.menu_bar.add_button("Reset View", map.camera.reset_scale)
        self.menu_bar.add_button("Clear Values")
        self.menu_bar.add_button("Center on Boat")