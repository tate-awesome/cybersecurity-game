from ....app_core import Context
from ._base_button import ImportantButton


class OpenFavoritePage(ImportantButton):
    '''Opens the page saved by SetCurrentPageAsFavorite - unavailable until one is saved.'''
    LABEL = "title_buttons_resume"

    @classmethod
    def is_available(cls, context: Context) -> bool:
        return context.preferences.has("page")

    def on_click(self):
        self.context.router.show(self.context.preferences.get("page"))
