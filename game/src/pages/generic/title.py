from ...app_core import Context
from ...widgets import TitleMenu
from ...widgets.frame_widgets.important_buttons import LinkToPage, TITLE_ACTIONS
from ..page import Page

class TitlePage(Page):
    '''
    Page constructor for build_type "title". Reads its own config and
    builds a TitleMenu with one button per entry in config["buttons"].

    Each button is one of:
      - {"link": "<page key>"} - a LinkToPage to that page, labeled with
        the linked page's own "link_label" (see PageManager.link_label).
      - {"action": "<name>"} - one of the important buttons in
        important_buttons.TITLE_ACTIONS.

    An optional config["background"] plays a procedural visual behind the
    menu - see Page.add_background.
    '''

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
            panel.add_important(LinkToPage, button["link"])
            return

        action = button.get("action")
        if action not in TITLE_ACTIONS:
            print(f"Title button config {button!r} has no link and unknown action {action!r}, skipping")
            return
        panel.add_important(TITLE_ACTIONS[action])
