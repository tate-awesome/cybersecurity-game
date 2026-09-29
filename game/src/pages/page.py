from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QWidget
from ..app_core import Context

class Page(QWidget):
    '''
    Superclass for pages. Inherits QWidget. Router places the built page as
    the root window's central widget, so a page doesn't place itself the
    way a CTkFrame used to pack itself into its parent - it just needs a
    layout of its own for whatever it adds as children.
    '''

    def __init__(self, context: Context):
        super().__init__()
        self.context = context
        self.router = context.router
        self.style = context.style

        # A plain QWidget doesn't paint a stylesheet background at all by
        # default (unlike QFrame/QScrollArea, which do) - see Panel/
        # BaseForm for the same fix and the full explanation.
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet(self.style.themed(f"background-color: {self.style.color('root')};", self))
        self.setLayout(QVBoxLayout())
        self.setContentsMargins(self.style.igap, self.style.igap, self.style.igap, self.style.igap)
        # A page's own MenuBar and its Panes content are both typically
        # "widget"-colored - with no gap between them they read as one
        # fused bar instead of two distinct regions (global page toolbar vs.
        # the panel grid below it).
        self.layout().setSpacing(self.style.igap)

    def build_menu_bar(self, menu_bar_config: dict):
        '''
        Builds the page's MenuBar and calls one MenuBar method per
        {"builtin": "<method_name>"} entry in menu_bar_config["buttons"]
        (already expanded from any {"_ref": ...} splices by Json).
        Returns the MenuBar.
        '''
        from ..widgets import MenuBar
        title = menu_bar_config.get("title", "_default")
        menu_bar = MenuBar(self, self.context, title)

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
        return menu_bar

    def add_background(self, config: dict):
        '''
        Plays a procedural visual behind this page's content if its config
        has a "background": {"visual": <VISUALS key or "cycle">,
        "blur": <px, default 0>, "intensity": <0-1, default 1>}.
        Call it before adding content that should be drawn on top.
        '''
        background = config.get("background")
        if not isinstance(background, dict):
            return
        from ..widgets import VisualBackground
        VisualBackground(
            self, self.context,
            background.get("visual"),
            intensity=background.get("intensity", 1.0),
            in_layout=False,
            blur=background.get("blur", 0.0),
            # Same running network from page to page, not a fresh one each time
            shared=True,
        )
