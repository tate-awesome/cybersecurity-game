import shutil
from ....app_core.context.style import Style
from ...popup import confirm_dialog
from ._base_button import ImportantButton


class DeleteAllUserData(ImportantButton):
    '''
    Asks for confirmation, then wipes the entire user_data folder - every
    page's autosaved settings/panes, saved captures, and preferences.json -
    and recreates the empty directory structure the app expects to find
    there. A full factory reset, unlike ResetCurrentPageToDefaults (which
    only clears the current page's save and leaves preferences alone).
    '''
    LABEL = "title_buttons_delete_user_data"
    TOOLTIP = "menu_bar_tooltips_delete_user_data_button"

    def on_click(self):
        message = ("Are you sure you want to delete all user data?\n"
                   "Saved page progress, captures, and preferences will be permanently lost.")
        confirm_dialog(self.window(), self.context, message, "Yes, delete", "No, cancel", self.delete)

    def delete(self):
        context = self.context
        shutil.rmtree(context.paths.user_data, ignore_errors=True)
        context.style = Style(context)  # reset style to default
        context.paths.create_user_dirs()
        context.preferences.clear()
        # save=False so nothing gets written back into the folder that was just wiped
        context.router.refresh(save=False)
