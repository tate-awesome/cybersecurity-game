import copy
from collections.abc import Callable
from typing import ClassVar

from PySide6.QtCore import QEvent, QObject, Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (QApplication, QColorDialog, QComboBox, QDialog, QGridLayout, QHBoxLayout, QLabel,
                               QLineEdit, QPlainTextEdit, QPushButton, QScrollArea, QTabWidget, QVBoxLayout, QWidget)

from ..app_core.context.themes import (BUTTON_KINDS, DATA_MATERIALS, INK_MATERIALS, MATERIALS, MAX_BACKGROUND_BLUR, MAX_BUTTON_LIFT,
                                      MAX_BUTTON_RADIUS, MAX_BUTTON_SHADOW, MAX_PANEL_FRAME, MAX_PANEL_RADIUS, MAX_SHADOW_REACH,
                                      OVERLAY_SHADOW)
from .. import widgets
from ..widgets import MenuBar, popup
from ..widgets.frame_widgets.important_buttons import POPUP_MARK, developer_text
from .generic.title import TitlePage
from .generic.workspace_select import WorkspaceSelectPage
from .settings import SettingsPage


# How tall each row of the panels preview's grid is, and how many panels across it
PANEL_ROW_HEIGHT = 360
PANEL_COLUMNS = 2
# The pages the other preview tabs show (see ThemeEditorPage.build_preview)
START_PAGE = "start"
WORKSPACE_SELECT_PAGE = "title/select_workspace"
# Shown after the name of a theme with unsaved edits
UNSAVED_MARK = " *"
# What a shadow turned on in the Shadows tab starts as (see ThemeEditorPage.turn_shadow) -
# a lit edge in white, up and left, the way panels are lit
NEW_SHADOWS = {
    "panel_shadow": OVERLAY_SHADOW,
    "panel_light": {"x": -6, "y": -6, "blur": 14, "dark": {"color": "#ffffff", "opacity": 0.6}, "light": {"color": "#ffffff", "opacity": 0.8}},
    "overlay_shadow": OVERLAY_SHADOW,
    "popup_shadow": OVERLAY_SHADOW,
}


class LookOnly(QObject):
    '''
    Makes a page shown as a preview (see ThemeEditorPage.build_preview)
    look-only: hovering it still shows, and its lists still scroll, but
    clicks and keys never reach it - its buttons would otherwise leave the
    theme editor, or the app.
    '''

    BLOCKED = (QEvent.Type.MouseButtonPress, QEvent.Type.MouseButtonRelease, QEvent.Type.MouseButtonDblClick,
               QEvent.Type.KeyPress, QEvent.Type.KeyRelease)

    def __init__(self, page: QWidget):
        super().__init__(page)
        self.page = page
        QApplication.instance().installEventFilter(self)

    def eventFilter(self, watched, event):
        if event.type() not in self.BLOCKED or not isinstance(watched, QWidget):
            return False
        try:
            return watched is self.page or self.page.isAncestorOf(watched)
        except RuntimeError:  # the page is being deleted
            return False


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
        swatch.clicked.connect(lambda checked=False: self.pick_color(swatch, lambda color: self.style.set_material_value(name, color=color)))
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

    def pick_color(self, swatch: QPushButton, apply: Callable[[str], None]):
        '''Picks another color for swatch - applied ("#rrggbb") as it's picked, so it shows everywhere, and put back if cancelled.'''
        original = swatch.text()
        dialog = QColorDialog(QColor(original), self)

        def preview(color: QColor):
            apply(color.name())
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
    edited, and whether the theme allows transparency), Materials (each
    kind of widget's color, and its opacity if the theme allows
    transparency - for the mode being edited) and Shadows (every shadow the
    theme draws - see build_shadows_tab). Edits show at once, everywhere;
    Save writes them to the theme's file. On the right, tabs previewing the
    real thing (see build_preview): one of every panel, the start menu and
    the workspace selector - so each change shows on everything it touches.
    '''

    LABEL_WIDTH = 170
    CONTROL_WIDTH = 300  # room for a material's color and opacity side by side
    SHOW_NOTES = False  # no room beside the gallery - rows explain themselves in tooltips
    TITLE = "theme_editor"

    selected_tab: ClassVar[int] = 0
    # The preview tab showing (see build_preview) - kept for the next time the page opens
    preview_tab: ClassVar[int] = 0

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
        self.preview = self.build_preview()
        row.addWidget(self.preview, 1)

    def build_tabs(self):
        self.build_general_tab()
        self.build_materials_tab()
        self.build_shadows_tab()
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

        # Not an edit - which mode is shown, so it works on built-in themes too.
        # Off for a theme with only one mode (see Style.theme_modes)
        dark = style.current_theme.partition("_")[0] == "dark"
        mode_box = self.checkbox(dark, lambda on: style.set_theme(f"{'dark' if on else 'light'}_{style.theme_family()}"))
        mode_box.setEnabled(len(style.theme_modes()) > 1)
        section.row("theme_editor_rows_dark_mode", mode_box, "theme_editor_row_notes_dark_mode")

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

    def build_shadows_tab(self):
        '''
        Every shadow the theme draws, each in its section: around panels,
        their lit edge, under overlays and popup windows - each one's
        offset and blur, and its color and opacity in the mode being edited
        (see shadow_rows) - and buttons' lift and hard shadow.
        '''
        style = self.style
        editable = style.is_editable()
        tab = self.new_tab("shadows")

        for key in ("panel_shadow", "panel_light"):
            section = self.section(tab, key)
            on = self.checkbox(style.setting(key) is not None, lambda on, key=key: self.turn_shadow(key, on))
            on.setEnabled(editable)
            section.row("theme_editor_rows_shadow_on", on, f"theme_editor_row_notes_{key}_on")
            self.shadow_rows(section, key, editable and style.setting(key) is not None)

        section = self.section(tab, "overlay_shadow")
        outline = self.dropdown({value: self.labels.get(f"theme_editor_overlay_outline_{value}") for value in ("accent", "shadow")},
                                style.setting("overlay_outline"), lambda value: style.set_setting("overlay_outline", value))
        outline.setEnabled(editable)
        section.row("theme_editor_rows_overlay_outline", outline, "theme_editor_row_notes_overlay_outline")
        self.shadow_rows(section, "overlay_shadow", editable and style.setting("overlay_outline") == "shadow")
        # A combo box's list opens as an overlay (see ChoiceList)
        example = QComboBox()
        example.setFont(style.get_font())
        example.addItems([self.labels.get(f"theme_editor_example_choice_{number}") for number in range(1, 4)])
        section.row("theme_editor_rows_try_overlay", example, "theme_editor_row_notes_try_overlay")

        section = self.section(tab, "popup_shadow")
        own = style.setting("popup_shadow") is not None
        same = self.checkbox(not own, self.share_popup_shadow)
        same.setEnabled(editable)
        section.row("theme_editor_rows_popup_same", same, "theme_editor_row_notes_popup_same")
        self.shadow_rows(section, "popup_shadow", editable and own)
        section.row("theme_editor_rows_try_popup",
                    self.button("theme_editor_try_popup", lambda: popup.message(self, self.context, self.labels.get("theme_editor_example_popup"))),
                    "theme_editor_row_notes_try_popup")

        section = self.section(tab, "button_shadows")
        for key, most in (("button_lift", MAX_BUTTON_LIFT), ("button_shadow", MAX_BUTTON_SHADOW)):
            slider = self.slider(style.setting(key), 0, most, "px", lambda value, key=key: style.set_setting(key, value), live=False)
            slider.setEnabled(editable)
            section.row(f"theme_editor_rows_{key}", slider, f"theme_editor_row_notes_{key}")

    def shadow_rows(self, section: "SettingsSection", key: str, editable: bool):
        '''
        section's rows for one of the theme's shadows (see
        Style.shadow_setting): how far across and down it falls and how
        blurred it is, then its color and opacity in the mode being edited.
        A shadow the theme hasn't shows what it would start as (see NEW_SHADOWS).
        '''
        style = self.style
        shadow = style.shadow_setting(key) or NEW_SHADOWS[key]
        # Applied once let go - each change restyles everything (see Style.set_setting)
        for name, least in (("x", -MAX_SHADOW_REACH), ("y", -MAX_SHADOW_REACH), ("blur", 0)):
            slider = self.slider(shadow[name], least, MAX_SHADOW_REACH, "px",
                                 lambda value, name=name: self.edit_shadow(key, **{name: value}), live=False)
            slider.setEnabled(editable)
            section.row(f"theme_editor_rows_shadow_{name}", slider, f"theme_editor_row_notes_shadow_{name}")
        entry = shadow[style.current_theme.partition("_")[0]]
        row = QWidget()
        layout = QHBoxLayout(row)
        layout.setContentsMargins(0, 0, 0, 0)
        swatch = QPushButton()
        swatch.setFont(style.get_font("mono"))
        swatch.setObjectName(f"_swatch_{id(swatch)}")
        self.paint_swatch(swatch, entry["color"])
        # The tabs aren't built again while picking - the swatch has to outlive the picker
        swatch.clicked.connect(lambda checked=False: self.pick_color(swatch, lambda color: self.edit_shadow(key, rebuild=False, color=color)))
        layout.addWidget(swatch, 1)
        layout.addWidget(self.slider(round(entry["opacity"] * 100), 0, 100, "%",
                                     lambda value: self.edit_shadow(key, opacity=value / 100), live=False), 1)
        row.setEnabled(editable)
        section.row("theme_editor_rows_shadow_color", row, "theme_editor_row_notes_shadow_color")

    def edit_shadow(self, key: str, rebuild: bool = True, **changes):
        '''
        Changes one of the theme's shadows (see shadow_rows): "x", "y" and
        "blur" in both modes, "color" and "opacity" in the mode being
        edited. rebuild=False keeps the tabs as they are (see rebuild_tabs).
        '''
        style = self.style
        shadow = copy.deepcopy(style.shadow_setting(key) or NEW_SHADOWS[key])
        mode = style.current_theme.partition("_")[0]
        for name, value in changes.items():
            (shadow if name in ("x", "y", "blur") else shadow[mode])[name] = value
        style.set_setting(key, shadow)
        if not rebuild:
            self.rebuild_timer.stop()

    def turn_shadow(self, key: str, on: bool):
        '''Gives the theme one of its panel shadows (see NEW_SHADOWS) - or takes it away.'''
        self.style.set_setting(key, copy.deepcopy(NEW_SHADOWS[key]) if on else None)

    def share_popup_shadow(self, same: bool):
        '''Gives popup windows the panels' shadow - or their own, starting as a copy of it.'''
        style = self.style
        style.set_setting("popup_shadow", None if same else copy.deepcopy(style.shadow_setting("popup_shadow") or NEW_SHADOWS["popup_shadow"]))

    # Preview
    def build_preview(self) -> QTabWidget:
        '''
        Tabs showing the theme on the real thing: one of every panel (see
        build_panels_preview), and the start menu and the workspace
        selector - look-only (see LookOnly), as their buttons would leave
        the theme editor.
        '''
        tabs = QTabWidget()
        tabs.setFont(self.style.get_font("default"))
        tabs.addTab(self.build_panels_preview(), self.labels.get("theme_editor_preview_panels"))
        for page_class, key, name in ((TitlePage, START_PAGE, "start"), (WorkspaceSelectPage, WORKSPACE_SELECT_PAGE, "workspaces")):
            page = page_class(self.context, key, preview=True)
            LookOnly(page)
            tabs.addTab(page, self.labels.get(f"theme_editor_preview_{name}"))
        tabs.setCurrentIndex(min(type(self).preview_tab, tabs.count() - 1))
        tabs.currentChanged.connect(lambda index: setattr(type(self), "preview_tab", index))
        return tabs

    def build_panels_preview(self) -> QScrollArea:
        '''One of every panel (see widgets.PANELS) in a grid, under a note saying what they are.'''
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { background-color: transparent; border: none; }")
        body = QWidget()
        self.style.set_material(body, "none")
        column = QVBoxLayout(body)
        column.setSpacing(self.style.igap)
        column.setContentsMargins(self.style.igap, self.style.igap, self.style.igap, self.style.igap)

        note = QLabel(self.labels.get("theme_editor_gallery_note"))
        note.setFont(self.style.get_font("small"))
        note.setWordWrap(True)
        column.addWidget(note)

        grid = QGridLayout()
        grid.setSpacing(self.style.igap)
        for col in range(PANEL_COLUMNS):
            grid.setColumnStretch(col, 1)
        for index, key in enumerate(widgets.PANELS):
            # Panels add themselves to their master's layout
            cell = QWidget()
            cell.setLayout(QVBoxLayout())
            cell.layout().setContentsMargins(0, 0, 0, 0)
            cell.setFixedHeight(PANEL_ROW_HEIGHT)
            grid.addWidget(cell, index // PANEL_COLUMNS, index % PANEL_COLUMNS)
            # The first copy's id, as in a layout - a panel set up per copy (the ModBus models) needs one
            widgets.panel(key, cell, self.context, panel_id=f"{key}_1")
        column.addLayout(grid)
        column.addStretch(1)
        scroll.setWidget(body)
        return scroll
