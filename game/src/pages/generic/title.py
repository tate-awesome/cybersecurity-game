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

    Either can have "beside": another such entry, placed just to its
    right - short, growing to its full text on hover (see
    TitleMenu.add_beside) - e.g. the start page's "» Resume" beside
    Workspaces, growing to "» Resume in <workspace>".

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
        self.menu = panel

    def appear_targets(self):
        # The title and each button arrive one by one, not the menu as a block
        return self.menu.items

    def build_button(self, button: dict, panel: TitleMenu):
        made = self.button_for(button)
        if made is None:
            return
        button_class, args = made
        added = panel.add_important(button_class, *args)
        # {"beside": {...}} - a second button just right of this one, growing to its full text on hover
        beside = self.button_for(button["beside"]) if isinstance(button.get("beside"), dict) else None
        if added is not None and beside is not None and beside[0].is_available(self.context):
            panel.add_beside(added, beside[0](self.context, *beside[1]))

    def button_for(self, button: dict) -> tuple[type, tuple] | None:
        '''The button class (and its extra constructor args) a title button config entry asks for.'''
        if "link" in button:
            return LinkToPage, (button["link"],)
        action = button.get("action")
        if action not in TITLE_ACTIONS:
            print(f"Title button config {button!r} has no link and unknown action {action!r}, skipping")
            return None
        return TITLE_ACTIONS[action], ()
