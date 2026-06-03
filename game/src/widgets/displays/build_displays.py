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

        self.create_menu_bar(parent)

        self.create_menu_button(self.menu_bar, "Customize")
        self.create_menu_button(self.menu_bar, "Reset View")
        self.create_menu_button(self.menu_bar, "Clear Values")
        self.create_menu_button(self.menu_bar, "Center on Boat") #Move with boat

    def create_menu_bar(self, parent):
        frame = CTkFrame(parent)
        frame.pack(side="top", fill="x", pady=self.style.gaptop, padx=self.style.gap)

        header = CTkLabel(frame, text="Data Displays", font=self.style.get_font(), padx=self.style.igap)
        header.pack(fill=Y, side="left", padx=self.style.gap)
        return frame

    def create_menu_button(self, frame, text, function=None):
        med = self.style.get_font()
        button = CTkButton(frame, text=text, command=function, font=med)
        button.pack(side="right", padx=self.style.gap, pady=self.style.gap)
        return button
