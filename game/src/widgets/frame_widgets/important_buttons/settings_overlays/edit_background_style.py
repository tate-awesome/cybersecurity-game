from .....app_core.context.style import BACKGROUND_FPS_RANGE, SURFACE_BLUR_MAX, SURFACE_KINDS
from ....visuals import VISUALS
from ...overlay import Overlay
from .settings_overlay_button import SettingsOverlayButton


class EditBackgroundStyle(SettingsOverlayButton):
    '''
    Opens sliders for how see-through each kind of surface is (panels,
    menu bars, widgets, fields, buttons) and how much the background
    behind it is blurred - frosted glass (see style.SURFACE_KINDS and
    app_core.context.backdrop) - plus whether buttons are inverted (see
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
        for kind in SURFACE_KINDS:
            opacity.slider(("surface_opacity", kind), round(style.surface_opacity[kind] * 100), 0, 100,
                           lambda value, kind=kind: style.set_surface(kind, opacity=value / 100), suffix="%")

        blur = self.section("surface_blur")
        for kind in SURFACE_KINDS:
            blur.slider(("surface_blur", kind), round(style.surface_blur[kind]), 0, int(SURFACE_BLUR_MAX),
                        lambda value, kind=kind: style.set_surface(kind, blur=value), suffix=" px")
        blur.button(self.context.labels.get("settings_labels_surface_reset"), self.reset,
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
