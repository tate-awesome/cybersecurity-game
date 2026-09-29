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

    def build_menu_bar(self, title: str, buttons: list[str]):
        '''
        Builds the page's MenuBar - titled with the labels key
        "menu_bar_titles_<title>" - and adds one button per name in
        buttons, in order, each the name of a MenuBar button method
        (e.g. "quit_button"). Returns the MenuBar.
        '''
        from ..widgets import MenuBar
        menu_bar = MenuBar(self, self.context, title)

        for name in buttons:
            method = getattr(menu_bar, name, None) if isinstance(name, str) else None
            if not callable(method):
                print(f"MenuBar has no button named {name!r}, skipping")
                continue
            method()
        return menu_bar

    def add_background(self, config: dict, default: dict | None = None) -> bool:
        '''
        Plays a procedural visual behind this page's content if its config
        has a "background": {
            "visual": <VISUALS key or "cycle">,
            "blur": <px, default 0>,
            "intensity": <0-1, default 1>,
            "animate": <default true - false shows a still frame>,
            "packets": <default true - false draws a network mesh without traffic>
        }. With no "background" key, `default` is used instead (if given);
        "background": false turns it off even when there's a default.
        Call it before adding content that should be drawn on top.
        Returns whether a background was added.
        '''
        background = config.get("background", default)
        if not isinstance(background, dict):
            return False
        from ..widgets import VisualBackground
        VisualBackground(
            self, self.context,
            background.get("visual"),
            intensity=background.get("intensity", 1.0),
            in_layout=False,
            blur=background.get("blur", 0.0),
            # Same running network from page to page, not a fresh one each time
            shared=True,
            animate=background.get("animate", True),
            paint_options={"packets": background.get("packets", True)},
        )
        return True
