from ._base_button import ImportantButton


class OpenWorkspaceSorter(ImportantButton):
    '''Opens the Sort and Categorize Workspaces page (Back returns here).'''
    LABEL = "menu_bar_buttons_workspace_sorter_button"
    TOOLTIP = "menu_bar_tooltips_workspace_sorter_button"
    OPENS = "page"

    def on_click(self):
        self.context.router.show("demo/workspace_sorter")
