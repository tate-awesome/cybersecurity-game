from ._base_button import ImportantButton


class GoBackToPreviousPage(ImportantButton):
    '''Navigates back one page in the router's history.'''
    LABEL = "menu_bar_buttons_back_button"
    TOOLTIP = "menu_bar_tooltips_back_button"

    def on_click(self):
        self.context.router.go_back()
