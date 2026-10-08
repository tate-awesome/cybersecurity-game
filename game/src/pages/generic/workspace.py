from ...app_core import Context

# Better Widgets
from ... import widgets
from ..page import Page

class WorkspacePage(Page):
    '''
    Page constructor for build_type "workspace". Reads its own config.json
    (resolved by PageManager from the key it was navigated to) and builds a
    MenuBar plus a tree of Panes/panels from the "menu_bar", "layout_shape"
    and "layout_weights" sections, instead of hardcoding a specific page's layout.
    '''

    # Used when a page's config has no "background" of its own (set
    # "background": false to turn it off). Shares the title pages'
    # network, frozen where it was when the page opened.
    DEFAULT_BACKGROUND = {"visual": "network_mesh", "blur": 6, "animate": False, "packets": False}

    def __init__(self, context: Context):
        super().__init__(context)

        key = context.router.current_page
        config = context.pages.prepare_page_config(key)

        # The network behind the gaps between panels - still and without
        # packets, so it reads as texture and never makes the panels
        # above it repaint. The panes turn transparent only if it's there.
        self.transparent_panes = self.add_background(config, self.DEFAULT_BACKGROUND)

        self.build_menu_bar(config.get("title", "_default"), config.get("menu_bar", []))

        layout = config.get("layout")
        self.panes_root = self.build_panes(layout, self) if layout else None

    def build_panes(self, node: dict, master):
        '''
        Recursively builds a widgets.Panes tree from a layout-tree node:
        {"orientation": ..., "children": [{"id": ..., "weight": ..., "panes": {...}} | {"id": ..., "weight": ..., "widget": "<panel type>"}]}
        (PageManager.layout_tree builds this from a page config's
        layout_shape and layout_weights). Each child's "weight" is its proportional share of its parent -
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

        panes = widgets.Panes(master, self.context, node.get("orientation", "horizontal"), len(children), divisors, False,
                              transparent=self.transparent_panes, ids=[child["id"] for child in children])

        for i, child in enumerate(children):
            pane = panes.pane(i)
            if "panes" in child:
                self.build_panes(child["panes"], pane)
            elif "widget" in child:
                # A panel's type is its class's KEY (see widgets.PANELS)
                widgets.panel(child["widget"], pane, self.context, panel_id=child["id"])
            else:
                print(f"Pane-tree child {child!r} has neither 'panes' nor 'widget', skipping")

        return panes
