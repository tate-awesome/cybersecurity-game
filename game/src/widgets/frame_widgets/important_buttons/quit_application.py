from ._base_button import ImportantButton


class QuitApplication(ImportantButton):
    '''Stops every running process and closes the app.'''
    LABEL = "menu_bar_buttons_quit_button"
    TOOLTIP = "menu_bar_tooltips_quit_button"

    def on_click(self):
        self.context.router.quit()
