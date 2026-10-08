from ._base_button import ImportantButton


class OpenTitlePage(ImportantButton):
    '''Opens the start page (Back returns here).'''
    LABEL = "menu_bar_buttons_title_button"
    TOOLTIP = "menu_bar_tooltips_title_button"

    def on_click(self):
        self.context.router.show("start")
