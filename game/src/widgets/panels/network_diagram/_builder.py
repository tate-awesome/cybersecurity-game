from ....app_core.context import Context
from ....network.data_buffer import DataBuffer
from ..panel import Panel
from typing import cast

class Builder(Panel):
    def __init__(self, master, context: Context):
        super().__init__(master, context, "Network Diagram")
        self.buffer = cast(DataBuffer, self.context.net.data_buffer)

        self.menu_bar.minimize_button(None, master)
        self.menu_bar.add_button("Freeze Time")
        self.menu_bar.add_button("Show Less")
        self.menu_bar.add_button("Show More")