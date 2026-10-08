from ....app_core import Context
from ...popup import confirm_dialog
from ._base_button import ImportantButton


class WorkspaceSaveResetButton(ImportantButton):
    '''
    Shared by buttons that reset one part ("settings" or "panes") of the
    current workspace's autosave (see PageManager.save_current_page): asks
    for confirmation, autosaves first (so the other part keeps what's on
    screen right now), deletes PART, and rebuilds the page without
    re-autosaving - so it comes back with that part at its defaults.
    Only offered on workspace pages, the only ones with an autosave.
    '''
    PART = ""
    MESSAGE = ""

    @classmethod
    def is_available(cls, context: Context) -> bool:
        return context.pages.get_build_type(context.router.current_page) == "workspace"

    def on_click(self):
        confirm_dialog(self.window(), self.context, self.MESSAGE, "Yes, reset", "No, cancel", self.reset)

    def reset(self):
        key = self.context.router.current_page
        self.context.save_page()
        self.context.pages.delete_saved_page_part(key, self.PART)
        self.context.router.refresh(save=False)
