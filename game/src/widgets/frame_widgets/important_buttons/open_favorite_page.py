from ....app_core import Context
from ._base_button import ImportantButton


class OpenFavoritePage(ImportantButton):
    '''
    Opens the page saved by SetCurrentPageAsFavorite (the bookmark), and
    says which - "Resume in <workspace>". Unavailable until there's a
    bookmark to a page that still exists.
    '''
    LABEL = "title_buttons_resume"

    @classmethod
    def is_available(cls, context: Context) -> bool:
        return context.preferences.has("page") and context.preferences.get("page") in context.pages.build_types

    def __init__(self, context: Context):
        super().__init__(context)
        name = context.labels.get(context.pages.link_label(context.preferences.get("page")))
        self.setText(context.labels.get("title_buttons_resume_in").replace("{workspace}", name))
        # What it shows until hovered, beside another button (see GrowingButton)
        self.short_text = context.labels.get("title_buttons_resume")

    def on_click(self):
        self.context.router.show(self.context.preferences.get("page"))
