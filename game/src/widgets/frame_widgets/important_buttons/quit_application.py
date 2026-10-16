from PySide6.QtWidgets import QWidget
from ....app_core import Context
from ...popup import confirm_dialog
from ._base_button import ImportantButton


def ask_to_quit(context: Context, master: QWidget):
    '''Asks whether to quit, then stops every running process and closes the app - Quit, wherever it is.'''
    labels = context.labels
    confirm_dialog(master, context, labels.get("quit_confirm_message"), labels.get("quit_confirm_yes"),
                   labels.get("quit_confirm_no"), context.router.quit)


class QuitApplication(ImportantButton):
    '''Asks first, then stops every running process and closes the app.'''
    LABEL = "menu_bar_buttons_quit_button"
    TOOLTIP = "menu_bar_tooltips_quit_button"
    ICON = "power"
    OPENS = "warning"

    def on_click(self):
        ask_to_quit(self.context, self.window())
