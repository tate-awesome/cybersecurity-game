from ._base_button import ImportantButton


class OpenThemeEditor(ImportantButton):
    '''Opens the theme editor - every advanced theme setting (Back returns here).'''
    LABEL = "menu_bar_buttons_theme_editor_button"
    TOOLTIP = "menu_bar_tooltips_theme_editor_button"
    OPENS = "page"

    def on_click(self):
        self.context.router.show("theme_editor")
