from typing import ClassVar

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QComboBox, QGridLayout, QHBoxLayout, QLabel, QScrollArea, QVBoxLayout, QWidget

from ..app_core.context.style import THEME_ADJUST_RANGE, THEME_TINT_MAX
from ..app_core.context.themes import MATERIALS, PALETTE_KEYS, is_color
from ..widgets.frame_widgets.important_buttons import ResetTheme
from ..widgets.panels.examples import EXAMPLE_PANELS
from .settings import SettingsPage

# The theme editor's own menu bar - the theme buttons it doesn't already have as rows, and navigation
THEME_EDITOR_MENU_BAR = ["help_button", "toggle_button", "theme_button", "import_themes_button", "reset_theme_button",
                         "back_button", "settings_button", "workspaces_button", "title_button", "quit_button"]

# How tall each row of the gallery's grid is (a panel spanning two rows gets both, and the gap)
GALLERY_ROW_HEIGHT = 340


class ThemeEditorPage(SettingsPage):
    '''
    Every theme setting beyond the few on the settings page and in the
    menu bar's Themes section (see SettingsPage.theme_rows) - accents and
    hierarchies, every special theme, tint and layer fine-tuning - and
    the theme's materials (see themes.py), in tabs on the left. Bundled
    themes' materials are read-only: Customize copies the theme into the
    user's own file (see Style.customize), whose materials change live. On the
    right, a scrolling grid of example panels (see widgets.panels.examples) -
    every kind of panel body with made-up data - so each change shows on
    everything it touches.
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
        self.build_colors_tab()
        self.build_materials_tab()
        # As wide as the widest tab's rows need (their names' length depends on the
        # language and font), plus the scrollbar - the gallery gets the rest
        content = max(self.tabs.widget(index).widget().sizeHint().width() for index in range(self.tabs.count()))
        self.tabs.setFixedWidth(content + self.style.get_scrollbar_size() + self.style.igap * 2)

    # Tabs
    def build_colors_tab(self):
        style = self.style
        tab = self.new_tab("colors")

        theme = self.section(tab, "theme_colors")
        mode, _, family = style.current_theme.partition("_")
        preset = style.is_preset()
        theme.row("settings_page_rows_mode", self.dropdown(
            {"dark": self.labels.get("settings_page_mode_dark"), "light": self.labels.get("settings_page_mode_light")},
            mode, lambda value: style.set_theme(f"{value}_{family}")), "settings_page_row_notes_mode")
        # While a special theme is in use, these show that instead - so any pick switches back
        in_use = {"": self.labels.get("settings_page_special_in_use")} if preset else {}
        theme.row("settings_page_rows_accent", self.dropdown(
            {**in_use, **{name: name.replace("_", " ").title() for name in style.accents}},
            "" if preset else style.theme_accent, style.set_accent), "settings_page_row_notes_accent")
        theme.row("settings_page_rows_hierarchy", self.dropdown(
            {**in_use, **{name: name.replace("_", " ").title() for name in style.hierarchies}},
            "" if preset else style.theme_hierarchy, style.set_hierarchy), "settings_page_row_notes_hierarchy")
        # Rebuilds the page, so only on release - not every step of a drag.
        # Special themes have their own colors, so it does nothing for them
        tint = self.slider(round(style.theme_tint * 100), 0, round(THEME_TINT_MAX * 100), "%",
                           lambda value: style.set_tint(value / 100), live=False)
        tint.setEnabled(not preset)
        theme.row("settings_page_rows_tint", tint, "settings_page_row_notes_tint")
        theme.row("settings_page_rows_inset", self.checkbox(style.theme_inset, style.set_inset), "settings_page_row_notes_inset")
        theme.row("settings_labels_surface_invert_buttons", self.checkbox(style.invert_buttons, style.set_invert_buttons),
                  "settings_tooltips_surface_invert_buttons")

        special = self.section(tab, "special_themes")
        presets = style.preset_names()
        special.row("settings_page_rows_special_theme", self.dropdown(
            {"": self.labels.get("settings_page_no_special_theme"), **presets}, family if preset else "",
            lambda value: style.set_family(value or f"{style.theme_accent}.{style.theme_hierarchy}"),
            {name: style.preset_info[name].get("note", "") for name in presets}), "settings_page_row_notes_special_theme")

        # Per mode: step size and height shape accent + hierarchy themes; border contrast is for every theme
        layers = self.section(tab, "layers_and_borders")
        for theme_mode in ("dark", "light"):
            for key in THEME_ADJUST_RANGE:
                low, high = THEME_ADJUST_RANGE[key]
                percent = key != "height"  # height is in L* steps, the others are multipliers
                scale = 100 if percent else 1
                control = self.slider(round(style.theme_adjust[theme_mode][key] * scale), round(low * scale), round(high * scale),
                                      "%" if percent else "",
                                      lambda value, theme_mode=theme_mode, key=key, scale=scale: style.set_adjust(theme_mode, key, value / scale),
                                      live=False)
                control.setEnabled(key == "border" or not preset)
                layers.row(f"settings_page_rows_{theme_mode}_{key}", control, f"settings_page_row_notes_adjust_{key}")

        reset = self.section(tab, "theme_reset")
        reset.row("settings_page_rows_reset_theme", ResetTheme(self.context), "settings_page_row_notes_reset_theme")

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
