from ...app_core import Context
from ...widgets import TitleMenu
from ..page import Page
from ..demo.v0.main import run as run_demo_proof

class TitlePage(Page):
    '''
    Page constructor for build_type "title". Reads its own config.json and
    builds a TitleMenu with one button per entry in config["buttons"].

    Each button is {"label": <labels.title_buttons key>, "action": <name>, ...}.
    A {"_from_manifest": "<table>"} entry expands into one navigate button
    per entry of that manifest table (see expand_from_manifest) instead of
    being a button itself, so link-heavy pages (mode/lesson select) don't
    have to hand-list every link the manifest already knows about.
    '''

    ACTIONS = ("navigate", "back", "quit", "open_ap_config", "resume", "demo_proof")

    def __init__(self, context: Context):
        super().__init__(context)

        key = context.router.current_page
        config = context.pages.load_page_config(key)

        panel = TitleMenu(self, context, config.get("title", "_default"))
        self.build_buttons(config.get("buttons", []), panel)

    def build_buttons(self, buttons_config: list, panel: TitleMenu):
        for button in buttons_config:
            table = button.get("_from_manifest")
            if table is not None:
                for generated in self.expand_from_manifest(table):
                    self.build_button(generated, panel)
            else:
                self.build_button(button, panel)

    def expand_from_manifest(self, table_name: str) -> list[dict]:
        '''
        Expands a manifest table (e.g. "old_game_modes", "lessons") into one
        {"label": ..., "action": "navigate", "target": ...} button per entry.
        A plain string entry (old_game_modes) is the target page key directly;
        a dict entry (lessons) carries its target under "path" and an
        optional display label under "title_label".
        '''
        table = self.context.pages.get(table_name)
        buttons = []
        for key, value in table.items():
            if isinstance(value, dict):
                target = value.get("path", key)
                label = value.get("title_label", key)
            else:
                target = value
                label = key
            buttons.append({"label": label, "action": "navigate", "target": target})
        return buttons

    def build_button(self, button: dict, panel: TitleMenu):
        action = button.get("action")
        label = button.get("label", "_default")

        if action == "navigate":
            target = button.get("target")
            panel.button(label, lambda target=target: self.router.show(target))
        elif action == "back":
            panel.button(label, self.router.go_back)
        elif action == "quit":
            panel.button(label, self.router.quit)
        elif action == "open_ap_config":
            panel.button(label, self.context.open_ap_config_page)
        elif action == "resume":
            if self.context.preferences.has("page"):
                target = self.context.preferences.get("page")
                panel.button(label, lambda target=target: self.router.show(target))
        elif action == "demo_proof":
            panel.button(label, run_demo_proof)
        else:
            print(f"Title button config {button!r} has unknown action {action!r}, skipping")
