from ...overlay import Overlay
from ..refresh_current_page import RefreshCurrentPage
from .settings_overlay_button import SettingsOverlayButton


class RefreshAndCloseOverlay(RefreshCurrentPage):
    '''RefreshCurrentPage for inside an overlay - closes it first, since the rebuild deletes the button it hangs off.'''

    def on_click(self):
        self.window().hide()
        super().on_click()


class EditWorkspaceAvailability(SettingsOverlayButton):
    '''
    A debugging tool: opens checkboxes for what this workspace offers at all
    ("available" - forms, models, ...). Panels only read it while building,
    so the overlay ends with a refresh button to apply the changes.
    '''
    LABEL = "menu_bar_buttons_debug_availability_button"
    TOOLTIP = "menu_bar_tooltips_debug_availability_button"

    def populate(self, overlay: Overlay):
        available = self.section("available")
        for key in self.context.states.get("available"):
            available.checkbox("available", key)
        overlay.layout().addWidget(RefreshAndCloseOverlay(self.context))
