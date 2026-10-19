from PySide6.QtWidgets import QLabel
from ....app_core import Context
from ..overlay import Overlay
from ._base_button import ImportantButton, developer_text

# Qt's "no maximum" widget size (QWIDGETSIZE_MAX, which PySide6 doesn't export)
QWIDGETSIZE_MAX = (1 << 24) - 1

# Sections shown only in developer mode - marked as developer-only, header and every button
DEVELOPER_SECTIONS = {"debug_tools"}

# One titled block of a group: (header key - "menu_bar_headers_<key>", or None - , its buttons in order)
Section = tuple[str | None, list[type[ImportantButton]]]


def offered_sections(context: Context, sections: list[Section]) -> list[Section]:
    '''
    The sections as they are right now - each with just its available
    buttons (see ImportantButton.is_available), developer-only ones only in
    developer mode, and any left empty dropped.
    '''
    developer = context.preferences.is_developer()
    offered = [(header, [button_class for button_class in button_classes if button_class.is_available(context)])
               for header, button_classes in sections if developer or header not in DEVELOPER_SECTIONS]
    return [section for section in offered if section[1]]


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
        self.overlay = Overlay(context.root, context, self, self.populate)

    def show_icon(self, icon: str, active_icon: str | None = None):
        '''Shows the group as just its icon - the overlay's ▾/▴ isn't in the icon font, so open or closed it keeps the icon.'''
        super().show_icon(icon, active_icon)
        self.overlay.closed_text = self.overlay.open_text = self.text()

    def populate(self, overlay: Overlay):
        for header, button_classes in self.sections:
            developer = header in DEVELOPER_SECTIONS
            if header is not None:
                text = self.context.labels.get(f"menu_bar_headers_{header}")
                label = QLabel(developer_text(text) if developer else text)
                label.setFont(self.context.style.get_font("small"))
                if developer:
                    # The mark's fallback font has a taller line - keep the header's own
                    label.setFixedHeight(label.fontMetrics().height())
                overlay.layout().addWidget(label)
            for button_class in button_classes:
                button = button_class(self.context)
                if developer:
                    button.mark_developer_only()
                if not button.property("opens_overlay"):
                    # Close first, then act - an action that opens a dialog or
                    # rebuilds the page shouldn't do it under an open popup
                    button.clicked.disconnect()
                    button.clicked.connect(lambda checked=False, button=button: (overlay.hide(), button.on_click()))
                overlay.layout().addWidget(button)
