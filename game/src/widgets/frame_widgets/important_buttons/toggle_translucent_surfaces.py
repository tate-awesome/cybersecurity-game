from ._base_button import ToggleButton


class ToggleTranslucentSurfaces(ToggleButton):
    '''Lets surfaces be as see-through as the theme makes them, or makes everything solid (see Style.set_translucent_surfaces).'''
    LABEL = "menu_bar_buttons_transparency_on_button"
    ACTIVE_LABEL = "menu_bar_buttons_transparency_off_button"
    TOOLTIP = "menu_bar_tooltips_transparency_button"

    def is_active(self) -> bool:
        return self.context.style.translucent_surfaces

    def start(self):
        self.context.style.set_translucent_surfaces(True)

    def stop(self):
        self.context.style.set_translucent_surfaces(False)
