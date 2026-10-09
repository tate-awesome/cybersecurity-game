from collections.abc import Callable

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QCheckBox, QComboBox, QDialog, QGridLayout, QLabel, QPushButton, QSlider, QVBoxLayout, QWidget

from ....app_core.context.style import THEME_TINT_MAX
from ._base_button import ImportantButton


class SelectColorTheme(ImportantButton):
    '''Opens the theme window (see ThemeWindow) - or brings it to the front if it's already open.'''
    LABEL = "menu_bar_buttons_theme_button"
    TOOLTIP = "menu_bar_tooltips_theme_button"
    POPOUT = True

    def on_click(self):
        ThemeWindow.open(self.context)


class ThemeWindow(QDialog):
    '''
    A small window with every theme setting - the same ones as the settings
    page's Theme and Special Themes sections - and a link to the settings
    page's Appearance tab. Each setting applies as soon as it's picked.

    A window rather than an overlay: a theme change rebuilds the page, which
    would take an overlay (and the button it hangs from) down with it. This
    window belongs to the main window instead, so it stays open while the
    page rebuilds behind it, and the app's stylesheet recolors it.
    '''
    _window: "ThemeWindow | None" = None

    @classmethod
    def open(cls, context):
        if cls._window is None:
            cls._window = ThemeWindow(context)
        cls._window.show()
        cls._window.raise_()
        cls._window.activateWindow()

    def __init__(self, context):
        super().__init__(context.root)
        self.context = context
        self.setWindowTitle(context.labels.get("theme_window_title"))
        self.setLayout(QVBoxLayout())
        self.body: QWidget | None = None  # filled in on show (see showEvent)

    def showEvent(self, event):
        # Anything changed while it was closed (e.g. Toggle Theme) shows when it opens again
        self.populate()
        super().showEvent(event)

    def changed(self, apply: Callable[[], None]):
        '''Applies a setting, then rebuilds this window's controls to match - once the control that changed is done with its signal.'''
        apply()
        QTimer.singleShot(0, self.populate)

    def populate(self):
        style, labels = self.context.style, self.context.labels
        if self.body is not None:
            self.body.deleteLater()
        self.body = QWidget()
        self.layout().addWidget(self.body)
        column = QVBoxLayout(self.body)
        column.setContentsMargins(0, 0, 0, 0)
        grid = QGridLayout()
        grid.setHorizontalSpacing(style.igap)
        column.addLayout(grid)
        mode, _, family = style.current_theme.partition("_")
        preset = style.is_preset()

        def row(name: str, note: str, control):
            label = QLabel(labels.get(name))
            label.setFont(style.get_font())
            label.setToolTip(labels.get(note))
            control.setToolTip(labels.get(note))
            index = grid.rowCount()
            grid.addWidget(label, index, 0)
            grid.addWidget(control, index, 1)
            return control

        def dropdown(options: dict[str, str], current: str, apply: Callable[[str], None]) -> QComboBox:
            combo = QComboBox()
            combo.setFont(style.get_font())
            for value, text in options.items():
                combo.addItem(text, value)
            combo.setCurrentIndex(max(0, combo.findData(current)))  # before connecting, so it isn't a change
            combo.currentIndexChanged.connect(lambda index: self.changed(lambda: apply(combo.itemData(index))))
            return combo

        def checkbox(checked: bool, apply: Callable[[bool], None]) -> QCheckBox:
            box = QCheckBox()
            box.setChecked(checked)
            box.toggled.connect(lambda on: self.changed(lambda: apply(on)))
            return box

        row("settings_page_rows_mode", "settings_page_row_notes_mode", dropdown(
            {"dark": labels.get("settings_page_mode_dark"), "light": labels.get("settings_page_mode_light")},
            mode, lambda value: style.set_theme(f"{value}_{family}")))
        # A special theme has its own colors - accent, hierarchy and tint only apply without one
        row("settings_page_rows_accent", "settings_page_row_notes_accent", dropdown(
            {name: name.replace("_", " ").title() for name in style.accents},
            style.theme_accent, style.set_accent)).setEnabled(not preset)
        row("settings_page_rows_hierarchy", "settings_page_row_notes_hierarchy", dropdown(
            {name: name.replace("_", " ").title() for name in style.hierarchies},
            style.theme_hierarchy, style.set_hierarchy)).setEnabled(not preset)

        # Applies on release - every step of a drag would rebuild the page
        tint = QSlider(Qt.Orientation.Horizontal)
        tint.setRange(0, round(THEME_TINT_MAX * 100))
        tint.setValue(round(style.theme_tint * 100))
        tint.setTracking(False)
        tint.setEnabled(not preset)
        readout = QLabel(f"{tint.value()}%")
        readout.setFont(style.get_font())
        readout.setMinimumWidth(readout.fontMetrics().horizontalAdvance(f"{tint.maximum()}%") + 4)
        readout.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        tint.sliderMoved.connect(lambda value: readout.setText(f"{value}%"))
        tint.valueChanged.connect(lambda value: self.changed(lambda: style.set_tint(value / 100)))
        row("settings_page_rows_tint", "settings_page_row_notes_tint", tint)
        grid.addWidget(readout, grid.rowCount() - 1, 2)

        row("settings_page_rows_inset", "settings_page_row_notes_inset", checkbox(style.theme_inset, style.set_inset))
        row("settings_labels_surface_invert_buttons", "settings_tooltips_surface_invert_buttons", checkbox(
            style.invert_buttons, style.set_invert_buttons))
        special = row("settings_page_rows_special_theme", "settings_page_row_notes_special_theme", dropdown(
            {"": labels.get("settings_page_no_special_theme"), **style.preset_names()}, family if preset else "",
            lambda value: style.set_family(value or f"{style.theme_accent}.{style.theme_hierarchy}")))
        for index in range(1, special.count()):
            note = style.preset_info[special.itemData(index)].get("note")
            if note:
                special.setItemData(index, note, Qt.ItemDataRole.ToolTipRole)

        more = QPushButton(labels.get("theme_picker_settings"))
        more.setFont(style.get_font())
        more.clicked.connect(lambda checked=False: self.open_settings())
        column.addWidget(more)

    def open_settings(self):
        # Imported here - pages import widgets, so not at the top
        from ....pages.settings import SettingsPage
        self.close()
        SettingsPage.selected_tab = SettingsPage.APPEARANCE_TAB
        self.context.router.show("settings")
