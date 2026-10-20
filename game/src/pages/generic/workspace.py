from ...app_core import Context

# Better Widgets
from ... import widgets
from ..page import Page

class WorkspacePage(Page):
    '''
    Page constructor for build_type "workspace". Reads its own config.json
    (resolved by PageManager from the key it was navigated to) and builds a
    MenuBar plus a DockArea of panels from the "menu_bar", "layout_shape"
    and "layout_weights" sections, instead of hardcoding a specific page's layout.
    '''

    # Used when a page's config has no "background" of its own (set
    # "background": false to turn it off). Shares the title pages'
    # network, still drifting - with its traffic stopped unless the user
    # turns on "Detailed Background" (off by default: it's distracting
    # behind the panels).
    DEFAULT_BACKGROUND = {"blur": 6, "packets": False}

    def __init__(self, context: Context):
        super().__init__(context)

        key = context.router.current_page
        config = context.pages.prepare_page_config(key)

        # The network behind the gaps between panels - slowly drifting and
        # without packets, so it reads as texture rather than content. The
        # panes turn transparent only if it's there.
        self.transparent_panes = self.add_background(config, self.DEFAULT_BACKGROUND, workspace=True)

        self.build_menu_bar(config.get("title", "_default"), config.get("menu_bar", []))

        # The panels, which the user can rearrange by dragging them by
        # their menu bars - autosaved with the page (see PageManager.save_current_page)
        layout = config.get("layout")
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.dock = widgets.DockArea(self, self.context, layout, self.make_panel, transparent=self.transparent_panes) if layout else None

    def make_panel(self, panel_id: str, master):
        # A panel's type is its class's KEY (see widgets.PANELS)
        return widgets.panel(self.context.pages.panel_type(panel_id), master, self.context, panel_id=panel_id)
