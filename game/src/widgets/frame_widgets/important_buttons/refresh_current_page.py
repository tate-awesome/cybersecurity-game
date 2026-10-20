from ...popup import confirm_dialog
from ._base_button import ImportantButton
from .reset_saved_workspace_layout import ResetSavedWorkspaceLayout


class RefreshCurrentPage(ImportantButton):
    '''
    Asks first, then autosaves the current page and rebuilds it - a
    workspace with its layout reset too: its panels back where they
    started, at their default sizes (see ResetSavedWorkspaceLayout).
    '''
    LABEL = "menu_bar_buttons_refresh_button"
    TOOLTIP = "menu_bar_tooltips_refresh_button"
    ICON = "reload"
    OPENS = "warning"  # it asks first
    MESSAGE = "Refresh this page?\nIt's rebuilt, keeping your inputs and everything running."
    WORKSPACE_MESSAGE = ("Refresh this workspace?\nIt's rebuilt with its panels back where they started, at their default sizes. "
                         "Your inputs and everything running are kept.")

    def on_click(self):
        if ResetSavedWorkspaceLayout.is_available(self.context):
            confirm_dialog(self.window(), self.context, self.WORKSPACE_MESSAGE, "Yes, refresh", "No, cancel",
                           self.reset_layout)
        else:
            confirm_dialog(self.window(), self.context, self.MESSAGE, "Yes, refresh", "No, cancel", self.context.router.refresh)

    def reset_layout(self):
        key = self.context.router.current_page
        self.context.save_page()
        self.context.pages.delete_saved_page_part(key, ResetSavedWorkspaceLayout.PART)
        self.context.router.refresh(save=False)
