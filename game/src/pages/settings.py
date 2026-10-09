from collections.abc import Callable
from typing import ClassVar

from PySide6.QtCore import Qt
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import (QCheckBox, QComboBox, QFrame, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
                               QScrollArea, QSlider, QTabWidget, QVBoxLayout, QWidget)

from ..app_core import Context
from ..app_core.context.style import BACKGROUND_FPS_RANGE, SURFACE_BLUR_MAX, SURFACE_KINDS
from ..widgets import MenuBar, VISUALS
from ..widgets.frame_widgets.important_buttons import (DeleteAllUserData, DeleteAllWorkspaceSavedData,
                                                       LoadLocalizationLabelsFile, OpenAccessPointConfigInBrowser,
                                                       OpenWorkspaceEditor)
from .page import Page

# This page's own menu bar - plain navigation; everything else is on the page
SETTINGS_MENU_BAR = ["help_button", "back_button", "workspaces_button", "title_button", "quit_button"]  # (not settings_button - it's here)


class SettingsPage(Page):
    '''
    Every app-wide setting on one page, laid out like the workspace editor:
    tabs of sections, each section a titled card with an explanation, and
    one setting per row - its name, its control, and what it does.

    It unpacks the important buttons and dropdowns that don't belong to a
    workspace or panel (the theme buttons, the Background dropdown, the
    labels file, the favorite page, the data and debug tools) into plain
    rows, and adds the preferences that had no button at all (fullscreen,
    developer mode). Everything applies as soon as it's changed and is
    saved like any other preference - there's no Save button. Changes that
    need the page rebuilt (theme, language, developer mode) rebuild it in
    place, on the same tab.

    Text comes from labels: tabs "settings_page_tabs_<tab>", sections
    "settings_page_sections_<section>" (with "settings_page_notes_<section>"
    explaining them), and rows "settings_page_rows_<row>" (described by
    "settings_page_row_notes_<row>") - or, for the surface and background
    settings, the same "settings_labels_"/"settings_tooltips_" keys the
    Background dropdown uses.
    '''

    LABEL_WIDTH = 240
    CONTROL_WIDTH = 300

    # Kept on the class so it survives the rebuilds some settings trigger
    selected_tab: ClassVar[int] = 0

    def __init__(self, context: Context):
        super().__init__(context)
        self.labels = context.labels
        # The page's own background, so appearance changes preview live behind the settings
        self.add_background({"background": {"blur": 6}})

        menu_bar = MenuBar(self, context, "settings")
        menu_bar.add_config_buttons(SETTINGS_MENU_BAR)

        self.tabs = QTabWidget()
        self.tabs.setFont(self.style.get_font("default"))
        self.layout().addWidget(self.tabs, 1)

        self.build_appearance_tab()
        self.build_background_tab()
        self.build_general_tab()
        self.build_data_tab()
        self.build_developer_tab()

        self.tabs.setCurrentIndex(min(SettingsPage.selected_tab, self.tabs.count() - 1))
        self.tabs.currentChanged.connect(self.remember_tab)

    def remember_tab(self, index: int):
        SettingsPage.selected_tab = index

    # Tabs
    def build_appearance_tab(self):
        style = self.style
        tab = self.new_tab("appearance")

        theme = self.section(tab, "theme")
        mode, _, family = style.current_theme.partition("_")
        theme.row("settings_page_rows_mode", self.dropdown(
            {"dark": self.labels.get("settings_page_mode_dark"), "light": self.labels.get("settings_page_mode_light")},
            mode, lambda value: style.set_theme(f"{value}_{family}")), "settings_page_row_notes_mode")
        theme.row("settings_page_rows_color", self.dropdown(
            {name: name.title() for name in style.theme_families()},
            family, lambda value: style.set_theme(f"{mode}_{value}")), "settings_page_row_notes_color")
        theme.row("settings_labels_surface_invert_buttons", self.checkbox(style.invert_buttons, style.set_invert_buttons),
                  "settings_tooltips_surface_invert_buttons")

        # The Background dropdown's two columns, each its own section
        opacity = self.section(tab, "surface_opacity")
        for kind in SURFACE_KINDS:
            opacity.row(f"settings_labels_surface_opacity_{kind}", self.slider(
                round(style.surface_opacity[kind] * 100), 0, 100, "%",
                lambda value, kind=kind: style.set_surface(kind, opacity=value / 100)),
                f"settings_tooltips_surface_opacity_{kind}")
        blur = self.section(tab, "surface_blur")
        for kind in SURFACE_KINDS:
            blur.row(f"settings_labels_surface_blur_{kind}", self.slider(
                round(style.surface_blur[kind]), 0, int(SURFACE_BLUR_MAX), " px",
                lambda value, kind=kind: style.set_surface(kind, blur=value)),
                f"settings_tooltips_surface_blur_{kind}")

        reset = self.section(tab, "appearance_reset")
        reset.row("settings_page_rows_reset_surfaces", self.button(
            "settings_page_buttons_reset", self.reset_surfaces), "settings_page_row_notes_reset_surfaces")

    def build_background_tab(self):
        style = self.style
        tab = self.new_tab("background")
        section = self.section(tab, "background")
        section.row("settings_labels_background_enabled",
                    self.checkbox(style.background_enabled, lambda on: style.set_background(enabled=on)),
                    "settings_tooltips_background_enabled")
        section.row("settings_labels_background_visual",
                    self.dropdown({key: self.labels.get(f"visual_names_{key}") for key in [*VISUALS, "cycle"]},
                                  style.background_visual, lambda key: style.set_background(visual=key)),
                    "settings_tooltips_background_visual")
        section.row("settings_labels_background_animate",
                    self.checkbox(style.background_animate, lambda on: style.set_background(animate=on)),
                    "settings_tooltips_background_animate")
        section.row("settings_labels_background_detailed",
                    self.checkbox(style.background_detailed, lambda on: style.set_background(detailed=on)),
                    "settings_tooltips_background_detailed")
        section.row("settings_labels_background_fps",
                    self.integer(style.background_fps, *BACKGROUND_FPS_RANGE, lambda fps: style.set_background(fps=fps)),
                    "settings_tooltips_background_fps")

        reset = self.section(tab, "background_reset")
        reset.row("settings_page_rows_reset_background", self.button(
            "settings_page_buttons_reset", self.reset_background), "settings_page_row_notes_reset_background")

    def build_general_tab(self):
        context = self.context
        preferences = context.preferences
        tab = self.new_tab("general")

        display = self.section(tab, "display")
        display.row("settings_page_rows_fullscreen",
                    self.checkbox(context.root.isFullScreen(), self.set_fullscreen), "settings_page_row_notes_fullscreen")

        language = self.section(tab, "language")
        current = preferences.get("labels_file") if preferences.has("labels_file") else None
        file_name = QLabel(str(current).replace("\\", "/").rsplit("/", 1)[-1] if current
                           else self.labels.get("settings_page_default_labels"))
        file_name.setFont(self.style.get_font())
        language.row("settings_page_rows_labels_file", file_name, "settings_page_row_notes_labels_file")
        language.row("settings_page_rows_load_labels", LoadLocalizationLabelsFile(context), "settings_page_row_notes_load_labels")
        if current:
            language.row("settings_page_rows_default_labels", self.button(
                "settings_page_buttons_default_labels", self.use_default_labels), "settings_page_row_notes_default_labels")

        navigation = self.section(tab, "navigation")
        pages = context.pages
        workspaces = sorted((key for key, kind in pages.build_types.items() if kind == "workspace"),
                            key=lambda key: self.labels.get(pages.link_label(key)))
        options = {"": self.labels.get("settings_page_no_favorite")}
        options.update({key: self.labels.get(pages.link_label(key)) for key in workspaces})
        favorite = preferences.get("page") if preferences.has("page") else ""
        navigation.row("settings_page_rows_favorite", self.dropdown(options, favorite, lambda key: preferences.set("page", key)),
                       "settings_page_row_notes_favorite")

        hardware = self.section(tab, "access_point")
        hardware.row("settings_page_rows_ap_config", OpenAccessPointConfigInBrowser(context), "settings_page_row_notes_ap_config")

    def build_data_tab(self):
        tab = self.new_tab("data")
        section = self.section(tab, "saved_data")
        section.row("settings_page_rows_delete_workspace_data", DeleteAllWorkspaceSavedData(self.context),
                    "settings_page_row_notes_delete_workspace_data")
        section.row("settings_page_rows_delete_user_data", DeleteAllUserData(self.context),
                    "settings_page_row_notes_delete_user_data")

    def build_developer_tab(self):
        context = self.context
        tab = self.new_tab("developer")
        mode = self.section(tab, "developer_mode")
        mode.row("settings_page_rows_is_developer", self.checkbox(context.preferences.is_developer(), self.set_developer),
                 "settings_page_row_notes_is_developer")
        if not context.preferences.is_developer():
            return
        tools = self.section(tab, "developer_tools")
        tools.row("settings_page_rows_debug_labels", self.checkbox(context.labels.is_debug(), self.set_debug_labels),
                  "settings_page_row_notes_debug_labels")
        tools.row("settings_page_rows_workspace_editor", OpenWorkspaceEditor(context), "settings_page_row_notes_workspace_editor")

    # Actions
    def reset_surfaces(self):
        self.style.reset_surfaces()
        self.router.refresh()  # so the sliders show the defaults

    def reset_background(self):
        self.style.load_default_background()
        self.style.set_background()  # saves the defaults
        self.router.refresh()

    def set_fullscreen(self, on: bool):
        # Stored as a string, like KeyBinds (F11) does
        self.context.preferences.set("fullscreen", str(on))
        if on:
            self.context.root.showFullScreen()
        else:
            self.context.root.showNormal()

    def use_default_labels(self):
        self.context.preferences.set("labels_file", "")
        self.labels.reset()
        self.router.refresh()

    def set_developer(self, on: bool):
        self.context.preferences.set("is_developer", 1 if on else 0)
        self.router.refresh()  # menu bars, and the tools below, follow it

    def set_debug_labels(self, on: bool):
        self.labels.set_debug(on)
        self.router.refresh()

    # Layout
    def new_tab(self, name: str) -> QVBoxLayout:
        '''A scrolling tab whose sections stack from the top - like the workspace editor's new_tab, but see-through to the background.'''
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet(self.style.themed("QScrollArea { background-color: transparent; border: none; }"))
        body = QWidget()
        body.setStyleSheet("background-color: transparent;")
        column = QVBoxLayout(body)
        column.setSpacing(self.style.igap)
        column.setContentsMargins(0, self.style.igap, self.style.igap, 0)
        column.addStretch(1)
        scroll.setWidget(body)
        self.tabs.addTab(scroll, self.labels.get(f"settings_page_tabs_{name}"))
        return column

    def section(self, tab: QVBoxLayout, name: str) -> "SettingsSection":
        section = SettingsSection(self, name)
        tab.insertWidget(tab.count() - 1, section)  # above the trailing stretch
        return section

    # Controls - each applies its setting through `changed` as soon as it changes
    def checkbox(self, checked: bool, changed: Callable[[bool], None]) -> QCheckBox:
        box = QCheckBox()
        box.setChecked(checked)  # before connecting, so loading it doesn't count as a change
        box.toggled.connect(changed)
        return box

    def dropdown(self, options: dict[str, str], current: str, changed: Callable[[str], None]) -> QComboBox:
        '''A choice between options (stored value -> shown text); changed gets the stored value.'''
        values = list(options)
        if current not in options:
            values.append(current)
        combo = QComboBox()
        combo.setFont(self.style.get_font())
        combo.addItems([options.get(value, str(value)) for value in values])
        combo.setCurrentIndex(values.index(current))
        combo.currentIndexChanged.connect(lambda index: changed(values[index]))
        return combo

    def slider(self, value: int, minimum: int, maximum: int, suffix: str, changed: Callable[[int], None]) -> QWidget:
        row = QWidget()
        layout = QHBoxLayout(row)
        layout.setContentsMargins(0, 0, 0, 0)
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(minimum, maximum)
        slider.setValue(value)
        readout = QLabel(f"{value}{suffix}")
        readout.setFont(self.style.get_font())
        readout.setMinimumWidth(readout.fontMetrics().horizontalAdvance(f"{maximum}{suffix}") + 4)
        readout.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(slider, 1)
        layout.addWidget(readout)

        def on_change(new_value: int):
            readout.setText(f"{new_value}{suffix}")
            changed(new_value)
        slider.valueChanged.connect(on_change)
        return row

    def integer(self, value: int, minimum: int, maximum: int, changed: Callable[[int], None]) -> QLineEdit:
        '''A whole number in [minimum, maximum] - anything else is undone when editing finishes.'''
        entry = QLineEdit(str(value))
        entry.setFont(self.style.get_font())
        entry.setValidator(QIntValidator(minimum, maximum, entry))
        entry.setMaximumWidth(120)
        current = [value]

        def save():
            try:
                new_value = int(entry.text())
            except ValueError:
                new_value = None
            if new_value is None or not minimum <= new_value <= maximum:
                entry.setText(str(current[0]))
            elif new_value != current[0]:
                current[0] = new_value
                changed(new_value)
        entry.editingFinished.connect(save)
        return entry

    def button(self, label: str, clicked: Callable[[], None]) -> QPushButton:
        button = QPushButton(self.labels.get(label))
        button.setFont(self.style.get_font())
        button.clicked.connect(lambda checked=False: clicked())
        return button


class SettingsSection(QFrame):
    '''
    One titled card of settings, like a workspace editor section: its
    title, an explanation, then a row per setting - name | control | what
    it does.
    '''

    def __init__(self, page: SettingsPage, name: str):
        super().__init__()
        self.page = page
        style = page.style
        labels = page.labels
        self.setStyleSheet(style.themed(
            f"QFrame {{ background-color: {style.color('panel')}; border-radius: {style.PANEL_RADIUS}px; }}", self))
        layout = QVBoxLayout(self)
        layout.setContentsMargins(style.igap * 2, style.igap, style.igap * 2, style.igap)
        header = QLabel(labels.get(f"settings_page_sections_{name}"))
        header.setFont(style.get_font("title_btn"))
        layout.addWidget(header)
        explanation = QLabel(labels.get(f"settings_page_notes_{name}"))
        explanation.setFont(style.get_font("small"))
        explanation.setWordWrap(True)
        layout.addWidget(explanation)

        self.grid = QGridLayout()
        self.grid.setHorizontalSpacing(style.igap * 2)
        self.grid.setVerticalSpacing(style.igap)
        # Same column widths in every section, so controls line up down the page
        self.grid.setColumnMinimumWidth(0, page.LABEL_WIDTH)
        self.grid.setColumnMinimumWidth(1, page.CONTROL_WIDTH)
        self.grid.setColumnStretch(2, 1)
        layout.addLayout(self.grid)
        self.count = 0

    def row(self, name: str, control: QWidget, note: str):
        '''A setting: its name (labels key), its control, and what it does (labels key).'''
        style, labels = self.page.style, self.page.labels
        label = QLabel(labels.get(name))
        label.setFont(style.get_font())
        description = QLabel(labels.get(note))
        description.setFont(style.get_font("small"))
        description.setWordWrap(True)
        label.setToolTip(description.text())
        control.setToolTip(control.toolTip() or description.text())
        # Narrow controls (checkboxes, number boxes, buttons) sit at the column's
        # left edge; dropdowns and sliders fill it
        narrow = isinstance(control, (QCheckBox, QLineEdit, QPushButton, QLabel))
        # Never wider than the column - a long choice (a workspace name) would
        # otherwise push this row's description out of line with the rest
        control.setMaximumWidth(min(control.maximumWidth(), self.page.CONTROL_WIDTH))
        if isinstance(control, QComboBox):
            control.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon)
            control.setMinimumContentsLength(12)
        align = Qt.AlignmentFlag.AlignVCenter | (Qt.AlignmentFlag.AlignLeft if narrow else Qt.AlignmentFlag(0))
        self.grid.addWidget(label, self.count, 0, Qt.AlignmentFlag.AlignVCenter)
        self.grid.addWidget(control, self.count, 1, align)
        self.grid.addWidget(description, self.count, 2, Qt.AlignmentFlag.AlignVCenter)
        self.count += 1
