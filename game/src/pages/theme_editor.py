from typing import ClassVar

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QComboBox, QGridLayout, QHBoxLayout, QLabel, QScrollArea, QVBoxLayout, QWidget

from ..app_core.context.themes import MATERIALS, PALETTE_KEYS, is_color
from ..widgets.panels.examples import EXAMPLE_PANELS
from .settings import SettingsPage

# The theme editor's own menu bar - the Appearance dropdown's theme buttons, and navigation
THEME_EDITOR_MENU_BAR = ["help_button", "toggle_button", "theme_button", "appearance_settings_button",
                         "back_button", "settings_button", "workspaces_button", "title_button", "quit_button"]

# How tall each row of the gallery's grid is (a panel spanning two rows gets both, and the gap)
GALLERY_ROW_HEIGHT = 340


class ThemeEditorPage(SettingsPage):
    '''
    The theme's materials (see themes.py) in a tab on the left. Bundled
    themes' materials are read-only: Customize copies the theme into the
    user's own file (see Style.customize), whose materials change live. On
    the right, a scrolling grid of example panels (see
    widgets.panels.examples) - every kind of panel body with made-up data -
    so each change shows on everything it touches.
    '''

    LABEL_WIDTH = 190
    CONTROL_WIDTH = 300  # room for a material's color and opacity side by side
    SHOW_NOTES = False  # no room beside the gallery - rows explain themselves in tooltips
    TITLE = "theme_editor"
    MENU_BAR_BUTTONS = THEME_EDITOR_MENU_BAR

    selected_tab: ClassVar[int] = 0

    def place_tabs(self):
        row = QHBoxLayout()
        row.setSpacing(self.style.igap)
        self.layout().addLayout(row, 1)
        row.addWidget(self.tabs)
        self.gallery = self.build_gallery()
        row.addWidget(self.gallery, 1)

    def build_tabs(self):
        self.build_materials_tab()
        # As wide as the widest tab's rows need (their names' length depends on the
        # language and font), plus the scrollbar - the gallery gets the rest
        content = max(self.tabs.widget(index).widget().sizeHint().width() for index in range(self.tabs.count()))
        self.tabs.setFixedWidth(content + self.style.get_scrollbar_size() + self.style.igap * 2)

    # Tabs
    def build_materials_tab(self):
        style = self.style
        tab = self.new_tab("materials")

        materials = self.section(tab, "materials")
        editable = style.is_editable()
        if not editable:
            materials.row("settings_page_rows_customize_theme", self.button(
                "settings_page_buttons_customize_theme", style.customize), "settings_page_row_notes_customize_theme")
        mode = style.current_theme.partition("_")[0]
        for name in MATERIALS:
            control = self.material_control(name, style.theme_materials()[name][mode])
            control.setEnabled(editable)
            materials.row(f"theme_materials_{name}", control, f"theme_materials_notes_{name}")
            # Only once placed - placing an editable box resets the font it was given
            control.findChild(QComboBox).setFont(style.get_font())

        translucency = self.section(tab, "translucency")
        translucency.row("settings_page_rows_translucent_surfaces",
                         self.checkbox(style.translucent_surfaces, style.set_translucent_surfaces),
                         "settings_page_row_notes_translucent_surfaces")

        reset = self.section(tab, "appearance_reset")
        reset.row("settings_page_rows_reset_surfaces", self.button(
            "settings_page_buttons_reset", self.reset_surfaces), "settings_page_row_notes_reset_surfaces")

    def reset_surfaces(self):
        self.style.reset_surfaces()

    def material_control(self, name: str, entry: dict) -> QWidget:
        '''A material's color - a palette key, or type a hex code - and its opacity, side by side.'''
        row = QWidget()
        layout = QHBoxLayout(row)
        layout.setContentsMargins(0, 0, 0, 0)
        color = QComboBox()
        color.setEditable(True)
        color.addItems(PALETTE_KEYS)
        color.setCurrentText(entry["color"])  # before connecting, so loading it isn't an edit
        color.setMinimumContentsLength(9)
        color.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon)
        # Typing a hex code passes through partial ones - only whole colors apply
        color.currentTextChanged.connect(lambda text: is_color(text) and self.style.set_material_value(name, color=text))
        layout.addWidget(color)
        layout.addWidget(self.slider(round(entry["opacity"] * 100), 0, 100, "%",
                                     lambda value: self.style.set_material_value(name, opacity=value / 100)), 1)
        return row

    # Gallery
    def build_gallery(self) -> QScrollArea:
        '''The example panels in a grid (see examples.EXAMPLE_PANELS), under a note saying what they are.'''
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { background-color: transparent; border: none; }")
        body = QWidget()
        self.style.set_material(body, "none")
        column = QVBoxLayout(body)
        column.setSpacing(self.style.igap)
        column.setContentsMargins(0, 0, self.style.igap, 0)

        note = QLabel(self.labels.get("theme_editor_gallery_note"))
        note.setFont(self.style.get_font("small"))
        note.setWordWrap(True)
        column.addWidget(note)

        grid = QGridLayout()
        grid.setSpacing(self.style.igap)
        rows = max(row + row_span for _, (row, _, row_span, _) in EXAMPLE_PANELS)
        columns = max(col + col_span for _, (_, col, _, col_span) in EXAMPLE_PANELS)
        for row in range(rows):
            grid.setRowMinimumHeight(row, GALLERY_ROW_HEIGHT)
        for col in range(columns):
            grid.setColumnStretch(col, 1)
        for panel_class, (row, col, row_span, col_span) in EXAMPLE_PANELS:
            # Panels add themselves to their master's layout
            cell = QWidget()
            cell.setLayout(QVBoxLayout())
            cell.layout().setContentsMargins(0, 0, 0, 0)
            cell.setFixedHeight(row_span * GALLERY_ROW_HEIGHT + (row_span - 1) * self.style.igap)
            grid.addWidget(cell, row, col, row_span, col_span)
            panel_class(cell, self.context)
        column.addLayout(grid)
        column.addStretch(1)
        scroll.setWidget(body)
        return scroll
