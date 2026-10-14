from collections.abc import Callable
from typing import ClassVar

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIntValidator, QKeySequence
from PySide6.QtWidgets import (QCheckBox, QComboBox, QFrame, QGridLayout, QHBoxLayout, QKeySequenceEdit, QLabel, QLineEdit,
                               QPushButton, QScrollArea, QSlider, QTabWidget, QVBoxLayout, QWidget)

from ..app_core import Context
from ..app_core.context.keybinds import DEFAULT_KEYBINDS
from ..app_core.context.performance import QUALITY_PRESETS, UI_FPS_RANGE
from ..app_core.context.style import BACKGROUND_FPS_RANGE
from ..widgets import MenuBar, VISUALS
from ..widgets.frame_widgets.important_buttons import (DeleteAllUserData, DeleteAllWorkspaceSavedData, ImportThemes, LinkToPage,
                                                       LoadLocalizationLabelsFile, OpenAccessPointConfigInBrowser,
                                                       OpenThemeEditor, OpenWorkspaceEditor, ResetTheme, developer_text)
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
    keybinds, developer mode). Everything applies as soon as it's changed and is
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
    # Whether rows show what they do in a third column - otherwise only as a tooltip
    SHOW_NOTES = True
    # The menu bar's title ("menu_bar_titles_<TITLE>") and buttons
    TITLE = "settings"
    MENU_BAR_BUTTONS = SETTINGS_MENU_BAR

    # Kept on the class so it survives the rebuilds some settings trigger
    # (a subclass keeps its own - see remember_tab)
    selected_tab: ClassVar[int] = 0
    # The first tab built (see build_tabs) - the menu bar's Appearance Settings button opens straight to it
    APPEARANCE_TAB: ClassVar[int] = 0

    def __init__(self, context: Context):
        super().__init__(context)
        self.labels = context.labels
        # The page's own background, so appearance changes preview live behind the settings
        self.add_background({"background": {"blur": 6}})

        menu_bar = MenuBar(self, context, self.TITLE)
        self.add_menu_bar_entries(menu_bar)
        menu_bar.add_config_buttons(self.MENU_BAR_BUTTONS)

        self.tabs = QTabWidget()
        self.tabs.setFont(self.style.get_font("default"))
        self.place_tabs()
        self.build_tabs()

        self.tabs.setCurrentIndex(min(type(self).selected_tab, self.tabs.count() - 1))
        self.tabs.currentChanged.connect(self.remember_tab)

        # A theme change restyles everything in place - only the rows showing
        # theme settings need to catch up (see rebuild_tabs). On a timer, not
        # at once: the control that changed the theme is still in its signal
        self.rebuild_timer = QTimer(self)
        self.rebuild_timer.setSingleShot(True)
        self.rebuild_timer.setInterval(0)
        self.rebuild_timer.timeout.connect(self.rebuild_tabs)
        self.style.signals.changed.connect(self.rebuild_timer.start)

    def rebuild_tabs(self):
        '''Builds the tabs again in place, on the same tab and scrolled to the same place.'''
        index = self.tabs.currentIndex()
        scrolled = [self.tabs.widget(i).verticalScrollBar().value() for i in range(self.tabs.count())]
        self.tabs.blockSignals(True)
        while self.tabs.count():
            tab = self.tabs.widget(0)
            self.tabs.removeTab(0)
            tab.deleteLater()
        self.build_tabs()
        self.tabs.setCurrentIndex(min(index, self.tabs.count() - 1))
        self.tabs.blockSignals(False)
        # Once the new tabs have their size, so there's room to scroll to
        def scroll_back():
            for i, value in enumerate(scrolled[:self.tabs.count()]):
                self.tabs.widget(i).verticalScrollBar().setValue(value)
        QTimer.singleShot(0, self.tabs, scroll_back)

    def add_menu_bar_entries(self, menu_bar: MenuBar):
        '''Anything a subclass's menu bar has before the MENU_BAR_BUTTONS (see ThemeEditorPage).'''

    def place_tabs(self):
        '''Puts self.tabs on the page - filling it, below the menu bar.'''
        self.layout().addWidget(self.tabs, 1)

    def build_tabs(self):
        self.build_appearance_tab()
        self.build_background_tab()
        self.build_performance_tab()
        self.build_general_tab()
        self.build_data_tab()
        self.build_developer_tab()

    def remember_tab(self, index: int):
        type(self).selected_tab = index

    # Tabs
    def build_appearance_tab(self):
        '''
        Just the theme settings almost everyone needs (see theme_rows) -
        everything finer is on the theme editor page.
        '''
        tab = self.new_tab("appearance")
        self.theme_rows(self.section(tab, "theme"))

    def theme_rows(self, theme: "SettingsSection"):
        '''
        Light or dark, the theme selector (the default themes and imported
        ones - see Style.theme_choices), and links to the theme editor, the
        imported themes folder and resetting the theme. The menu bar's Themes
        section has the first two, and links here (see OpenAppearanceSettings).
        '''
        style, context = self.style, self.context
        mode, _, family = style.current_theme.partition("_")
        theme.row("settings_page_rows_dark_mode", self.checkbox(
            mode == "dark", lambda on: style.set_theme(f"{'dark' if on else 'light'}_{style.theme_family()}")),
            "settings_page_row_notes_dark_mode")
        choices = style.theme_choices()
        # A theme made in the theme editor isn't one of the choices - shown as such, so any pick switches back
        custom = {} if family in choices else {family: self.labels.get("settings_page_custom_theme")}
        theme.row("settings_page_rows_theme", self.dropdown(
            {**choices, **custom}, family, lambda value: value in choices and style.set_family(value),
            {name: style.preset_info[name].get("note", "") for name in choices}), "settings_page_row_notes_theme")
        theme.row("settings_page_rows_theme_editor", OpenThemeEditor(context), "settings_page_row_notes_theme_editor")
        theme.row("settings_page_rows_import_themes", ImportThemes(context), "settings_page_row_notes_import_themes")
        theme.row("settings_page_rows_reset_theme", ResetTheme(context), "settings_page_row_notes_reset_theme")

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

        preview = self.section(tab, "background_preview")
        preview.row("settings_page_rows_visuals_demo", LinkToPage(self.context, "demo/visuals"),
                    "settings_page_row_notes_visuals_demo")

        reset = self.section(tab, "background_reset")
        reset.row("settings_page_rows_reset_background", self.button(
            "settings_page_buttons_reset", self.reset_background), "settings_page_row_notes_reset_background")

    def build_performance_tab(self):
        performance = self.context.performance
        tab = self.new_tab("performance")

        # A preset changes rows on this tab and the background tab - rebuilt so they show it
        presets = self.section(tab, "performance_preset")
        options = {"": self.labels.get("settings_page_performance_presets_custom")}
        options.update({name: self.labels.get(f"settings_page_performance_presets_{name}") for name in QUALITY_PRESETS})
        presets.row("settings_page_rows_performance_preset", self.dropdown(
            options, performance.current_preset(), self.apply_performance_preset,
            {name: self.labels.get(f"settings_page_performance_preset_notes_{name}") for name in QUALITY_PRESETS}),
            "settings_page_row_notes_performance_preset")

        rates = self.section(tab, "frame_rate")
        rates.row("settings_page_rows_ui_fps",
                  self.integer(performance.ui_fps, *UI_FPS_RANGE, lambda fps: performance.set(ui_fps=fps)),
                  "settings_page_row_notes_ui_fps")

        rendering = self.section(tab, "rendering")
        rendering.row("settings_page_rows_antialiasing",
                      self.checkbox(performance.antialiasing, lambda on: performance.set(antialiasing=on)),
                      "settings_page_row_notes_antialiasing")
        rendering.row("settings_page_rows_page_transitions",
                      self.checkbox(performance.page_transitions, lambda on: performance.set(page_transitions=on)),
                      "settings_page_row_notes_page_transitions")

        monitoring = self.section(tab, "monitoring")
        monitoring.row("settings_page_rows_performance_overlay",
                       self.checkbox(performance.overlay_enabled, lambda on: performance.set(overlay=on)),
                       "settings_page_row_notes_performance_overlay")
        monitoring.row("settings_page_rows_performance_log",
                       self.checkbox(performance.log_enabled, lambda on: performance.set(log=on)),
                       "settings_page_row_notes_performance_log")

        helper = self.section(tab, "network_helper")
        helper.row("settings_page_rows_network_helper",
                   self.checkbox(self.context.helper.enabled, self.context.helper.set_enabled),
                   "settings_page_row_notes_network_helper")

        reset = self.section(tab, "performance_reset")
        reset.row("settings_page_rows_reset_performance", self.button(
            "settings_page_buttons_reset", self.reset_performance), "settings_page_row_notes_reset_performance")

    def build_general_tab(self):
        context = self.context
        preferences = context.preferences
        tab = self.new_tab("general")

        display = self.section(tab, "display")
        fullscreen = self.checkbox(context.root.isFullScreen(), self.set_fullscreen)
        # Follows F11 too - a slot on the checkbox, so it's dropped with this page
        context.root.fullscreen_changed.connect(fullscreen.setChecked)
        display.row("settings_page_rows_fullscreen", fullscreen, "settings_page_row_notes_fullscreen")
        display.row("settings_page_rows_fade_in",
                    self.checkbox(preferences.is_fade_in(), lambda on: preferences.set("fade_in", on)),
                    "settings_page_row_notes_fade_in")
        display.row("settings_page_rows_fade_out",
                    self.checkbox(preferences.is_fade_out(), lambda on: preferences.set("fade_out", on)),
                    "settings_page_row_notes_fade_out")

        keybinds = self.section(tab, "keybinds")
        for action in DEFAULT_KEYBINDS:
            keybinds.row(f"settings_page_rows_keybind_{action}", self.keybind(action), f"settings_page_row_notes_keybind_{action}")
        keybinds.row("settings_page_rows_reset_keybinds", self.button(
            "settings_page_buttons_reset", self.reset_keybinds), "settings_page_row_notes_reset_keybinds")

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
        # Developer-only, so marked as such (see important_buttons.DEVELOPER_MARK)
        tools = self.section(tab, "developer_tools", developer=True)
        tools.row("settings_page_rows_debug_labels", self.checkbox(context.labels.is_debug(), self.set_debug_labels),
                  "settings_page_row_notes_debug_labels")
        editor = OpenWorkspaceEditor(context)
        editor.mark_developer_only()
        tools.row("settings_page_rows_workspace_editor", editor, "settings_page_row_notes_workspace_editor")

    # Actions
    def reset_background(self):
        self.style.load_default_background()
        self.style.set_background()  # saves the defaults
        self.router.refresh()

    def apply_performance_preset(self, name: str):
        if name:  # "" (Custom) just means the settings below don't match a preset
            self.context.performance.apply_preset(name)
            self.router.refresh()

    def reset_performance(self):
        self.context.performance.reset()
        self.router.refresh()

    def set_fullscreen(self, on: bool):
        self.context.keybinds.set_fullscreen(on, save=True)

    def set_keybind(self, action: str, sequence: str):
        # Keys taken from another action unbind it - rebuilt so its box shows that
        if self.context.keybinds.rebind(action, sequence):
            self.router.refresh()

    def reset_keybinds(self):
        self.context.keybinds.reset()
        self.router.refresh()

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
        scroll.setStyleSheet("QScrollArea { background-color: transparent; border: none; }")
        body = QWidget()
        self.style.set_material(body, "none")
        column = QVBoxLayout(body)
        column.setSpacing(self.style.igap)
        column.setContentsMargins(0, self.style.igap, self.style.igap, 0)
        column.addStretch(1)
        scroll.setWidget(body)
        self.tabs.addTab(scroll, self.labels.get(f"settings_page_tabs_{name}"))
        return column

    def section(self, tab: QVBoxLayout, name: str, developer: bool = False) -> "SettingsSection":
        section = SettingsSection(self, name, developer)
        tab.insertWidget(tab.count() - 1, section)  # above the trailing stretch
        return section

    # Controls - each applies its setting through `changed` as soon as it changes
    def checkbox(self, checked: bool, changed: Callable[[bool], None]) -> QCheckBox:
        box = QCheckBox()
        box.setChecked(checked)  # before connecting, so loading it doesn't count as a change
        box.toggled.connect(changed)
        return box

    def dropdown(self, options: dict[str, str], current: str, changed: Callable[[str], None],
                 tips: dict[str, str] | None = None) -> QComboBox:
        '''A choice between options (stored value -> shown text), each with an optional tooltip; changed gets the stored value.'''
        values = list(options)
        if current not in options:
            values.append(current)
        combo = QComboBox()
        combo.setFont(self.style.get_font())
        combo.addItems([options.get(value, str(value)) for value in values])
        for index, value in enumerate(values):
            if tips and tips.get(value):
                combo.setItemData(index, tips[value], Qt.ItemDataRole.ToolTipRole)
        combo.setCurrentIndex(values.index(current))
        combo.currentIndexChanged.connect(lambda index: changed(values[index]))
        return combo

    def slider(self, value: int, minimum: int, maximum: int, suffix: str, changed: Callable[[int], None],
               live: bool = True) -> QWidget:
        '''live=False only calls changed once a drag is let go - for settings that rebuild the page.'''
        row = QWidget()
        layout = QHBoxLayout(row)
        layout.setContentsMargins(0, 0, 0, 0)
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(minimum, maximum)
        slider.setValue(value)
        slider.setTracking(live)
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
        slider.sliderMoved.connect(lambda new_value: readout.setText(f"{new_value}{suffix}"))
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

    def keybind(self, action: str) -> QKeySequenceEdit:
        '''Click and press keys to bind the action; the clear button unbinds it.'''
        edit = QKeySequenceEdit(QKeySequence(self.context.keybinds.sequence(action)))
        edit.setFont(self.style.get_font())
        edit.setMaximumSequenceLength(1)  # one key combination, not a chord of several
        edit.setClearButtonEnabled(True)
        edit.keySequenceChanged.connect(lambda sequence: self.set_keybind(action, sequence.toString()))
        return edit

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

    def __init__(self, page: SettingsPage, name: str, developer: bool = False):
        super().__init__()
        self.page = page
        # A developer-only section marks its title and every row's name
        self.developer = developer
        style = page.style
        labels = page.labels
        style.set_material(self, "panel", rounded=True)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(style.igap * 2, style.igap, style.igap * 2, style.igap)
        title = labels.get(f"settings_page_sections_{name}")
        header = QLabel(developer_text(title) if developer else title)
        header.setFont(style.get_font("title_btn"))
        if developer:
            # The mark's fallback font has a taller line - keep the title's own
            header.setFixedHeight(header.fontMetrics().height())
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
        self.grid.setColumnStretch(2 if page.SHOW_NOTES else 1, 1)
        layout.addLayout(self.grid)
        self.count = 0

    def row(self, name: str, control: QWidget, note: str):
        '''A setting: its name (labels key), its control, and what it does (labels key).'''
        style, labels = self.page.style, self.page.labels
        label = QLabel(developer_text(labels.get(name)) if self.developer else labels.get(name))
        label.setFont(style.get_font())
        if self.developer:
            label.setFixedHeight(label.fontMetrics().height())  # (see the header's, in __init__)
        description = QLabel(labels.get(note))
        description.setFont(style.get_font("small"))
        description.setWordWrap(True)
        label.setToolTip(description.text())
        control.setToolTip(control.toolTip() or description.text())
        if not self.page.SHOW_NOTES:
            description.deleteLater()  # only needed for its text, as the tooltips above
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
        if self.page.SHOW_NOTES:
            self.grid.addWidget(description, self.count, 2, Qt.AlignmentFlag.AlignVCenter)
        self.count += 1
