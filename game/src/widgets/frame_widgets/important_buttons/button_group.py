from PySide6.QtWidgets import QLabel
from ....app_core import Context
from ..overlay import Overlay
from ._base_button import ImportantButton

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
        Overlay(context.root, context, self, self.populate)

    def populate(self, overlay: Overlay):
        for header, button_classes in self.sections:
            if header is not None:
                label = QLabel(self.context.labels.get(f"menu_bar_headers_{header}"))
                label.setFont(self.context.style.get_font("small"))
                overlay.layout().addWidget(label)
            for button_class in button_classes:
                button = button_class(self.context)
                if not button.property("opens_overlay"):
                    # Close first, then act - an action that opens a dialog or
                    # rebuilds the page shouldn't do it under an open popup
                    button.clicked.disconnect()
                    button.clicked.connect(lambda checked=False, button=button: (overlay.hide(), button.on_click()))
                overlay.layout().addWidget(button)
