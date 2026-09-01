from ...app_core import Context

# Better Widgets
from ... import widgets
from ..page import Page

# Network
from ...network.network_controller import HardwareAttacker as HardwareNetwork

class WorkspacePage(Page):
    '''
    Page constructor for build_type "workspace". Reads its own config.json
    (resolved by PageManager from the key it was navigated to) and builds a
    MenuBar plus a tree of Panes/panels from the "menu_bar" and "panes"
    sections, instead of hardcoding a specific page's layout.
    '''

    def __init__(self, context: Context):
        super().__init__(context)

        key = context.router.current_page
        config = context.pages.prepare_page_config(key)

        context.refresh_net(HardwareNetwork)

        self.build_menu_bar(config.get("menu_bar", {}))

        panes_config = config.get("panes")
        self.panes_root = self.build_panes(panes_config, self) if panes_config else None

    def build_menu_bar(self, menu_bar_config: dict):
        '''
        Builds the page's MenuBar and calls one MenuBar method per
        {"builtin": "<method_name>"} entry in menu_bar_config["buttons"]
        (already expanded from any {"_ref": ...} splices by Json).
        '''
        title = menu_bar_config.get("title", "_default")
        menu_bar = widgets.MenuBar(self, self.context, title)

        for button in menu_bar_config.get("buttons", []):
            name = button.get("builtin")
            if name is None:
                print(f"Menu bar button config {button!r} has no 'builtin' key, skipping")
                continue
            method = getattr(menu_bar, name, None)
            if not callable(method):
                print(f"MenuBar has no builtin button named {name!r}, skipping")
                continue
            method()

    def build_panes(self, node: dict, master):
        '''
        Recursively builds a widgets.Panes tree from a pane-tree node:
        {"orientation": ..., "children": [{"weight": ..., "panes": {...}} | {"weight": ..., "widget": {...}}]}
        Each child's "weight" is its proportional share of its parent -
        bigger weight, bigger pane - converted here into the divisors
        widgets.Panes actually expects (pane size = total size / divisor).
        Returns the Panes built at this node, so the caller can hang onto
        the outermost one (see self.panes_root) - PageManager reads its
        current sizes back out through Panes.get_weights() to autosave.
        '''
        children = node.get("children", [])
        if not children:
            return None

        weights = [child.get("weight", 1) for child in children]
        total_weight = sum(weights)
        divisors = [total_weight / weight for weight in weights]

        panes = widgets.Panes(master, self.context, node.get("orientation", "horizontal"), len(children), divisors, True)

        for i, child in enumerate(children):
            pane = panes.pane(i)
            if "panes" in child:
                self.build_panes(child["panes"], pane)
            elif "widget" in child:
                widget = child["widget"]
                widgets.panel(widget.get("type"), pane, self.context)
            else:
                print(f"Pane-tree child {child!r} has neither 'panes' nor 'widget', skipping")

        return panes
