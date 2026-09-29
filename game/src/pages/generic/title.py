from ...app_core import Context
from ...widgets import TitleMenu, popup
from ..page import Page

class TitlePage(Page):
    '''
    Page constructor for build_type "title". Reads its own config and
    builds a TitleMenu with one button per entry in config["buttons"].

    Each button is one of:
      - {"link": "<page key>"} - navigates to that page, labeled with
        the linked page's own "link_label" (see PageManager.link_label).
      - {"action": "<name>"} - one of the built-in actions below, each
        with its own fixed label.

    An optional config["background"] plays a procedural visual behind the
    menu - see Page.add_background.
    '''

    # Built-in action name -> the labels key its button shows
    ACTION_LABELS = {
        "back": "title_buttons_back",
        "quit": "title_buttons_quit",
        "resume": "title_buttons_resume",
        "open_ap_config": "title_buttons_ap_page",
        "delete_user_data": "title_buttons_delete_user_data",
    }

    def __init__(self, context: Context):
        super().__init__(context)

        key = context.router.current_page
        config = context.pages.load_page_config(key)

        self.add_background(config)

        panel = TitleMenu(self, context, config.get("title", "_default"))
        for button in config.get("buttons", []):
            self.build_button(button, panel)

    def build_button(self, button: dict, panel: TitleMenu):
        if "link" in button:
            target = button["link"]
            panel.button(self.context.pages.link_label(target), lambda target=target: self.router.show(target))
            return

        action = button.get("action")
        if action not in self.ACTION_LABELS:
            print(f"Title button config {button!r} has no link and unknown action {action!r}, skipping")
            return
        label = self.ACTION_LABELS[action]

        if action == "back":
            panel.button(label, self.router.go_back)
        elif action == "quit":
            panel.button(label, self.router.quit)
        elif action == "open_ap_config":
            panel.button(label, self.context.open_ap_config_page)
        elif action == "resume":
            if self.context.preferences.has("page"):
                target = self.context.preferences.get("page")
                panel.button(label, lambda target=target: self.router.show(target))
        elif action == "delete_user_data":
            panel.button(label, lambda: popup.delete_user_data_dialog(self, self.context, self.context.delete_user_data))
