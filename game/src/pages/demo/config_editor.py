import copy
import json
import re
from typing import Any, ClassVar
from collections.abc import Callable

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont, QFontMetrics
from PySide6.QtWidgets import (QCheckBox, QComboBox, QDialog, QFrame, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
                               QPlainTextEdit, QScrollArea, QTabWidget, QVBoxLayout, QWidget)

from ...app_core import Context
from ...pages.page import Page
from ..generic.workspace_select import NoteBrowser, WorkspaceSelectPage
from .layout_editor import LayoutEditor
from ...widgets.frame_widgets.find_bar import FindBar
from ...widgets import MenuBar, PANELS, popup
from ...widgets.frame_widgets.menu_bar import MENU_BAR_GROUPS
from ...widgets.panels.modbus_model._builder import DEFENDER_MODELS, MODELS

# The standard left-to-right order for menu bar buttons (see MenuBar.page_buttons)
BUTTON_ORDER = [
    "toggle_button", "theme_button", "labels_button", "page_button",
    "pcap_button", "save_button", "load_button", "stream_button", "preset_button", "data_button",
    "workspace_editor_button", "delete_all_workspace_data_button", "refresh_button", "reset_button", "help_button",
    "back_button", "quit_button",
]

# This page's own menu bar buttons (the other demo pages use DEMO_MENU_BAR)
EDITOR_MENU_BAR = ["help_button", "labels_button", "toggle_button", "theme_button",
                   "page_button", "back_button", "workspaces_button", "title_button", "quit_button"]

# Qt's "no maximum" widget size (QWIDGETSIZE_MAX, which PySide6 doesn't export)
QWIDGETSIZE_MAX = (1 << 24) - 1

# Numeric fields that are real numbers, not 0/1 on-off switches
NUMBER_FIELDS = {"factor", "multiplier", "offset", "strip_chart_auto_fit_max_seconds"}

# Settings the game itself sets from a dropdown, shown as the same choices here - by
# path in _default.json. (A model panel's start_on is a dropdown too, but its
# choices follow that panel's available models - see model_panel_dropdown.)
SETTING_DROPDOWNS: dict[tuple, list[str]] = {}

# The settings tabs and the _default.json groups each one holds - or, for a tab
# with sub-tabs, its (sub-tab, groups) pairs. Anything not listed here goes
# to the last tab, so a new setting is never left out.
SETTING_TABS: list[tuple[str, list[str] | list[tuple[str, list[str]]]]] = [
    ("Panel Availability", ["available", "network_action_forms_shown", "modbus_table_forms_shown",
                            "defender_modbus_forms_shown", "model_panels"]),
    ("Attacker Options", [
        ("Attacker Options", ["modbus_packet_modify_enabled", "network_action_form_inputs"]),
        ("Modbus Registers", ["modbus_registers"]),
        ("Packet Console", ["packet_console", "packet_filter_categories", "packet_filter_checkboxes",
                            "packet_filter_entries", "packet_columns"]),
    ]),
    ("Defender Options", []),
    ("Appearance", ["model_sprites", "model_colors", "strip_chart_sprites", "strip_chart_colors",
                    "strip_chart_auto_fit", "strip_chart_auto_fit_max_seconds"]),
    ("Misc.", []),
]

# start_on's choice for "the first model this panel offers"
FIRST_OFFERED = "(first offered)"


def menu_bar_buttons() -> list[str]:
    '''Every MenuBar button a page config's "menu_bar" can name, in the standard order.'''
    names = [name for name, method in inspect.getmembers(MenuBar, inspect.isfunction)
             if name.endswith("_button") and list(inspect.signature(method).parameters) == ["self"]]
    return sorted(names, key=lambda name: (BUTTON_ORDER.index(name) if name in BUTTON_ORDER else len(BUTTON_ORDER), name))


def is_switch(key: str, default) -> bool:
    '''Whether a default value is a 0/1 on-off switch (shown as a checkbox).'''
    if isinstance(default, bool):
        return True
    return isinstance(default, (int, float)) and key not in NUMBER_FIELDS and default in (0, 1)


def set_nested(data: dict, path: tuple, value):
    '''Sets path in data, making any dicts along the way that aren't there yet.'''
    for key in path[:-1]:
        if not isinstance(data.get(key), dict):
            data[key] = {}
        data = data[key]
    data[path[-1]] = value


def remove_nested(data: dict, path: tuple):
    '''Removes path from data, then any dicts along it left empty.'''
    parents = []
    for key in path[:-1]:
        if not isinstance(data.get(key), dict):
            return
        parents.append((data, key))
        data = data[key]
    data.pop(path[-1], None)
    for parent, key in reversed(parents):
        if parent[key] == {}:
            del parent[key]


class ConfigEditor(Page):
    '''
    Demo page for editing workspace configs with a form instead of raw
    JSON. The menu bar dropdown picks a workspace; the form below shows:

      - its own fields (name, section, order, description, ...)
      - its menu bar buttons, as checkboxes (saved in the standard order)
      - its pane layout's shape and weights (layout_shape, layout_weights)
      - every field in _default.json, holding the workspace's current value,
        split across tabs by SETTING_TABS

    Every section has a plain-language explanation (from
    _default_notes.json). The form is built only from fields that already
    exist, so new fields can't be added here. Save Config checks the form
    and writes the workspace's config.json - with "settings" holding only
    what differs from _default.json.
    '''

    NOTES_FILE = "_default_notes.json"
    LABEL_WIDTH = 380

    # Kept on the class so it survives the page rebuild that the theme
    # buttons trigger (see Style.toggle_mode/select_theme -> router.refresh)
    selected_key: str | None = None
    selected_tab: int = 0
    # Each settings tab with sub-tabs' last-picked sub-tab, by its title
    selected_subtabs: ClassVar[dict[str, int]] = {}

    def __init__(self, context: Context):
        super().__init__(context)
        self.labels = context.labels
        self.pages = context.pages
        self.json = context.json
        self.default_settings = context.states.get_default()
        self.notes = context.json.load(context.paths.packages / self.NOTES_FILE)
        self.label_width = self.key_column_width()
        self.categories = [section.get("category") for section in
                           self.pages.load_page_config("title/select_workspace").get("sections", [])]

        # Display name -> page key for every workspace, listed or not
        keys = sorted(key for key, build_type in self.pages.build_types.items() if build_type == "workspace")
        self.keys_by_name = {self.workspace_name(key): key for key in keys}
        if ConfigEditor.selected_key not in keys:
            ConfigEditor.selected_key = keys[0] if keys else None

        menu_bar = MenuBar(self, context, "config_editor_demo")
        self.dropdown = None
        if keys:
            self.dropdown = menu_bar.add_dropdown(list(self.keys_by_name), self.pick,
                                                  default=self.workspace_name(ConfigEditor.selected_key))
        menu_bar.add_button("new_workspace", lambda: self.unless_unsaved(self.new_workspace))
        if keys:
            menu_bar.add_button("delete_workspace", lambda: self.unless_unsaved(self.delete_workspace))
        menu_bar.add_button("save_config", self.save)
        if keys:
            menu_bar.add_button("open_workspace", lambda: self.unless_unsaved(self.open_workspace))
        menu_bar.add_config_buttons(EDITOR_MENU_BAR)

        self.tabs = QTabWidget()
        self.tabs.setFont(self.style.get_font("default"))
        self.tabs.currentChanged.connect(self.remember_tab)
        self.layout().addWidget(self.tabs, 1)
        self.find_bar = FindBar(self, context, self.tabs)
        self.layout().addWidget(self.find_bar)
        self.status = QLabel()
        self.status.setFont(self.style.get_font("default"))
        self.status.setWordWrap(True)
        self.layout().addWidget(self.status)

        self.load(ConfigEditor.selected_key)

    def key_column_width(self) -> int:
        '''
        The key column's width in every section - at least LABEL_WIDTH, and
        wide enough for the longest (indented) settings key - so each
        section's columns, and its Clear/Edit buttons, line up with the rest.
        '''
        metrics = QFontMetrics(self.style.get_font("default"))
        bold = QFont(self.style.get_font("default"))
        bold.setBold(True)
        bold_metrics = QFontMetrics(bold)
        widest = 0
        def walk(settings: dict, depth: int):
            nonlocal widest
            for key, value in settings.items():
                text = Rows.INDENT * depth + key
                widest = max(widest, metrics.horizontalAdvance(text), bold_metrics.horizontalAdvance(text))
                if isinstance(value, dict):
                    walk(value, depth + 1)
        walk(self.default_settings, 0)
        return max(self.LABEL_WIDTH, widest + self.style.igap * 2)

    def workspace_name(self, key: str) -> str:
        return self.labels.get(self.pages.link_label(key))

    # Creating and deleting workspaces
    def workspace_folder(self) -> str:
        '''The folder workspaces live in, as listed by the workspace select page.'''
        return self.pages.load_page_config("title/select_workspace").get("link_folder", "workspaces")

    def unless_unsaved(self, action: Callable[[], None]):
        '''Runs action, first asking to discard any unsaved changes.'''
        if not self.dirty:
            action()
            return
        popup.confirm_dialog(self, self.context, "Discard your unsaved changes to this workspace?",
                             "Yes, discard", "No, keep editing", action)

    def new_workspace(self):
        NewWorkspaceDialog(self).show()

    def create_workspace(self, name: str, folder: str, template_key: str):
        '''
        Makes a new workspace by copying template_key's config - its layout,
        menu bar and settings - with a fresh name, description and place at
        the end of its section, plus the two labels it needs, then opens it.
        '''
        key = f"{self.workspace_folder()}/{folder}"
        config = json.loads(self.pages.config_paths[template_key].read_text(encoding="utf-8"))
        config.pop("_dev_note", None)
        category = config.get("category")
        orders = [other.get("order", 0) for other in self.pages.pages_in(self.workspace_folder()).values()
                  if other.get("category") == category]
        config.update({
            "_note": [f"# {name}", "Describe this workspace here: its summary, objectives, reading, and videos."],
            "link_label": f"title_buttons_workspace_{folder}",
            "include": 1,
            "order": max(orders, default=0) + 1,
            "prerequisites": [],
            "title": f"{folder}_workspace",
        })
        # _note first, the way every workspace config starts
        config = {"_note": config.pop("_note"), **config}
        self.labels.add_default_label(config["link_label"], name, after_prefix="title_buttons_workspace_")
        self.labels.add_default_label(f"menu_bar_titles_{config['title']}", name, after_prefix="menu_bar_titles_")
        self.pages.create_folder_page(key, config)
        self.router.register_discovered_pages()
        ConfigEditor.selected_key = key
        self.router.refresh(save=False)

    def open_workspace(self):
        '''Shows the workspace being edited, as saved (Back returns here).'''
        if ConfigEditor.selected_key is not None:
            self.router.show(ConfigEditor.selected_key)

    def delete_workspace(self):
        key = ConfigEditor.selected_key
        if key is not None:
            DeleteWorkspaceDialog(self, key).show()

    def remove_workspace(self, key: str):
        '''
        Permanently deletes a workspace: its folder, every student's saved
        data for it, other workspaces' prerequisites naming it, and its two
        labels (unless another page still uses them).
        '''
        config = self.pages.load_page_config(key)
        label_keys = [config.get("link_label"), f"menu_bar_titles_{config.get('title')}"]
        self.pages.delete_folder_page(key)
        still_used = set()
        for other_key in self.pages.config_paths:
            other = self.pages.load_page_config(other_key)
            still_used |= {other.get("link_label"), f"menu_bar_titles_{other.get('title')}"}
        self.labels.remove_default_labels([label for label in label_keys if label not in still_used])
        self.router.register_discovered_pages()
        ConfigEditor.selected_key = None
        self.router.refresh(save=False)

    # Loading
    def pick(self, name: str):
        key = self.keys_by_name[name]
        if key == ConfigEditor.selected_key:
            return
        if not self.dirty:
            self.load(key)
            return
        # Put the dropdown back until the switch is confirmed
        self.set_dropdown(ConfigEditor.selected_key)
        def discard():
            self.load(key)
            self.set_dropdown(key)
        popup.confirm_dialog(self, self.context, "Discard your unsaved changes to this workspace?",
                             "Yes, discard", "No, keep editing", discard)

    def set_dropdown(self, key: str):
        if self.dropdown is not None:
            self.dropdown.blockSignals(True)
            self.dropdown.setCurrentText(self.workspace_name(key))
            self.dropdown.blockSignals(False)

    def load(self, key: str | None):
        ConfigEditor.selected_key = key
        self.dirty = False
        # Each reads its widget back as a config value, raising ValueError with a message if it can't
        self.field_readers: dict[str, Callable[[], Any]] = {}
        self.setting_cells: list[SettingCell] = []
        self.usage_labels: dict[str, QLabel] = {}
        self.setting_frames: dict[str, QFrame] = {}
        self.button_boxes: dict[str, QCheckBox] = {}
        self.prerequisite_boxes: dict[str, QCheckBox] = {}
        self.field_widgets: dict[str, QWidget] = {}
        # Each model panel's rows (grid, first row, row after its last), and its
        # cells by key under it (see refresh_model_panels)
        self.model_panel_rows: dict[str, tuple[QGridLayout, int, int]] = {}
        self.model_panel_cells: dict[str, dict[tuple, SettingCell]] = {}

        # Rebuilding the tabs changes the current tab, which shouldn't count as picking one
        self.tabs.blockSignals(True)
        # clear() only takes the pages out of the tab widget - delete them too
        old_pages = [self.tabs.widget(index) for index in range(self.tabs.count())]
        self.tabs.clear()
        for page in old_pages:
            page.deleteLater()
        self.build_tabs(key)
        self.tabs.blockSignals(False)

    def build_tabs(self, key: str | None):
        if key is None:
            self.set_status("No workspaces found.", "field_text")
            return
        try:
            self.config = json.loads(self.pages.config_paths[key].read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            self.config = None
            self.set_status(f"This workspace's config.json isn't valid JSON (line {error.lineno}): {error.msg}", "red")
            return

        self.form = self.new_tab("Workspace")
        self.build_workspace_section()
        self.build_description_tab()
        self.form = self.new_tab("Menu Bar")
        self.build_menu_bar_section()
        self.layout_editor = LayoutEditor(self, self.config.get("layout_shape"), self.config.get("layout_weights"))
        self.tabs.addTab(self.layout_editor.shape_tab, "Layout Shape")
        self.tabs.addTab(self.layout_editor.weights_tab, "Layout Weights")
        raw = self.config.get("settings", {})
        self.raw_settings = raw if isinstance(raw, dict) else {}
        self.build_settings_tabs()
        self.refresh_model_panels()
        self.refresh_usage()
        self.tabs.setCurrentIndex(min(ConfigEditor.selected_tab, self.tabs.count() - 1))
        self.set_status(f"Editing {self.pages.config_paths[key]}", "field_text")

    # Tabs
    def new_tab(self, title: str, tabs: QTabWidget | None = None) -> "TopLayout":
        '''Adds a scrolling tab (to tabs, default the page's own) and returns where its sections go (they stack from the top).'''
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet(self.style.themed("QScrollArea { background-color: transparent; border: none; }"))
        body = QWidget()
        self.paint_root(body)
        form = QVBoxLayout(body)
        form.setSpacing(self.style.igap)
        form.setContentsMargins(0, self.style.igap, self.style.igap, 0)
        form.addStretch(1)
        scroll.setWidget(body)
        (tabs or self.tabs).addTab(scroll, title)
        return TopLayout(form)

    def paint_root(self, widget: QWidget):
        '''
        Paints widget the page's root color. A scroll area's body is a plain
        QWidget, which otherwise shows Qt's default grey in every gap
        between the sections it holds.
        '''
        widget.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        widget.setStyleSheet(self.style.themed(f"background-color: {self.style.color('root')};", widget))

    def remember_tab(self, index: int):
        ConfigEditor.selected_tab = index

    def build_description_tab(self):
        '''
        The markdown the workspace select page shows for this workspace
        (_note), with a live preview beside it - rendered the same way
        that page does, images included - and the developer note below.
        '''
        page = QWidget()
        columns = QHBoxLayout(page)
        columns.setSpacing(self.style.igap)
        self.tabs.addTab(page, "Description")

        left = QVBoxLayout()
        columns.addLayout(left, 1)
        note = self.config.get("_note", "")
        note_text = "\n\n".join(note) if isinstance(note, list) else str(note)
        readers = {}
        for name, rows in (("_note", None), ("_dev_note", 4)):
            label = QLabel(name)
            label.setFont(self.style.get_font("title_btn"))
            left.addWidget(label)
            explanation = QLabel(self.workspace_note(name))
            explanation.setFont(self.style.get_font("small"))
            explanation.setWordWrap(True)
            left.addWidget(explanation)
            text = note_text if name == "_note" else str(self.config.get("_dev_note", ""))
            editor, reader = self.text_area(text, rows=rows)
            left.addWidget(editor, 1 if rows is None else 0)
            readers[name] = (editor, reader)
        note_editor, note_reader = readers["_note"]
        self.field_readers["_dev_note"] = readers["_dev_note"][1]

        def read_note():
            # Unedited: keep the original blocks, even ones with blank lines inside them
            if note_reader() == note_text:
                return note
            return [block.strip() for block in note_reader().split("\n\n") if block.strip()]
        self.field_readers["_note"] = read_note

        preview = NoteBrowser()
        preview.setOpenExternalLinks(True)
        preview.setFont(self.style.get_font("default"))
        preview.setStyleSheet(self.style.themed(
            f"QTextBrowser {{ background-color: {self.style.color('field')}; color: {self.style.color('field_text')};"
            f" border: none; border-radius: {self.style.PANEL_RADIUS}px; padding: 8px; }}"))
        preview.setSearchPaths([str(self.pages.config_paths[ConfigEditor.selected_key].parent)])
        columns.addWidget(preview, 1)
        def refresh_preview():
            preview.document().clear()
            preview.setMarkdown(WorkspaceSelectPage.join_note(read_note()))
        note_editor.textChanged.connect(refresh_preview)
        refresh_preview()

    # Form building - one value per row: its name on the left, its input on the right
    def section(self, title: str, explanation: str | None, note: QLabel | None = None) -> "Rows":
        frame = QFrame()
        frame.setStyleSheet(self.style.themed(
            f"QFrame {{ background-color: {self.style.color('panel')}; border-radius: {self.style.PANEL_RADIUS}px; }}", frame))
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(self.style.igap * 2, self.style.igap, self.style.igap * 2, self.style.igap)
        header = QLabel(title)
        header.setFont(self.style.get_font("title_btn"))
        layout.addWidget(header)
        if explanation:
            text = QLabel(explanation)
            text.setFont(self.style.get_font("small"))
            text.setWordWrap(True)
            layout.addWidget(text)
        if note is not None:
            layout.addWidget(note)
        grid = QGridLayout()
        grid.setHorizontalSpacing(self.style.igap * 2)
        grid.setColumnStretch(1, 1)
        # Same label column width in every section, so inputs line up down the page
        grid.setColumnMinimumWidth(0, self.label_width)
        layout.addLayout(grid)
        self.form.addWidget(frame)
        return Rows(self, grid)

    def workspace_note(self, name: str) -> str:
        return self.notes.get("workspace_fields", {}).get(name, "")

    def build_workspace_section(self):
        rows = self.section("Workspace", "How this workspace is listed and named. Hover over a field's name for its explanation.")
        def add(name: str, widget: QWidget, reader: Callable[[], Any]):
            rows.add(name, widget, tooltip=self.workspace_note(name))
            self.field_readers[name] = reader
            self.field_widgets[name] = widget

        for name in ("link_label", "title"):
            entry, reader = self.text_entry(str(self.config.get(name, "")))
            add(name, entry, reader)
        box, reader = self.checkbox(self.config.get("include", 0), as_bool=False)
        add("include", box, reader)
        combo = QComboBox()
        combo.setFont(self.style.get_font("default"))
        combo.addItems([str(category) for category in self.categories])
        combo.setCurrentText(str(self.config.get("category", "")))
        combo.currentIndexChanged.connect(self.mark_dirty)
        add("category", combo, combo.currentText)
        for name in ("order", "estimated_minutes"):
            entry, reader = self.number_entry(name, self.config.get(name, 0), integer=True)
            add(name, entry, reader)
        box, reader = self.checkbox(self.config.get("gradable", False), as_bool=True)
        add("gradable", box, reader)

        # Prerequisites: one row per other workspace
        rows.heading("prerequisites", tooltip=self.workspace_note("prerequisites"))
        chosen = set(self.config.get("prerequisites", []))
        for name, key in self.keys_by_name.items():
            if key == ConfigEditor.selected_key:
                continue
            box, _ = self.checkbox(key in chosen, as_bool=True)
            rows.add(name, box, depth=1)
            self.prerequisite_boxes[key] = box
        self.field_readers["prerequisites"] = lambda: [key for key, box in self.prerequisite_boxes.items() if box.isChecked()]


    def build_menu_bar_section(self):
        rows = self.section("menu_bar", self.workspace_note("menu_bar") + " Checked buttons are grouped and ordered as listed here "
                            "(see MENU_BAR_GROUPS in menu_bar.py). A group or header checkbox turns all of its buttons on or off.")
        chosen = set(self.config.get("menu_bar", []))
        for group_key, sections in MENU_BAR_GROUPS.items():
            group_box = self.group_checkbox()
            rows.add(group_key, group_box, tooltip=self.labels.get(f"menu_bar_buttons_{group_key}"))
            group_boxes = []
            for header, names in sections:
                header_box = self.group_checkbox()
                rows.add(header, header_box, depth=1, tooltip=self.labels.get(f"menu_bar_headers_{header}"))
                header_boxes = []
                for name in names:
                    box, _ = self.checkbox(name in chosen, as_bool=True)
                    rows.add(name, box, depth=2)
                    self.button_boxes[name] = box
                    header_boxes.append(box)
                self.link_group_checkbox(header_box, header_boxes)
                group_boxes += header_boxes
            self.link_group_checkbox(group_box, group_boxes)

    def group_checkbox(self) -> QCheckBox:
        '''A checkbox standing for several others - see link_group_checkbox.'''
        box = QCheckBox()
        box.setFont(self.style.get_font("default"))
        box.setTristate(True)
        return box

    def link_group_checkbox(self, group_box: QCheckBox, boxes: list[QCheckBox]):
        '''
        Makes group_box show whether all, some, or none of boxes are
        checked, and clicking it check all of them - or uncheck all, if they
        already were. It's never saved itself; only boxes are.
        '''
        def sync():
            checked = sum(box.isChecked() for box in boxes)
            state = (Qt.CheckState.Checked if checked == len(boxes)
                     else Qt.CheckState.PartiallyChecked if checked else Qt.CheckState.Unchecked)
            group_box.blockSignals(True)
            group_box.setCheckState(state)
            group_box.blockSignals(False)

        def click(*_):
            target = not all(box.isChecked() for box in boxes)
            for box in boxes:
                box.setChecked(target)
            sync()

        for box in boxes:
            box.toggled.connect(sync)
        group_box.clicked.connect(click)
        sync()

    def build_settings_tabs(self):
        '''
        One tab per SETTING_TABS entry - or a row of sub-tabs, for an entry
        that lists them - each holding its settings groups in _default.json's order.
        '''
        def pages(entries) -> list[tuple[str, list[str]]]:
            return entries if entries and isinstance(entries[0], tuple) else []
        listed = {name for _, entries in SETTING_TABS
                  for name in ([name for _, names in pages(entries) for name in names] or entries)}
        self.settings_forms: dict[str, TopLayout] = {}
        for title, entries in SETTING_TABS:
            if not pages(entries):
                if title == SETTING_TABS[-1][0]:
                    entries = entries + [name for name in self.default_settings if name not in listed]
                self.form = self.new_tab(title)
                self.build_settings_page(title, entries)
                continue
            subtabs = QTabWidget()
            subtabs.setFont(self.style.get_font("default"))
            self.tabs.addTab(subtabs, title)
            for subtitle, names in pages(entries):
                self.form = self.new_tab(subtitle, subtabs)
                self.build_settings_page(subtitle, names)
            subtabs.setCurrentIndex(min(ConfigEditor.selected_subtabs.get(title, 0), subtabs.count() - 1))
            subtabs.currentChanged.connect(lambda index, title=title: ConfigEditor.selected_subtabs.__setitem__(title, index))

    def build_settings_page(self, title: str, names: list[str]):
        '''The settings groups named, in _default.json's order, on the tab self.form belongs to.'''
        names = [name for name in self.default_settings if name in names]
        if not names:
            self.section(title, "No settings here yet.")
        for name in names:
            self.build_setting_section(name, self.default_settings[name])
            self.settings_forms[name] = self.form

    def build_setting_section(self, name: str, default):
        explanation = self.notes.get("settings_fields", {}).get(name, "No explanation yet - add one to _default_notes.json.")
        usage = QLabel()
        usage.setWordWrap(True)
        self.usage_labels[name] = usage
        rows = self.section(name, explanation, note=usage)
        self.setting_frames[name] = rows.grid.parentWidget()
        rows.setting_header()
        if isinstance(default, dict):
            self.add_setting_rows(rows, (name,), default, depth=0)
        else:
            self.add_setting_row(rows, (name,), default, depth=0)

    def add_setting_rows(self, rows: "Rows", path: tuple, default: dict, depth: int):
        for key, item_default in default.items():
            first_row = rows.row
            if isinstance(item_default, dict):
                description, details = self.key_notes(path + (key,))
                rows.heading(key, depth=depth, tooltip=details, description=description)
                self.add_setting_rows(rows, path + (key,), item_default, depth + 1)
            else:
                self.add_setting_row(rows, path + (key,), item_default, depth)
            if path == ("model_panels",):
                self.model_panel_rows[key] = (rows.grid, first_row, rows.row)

    def key_notes(self, path: tuple) -> tuple[str, str]:
        '''
        One settings key's (description, details) from _default_notes.json's
        "settings_keys", nested like _default.json: the short description
        for the Description column and the longer details for the key's
        tooltip. A "*" entry covers any key without its own (every hreg_N),
        and a nested object's "_note" explains its heading. A top-level key
        with neither falls back to its "settings_fields" explanation as its
        tooltip.
        '''
        node = self.notes.get("settings_keys", {})
        for key in path:
            node = node.get(key, node.get("*")) if isinstance(node, dict) else None
        if isinstance(node, dict) and "description" not in node:
            node = node.get("_note")
        if isinstance(node, dict):
            return str(node.get("description", "")), str(node.get("details", ""))
        if len(path) == 1:
            return "", self.notes.get("settings_fields", {}).get(path[0], "")
        return "", ""

    def layout_panels(self) -> list[str]:
        '''The panel types in the layout being edited, in layout order, each once.'''
        found = []
        def walk(entry: dict):
            if "widget" in entry:
                if entry["widget"] not in found:
                    found.append(entry["widget"])
            else:
                for child in entry["panes"]["children"]:
                    walk(child)
        walk(self.layout_editor.root)
        return found

    def refresh_usage(self):
        '''
        Notes under each settings group which panels in this layout use it
        (each panel class lists its keys in SETTINGS). Called again whenever
        the layout's shape changes.
        '''
        panels = self.layout_panels()
        self.show_layout_model_panels()
        for name, label in getattr(self, "usage_labels", {}).items():
            users = [panel for panel in panels if name in getattr(PANELS.get(panel), "SETTINGS", ())]
            font = QFont(self.style.get_font("small"))   # a copy - get_font's font is shared
            if users:
                label.setText("Used by panels: " + ", ".join(users))
                label.setStyleSheet("")
            else:
                label.setText("Not used by any panel in this layout")
                font.setItalic(True)
                text = QColor(self.style.color("text"))
                label.setStyleSheet(f"color: rgba({text.red()}, {text.green()}, {text.blue()}, 150);")
            label.setFont(font)
        self.sort_settings(panels)

    def show_layout_model_panels(self):
        '''Shows only the model_panels entries for model panels the layout has - the rest are ignored.'''
        in_layout = set(self.layout_editor.all_ids())
        for panel_id, (grid, first, end) in self.model_panel_rows.items():
            for row in range(first, end):
                for column in range(grid.columnCount()):
                    item = grid.itemAtPosition(row, column)
                    if item is not None and item.widget() is not None:
                        item.widget().setVisible(panel_id in in_layout)

    # Model panels: start_on's choices and the Auto-Switch rows follow each panel's available models
    @staticmethod
    def cell_value(cell: "SettingCell"):
        '''What a setting will be once saved: its input if touched, else its default.'''
        if not cell.touched:
            return cell.default
        try:
            return cell.reader()
        except ValueError:
            return cell.default

    def offered_models(self, panel_id: str) -> list[str]:
        cells = self.model_panel_cells.get(panel_id, {})
        return [model for model in MODELS
                if ("available", model) in cells and self.cell_value(cells[("available", model)]) in (1, "1", True)]

    def refresh_model_panels(self):
        '''
        For each model panel: start_on only offers the models checked under
        its available, and the Auto-Switch rows are only editable when they
        can apply - both polled models offered, and for auto_switch_on_poll,
        the checkbox shown too. Called on every form change (see mark_dirty).
        '''
        for panel_id, cells in self.model_panel_cells.items():
            models = self.offered_models(panel_id)
            start = cells.get(("start_on",))
            if start is not None:
                combo = start.widget
                current = combo.currentData()
                combo.blockSignals(True)
                combo.clear()
                combo.addItem(FIRST_OFFERED, "")
                for model in models:
                    combo.addItem(self.labels.get(f"modbus_model_options_{model}"), model)
                combo.setCurrentIndex(max(0, combo.findData(current)))
                combo.blockSignals(False)
            show = cells.get(("show_auto_switch_checkbox",))
            run = cells.get(("auto_switch_on_poll",))
            both_polled = DEFENDER_MODELS <= set(models)
            if show is not None:
                show.widget.setEnabled(both_polled)
            if run is not None:
                run.widget.setEnabled(both_polled and show is not None and self.cell_value(show) in (1, "1", True))

    def model_panel_dropdown(self, value) -> tuple[QComboBox, Callable[[], str]]:
        '''start_on's dropdown - filled with its panel's offered models by refresh_model_panels.'''
        combo = QComboBox()
        combo.setFont(self.style.get_font("default"))
        combo.addItem(FIRST_OFFERED, "")
        if value:
            combo.addItem(self.labels.get(f"modbus_model_options_{value}"), value)
            combo.setCurrentIndex(1)
        combo.setMaximumWidth(360)
        combo.currentIndexChanged.connect(self.mark_dirty)
        return combo, combo.currentData

    def sort_settings(self, panels: list[str]):
        '''
        Orders each settings tab's groups by how many panels in this layout use
        them, most first - then by how many panel types use them at all, then
        in _default.json's order. Groups nothing in the layout uses end up last.
        '''
        frames = getattr(self, "setting_frames", {})
        if not frames:
            return
        names = list(self.default_settings)
        def in_layout(name):
            return sum(1 for panel in panels if name in getattr(PANELS.get(panel), "SETTINGS", ()))
        def overall(name):
            return sum(1 for panel_class in PANELS.values() if name in getattr(panel_class, "SETTINGS", ()))
        order = sorted(frames, key=lambda name: (-in_layout(name), -overall(name), names.index(name)))
        for form in {id(form): form for form in self.settings_forms.values()}.values():
            tab_order = [name for name in order if self.settings_forms[name] is form]
            for position, name in enumerate(tab_order):
                if form.layout.indexOf(frames[name]) != position:
                    form.layout.removeWidget(frames[name])
                    form.layout.insertWidget(position, frames[name])

    def config_value(self, path: tuple):
        '''(True, value) if this workspace's own "settings" has path, else (False, None).'''
        node = self.raw_settings
        for key in path:
            if not isinstance(node, dict) or key not in node:
                return False, None
            node = node[key]
        return True, node

    def add_setting_row(self, rows: "Rows", path: tuple, default, depth: int):
        '''
        One setting: its key, its _default.json value, and - if the
        workspace's config has the key ("touched") - a Clear button and its
        input; otherwise ("untouched") just an Edit button.
        '''
        touched, value = self.config_value(path)
        widget, reader = self.leaf(path, default, value if touched else default)
        cell = SettingCell(self, path, widget, reader, default, touched)
        description, details = self.key_notes(path)
        cell.label = rows.add(path[-1], cell, depth=depth, tooltip=details, description=description,
                              default_text=SettingCell.describe(path[-1], default))
        cell.show_state()
        self.setting_cells.append(cell)
        if path[0] == "model_panels" and len(path) > 2:
            self.model_panel_cells.setdefault(path[1], {})[path[2:]] = cell

    # Widgets, each paired with a reader that turns it back into a config value
    def leaf(self, path: tuple, default, value) -> tuple[QWidget, Callable[[], Any]]:
        key = path[-1]
        if path[0] == "model_panels" and path[2:] == ("start_on",):
            return self.model_panel_dropdown(value)
        if path in SETTING_DROPDOWNS:
            return self.choice_dropdown(SETTING_DROPDOWNS[path], value)
        if is_switch(key, default):
            return self.checkbox(value, as_bool=isinstance(default, bool), as_float=isinstance(value, float))
        if isinstance(default, (int, float)):
            return self.number_entry(key, value, integer=isinstance(default, int))
        if isinstance(default, list):
            # One item per line, so items can hold commas
            editor, reader = self.text_area("\n".join(str(item) for item in value), rows=max(1, min(len(value), 6)))
            editor.setToolTip("One item per line")
            return editor, lambda: [item.strip() for item in reader().split("\n")]
        return self.text_entry(str(value))

    def checkbox(self, value, as_bool: bool, text: str = "", as_float: bool = False) -> tuple[QCheckBox, Callable[[], Any]]:
        box = QCheckBox(text)
        box.setFont(self.style.get_font("default"))
        box.setChecked(value in (1, "1", True))
        box.toggled.connect(self.mark_dirty)
        if as_bool:
            return box, box.isChecked
        on, off = (1.0, 0.0) if as_float else (1, 0)
        return box, lambda: on if box.isChecked() else off

    def choice_dropdown(self, options: list[str], value) -> tuple[QComboBox, Callable[[], str]]:
        '''
        A fixed set of choices, each explained by its tooltip (its "available"
        description in _default_notes.json, when it has one). A value that
        isn't one of them is kept as an extra choice, so loading and saving
        never changes it.
        '''
        combo = QComboBox()
        combo.setFont(self.style.get_font("default"))
        choices = list(options) + ([str(value)] if str(value) not in options else [])
        notes = self.notes.get("settings_keys", {}).get("available", {})
        for index, choice in enumerate(choices):
            combo.addItem(choice)
            note = notes.get(choice)
            if isinstance(note, dict):
                combo.setItemData(index, note.get("details", ""), Qt.ItemDataRole.ToolTipRole)
        combo.setCurrentText(str(value))
        combo.setMaximumWidth(360)
        combo.currentIndexChanged.connect(self.mark_dirty)
        return combo, combo.currentText

    def text_entry(self, text: str) -> tuple[QLineEdit, Callable[[], str]]:
        entry = QLineEdit(text)
        entry.setFont(self.style.get_font("default"))
        entry.textChanged.connect(self.mark_dirty)
        return entry, entry.text

    def number_entry(self, name: str, value, integer: bool = False) -> tuple[QLineEdit, Callable[[], Any]]:
        entry, text = self.text_entry(f"{value:g}" if isinstance(value, float) else str(value))
        entry.setMaximumWidth(140)
        def read():
            try:
                number = float(text())
            except ValueError:
                raise ValueError(f'"{name}" must be a number, not "{text()}"') from None
            if integer:
                if number != int(number):
                    raise ValueError(f'"{name}" must be a whole number, not "{text()}"')
                return int(number)
            return int(number) if number == int(number) and "." not in text() else number
        return entry, read

    def text_area(self, text: str, rows: int | None) -> tuple[QPlainTextEdit, Callable[[], str]]:
        '''A multi-line text box, rows lines tall - or growing to fill its space if rows is None.'''
        editor = QPlainTextEdit(text)
        editor.setFont(self.style.get_font("default"))
        if rows is not None:
            editor.setFixedHeight(self.fontMetrics().lineSpacing() * rows + 16)
        editor.textChanged.connect(self.mark_dirty)
        return editor, editor.toPlainText

    # Saving
    def mark_dirty(self, *_):
        # Every form change comes through here, so dependent rows update with it
        self.refresh_model_panels()
        if not self.dirty:
            self.dirty = True
            self.set_status("Unsaved changes.", "field_text")

    def set_status(self, text: str, color: str):
        self.status.setText(text)
        self.status.setStyleSheet(f"color: {self.style.color(color)};")

    def save(self):
        key = ConfigEditor.selected_key
        if key is None or self.config is None:
            return
        config, errors = self.collect()
        if errors:
            shown = errors[:6] + ([f"...and {len(errors) - 6} more"] if len(errors) > 6 else [])
            self.set_status("Can't save yet:\n" + "\n".join(f"- {error}" for error in shown), "red")
            return
        self.pages.config_paths[key].write_text(self.json.format_config(config), encoding="utf-8")
        self.config = config
        self.dirty = False
        self.set_status(f"Saved {self.pages.config_paths[key]}", "green")

    def collect(self) -> tuple[dict, list[str]]:
        '''The workspace's config rebuilt from the form, keeping its fields in their original order, plus any problems.'''
        config = copy.deepcopy(self.config)
        errors = []
        def read(reader):
            try:
                return reader(), None
            except ValueError as error:
                errors.append(str(error))
                return None, True

        for name, reader in self.field_readers.items():
            value, failed = read(reader)
            if not failed:
                config[name] = value
        if not config.get("_dev_note"):
            config.pop("_dev_note", None)
        for name, prefix in (("link_label", ""), ("title", "menu_bar_titles_")):
            if f"{prefix}{config.get(name)}" not in self.labels.data:
                errors.append(f'"{name}": there\'s no label named "{prefix}{config.get(name)}" in assets/labels/_default.json')

        # Start from the file's own settings, so their order - and anything the form
        # doesn't know about - is kept; then write touched rows and drop cleared ones
        settings = copy.deepcopy(self.raw_settings)
        for cell in self.setting_cells:
            if cell.touched:
                value, failed = read(cell.reader)
                if not failed:
                    set_nested(settings, cell.path, value)
            else:
                remove_nested(settings, cell.path)
        config["settings"] = settings

        config["menu_bar"] = [name for name, box in self.button_boxes.items() if box.isChecked()]

        config.pop("panes", None)
        config["layout_shape"], config["layout_weights"], layout_errors = self.layout_editor.authored()
        errors += layout_errors
        for panel_id in self.layout_editor.all_ids():
            if panel_id in self.model_panel_cells and not self.offered_models(panel_id):
                errors.append(f'"model_panels" > "{panel_id}": turn on at least one model under available.')
        return config, errors


class Rows:
    '''Adds one-value-per-line rows to a form section: the field's name on the left, its input on the right.'''

    INDENT = "    "

    def __init__(self, page: ConfigEditor, grid: QGridLayout):
        self.page = page
        self.grid = grid
        self.row = 0

    def label(self, text: str, depth: int, tooltip: str) -> QLabel:
        label = QLabel(self.INDENT * depth + text)
        label.setFont(self.page.style.get_font("default"))
        label.setToolTip(tooltip)
        return label

    def heading(self, text: str, depth: int = 0, tooltip: str = "", description: str = ""):
        self.grid.addWidget(self.label(text, depth, tooltip), self.row, 0)
        if description:
            self.grid.addWidget(self.description(description), self.row, 1)
        self.row += 1

    def description(self, text: str) -> QLabel:
        '''A settings key's short explanation, wrapping within the Description column.'''
        label = QLabel(text)
        label.setFont(self.page.style.get_font("small"))
        label.setWordWrap(True)
        label.setMinimumWidth(self.DESCRIPTION_WIDTH)
        return label

    DEFAULT_WIDTH = 260
    DESCRIPTION_WIDTH = 260

    def setting_header(self):
        '''
        Column titles for a settings section: the key, what it does, its
        _default.json value, the Edit/Clear buttons (untitled), and this
        workspace's value.
        '''
        self.grid.setColumnStretch(1, 1)
        self.grid.setColumnStretch(4, 1)
        self.grid.setColumnMinimumWidth(1, self.DESCRIPTION_WIDTH)
        self.grid.setColumnMinimumWidth(2, self.DEFAULT_WIDTH)
        for column, text in ((1, "Description"), (2, "Default"), (4, "This workspace")):
            label = QLabel(text)
            label.setFont(self.page.style.get_font("small"))
            self.grid.addWidget(label, self.row, column)
        self.row += 1

    def add(self, text: str, widget: QWidget, depth: int = 0, tooltip: str = "", default_text: str | None = None,
            description: str = "") -> QLabel:
        label = self.label(text, depth, tooltip)
        if default_text is not None:
            # Settings rows: key, description and default centred on the row's buttons
            self.grid.addWidget(label, self.row, 0, Qt.AlignmentFlag.AlignVCenter)
            self.grid.addWidget(self.description(description), self.row, 1, Qt.AlignmentFlag.AlignVCenter)
            default = QLabel(default_text)
            default.setFont(self.page.style.get_font("default"))
            default.setWordWrap(True)
            default.setMaximumWidth(self.DEFAULT_WIDTH)
            self.grid.addWidget(default, self.row, 2, Qt.AlignmentFlag.AlignVCenter)
            self.grid.addWidget(widget.touch_button, self.row, 3, Qt.AlignmentFlag.AlignVCenter)
            self.grid.addWidget(widget, self.row, 4)
            self.row += 1
            return label
        self.grid.addWidget(label, self.row, 0, Qt.AlignmentFlag.AlignTop)
        # Inputs narrower than the column (checkboxes, number boxes) sit at its left edge instead of centered
        fills = not isinstance(widget, QCheckBox) and widget.maximumWidth() >= QWIDGETSIZE_MAX
        self.grid.addWidget(widget, self.row, 1, Qt.AlignmentFlag(0) if fills else Qt.AlignmentFlag.AlignLeft)
        self.row += 1
        return label


class SettingCell(QWidget):
    '''
    A setting's value column, beside its key, description and default value. The row
    reads key | description | default | button | this workspace, where the last column is
    this widget and the button (touch_button) is placed before it by Rows:

      - untouched (only _default.json has this key): Edit | "Uses default"
        Edit makes the row touched, showing its input, starting from the default.
      - touched (the workspace's config has this key): Clear | input
        The input can always be written to; Clear removes the key from the
        config, making the row untouched again.

    Nothing is checked or saved here - Save Config reads every touched input.
    '''

    UNTOUCHED_TEXT = "Uses default"

    def __init__(self, page: ConfigEditor, path: tuple, widget: QWidget, reader: Callable[[], Any], default, touched: bool):
        super().__init__()
        self.page = page
        self.path = path
        self.widget = widget
        self.reader = reader
        self.default = default
        self.touched = touched
        self.label: QLabel | None = None

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Not in this widget's own layout - Rows puts it in the column before it
        self.touch_button = QPushButton()
        self.touch_button.setFont(page.style.get_font("small"))
        self.touch_button.clicked.connect(lambda checked=False: self.toggle())
        width = max(self.touch_button.fontMetrics().horizontalAdvance(text) for text in ("Edit", "Clear")) + 32
        self.touch_button.setFixedWidth(width)

        # Untouched rows show this where the input would be
        self.placeholder = QLabel(self.UNTOUCHED_TEXT)
        italic = QFont(page.style.get_font("default"))   # a copy - get_font's font is shared
        italic.setItalic(True)
        self.placeholder.setFont(italic)
        text = QColor(page.style.color("text"))
        self.placeholder.setStyleSheet(f"color: rgba({text.red()}, {text.green()}, {text.blue()}, 150);")
        layout.addWidget(self.placeholder, 1)

        self.holder = QWidget()
        holder_layout = QHBoxLayout(self.holder)
        holder_layout.setContentsMargins(0, 0, 0, 0)
        fills = not isinstance(widget, QCheckBox) and widget.maximumWidth() >= QWIDGETSIZE_MAX
        holder_layout.addWidget(widget, 1 if fills else 0)
        if not fills:
            holder_layout.addStretch(1)
        layout.addWidget(self.holder, 1)

    @staticmethod
    def describe(key: str, default) -> str:
        if is_switch(key, default):
            return "on" if default in (1, True) else "off"
        if isinstance(default, list):
            return ", ".join(str(item) for item in default) if any(str(item) for item in default) else "(empty)"
        if isinstance(default, float):
            return f"{default:g}"
        return str(default) if str(default) else "(empty)"

    def show_state(self):
        self.holder.setVisible(self.touched)
        self.placeholder.setVisible(not self.touched)
        self.touch_button.setText("Clear" if self.touched else "Edit")
        if self.label is not None:
            font = self.label.font()
            font.setBold(self.touched)
            self.label.setFont(font)

    def toggle(self):
        self.touched = not self.touched
        if not self.touched:
            self.reset_input()
        self.show_state()
        self.page.mark_dirty()
        if self.touched:
            self.widget.setFocus()

    def reset_input(self):
        '''Puts the input back to the default, so touching the row again starts from there.'''
        widget, default = self.widget, self.default
        widget.blockSignals(True)
        if isinstance(widget, QCheckBox):
            widget.setChecked(default in (1, "1", True))
        elif isinstance(widget, QPlainTextEdit):
            widget.setPlainText("\n".join(str(item) for item in default))
        elif isinstance(widget, QComboBox):
            # Choices with data (start_on's) are matched by it, plain ones by text
            index = widget.findData(default)
            if index >= 0:
                widget.setCurrentIndex(index)
            else:
                widget.setCurrentText(str(default))
        elif isinstance(widget, QLineEdit):
            widget.setText(f"{default:g}" if isinstance(default, float) else str(default))
        widget.blockSignals(False)


class NewWorkspaceDialog(QDialog):
    '''
    Asks for a new workspace's name, its folder name (filled in from the name
    until edited by hand), and which existing workspace to copy its layout,
    menu bar and settings from - the form can't add or remove panels itself.
    '''

    FOLDER_PATTERN = re.compile(r"[a-z][a-z0-9_]*")

    def __init__(self, editor: ConfigEditor):
        super().__init__(editor)
        self.editor = editor
        style = editor.style
        self.setWindowTitle("New Workspace")
        self.setModal(True)
        self.resize(600, 300)
        layout = QVBoxLayout(self)
        grid = QGridLayout()
        layout.addLayout(grid)

        def add(row: int, text: str, widget: QWidget):
            label = QLabel(text)
            label.setFont(style.get_font())
            widget.setFont(style.get_font())
            grid.addWidget(label, row, 0)
            grid.addWidget(widget, row, 1)

        self.name = QLineEdit()
        self.name.setPlaceholderText("e.g. Wireless Sniffing")
        add(0, "Name", self.name)
        self.folder = QLineEdit()
        self.folder.setPlaceholderText("e.g. wireless_sniffing")
        add(1, "Folder", self.folder)
        self.template = QComboBox()
        self.template.addItems(list(editor.keys_by_name))
        if ConfigEditor.selected_key is not None:
            self.template.setCurrentText(editor.workspace_name(ConfigEditor.selected_key))
        add(2, "Copy layout from", self.template)

        self.error = QLabel()
        self.error.setFont(style.get_font("small"))
        self.error.setWordWrap(True)
        self.error.setStyleSheet(f"color: {style.color('red')};")
        layout.addWidget(self.error)
        layout.addStretch(1)

        buttons = QHBoxLayout()
        layout.addLayout(buttons)
        create = QPushButton("Create")
        create.setFont(style.get_font())
        create.clicked.connect(self.create)
        buttons.addWidget(create)
        cancel = QPushButton("Cancel")
        cancel.setFont(style.get_font())
        cancel.clicked.connect(self.reject)
        buttons.addWidget(cancel)

        self.folder_edited = False
        self.name.textEdited.connect(self.suggest_folder)
        self.folder.textEdited.connect(lambda _: setattr(self, "folder_edited", True))

    def suggest_folder(self, name: str):
        if not self.folder_edited:
            self.folder.setText(re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_"))

    def problems(self, name: str, folder: str) -> list[str]:
        editor = self.editor
        if not name:
            return ["Give the workspace a name."]
        if not self.FOLDER_PATTERN.fullmatch(folder):
            return ["The folder name must start with a lowercase letter and use only lowercase letters, numbers, and underscores."]
        key = f"{editor.workspace_folder()}/{folder}"
        if (editor.context.paths.pages / key).exists():
            return [f"There's already a folder named \"{folder}\"."]
        taken = [label for label in (f"title_buttons_workspace_{folder}", f"menu_bar_titles_{folder}_workspace")
                 if label in editor.labels.data]
        if taken:
            return [f"The label \"{taken[0]}\" already exists - pick a different folder name."]
        return []

    def create(self):
        name, folder = self.name.text().strip(), self.folder.text().strip()
        problems = self.problems(name, folder)
        if problems:
            self.error.setText(problems[0])
            return
        template = self.editor.keys_by_name[self.template.currentText()]
        self.accept()
        self.editor.create_workspace(name, folder, template)


class DeleteWorkspaceDialog(QDialog):
    '''
    Deleting a workspace can't be undone, so it has to be confirmed by
    typing the workspace's folder name exactly.
    '''

    def __init__(self, editor: ConfigEditor, key: str):
        super().__init__(editor)
        self.editor = editor
        self.key = key
        style = editor.style
        folder = key.rsplit("/", 1)[-1]
        self.setWindowTitle("Delete Workspace")
        self.setModal(True)
        self.resize(600, 300)
        layout = QVBoxLayout(self)

        message = QLabel(
            f"Permanently delete \"{editor.workspace_name(key)}\"?\n\n"
            f"This deletes its folder ({key}) and everything in it, its labels, and every student's saved "
            "data for it. It can't be undone.\n\n"
            f"Type {folder} below to confirm."
        )
        message.setFont(style.get_font())
        message.setWordWrap(True)
        layout.addWidget(message)
        confirm = QLineEdit()
        confirm.setFont(style.get_font())
        confirm.setPlaceholderText(folder)
        layout.addWidget(confirm)
        layout.addStretch(1)

        buttons = QHBoxLayout()
        layout.addLayout(buttons)
        self.delete_button = QPushButton("Delete forever")
        self.delete_button.setFont(style.get_font())
        self.delete_button.setEnabled(False)
        self.delete_button.clicked.connect(self.delete)
        buttons.addWidget(self.delete_button)
        cancel = QPushButton("Cancel")
        cancel.setFont(style.get_font())
        cancel.clicked.connect(self.reject)
        buttons.addWidget(cancel)
        confirm.textChanged.connect(lambda text: self.delete_button.setEnabled(text == folder))

    def delete(self):
        self.accept()
        self.editor.remove_workspace(self.key)


class TopLayout:
    '''A tab's section list: sections go above its trailing stretch, so they stack from the top.'''

    def __init__(self, layout: QVBoxLayout):
        self.layout = layout

    def addWidget(self, widget: QWidget):
        self.layout.insertWidget(self.layout.count() - 1, widget)
