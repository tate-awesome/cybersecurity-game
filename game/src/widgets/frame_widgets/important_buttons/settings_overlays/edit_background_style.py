from .....app_core.context.style import BACKGROUND_FPS_RANGE
from ....visuals import VISUALS
from ...overlay import Overlay
from .settings_overlay_button import SettingsOverlayButton


class EditBackgroundStyle(SettingsOverlayButton):
    '''
    Opens whether surfaces can be see-through (how much is each theme's
    materials - see themes.py), whether buttons are inverted (see
    style.DEFAULT_INVERT_BUTTONS) - and for the animated background behind
    pages: whether it's drawn, which visual, whether it animates, whether
    it's detailed, and its frame rate (see Style.background_*). Changes
    apply live and are saved as preferences, like the theme.
    '''
    LABEL = "menu_bar_buttons_background_button"
    TOOLTIP = "menu_bar_tooltips_background_button"

    def populate(self, overlay: Overlay):
        style = self.context.style
        labels = self.context.labels

        # The animated page background itself (see Page.add_background)
        background = self.section("background")
        background.toggle(("background_enabled",), style.background_enabled,
                          lambda checked: style.set_background(enabled=checked))
        names = {key: labels.get(f"visual_names_{key}") for key in [*VISUALS, "cycle"]}
        background.choice(("background_visual",), names, style.background_visual,
                          lambda key: style.set_background(visual=key))
        background.toggle(("background_animate",), style.background_animate,
                          lambda checked: style.set_background(animate=checked))
        background.toggle(("background_detailed",), style.background_detailed,
                          lambda checked: style.set_background(detailed=checked))
        background.integer(("background_fps",), style.background_fps, *BACKGROUND_FPS_RANGE,
                           lambda fps: style.set_background(fps=fps))

        opacity = self.section("surface_opacity")
        opacity.toggle(("surface_translucent",), style.translucent_surfaces, style.set_translucent_surfaces)
        opacity.toggle(("surface_invert_buttons",), style.invert_buttons, style.set_invert_buttons)
        opacity.button(self.context.labels.get("settings_labels_surface_reset"), self.reset,
                    self.context.labels.get("settings_tooltips_surface_reset"))

    def reset(self):
        self.context.style.reset_surfaces()
        self.context.style.load_default_background()
        self.context.style.set_background()  # saves the defaults
        # Rebuild the open overlay so its sliders show the defaults
        overlay = next((o for o in self.context.root.findChildren(Overlay) if o.button is self), None)
        if overlay is not None:
            overlay.hide()
            overlay.click_open()
