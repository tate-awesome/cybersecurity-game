import copy
import inspect
import json
import re
from typing import Any, Callable

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QCheckBox, QComboBox, QDialog, QFrame, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
                               QPlainTextEdit, QScrollArea, QVBoxLayout, QWidget)

from ...app_core import Context
from ...pages.page import Page
from ...widgets import MenuBar, PANELS, popup

# The standard left-to-right order for menu bar buttons (see MenuBar.page_buttons)
BUTTON_ORDER = [
    "toggle_button", "theme_button", "labels_button", "page_button",
    "pcap_button", "save_button", "load_button", "stream_button", "preset_button", "data_button",
    "delete_all_workspace_data_button", "refresh_button", "reset_button", "help_button",
    "back_button", "quit_button",
]

# Qt's "no maximum" widget size (QWIDGETSIZE_MAX, which PySide6 doesn't export)
QWIDGETSIZE_MAX = (1 << 24) - 1

# Numeric fields that are real numbers, not 0/1 on-off switches
NUMBER_FIELDS = {"factor", "multiplier", "offset", "strip_chart_auto_fit_max_seconds"}


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


def set_path(data: dict, path: tuple, value):
    for key in path[:-1]:
        data = data[key]
    data[path[-1]] = value


class ConfigEditor(Page):
    '''
    Demo page for editing workspace configs with a form instead of raw
    JSON. The menu bar dropdown picks a workspace; the form below shows:

      - its own fields (name, section, order, description, ...)
      - its menu bar buttons, as checkboxes (saved in the standard order)
      - its pane layout's weights (the layout itself can't be changed here)
      - every field in _default.json, holding the workspace's current value

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

    def __init__(self, context: Context):
        super().__init__(context)
        self.labels = context.labels
        self.pages = context.pages
        self.json = context.json
        self.default_settings = context.states.get_default()
        self.notes = context.json.load(context.paths.packages / self.NOTES_FILE)
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
        menu_bar.toggle_button()
        menu_bar.theme_button()
        menu_bar.labels_button()
        menu_bar.page_button()
        menu_bar.back_button()
        menu_bar.quit_button()

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet(self.style.themed("QScrollArea { background-color: transparent; border: none; }"))
        self.layout().addWidget(self.scroll, 1)
        self.status = QLabel()
        self.status.setFont(self.style.get_font("default"))
        self.status.setWordWrap(True)
        self.layout().addWidget(self.status)

        self.load(ConfigEditor.selected_key)

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
        self.setting_readers: list[tuple[tuple, Callable[[], Any]]] = []
        self.weight_readers: list[tuple[tuple, Callable[[], Any]]] = []
        self.button_boxes: dict[str, QCheckBox] = {}
        self.prerequisite_boxes: dict[str, QCheckBox] = {}

        body = QWidget()
        self.form = QVBoxLayout(body)
        self.form.setSpacing(self.style.igap)
        self.form.setContentsMargins(0, 0, self.style.igap, 0)
        self.scroll.setWidget(body)

        if key is None:
            self.set_status("No workspaces found.", "field_text")
            return
        try:
            self.config = json.loads(self.pages.config_paths[key].read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            self.config = None
            self.set_status(f"This workspace's config.json isn't valid JSON (line {error.lineno}): {error.msg}", "red")
            return

        self.build_workspace_section()
        self.build_menu_bar_section()
        self.build_panes_section()
        settings = copy.deepcopy(self.default_settings)
        self.json.deep_merge(settings, self.config.get("settings", {}))
        for name, default in self.default_settings.items():
            self.build_setting_section(name, default, settings[name])
        self.form.addStretch(1)
        self.set_status(f"Editing {self.pages.config_paths[key]}", "field_text")

    # Form building - one value per row: its name on the left, its input on the right
    def section(self, title: str, explanation: str | None) -> "Rows":
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
        grid = QGridLayout()
        grid.setHorizontalSpacing(self.style.igap * 2)
        grid.setColumnStretch(1, 1)
        # Same label column width in every section, so inputs line up down the page
        grid.setColumnMinimumWidth(0, self.LABEL_WIDTH)
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

        note = self.config.get("_note", "")
        note_text = "\n\n".join(note) if isinstance(note, list) else str(note)
        editor, note_reader = self.text_area(note_text, rows=14)
        def read_note():
            # Unedited: keep the original blocks, even ones with blank lines inside them
            if note_reader() == note_text:
                return note
            return [block.strip() for block in note_reader().split("\n\n") if block.strip()]
        add("_note", editor, read_note)
        editor, reader = self.text_area(str(self.config.get("_dev_note", "")), rows=3)
        add("_dev_note", editor, reader)

    def build_menu_bar_section(self):
        rows = self.section("menu_bar", self.workspace_note("menu_bar") + " Checked buttons appear in the order listed here.")
        chosen = set(self.config.get("menu_bar", []))
        for name in menu_bar_buttons():
            box, _ = self.checkbox(name in chosen, as_bool=True)
            rows.add(name, box)
            self.button_boxes[name] = box

    def build_panes_section(self):
        rows = self.section("panes", self.workspace_note("panes") + " Only the weights can be changed here.")
        def add_group(group: dict, path: tuple, depth: int):
            name = path[-1]
            kind = "side by side" if name.startswith("h_panes") else "stacked"
            entry, reader = self.number_entry("weight", group.get("weight", 1))
            rows.add(f"{name} ({kind})", entry, depth=depth)
            self.weight_readers.append((path + ("weight",), reader))
            for key, value in group.items():
                if key == "weight" or key.startswith("_"):
                    continue
                if self.pages.pane_group(key) and isinstance(value, dict):
                    add_group(value, path + (key,), depth + 1)
                else:
                    entry, reader = self.number_entry(key, value)
                    rows.add(key, entry, depth=depth + 1)
                    self.weight_readers.append((path + (key,), reader))
        for key, group in self.config.get("panes", {}).items():
            if self.pages.pane_group(key) and isinstance(group, dict):
                add_group(group, (key,), 0)

    def build_setting_section(self, name: str, default, value):
        explanation = self.notes.get("settings_fields", {}).get(name, "No explanation yet - add one to _default_notes.json.")
        rows = self.section(name, explanation)
        if isinstance(default, dict):
            self.add_setting_rows(rows, (name,), default, value, depth=0)
        else:
            widget, reader = self.leaf(name, default, value)
            rows.add(name, widget)
            self.setting_readers.append(((name,), reader))

    def add_setting_rows(self, rows: "Rows", path: tuple, default: dict, value: dict, depth: int):
        for key, item_default in default.items():
            if isinstance(item_default, dict):
                rows.heading(key, depth=depth)
                self.add_setting_rows(rows, path + (key,), item_default, value[key], depth + 1)
            else:
                widget, reader = self.leaf(key, item_default, value[key])
                rows.add(key, widget, depth=depth)
                self.setting_readers.append((path + (key,), reader))

    # Widgets, each paired with a reader that turns it back into a config value
    def leaf(self, key: str, default, value) -> tuple[QWidget, Callable[[], Any]]:
        if is_switch(key, default):
            return self.checkbox(value, as_bool=isinstance(default, bool))
        if isinstance(default, (int, float)):
            return self.number_entry(key, value, integer=isinstance(default, int))
        if isinstance(default, list):
            entry, reader = self.text_entry(", ".join(str(item) for item in value))
            entry.setToolTip("Separate items with commas")
            return entry, lambda: [item.strip() for item in reader().split(",")]
        return self.text_entry(str(value))

    def checkbox(self, value, as_bool: bool, text: str = "") -> tuple[QCheckBox, Callable[[], Any]]:
        box = QCheckBox(text)
        box.setFont(self.style.get_font("default"))
        box.setChecked(value in (1, "1", True))
        box.toggled.connect(self.mark_dirty)
        if as_bool:
            return box, box.isChecked
        return box, lambda: 1 if box.isChecked() else 0

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
                raise ValueError(f'"{name}" must be a number, not "{text()}"')
            if integer:
                if number != int(number):
                    raise ValueError(f'"{name}" must be a whole number, not "{text()}"')
                return int(number)
            return int(number) if number == int(number) and "." not in text() else number
        return entry, read

    def text_area(self, text: str, rows: int) -> tuple[QPlainTextEdit, Callable[[], str]]:
        editor = QPlainTextEdit(text)
        editor.setFont(self.style.get_font("default"))
        editor.setFixedHeight(self.fontMetrics().lineSpacing() * rows + 16)
        editor.textChanged.connect(self.mark_dirty)
        return editor, editor.toPlainText

    # Saving
    def mark_dirty(self, *_):
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

        settings = copy.deepcopy(self.default_settings)
        for path, reader in self.setting_readers:
            value, failed = read(reader)
            if not failed:
                set_path(settings, path, value)
        config["settings"] = self.json.diff(self.default_settings, settings)

        config["menu_bar"] = [name for name, box in self.button_boxes.items() if box.isChecked()]

        for path, reader in self.weight_readers:
            value, failed = read(reader)
            if not failed:
                if value <= 0:
                    errors.append(f'"{path[-1]}" weight must be above 0')
                set_path(config["panes"], path, value)
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

    def heading(self, text: str, depth: int = 0, tooltip: str = ""):
        self.grid.addWidget(self.label(text, depth, tooltip), self.row, 0)
        self.row += 1

    def add(self, text: str, widget: QWidget, depth: int = 0, tooltip: str = ""):
        self.grid.addWidget(self.label(text, depth, tooltip), self.row, 0, Qt.AlignmentFlag.AlignTop)
        # Inputs narrower than the column (checkboxes, number boxes) sit at its left edge instead of centered
        fills = not isinstance(widget, QCheckBox) and widget.maximumWidth() >= QWIDGETSIZE_MAX
        self.grid.addWidget(widget, self.row, 1, Qt.AlignmentFlag(0) if fills else Qt.AlignmentFlag.AlignLeft)
        self.row += 1


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
