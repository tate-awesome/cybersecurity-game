from PySide6.QtWidgets import QComboBox, QHBoxLayout, QLabel, QPushButton

from ..overlay import Overlay
from ._base_button import ImportantButton


class SelectColorTheme(ImportantButton):
    '''
    Opens a panel for a quick theme change: a dropdown, then Cancel / OK,
    and a link to the settings page's Appearance tab for everything else.
    The dropdown picks the accent color - or, while a special theme is in
    use, another special theme. OK applies it - keeping light or dark as
    they are (that's ToggleLightDarkMode's job) - and rebuilds the page in it.
    '''
    LABEL = "menu_bar_buttons_theme_button"
    TOOLTIP = "menu_bar_tooltips_theme_button"

    def __init__(self, context):
        super().__init__(context)
        Overlay(context.root, context, self, self.populate)

    def populate(self, overlay: Overlay):
        style, labels = self.context.style, self.context.labels
        if style.is_preset():
            options = style.preset_names()
            current = style.theme_family()
            apply_choice = style.set_family
            title = "theme_picker_special"
        else:
            options = {name: name.replace("_", " ").title() for name in style.accents}
            current = style.theme_accent
            apply_choice = style.set_accent
            title = "theme_picker_accent"
        values = list(options)

        label = QLabel(labels.get(title))
        label.setFont(style.get_font())
        overlay.layout().addWidget(label)

        dropdown = QComboBox()
        dropdown.setFont(style.get_font())
        dropdown.addItems(list(options.values()))
        dropdown.setCurrentIndex(values.index(current) if current in values else 0)
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
            choice = values[dropdown.currentIndex()] if values else current
            overlay.hide()
            if choice != current:
                apply_choice(choice)
        ok.clicked.connect(lambda checked=False: apply())
        buttons.addWidget(ok)
        overlay.layout().addLayout(buttons)

        more = QPushButton(labels.get("theme_picker_settings"))
        more.setFont(style.get_font())

        def open_settings():
            # Imported here - pages import widgets, so not at the top
            from ....pages.settings import SettingsPage
            overlay.hide()
            SettingsPage.selected_tab = SettingsPage.APPEARANCE_TAB
            self.context.router.show("settings")
        more.clicked.connect(lambda checked=False: open_settings())
        overlay.layout().addWidget(more)
