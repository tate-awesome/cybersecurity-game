from collections.abc import Callable
from typing import ClassVar

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIntValidator, QKeySequence
from PySide6.QtWidgets import (QCheckBox, QComboBox, QFrame, QGridLayout, QHBoxLayout, QKeySequenceEdit, QLabel, QLineEdit,
                               QPushButton, QScrollArea, QSlider, QTabWidget, QVBoxLayout, QWidget)

from ..app_core import Context
from ..app_core.context.keybinds import DEFAULT_KEYBINDS
from ..app_core.context.performance import QUALITY_PRESETS, UI_FPS_RANGE
from ..app_core.context.preferences import DEFAULT_FADE_IN, DEFAULT_FADE_OUT
from ..app_core.context.style import (BACKGROUND_FPS_RANGE, DEFAULT_BACKGROUND_ANIMATE, DEFAULT_BACKGROUND_DETAILED,
                                      DEFAULT_BACKGROUND_FPS, DEFAULT_BACKGROUND_VISUAL,
                                      DEFAULT_BACKGROUND_WORKSPACE_DISABLED, DEFAULT_BACKGROUND_WORKSPACE_FROZEN,
                                      NO_BACKGROUND)
from ..widgets import MenuBar
from ..widgets.visuals import background_choices
from ..widgets.frame_widgets.important_buttons import (DeleteAllUserData, DeleteAllWorkspaceSavedData, ImportThemes, LinkToPage,
                                                       LoadLocalizationLabelsFile, OpenAccessPointConfigInBrowser,
                                                       OpenThemeEditor, OpenWorkspaceEditor,
                                                       ToggleLightDarkMode,
                                                       developer_text)
from .page import Page


class SettingsPage(Page):
    '''
    Every app-wide setting on one page, laid out like the workspace editor:
    tabs of sections, each section a titled card with an explanation, and
    one setting per row - its name, its control, and what it does.

    It unpacks the important buttons and dropdowns that don't belong to a
    workspace or panel (Quick Settings, the labels file, the favorite page,
    the data and debug tools) into plain rows, and adds the preferences that had no button at all (fullscreen,
    keybinds, developer mode). Tabs run from what anyone would look for
    (General) to what only some should touch (Advanced, then Developer -
    only in developer mode). Everything applies as soon as it's changed and is
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
    # The menu bar's title ("menu_bar_titles_<TITLE>")
    TITLE = "settings"

    # Kept on the class so it survives the rebuilds some settings trigger
    # (a subclass keeps its own - see remember_tab)
    selected_tab: ClassVar[int] = 0

    def __init__(self, context: Context):
        super().__init__(context)
        self.labels = context.labels
        # The page's own background, so appearance changes preview live behind the settings
        self.add_background({"background": {"blur": 6}})

        menu_bar = MenuBar(self, context, self.TITLE)
        self.add_menu_bar_entries(menu_bar)

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
        '''Anything a subclass's menu bar has in its center (see ThemeEditorPage).'''

    def place_tabs(self):
        '''Puts self.tabs on the page - filling it, below the menu bar.'''
        self.layout().addWidget(self.tabs, 1)

    def build_tabs(self):
        # Most-wanted first - General is where the page opens (selected_tab's default)
        self.build_general_tab()
        self.build_appearance_tab()
        self.build_graphics_tab()
        self.build_keybinds_tab()
        self.build_troubleshooting_tab()
        self.build_advanced_tab()
        if self.context.preferences.is_developer():
            self.build_developer_tab()

    def remember_tab(self, index: int):
        type(self).selected_tab = index

    # Tabs
    def build_general_tab(self):
        '''What almost anyone would come to settings for.'''
        context = self.context
        preferences = context.preferences
        tab = self.new_tab("general")

        display = self.section(tab, "display")
        fullscreen = self.checkbox(context.root.isFullScreen(), self.set_fullscreen)
        # Follows F11 too - a slot on the checkbox, so it's dropped with this page
        context.root.fullscreen_changed.connect(fullscreen.setChecked)
        display.row("settings_page_rows_fullscreen", fullscreen, "settings_page_row_notes_fullscreen")

        language = self.section(tab, "language")
        current = preferences.get("labels_file") if preferences.has("labels_file") else None
        file_name = QLabel(str(current).replace("\\", "/").rsplit("/", 1)[-1] if current
                           else self.labels.get("settings_page_default_labels"))
        file_name.setFont(self.style.get_font())
        language.row("settings_page_rows_labels_file", file_name, "settings_page_row_notes_labels_file")
        language.row("settings_page_rows_load_labels", LoadLocalizationLabelsFile(context), "settings_page_row_notes_load_labels")
        if current:
            language.row("settings_page_rows_default_labels", self.default_labels_button(), "settings_page_row_notes_default_labels")

        navigation = self.section(tab, "navigation")
        pages = context.pages
        workspaces = sorted((key for key, kind in pages.build_types.items() if kind == "workspace"),
                            key=lambda key: self.labels.get(pages.link_label(key)))
        options = {"": self.labels.get("settings_page_no_favorite")}
        options.update({key: self.labels.get(pages.link_label(key)) for key in workspaces})
        favorite = preferences.get("page") if preferences.has("page") else ""
        navigation.row("settings_page_rows_favorite", self.dropdown(options, favorite, lambda key: preferences.set("page", key)),
                       "settings_page_row_notes_favorite")

    def build_appearance_tab(self):
        '''
        How the app looks: the theme settings almost everyone needs (see
        theme_rows - everything finer is on the theme editor page), the
        background's picture, and the window's fades. How smoothly it's all
        drawn is on the Graphics tab.
        '''
        style, preferences = self.style, self.context.preferences
        tab = self.new_tab("appearance")
        self.theme_rows(self.section(tab, "theme"))

        background = self.section(tab, "background")
        choices = background_choices(self.context)
        current = style.background_visual
        # One hidden from the pickers (on the visuals demo page) still shows by name while it plays
        shown = choices if current in choices else {**choices, current: self.labels.get(f"visual_names_{current}")}
        background.row("settings_labels_background_visual", self.dropdown(
            shown, current, self.set_background_visual,
            {key: self.labels.get(f"visual_descriptions_{key}") for key in shown}), "settings_tooltips_background_visual")
        background.row("settings_page_rows_visuals_demo", LinkToPage(self.context, "demo/visuals"),
                       "settings_page_row_notes_visuals_demo")

        window = self.section(tab, "window_effects")
        window.row("settings_page_rows_fade_in",
                   self.checkbox(preferences.is_fade_in(), lambda on: preferences.set("fade_in", on)),
                   "settings_page_row_notes_fade_in")
        window.row("settings_page_rows_fade_out",
                   self.checkbox(preferences.is_fade_out(), lambda on: preferences.set("fade_out", on)),
                   "settings_page_row_notes_fade_out")

        reset = self.section(tab, "appearance_reset")
        reset.row("settings_page_rows_reset_appearance", self.reset_appearance_button(), "settings_page_row_notes_reset_appearance")

    def theme_rows(self, theme: "SettingsSection"):
        '''
        Light or dark, the theme selector (the default themes and imported
        ones - see Style.theme_choices), the imported themes folder and
        inverted buttons. Quick Settings has the first two too. The theme
        editor is on the Advanced tab.
        '''
        style, context = self.style, self.context
        family = style.theme_family()
        theme.row("settings_page_rows_dark_mode", ToggleLightDarkMode(context), "settings_page_row_notes_dark_mode")
        choices = style.theme_choices()
        # A theme made in the theme editor isn't one of the choices - shown as such, so any pick switches back
        custom = {} if family in choices else {family: self.labels.get("settings_page_custom_theme")}
        theme.row("settings_page_rows_theme", self.dropdown(
            {**choices, **custom}, family, lambda value: value in choices and style.set_family(value),
            {name: style.preset_info[name].get("note", "") for name in choices}), "settings_page_row_notes_theme")
        theme.row("settings_page_rows_import_themes", ImportThemes(context), "settings_page_row_notes_import_themes")
        theme.row("settings_labels_surface_invert_buttons",
                  self.checkbox(style.invert_buttons, style.set_invert_buttons), "settings_tooltips_surface_invert_buttons")

    def build_graphics_tab(self):
        '''
        How smoothly and finely things are drawn - everything the quality
        preset sets (the background's framerate and animation among them),
        so a preset's effect shows on this one tab.
        '''
        performance, style = self.context.performance, self.style
        tab = self.new_tab("graphics")

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
        rates.row("settings_labels_background_fps",
                  self.integer(style.background_fps, *BACKGROUND_FPS_RANGE, lambda fps: style.set_background(fps=fps)),
                  "settings_tooltips_background_fps")

        rendering = self.section(tab, "rendering")
        rendering.row("settings_page_rows_antialiasing",
                      self.checkbox(performance.antialiasing, lambda on: performance.set(antialiasing=on)),
                      "settings_page_row_notes_antialiasing")
        rendering.row("settings_page_rows_page_transitions",
                      self.checkbox(performance.page_transitions, lambda on: performance.set(page_transitions=on)),
                      "settings_page_row_notes_page_transitions")
        # No background is always frozen - nothing to animate (see Style.background_frozen)
        freeze = self.checkbox(style.background_frozen(), lambda on: style.set_background(animate=not on))
        freeze.setEnabled(style.background_visual != NO_BACKGROUND)
        rendering.row("settings_page_rows_freeze_background", freeze, "settings_page_row_notes_freeze_background")
        rendering.row("settings_page_rows_freeze_workspace_background",
                      self.checkbox(style.background_workspace_frozen, lambda on: style.set_background(workspace_frozen=on)),
                      "settings_page_row_notes_freeze_workspace_background")
        rendering.row("settings_page_rows_disable_workspace_background",
                      self.checkbox(style.background_workspace_disabled, lambda on: style.set_background(workspace_disabled=on)),
                      "settings_page_row_notes_disable_workspace_background")
        rendering.row("settings_labels_background_detailed",
                      self.checkbox(style.background_detailed, lambda on: style.set_background(detailed=on)),
                      "settings_tooltips_background_detailed")

        reset = self.section(tab, "performance_reset")
        reset.row("settings_page_rows_reset_performance", self.reset_performance_button(),
                  "settings_page_row_notes_reset_performance")

    def build_keybinds_tab(self):
        tab = self.new_tab("keybinds")
        keybinds = self.section(tab, "keybinds")
        for action in DEFAULT_KEYBINDS:
            keybinds.row(f"settings_page_rows_keybind_{action}", self.keybind(action), f"settings_page_row_notes_keybind_{action}")
        keybinds.row("settings_page_rows_reset_keybinds", self.reset_keybinds_button(), "settings_page_row_notes_reset_keybinds")

    def build_troubleshooting_tab(self):
        '''
        Safe ways out when something looks or acts wrong: each group of
        settings back to its defaults (the same resets as on their own tabs),
        workspace data cleared, and the performance overlay.
        '''
        context = self.context
        tab = self.new_tab("troubleshooting")

        reset = self.section(tab, "reset_settings")
        reset.row("settings_page_rows_reset_appearance", self.reset_appearance_button(), "settings_page_row_notes_reset_appearance")
        reset.row("settings_page_rows_reset_performance", self.reset_performance_button(),
                  "settings_page_row_notes_reset_performance")
        reset.row("settings_page_rows_reset_keybinds", self.reset_keybinds_button(), "settings_page_row_notes_reset_keybinds")
        if context.preferences.has("labels_file") and context.preferences.get("labels_file"):
            reset.row("settings_page_rows_default_labels", self.default_labels_button(), "settings_page_row_notes_default_labels")

        data = self.section(tab, "saved_data")
        data.row("settings_page_rows_delete_workspace_data", DeleteAllWorkspaceSavedData(context),
                 "settings_page_row_notes_delete_workspace_data")

        monitoring = self.section(tab, "monitoring")
        monitoring.row("settings_page_rows_performance_overlay",
                       self.checkbox(context.performance.overlay_enabled, lambda on: context.performance.set(overlay=on)),
                       "settings_page_row_notes_performance_overlay")

    def build_advanced_tab(self):
        '''Settings that can break things if misused, or that need to know how the app works inside.'''
        context = self.context
        tab = self.new_tab("advanced")

        helper = self.section(tab, "network_helper")
        helper.row("settings_page_rows_network_helper",
                   self.checkbox(context.helper.enabled, context.helper.set_enabled),
                   "settings_page_row_notes_network_helper")

        editor = self.section(tab, "theme_editor")
        editor.row("settings_page_rows_theme_editor", OpenThemeEditor(context), "settings_page_row_notes_theme_editor")

        hardware = self.section(tab, "access_point")
        hardware.row("settings_page_rows_ap_config", OpenAccessPointConfigInBrowser(context), "settings_page_row_notes_ap_config")

        diagnostics = self.section(tab, "diagnostics")
        diagnostics.row("settings_page_rows_performance_log",
                        self.checkbox(context.performance.log_enabled, lambda on: context.performance.set(log=on)),
                        "settings_page_row_notes_performance_log")

        full_reset = self.section(tab, "full_reset")
        full_reset.row("settings_page_rows_delete_user_data", DeleteAllUserData(context),
                       "settings_page_row_notes_delete_user_data")

        mode = self.section(tab, "developer_mode")
        mode.row("settings_page_rows_is_developer", self.checkbox(context.preferences.is_developer(), self.set_developer),
                 "settings_page_row_notes_is_developer")

    def build_developer_tab(self):
        '''Only built in developer mode (switched on from the Advanced tab).'''
        context = self.context
        tab = self.new_tab("developer")
        # Developer-only, so marked as such (see important_buttons.DEVELOPER_MARK)
        tools = self.section(tab, "developer_tools", developer=True)
        tools.row("settings_page_rows_debug_labels", self.checkbox(context.labels.is_debug(), self.set_debug_labels),
                  "settings_page_row_notes_debug_labels")
        editor = OpenWorkspaceEditor(context)
        editor.mark_developer_only()
        tools.row("settings_page_rows_workspace_editor", editor, "settings_page_row_notes_workspace_editor")

    # Buttons shown on more than one tab - each placement needs its own widget
    def reset_appearance_button(self) -> QPushButton:
        return self.button("settings_page_buttons_reset", self.reset_appearance)

    def reset_performance_button(self) -> QPushButton:
        return self.button("settings_page_buttons_reset", self.reset_performance)

    def reset_keybinds_button(self) -> QPushButton:
        return self.button("settings_page_buttons_reset", self.reset_keybinds)

    def default_labels_button(self) -> QPushButton:
        return self.button("settings_page_buttons_default_labels", self.use_default_labels)

    # Actions
    def reset_appearance(self):
        '''Everything on the Appearance tab back to its default - the background's motion is Graphics' (see reset_performance).'''
        preferences = self.context.preferences
        preferences.set("fade_in", DEFAULT_FADE_IN)
        preferences.set("fade_out", DEFAULT_FADE_OUT)
        self.style.set_background(visual=DEFAULT_BACKGROUND_VISUAL)
        self.style.reset_theme()
        self.router.refresh()

    def set_background_visual(self, key: str):
        self.style.set_background(visual=key)
        # Freeze Background follows it (locked on for No Background) - rebuilt so it shows that
        self.rebuild_timer.start()

    def apply_performance_preset(self, name: str):
        if name:  # "" (Custom) just means the settings below don't match a preset
            self.context.performance.apply_preset(name)
            self.router.refresh()

    def reset_performance(self):
        '''Everything on the Graphics tab back to its default, the background's framerate, motion and detail too.'''
        self.context.performance.reset()
        self.style.set_background(animate=DEFAULT_BACKGROUND_ANIMATE, detailed=DEFAULT_BACKGROUND_DETAILED,
                                  fps=DEFAULT_BACKGROUND_FPS, workspace_frozen=DEFAULT_BACKGROUND_WORKSPACE_FROZEN,
                                  workspace_disabled=DEFAULT_BACKGROUND_WORKSPACE_DISABLED)
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
    One titled section of settings, like a workspace editor section: its
    title, an explanation, then a row per setting - name | control | what
    it does. Built like a panel (see themes' module docstring): a drawer
    with the title and explanation along its top, where a panel's menu bar
    is, and the rows on one card inside the drawer's frame.
    '''

    def __init__(self, page: SettingsPage, name: str, developer: bool = False):
        super().__init__()
        self.page = page
        # A developer-only section marks its title and every row's name
        self.developer = developer
        style = page.style
        labels = page.labels
        style.set_material(self, "panel", rounded=True, outlined=True)
        self.style = style
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        self.drawer_layout = layout

        # Along the drawer's top
        top = QVBoxLayout()
        top.setContentsMargins(style.igap * 2 - style.PANEL_BORDER_WIDTH, style.igap, style.igap * 2, style.igap)
        top.setSpacing(2)
        layout.addLayout(top)
        title = labels.get(f"settings_page_sections_{name}")
        header = QLabel(developer_text(title) if developer else title)
        header.setFont(style.get_font("title_btn"))
        if developer:
            # The mark's fallback font has a taller line - keep the title's own
            header.setFixedHeight(header.fontMetrics().height())
        top.addWidget(header)
        explanation = QLabel(labels.get(f"settings_page_notes_{name}"))
        explanation.setFont(style.get_font("small"))
        explanation.setWordWrap(True)
        top.addWidget(explanation)

        # Inside the drawer
        card = QWidget()
        style.set_material(card, "card")
        layout.addWidget(card)
        self.grid = QGridLayout(card)
        self.grid.setContentsMargins(style.igap * 2, style.igap, style.igap * 2, style.igap)
        self.grid.setHorizontalSpacing(style.igap * 2)
        self.grid.setVerticalSpacing(style.igap)
        # Same column widths in every section, so controls line up down the page
        self.grid.setColumnMinimumWidth(0, page.LABEL_WIDTH)
        self.grid.setColumnMinimumWidth(1, page.CONTROL_WIDTH)
        self.grid.setColumnStretch(2 if page.SHOW_NOTES else 1, 1)
        self.count = 0
        self.fit_frame()
        style.signals.changed.connect(self.fit_frame)

    def fit_frame(self):
        '''The drawer's frame around the card - the theme's "panel_frame" px left, right and below (see Panel.fit_frame).'''
        frame = self.style.setting("panel_frame") + self.style.PANEL_BORDER_WIDTH
        self.drawer_layout.setContentsMargins(frame, self.style.PANEL_BORDER_WIDTH, frame, frame)

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
