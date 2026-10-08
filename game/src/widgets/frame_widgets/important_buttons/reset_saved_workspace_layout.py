from ._workspace_save_button import WorkspaceSaveResetButton


class ResetSavedWorkspaceLayout(WorkspaceSaveResetButton):
    '''Resets this workspace's pane sizes to its defaults, keeping its saved inputs.'''
    LABEL = "menu_bar_buttons_reset_layout_button"
    TOOLTIP = "menu_bar_tooltips_reset_layout_button"
    PART = "layout_weights"
    MESSAGE = ("Reset the layout of this workspace?\n"
               "Its pane sizes go back to the workspace's defaults. Your inputs are kept.")
