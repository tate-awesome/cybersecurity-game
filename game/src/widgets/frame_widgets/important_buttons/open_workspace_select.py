from ._base_button import ImportantButton


class OpenWorkspaceSelect(ImportantButton):
    '''Opens the workspace select page (Back returns here).'''
    LABEL = "menu_bar_buttons_workspaces_button"
    TOOLTIP = "menu_bar_tooltips_workspaces_button"

    def on_click(self):
        self.context.router.show("title/select_workspace")
