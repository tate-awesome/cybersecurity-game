from ._workspace_save_button import WorkspaceSaveResetButton


class ClearSavedWorkspaceInputs(WorkspaceSaveResetButton):
    '''
    Resets this workspace's saved inputs (form entries, toggles, register
    settings, ...) to its defaults, keeping its pane layout.
    '''
    LABEL = "menu_bar_buttons_clear_inputs_button"
    TOOLTIP = "menu_bar_tooltips_clear_inputs_button"
    PART = "settings"
    MESSAGE = ("Clear your saved inputs for this workspace?\n"
               "Its form entries, toggles, register settings, and display styles go back to the workspace's defaults. "
               "Your pane layout is kept.")
