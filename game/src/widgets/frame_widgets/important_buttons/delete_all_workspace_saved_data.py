from ...popup import confirm_dialog
from ._base_button import ImportantButton


class DeleteAllWorkspaceSavedData(ImportantButton):
    '''
    Asks for confirmation, then deletes every workspace's autosaved data
    (only user_data/page_data - preferences are kept) and rebuilds the
    current page so anything showing saved-data state updates.
    '''
    LABEL = "menu_bar_buttons_delete_all_workspace_data_button"
    TOOLTIP = "menu_bar_tooltips_delete_all_workspace_data_button"

    def on_click(self):
        message = ("Delete your saved data for every workspace?\n"
                   "Every workspace's form entries, toggles, register settings, and panel sizes go back to their defaults. "
                   "Your theme, labels, and favorite page are kept.")
        confirm_dialog(self.window(), self.context, message, "Yes, delete", "No, cancel", self.delete)

    def delete(self):
        self.context.pages.delete_all_saved_pages()
        self.context.router.refresh(save=False)
