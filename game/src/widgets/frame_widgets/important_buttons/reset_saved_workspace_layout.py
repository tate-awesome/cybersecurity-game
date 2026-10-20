from ._workspace_save_button import WorkspaceSaveResetButton


class ResetSavedWorkspaceLayout(WorkspaceSaveResetButton):
    '''Puts this workspace's panels back where they started, at their default sizes, keeping its saved inputs.'''
    LABEL = "menu_bar_buttons_reset_layout_button"
    TOOLTIP = "menu_bar_tooltips_reset_layout_button"
    PART = ("layout_shape", "layout_weights")
    MESSAGE = ("Reset the layout of this workspace?\n"
               "Its panels go back where they started, at their default sizes. Your inputs are kept.")
