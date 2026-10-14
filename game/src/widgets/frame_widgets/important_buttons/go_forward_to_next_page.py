from ....app_core import Context
from ._base_button import ImportantButton


class GoForwardToNextPage(ImportantButton):
    '''Navigates forward again, to the page last gone back from (see Router.go_forward).'''
    LABEL = "menu_bar_buttons_forward_button"
    TOOLTIP = "menu_bar_tooltips_forward_button"

    @classmethod
    def is_available(cls, context: Context) -> bool:
        return bool(context.router.forward_stack)

    def on_click(self):
        self.context.router.go_forward()
