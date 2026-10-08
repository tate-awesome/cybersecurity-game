from ._base_button import ImportantButton


class OpenWorkspaceEditor(ImportantButton):
    '''Opens the workspace editor (Back returns here).'''
    LABEL = "menu_bar_buttons_workspace_editor_button"
    TOOLTIP = "menu_bar_tooltips_workspace_editor_button"

    def on_click(self):
        self.context.router.show("demo/config_editor")
