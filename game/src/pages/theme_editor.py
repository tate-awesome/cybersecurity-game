from collections.abc import Callable
from typing import ClassVar

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (QColorDialog, QComboBox, QDialog, QGridLayout, QHBoxLayout, QLabel,
                               QLineEdit, QPlainTextEdit, QPushButton, QScrollArea, QVBoxLayout, QWidget)

from ..app_core.context.themes import (BUTTON_KINDS, DATA_MATERIALS, INK_MATERIALS, MATERIALS, MAX_BACKGROUND_BLUR, MAX_BUTTON_RADIUS,
                                      MAX_PANEL_FRAME, MAX_PANEL_RADIUS)
from ..widgets import MenuBar, popup
from ..widgets.frame_widgets.important_buttons import POPUP_MARK, developer_text
from ..widgets.panels.examples import EXAMPLE_PANELS
from .settings import SettingsPage


# How tall each row of the gallery's grid is (a panel spanning two rows gets both, and the gap)
GALLERY_ROW_HEIGHT = 340
# Shown after the name of a theme with unsaved edits
UNSAVED_MARK = " *"


class MaterialEditor:
    '''
    The Materials tab's rows: each material's color, and its opacity if the
    theme allows transparency, for the mode being edited - shared by the
    theme editor and the developers' material editor popup (see
    MaterialEditorPopup). Mixed into something that has style, slider,
    new_tab and section like a SettingsPage's.
    '''

    def build_materials_tab(self):
        '''
        Every material for the mode being edited: surfaces with their
        opacity (if the theme allows transparency), each kind of button -
        its corners and its own materials - then text and lines.
        '''
        style = self.style
        editable = style.is_editable()
        tab = self.new_tab("materials")
        kinds = {kind: [kind, f"{kind}_hover", f"{kind}_border", f"{kind}_text", f"{kind}_hover_text"] for kind in BUTTON_KINDS}
        in_kinds = {name for names in kinds.values() for name in names}
        self.material_rows(self.section(tab, "materials"), [name for name in MATERIALS if name not in INK_MATERIALS and name not in in_kinds])
        for kind, names in kinds.items():
            section = self.section(tab, f"{kind}s")
            radius = self.slider(style.button_radius(kind), 0, MAX_BUTTON_RADIUS, "px",
                                 lambda value, kind=kind: style.set_button_radius(kind, value))
            radius.setEnabled(editable)
            section.row("theme_editor_rows_button_radius", radius, "theme_editor_row_notes_button_radius")
            self.material_rows(section, names)
        self.material_rows(self.section(tab, "ink_materials"),
                           [name for name in INK_MATERIALS if name not in in_kinds and name not in DATA_MATERIALS])
        self.material_rows(self.section(tab, "data_materials"), list(DATA_MATERIALS))

    def material_rows(self, section: "SettingsSection", names: list[str]):
        '''A row in section for each named material, in the mode being edited.'''
        style = self.style
        mode = style.current_theme.partition("_")[0]
        for name in names:
            with_opacity = style.allows_transparency() and name not in INK_MATERIALS
            control = self.material_control(name, style.theme_materials()[name][mode], with_opacity)
            control.setEnabled(style.is_editable())
            section.row(f"theme_materials_{name}", control, f"theme_materials_notes_{name}")

    def material_control(self, name: str, entry: dict, with_opacity: bool) -> QWidget:
        '''A material's color - click it to pick another - and, with_opacity, how solid it is.'''
        row = QWidget()
        layout = QHBoxLayout(row)
        layout.setContentsMargins(0, 0, 0, 0)
        swatch = QPushButton()
        swatch.setFont(self.style.get_font("mono"))
        swatch.setObjectName(f"_swatch_{id(swatch)}")
        self.paint_swatch(swatch, entry["color"])
        swatch.clicked.connect(lambda checked=False: self.pick_color(name, swatch))
        layout.addWidget(swatch, 1)
        if with_opacity:
            layout.addWidget(self.slider(round(entry["opacity"] * 100), 0, 100, "%",
                                         lambda value: self.style.set_material_value(name, opacity=value / 100)), 1)
        return row

    @staticmethod
    def paint_swatch(swatch: QPushButton, color: str):
        '''The button showing a material's color: filled with it, its hex code on it in black or white, whichever reads.'''
        text = "#000000" if QColor(color).lightnessF() > 0.55 else "#ffffff"
        swatch.setText(color)
        swatch.setStyleSheet(f"QPushButton#{swatch.objectName()} {{ background-color: {color}; color: {text};"
                             f" border: 1px solid {text}; }}")

    def pick_color(self, name: str, swatch: QPushButton):
        '''Picks a material's color - shown everywhere while picking, and put back if cancelled.'''
        original = swatch.text()
        dialog = QColorDialog(QColor(original), self)

        def preview(color: QColor):
            self.style.set_material_value(name, color=color.name())
            self.paint_swatch(swatch, color.name())
        dialog.currentColorChanged.connect(preview)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            preview(dialog.selectedColor())
        else:
            preview(QColor(original))


class ThemeEditorPage(MaterialEditor, SettingsPage):
    '''
    Makes and edits themes (see themes.py). The menu bar picks the theme
    to edit - any built-in one or the user's own - and has New Theme (a
    copy of any of them, as the user's own), Save, and for developers Make
    Built-in (see Style.make_built_in). Built-in themes can be looked at,
    but only the user's own can be changed.

    On the left, tabs: General (name, description, which mode is being
    edited, and whether the theme allows transparency) and Materials (each
    kind of widget's color, and its opacity if the theme allows
    transparency - for the mode being edited). Edits
    show at once, everywhere; Save writes them to the theme's file. On the
    right, a scrolling grid of example panels (see widgets.panels.examples)
    - every kind of panel body with made-up data - so each change shows on
    everything it touches.
    '''

    LABEL_WIDTH = 170
    CONTROL_WIDTH = 300  # room for a material's color and opacity side by side
    SHOW_NOTES = False  # no room beside the gallery - rows explain themselves in tooltips
    TITLE = "theme_editor"

    selected_tab: ClassVar[int] = 0

    # Menu bar
    def add_menu_bar_entries(self, menu_bar: MenuBar):
        labels = self.labels
        self.selector = menu_bar.add_dropdown([])
        self.selector.setToolTip(labels.get("menu_bar_tooltips_theme_editor_selector"))
        self.selector.setMinimumContentsLength(18)
        self.selector.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon)
        # activated - only the user's picks, not refresh_menu_bar refilling it
        self.selector.activated.connect(lambda index: self.select_theme(self.selector.itemData(index)))
        self.new_button = menu_bar.add_button("theme_editor_new", self.new_theme)
        self.new_button.setText(f"{self.new_button.text()} {POPUP_MARK}")
        self.new_button.setToolTip(labels.get("menu_bar_tooltips_theme_editor_new"))
        self.built_in_button = None
        if self.context.preferences.is_developer():
            self.built_in_button = menu_bar.add_button("theme_editor_make_built_in", self.make_built_in)
            self.built_in_button.setText(developer_text(self.built_in_button.text()))
            self.built_in_button.setToolTip(labels.get("menu_bar_tooltips_theme_editor_make_built_in"))
        self.save_button = menu_bar.add_button("theme_editor_save", self.style.save_theme)
        self.save_button.setToolTip(labels.get("menu_bar_tooltips_theme_editor_save"))
        self.style.signals.edited.connect(self.refresh_menu_bar)
        self.refresh_menu_bar()

    def refresh_menu_bar(self):
        '''The selector's themes - the current one picked - and which buttons apply to it.'''
        style = self.style
        family = style.theme_family()
        self.selector.blockSignals(True)
        self.selector.clear()
        built_in, own = style.editor_themes()
        self.fill_themes(self.selector, built_in, own)
        self.selector.setCurrentIndex(max(0, self.selector.findData(family)))
        self.selector.blockSignals(False)
        self.save_button.setEnabled(style.is_editable() and family in style.unsaved)
        if self.built_in_button is not None:
            self.built_in_button.setEnabled(style.is_user_theme(family))

    def fill_themes(self, combo: QComboBox, built_in: dict[str, str], own: dict[str, str]):
        '''Built-in themes, then the user's own (marked if unsaved), each with its family as data.'''
        for family, name in built_in.items():
            combo.addItem(name, family)
        if own:
            combo.insertSeparator(combo.count())
        for family, name in own.items():
            combo.addItem(name + (UNSAVED_MARK if family in self.style.unsaved else ""), family)

    def select_theme(self, family: str | None):
        if family and family != self.style.theme_family():
            self.leave_theme(lambda: self.style.set_family(family))

    def leave_theme(self, then: Callable[[], None]):
        '''Does then (which switches themes) - after asking, if the current theme has unsaved edits.'''
        style = self.style
        family = style.theme_family()
        if family not in style.unsaved:
            then()
            return
        self.refresh_menu_bar()  # back to the current theme until it's decided
        name = style.preset_name(family)

        def discard():
            style.discard_changes(family)
            then()
        popup.confirm_dialog(self, self.context, self.labels.get("theme_editor_discard").replace("{name}", name),
                             self.labels.get("theme_editor_discard_confirm"), self.labels.get("theme_editor_discard_cancel"),
                             discard)

    def new_theme(self):
        '''Asks which theme to start from, then makes the user's own copy of it and switches to it.'''
        labels = self.labels
        dialog = popup.PopupWindow(self, self.context, labels.get("theme_editor_new_title"))
        dialog.add_text(labels.get("theme_editor_new_prompt"))
        source = QComboBox()
        source.setFont(self.style.get_font())
        self.fill_themes(source, *self.style.editor_themes())
        source.setCurrentIndex(max(0, source.findData(self.style.theme_family())))
        dialog.body.addWidget(source)
        dialog.add_button(labels.get("theme_editor_new_confirm"), dialog.accept)
        dialog.add_button("Cancel", dialog.reject)
        if dialog.exec() == QDialog.DialogCode.Accepted and source.currentData():
            family = source.currentData()
            self.leave_theme(lambda: self.style.new_theme(family))

    def make_built_in(self):
        '''Developers: saves the theme being edited into assets/themes - asking first if that replaces one.'''
        style = self.style
        family = style.theme_family()
        if not style.is_user_theme(family):
            return

        def make():
            path = style.make_built_in(family)
            if path is not None:
                popup.message(self, self.context, self.labels.get("theme_editor_made_built_in").replace("{path}", str(path)))
        path = style.built_in_path(family)
        if path.exists():
            popup.confirm_dialog(self, self.context, self.labels.get("theme_editor_replace_built_in").replace("{name}", path.name),
                                 self.labels.get("theme_editor_replace_confirm"), self.labels.get("theme_editor_discard_cancel"),
                                 make)
        else:
            make()

    def rebuild_tabs(self):
        super().rebuild_tabs()
        self.refresh_menu_bar()

    # Layout
    def place_tabs(self):
        row = QHBoxLayout()
        row.setSpacing(self.style.igap)
        self.layout().addLayout(row, 1)
        row.addWidget(self.tabs)
        self.gallery = self.build_gallery()
        row.addWidget(self.gallery, 1)

    def build_tabs(self):
        self.build_general_tab()
        self.build_materials_tab()
        # As wide as the widest tab's rows need (their names' length depends on the
        # language and font), plus the scrollbar - the gallery gets the rest
        content = max(self.tabs.widget(index).widget().sizeHint().width() for index in range(self.tabs.count()))
        self.tabs.setFixedWidth(content + self.style.get_scrollbar_size() + self.style.igap * 2)

    # Tabs
    def build_general_tab(self):
        style = self.style
        family = style.theme_family()
        info = style.preset_info[family]
        editable = style.is_editable()
        tab = self.new_tab("general")
        section = self.section(tab, "theme_general")
        if not editable:
            new = QPushButton(f"{self.labels.get('menu_bar_buttons_theme_editor_new')} {POPUP_MARK}")
            new.setFont(style.get_font())
            new.clicked.connect(lambda checked=False: self.new_theme())
            section.row("theme_editor_rows_built_in", new, "theme_editor_row_notes_built_in")

        name = QLineEdit(info.get("label", family))
        name.setFont(style.get_font())
        name.setMinimumWidth(self.CONTROL_WIDTH)
        name.editingFinished.connect(lambda: style.set_theme_info(label=name.text()))
        name.setEnabled(editable)
        section.row("theme_editor_rows_name", name, "theme_editor_row_notes_name")

        description = QPlainTextEdit(info.get("note", ""))
        description.setFont(style.get_font())
        description.setFixedHeight(style.igap * 12)
        description.textChanged.connect(lambda: style.set_theme_info(note=description.toPlainText()))
        description.setEnabled(editable)
        section.row("theme_editor_rows_description", description, "theme_editor_row_notes_description")

        # Not an edit - which mode is shown, so it works on built-in themes too
        dark = style.current_theme.partition("_")[0] == "dark"
        section.row("theme_editor_rows_dark_mode", self.checkbox(
            dark, lambda on: style.set_theme(f"{'dark' if on else 'light'}_{style.theme_family()}")),
            "theme_editor_row_notes_dark_mode")

        transparency = self.checkbox(style.allows_transparency(), style.set_transparency)
        transparency.setEnabled(editable)
        section.row("theme_editor_rows_transparency", transparency, "theme_editor_row_notes_transparency")

        # The rest of the theme's look (see themes.STYLE_DEFAULTS) - the others are only in its file
        background = self.checkbox(style.setting("background"), lambda on: style.set_setting("background", on))
        background.setEnabled(editable)
        section.row("theme_editor_rows_background", background, "theme_editor_row_notes_background")
        theme_blur = style.setting("background_blur")
        blur = self.slider(-1 if theme_blur is None else theme_blur, -1, MAX_BACKGROUND_BLUR, "px",
                           lambda value: style.set_setting("background_blur", None if value < 0 else value), live=False)
        blur.setEnabled(editable)
        section.row("theme_editor_rows_background_blur", blur, "theme_editor_row_notes_background_blur")
        corners = self.slider(style.PANEL_RADIUS, 0, MAX_PANEL_RADIUS, "px", lambda value: style.set_setting("panel_radius", value))
        corners.setEnabled(editable)
        section.row("theme_editor_rows_panel_radius", corners, "theme_editor_row_notes_panel_radius")
        frame = self.slider(style.setting("panel_frame"), 0, MAX_PANEL_FRAME, "px", lambda value: style.set_setting("panel_frame", value))
        frame.setEnabled(editable)
        section.row("theme_editor_rows_panel_frame", frame, "theme_editor_row_notes_panel_frame")

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
