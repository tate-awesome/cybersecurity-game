from ._base_button import ImportantButton


class RefreshCurrentPage(ImportantButton):
    '''Autosaves the current page, then rebuilds it.'''
    LABEL = "menu_bar_buttons_refresh_button"
    TOOLTIP = "menu_bar_tooltips_refresh_button"

    def on_click(self):
        self.context.router.refresh()
