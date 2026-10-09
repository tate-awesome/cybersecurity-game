from PySide6.QtWidgets import QComboBox, QHBoxLayout, QLabel, QPushButton

from ..overlay import Overlay
from ._base_button import ImportantButton


class SelectColorTheme(ImportantButton):
    '''
    Opens a panel for picking the theme's color family: a dropdown, then
    Cancel / OK. OK applies it - keeping light or dark as they are (that's
    ToggleLightDarkMode's job) - and rebuilds the page in it.
    '''
    LABEL = "menu_bar_buttons_theme_button"
    TOOLTIP = "menu_bar_tooltips_theme_button"

    def __init__(self, context):
        super().__init__(context)
        Overlay(context.root, context, self, self.populate)

    def populate(self, overlay: Overlay):
        style, labels = self.context.style, self.context.labels
        mode, _, current = style.current_theme.partition("_")
        families = style.theme_families()

        label = QLabel(labels.get("theme_picker_color"))
        label.setFont(style.get_font())
        overlay.layout().addWidget(label)

        dropdown = QComboBox()
        dropdown.setFont(style.get_font())
        dropdown.addItems([family.title() for family in families])
        dropdown.setCurrentIndex(families.index(current) if current in families else 0)
        overlay.layout().addWidget(dropdown)

        buttons = QHBoxLayout()
        buttons.setSpacing(style.igap)
        buttons.addStretch(1)
        cancel = QPushButton(labels.get("theme_picker_cancel"))
        cancel.setFont(style.get_font())
        cancel.clicked.connect(lambda checked=False: overlay.hide())
        buttons.addWidget(cancel)
        ok = QPushButton(labels.get("theme_picker_ok"))
        ok.setFont(style.get_font())
        ok.setDefault(True)

        def apply():
            family = families[dropdown.currentIndex()]
            overlay.hide()
            if family != current:
                style.set_theme(f"{mode}_{family}")
        ok.clicked.connect(lambda checked=False: apply())
        buttons.addWidget(ok)
        overlay.layout().addLayout(buttons)
