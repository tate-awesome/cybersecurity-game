from ._base_button import ImportantButton


class OpenWorkspaceEditor(ImportantButton):
    '''Opens the Edit Workspaces page (Back returns here) - each workspace's own editor opens from its row there.'''
    LABEL = "menu_bar_buttons_workspace_editor_button"
    TOOLTIP = "menu_bar_tooltips_workspace_editor_button"
    OPENS = "page"

    def on_click(self):
        self.context.router.show("demo/workspace_sorter")
