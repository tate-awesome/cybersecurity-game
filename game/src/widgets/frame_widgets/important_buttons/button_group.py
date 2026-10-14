from PySide6.QtWidgets import QLabel
from ....app_core import Context
from ..overlay import Overlay
from ._base_button import ImportantButton

# Qt's "no maximum" widget size (QWIDGETSIZE_MAX, which PySide6 doesn't export)
QWIDGETSIZE_MAX = (1 << 24) - 1

# Groups shown only in developer mode - marked as developer-only, with every button in them
DEVELOPER_GROUPS = {"debug_button_group"}

# One titled block of a group: (header key - "menu_bar_headers_<key>", or None - , its buttons in order)
Section = tuple[str | None, list[type[ImportantButton]]]


class ButtonGroup(ImportantButton):
    '''
    Opens an overlay holding several important buttons, in titled sections
    (see MenuBar.MENU_BAR_GROUPS). Labeled "menu_bar_buttons_<group_key>",
    with the tooltip "menu_bar_tooltips_<group_key>".

    Like a menu, it closes as soon as one of its buttons is clicked - except
    buttons that open an overlay of their own, which opens on top of it.
    '''

    def __init__(self, context: Context, group_key: str, sections: list[Section]):
        super().__init__(context, f"menu_bar_buttons_{group_key}")
        self.setToolTip(context.labels.get(f"menu_bar_tooltips_{group_key}"))
        self.sections = sections
        self.developer_group = group_key in DEVELOPER_GROUPS
        if self.developer_group:
            self.mark_developer_only()  # before the overlay reads the text for its ▾
        self.overlay = Overlay(context.root, context, self, self.populate)

    def show_icon(self, icon: str, active_icon: str | None = None):
        '''
        Shows the group as just its icon - the overlay's ▾/▴ and the
        developer-only mark aren't in the icon font, so open or closed it
        keeps the icon, and Debug's bug says developer-only by itself.
        '''
        if self.developer_group:
            self.developer_only = False
            # (mark_developer_only fixed its height to the text's)
            self.setMinimumHeight(0)
            self.setMaximumHeight(QWIDGETSIZE_MAX)
        super().show_icon(icon, active_icon)
        self.overlay.closed_text = self.overlay.open_text = self.text()

    def populate(self, overlay: Overlay):
        for header, button_classes in self.sections:
            if header is not None:
                label = QLabel(self.context.labels.get(f"menu_bar_headers_{header}"))
                label.setFont(self.context.style.get_font("small"))
                overlay.layout().addWidget(label)
            for button_class in button_classes:
                button = button_class(self.context)
                if self.developer_group:
                    button.mark_developer_only()
                if not button.property("opens_overlay"):
                    # Close first, then act - an action that opens a dialog or
                    # rebuilds the page shouldn't do it under an open popup
                    button.clicked.disconnect()
                    button.clicked.connect(lambda checked=False, button=button: (overlay.hide(), button.on_click()))
                overlay.layout().addWidget(button)
