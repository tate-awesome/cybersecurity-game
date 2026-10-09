from .....app_core.context.style import SURFACE_BLUR_MAX, SURFACE_KINDS
from ...overlay import Overlay
from .settings_overlay_button import SettingsOverlayButton


class EditBackgroundStyle(SettingsOverlayButton):
    '''
    Opens sliders for how see-through each kind of surface is (panels,
    menu bars, widgets, fields, buttons) and how much the background
    behind it is blurred - frosted glass (see style.SURFACE_KINDS and
    app_core.context.backdrop) - plus whether buttons are inverted (see
    style.DEFAULT_INVERT_BUTTONS). Changes apply live and are saved as
    preferences, like the theme.
    '''
    LABEL = "menu_bar_buttons_background_button"
    TOOLTIP = "menu_bar_tooltips_background_button"

    def populate(self, overlay: Overlay):
        style = self.context.style

        opacity = self.section("surface_opacity")
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
        # Rebuild the open overlay so its sliders show the defaults
        overlay = next((o for o in self.context.root.findChildren(Overlay) if o.button is self), None)
        if overlay is not None:
            overlay.hide()
            overlay.click_open()
