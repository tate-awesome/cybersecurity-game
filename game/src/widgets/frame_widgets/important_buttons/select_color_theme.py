from ..overlay import Overlay
from .settings_overlays.settings_overlay_button import SettingsOverlayButton


class SelectColorTheme(SettingsOverlayButton):
    '''
    Opens the theme selector: the default themes (see style.CURATED_THEMES)
    and any imported ones (see ImportThemes), one button each - picking one
    applies it in the current mode. Everything finer (accents, hierarchies,
    every other preset, surfaces) is on the theme editor page.
    '''
    LABEL = "menu_bar_buttons_theme_button"
    TOOLTIP = "menu_bar_tooltips_theme_button"

    def populate(self, overlay: Overlay):
        style = self.context.style
        themes = self.section("themes")
        for family, name in style.theme_choices().items():
            button = themes.button(name, lambda family=family: self.apply(overlay, family),
                                   style.preset_info[family].get("note"))
            button.setCheckable(True)
            button.setChecked(family == style.theme_family())

    def apply(self, overlay: Overlay, family: str):
        # Close first - the theme change rebuilds the page, overlay and all
        overlay.close_chain()
        self.context.style.set_family(family)
