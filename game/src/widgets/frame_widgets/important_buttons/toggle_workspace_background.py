from ._base_button import ToggleButton


class ToggleWorkspaceBackground(ToggleButton):
    '''Leaves the background out of workspaces, or puts it back (the "background_workspace_disabled" preference - see Style.background_shown).'''
    LABEL = "menu_bar_buttons_disable_workspace_background_button"
    ACTIVE_LABEL = "menu_bar_buttons_enable_workspace_background_button"
    TOOLTIP = "menu_bar_tooltips_workspace_background_button"

    def is_active(self) -> bool:
        return self.context.style.background_workspace_disabled

    def start(self):
        self.context.style.set_background(workspace_disabled=True)

    def stop(self):
        self.context.style.set_background(workspace_disabled=False)
