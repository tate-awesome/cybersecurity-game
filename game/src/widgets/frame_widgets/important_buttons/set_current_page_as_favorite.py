from ._base_button import ImportantButton, ToggleButton


class SetCurrentPageAsFavorite(ImportantButton):
    '''Remembers the current page in preferences, for OpenFavoritePage.'''
    LABEL = "menu_bar_buttons_page_button"
    TOOLTIP = "menu_bar_tooltips_page_button"

    def on_click(self):
        self.context.preferences.save_page()


class ToggleBookmark(ToggleButton):
    '''
    The menu bar's bookmark: on while the current page is the bookmarked
    one (OpenFavoritePage's), and clicking it bookmarks this page - or,
    when it already is, takes the bookmark away.
    '''
    LABEL = "menu_bar_buttons_bookmark_off"
    ACTIVE_LABEL = "menu_bar_buttons_bookmark_on"
    TOOLTIP = "menu_bar_tooltips_page_button"

    def is_active(self) -> bool:
        preferences = self.context.preferences
        return preferences.has("page") and preferences.get("page") == self.context.router.current_page

    def start(self):
        self.context.preferences.save_page()

    def stop(self):
        self.context.preferences.set("page", "")
