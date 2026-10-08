from ....app_core import Context
from ._base_button import ImportantButton


class LinkToPage(ImportantButton):
    '''
    Navigates to another page. Labeled with the target page's own
    "link_label" (see PageManager.link_label), so every link to a page
    reads the same.
    '''

    def __init__(self, context: Context, target: str):
        super().__init__(context, context.pages.link_label(target))
        self.target = target

    def on_click(self):
        self.context.router.show(self.target)
