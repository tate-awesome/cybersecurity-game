from ._base_button import ImportantButton


class SetCurrentPageAsFavorite(ImportantButton):
    '''Remembers the current page in preferences, for OpenFavoritePage.'''
    LABEL = "menu_bar_buttons_page_button"
    TOOLTIP = "menu_bar_tooltips_page_button"

    def on_click(self):
        self.context.preferences.save_page()
