from ....app_core.context.style import NO_BACKGROUND
from ._base_button import ToggleButton


class ToggleFreezeBackground(ToggleButton):
    '''
    Holds the background still, or lets it animate again (the "background_animate"
    preference, inverted). With no background there's nothing to animate, so
    it shows frozen and can't be switched (see Style.background_frozen).
    '''
    LABEL = "menu_bar_buttons_freeze_background_button"
    ACTIVE_LABEL = "menu_bar_buttons_unfreeze_background_button"
    TOOLTIP = "menu_bar_tooltips_freeze_background_button"

    def __init__(self, context):
        super().__init__(context)
        self.sync_state()

    def is_active(self) -> bool:
        return self.context.style.background_frozen()

    def sync_state(self):
        super().sync_state()
        self.setEnabled(self.context.style.background_visual != NO_BACKGROUND)

    def start(self):
        self.context.style.set_background(animate=False)

    def stop(self):
        self.context.style.set_background(animate=True)
