from PySide6.QtWidgets import QWidget

from ....app_core import Context
from ...canvases.house import House
from ...canvases.world_map import WorldMap
from ...canvases.defender_world_map import DefenderWorldMap
from ...canvases.defender_hvac_chart import DefenderHVACChart
from ..panel import Panel


class FixedModel(Panel):
    '''
    One model canvas, hard coded - the single-model counterpart to
    modbus_model_panel, with no dropdown and no auto-switching, so a
    layout can show exactly the model it wants (or several side by side).
    Each subclass names its canvas class in CANVAS.
    '''

    KEY = "fixed_model_panel"
    CANVAS: type = None

    def __init__(self, master: QWidget, context: Context):
        super().__init__(master, context, self.KEY)
        self.model = self.CANVAS(self, context)
        self.menu_bar.minimize_button(self.model, master)


class SniffedSubmarineMap(FixedModel):
    KEY = "sniffed_submarine_map_panel"
    CANVAS = WorldMap
    # The settings keys (see _packages/_default.json) this panel reads or writes -
    # the workspace editor lists it under each of them
    SETTINGS = ("model_sprites", "model_colors")


class SniffedHVACHouse(FixedModel):
    KEY = "sniffed_hvac_house_panel"
    CANVAS = House
    SETTINGS = ("model_sprites", "model_colors")


class PolledSubmarineMap(FixedModel):
    KEY = "ap_polled_submarine_map_panel"
    CANVAS = DefenderWorldMap


class PolledHVACChart(FixedModel):
    KEY = "ap_polled_hvac_chart_panel"
    CANVAS = DefenderHVACChart
