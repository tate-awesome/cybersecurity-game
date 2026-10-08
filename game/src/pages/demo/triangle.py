from ...app_core import Context
from ...widgets import TriangleCanvas
from ...widgets.frame_widgets.important_buttons import (GoBackToPreviousPage, LoadLocalizationLabelsFile, QuitApplication,
                                                       SelectColorTheme, SetCurrentPageAsFavorite, ToggleLightDarkMode)
from ...pages.page import Page
from ...widgets import MenuBar

class Triangle(Page):
    '''
    Demo page for testing canvas, animations, camera, drawing, sprites, and transforms
    '''
    def __init__(self, context: Context):
        super().__init__(context)
        menu_bar = MenuBar(self, context, "triangle_demo")
        for button in (ToggleLightDarkMode, SelectColorTheme, LoadLocalizationLabelsFile, SetCurrentPageAsFavorite):
            menu_bar.add_important(button)
        menu_bar.add_important(GoBackToPreviousPage)
        menu_bar.add_important(QuitApplication)

        world_map = TriangleCanvas(self, context)