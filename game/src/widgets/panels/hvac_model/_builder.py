from ....app_core import Context
from ...canvases.house import House
from ..panel import Panel

class Builder(Panel):
    KEY = "hvac_panel"
    # The settings keys (see _packages/_default.json) this panel reads or writes -
    # the workspace editor lists it under each of them
    SETTINGS = (
        "hvac_house_sprites",
        "hvac_house_colors",
    )
    def __init__(self, master, context: Context):
        super().__init__(master, context, self.KEY)

        model = House(self, context)

        self.menu_bar.minimize_button(model, master)