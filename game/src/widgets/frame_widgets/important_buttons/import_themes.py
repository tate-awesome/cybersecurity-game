from ._base_button import ImportantButton, open_in_browser


class ImportThemes(ImportantButton):
    '''
    Opens the imported themes folder (user_data/themes) in the file
    manager. Theme files dropped in there show up in the theme selector
    the next time it opens (see Style.load_imported_themes).
    '''
    LABEL = "menu_bar_buttons_import_themes_button"
    TOOLTIP = "menu_bar_tooltips_import_themes_button"
    POPOUT = True

    def on_click(self):
        folder = self.context.paths.user_themes
        self.context.paths.generate_path(folder)  # in case user data was deleted since startup
        open_in_browser(folder.as_uri())
