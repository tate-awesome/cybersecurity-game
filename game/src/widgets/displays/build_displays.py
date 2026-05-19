from customtkinter import *

from ..style import Style
from .world_map import WorldMap
from .boat_focus import BoatFocus
from .values_table import ValuesTable
from .. import common

class Displays:
    def __init__(self, style, parent, context):
        self.style = style
        self.parent = parent
        self.context = context
        self.buffer = self.context.net.data_buffer


        top, bottom = common.create_bifold(style, self.parent)


        world_map = WorldMap(self.style, top, self.context, self.buffer)

