from ...popup import message
from ._base_button import ImportantButton


class ShowHelpMessage(ImportantButton):
    '''Shows a help popup for the current page.'''
    LABEL = "menu_bar_buttons_help_button"
    TOOLTIP = "menu_bar_tooltips_help_button"

    def on_click(self):
        message(self.window(), self.context, self.help_message())

    def help_message(self) -> str:
        # TODO get help from progress and current page
        return "You need to do something"
