from PySide6.QtCore import Qt
from PySide6.QtWidgets import QCheckBox, QComboBox, QFrame, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QWidget
from .....app_core import Context
from .....app_core.context.style import Style
from ...overlay import Overlay
from .._base_button import ImportantButton

# A path into context.states: setting keys, optionally ending in a list index
# (e.g. ("strip_chart_colors", "paths", 2))
StatePath = tuple[str | int, ...]


def is_checked(value) -> bool:
    return value in (1, "1", True)


def checked_value(old, checked: bool):
    '''A checkbox state in the same type the setting already uses ("1"/"0" or 1/0), so saves only differ when the value does.'''
    if isinstance(old, str):
        return "1" if checked else "0"
    return 1 if checked else 0


class SettingsSection(QFrame):
    '''
    One titled column of rows in a SettingsOverlayButton's overlay. Each row
    is a label plus an editor that writes straight to context.states - the
    widgets using that setting read it from there.

    Labels and tooltips come from "settings_labels_<path>" and
    "settings_tooltips_<path>" (the path's keys joined by "_", list indexes
    left out - a list item's label gets its 1-based number appended).
    '''

    def __init__(self, context: Context, title: str):
        super().__init__()
        self.context = context
        self.style = context.style
        self.setStyleSheet(self.style.themed(f"background-color: {self.style.color('widget')};", self))
        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(self.style.igap, self.style.igap, self.style.igap, self.style.igap)
        self.grid.setVerticalSpacing(self.style.cgap * 2)
        self.grid.setHorizontalSpacing(self.style.igap)

        header = QLabel(self.context.labels.get(f"settings_labels_{title}"))
        header.setFont(self.style.get_font())
        header.setToolTip(self.context.labels.get(f"settings_tooltips_{title}"))
        self.grid.addWidget(header, 0, 0, 1, 2)
        self.row = 1

    # States access
    def get(self, path: StatePath):
        keys = path[:-1] if isinstance(path[-1], int) else path
        value = self.context.states.get(*keys)
        return value[path[-1]] if isinstance(path[-1], int) else value

    def set(self, path: StatePath, value):
        if isinstance(path[-1], int):
            self.context.states.get(*path[:-1])[path[-1]] = value
        else:
            self.context.states.set(*path, value=value)

    # Rows
    def add_row(self, path: StatePath, editor: QWidget):
        keys = "_".join(str(key) for key in path if not isinstance(key, int))
        text = self.context.labels.get(f"settings_labels_{keys}")
        if isinstance(path[-1], int):
            text = f"{text} {path[-1] + 1}"
        label = QLabel(text)
        label.setFont(self.style.get_font())
        tooltip = self.context.labels.get(f"settings_tooltips_{keys}")
        label.setToolTip(tooltip)
        editor.setToolTip(tooltip)
        editor.setFont(self.style.get_font())
        self.grid.addWidget(label, self.row, 0)
        self.grid.addWidget(editor, self.row, 1)
        self.row += 1

    def checkbox(self, *path: str | int) -> QCheckBox:
        checkbox = QCheckBox()
        # Load before connecting, so restoring it doesn't itself trigger a save
        checkbox.setChecked(is_checked(self.get(path)))
        checkbox.toggled.connect(lambda checked: self.set(path, checked_value(self.get(path), checked)))
        self.add_row(path, checkbox)
        return checkbox

    def color(self, *path: str | int) -> QComboBox:
        '''An editable combobox offering the theme's color names (see Style.color) - any color name or hex code can be typed too.'''
        combobox = QComboBox()
        combobox.setEditable(True)
        combobox.addItems(Style.THEME_COLOR_NAMES)
        combobox.setCurrentText(str(self.get(path)))
        combobox.currentTextChanged.connect(lambda text: self.set(path, text))
        self.add_row(path, combobox)
        return combobox

    def dropdown(self, path: StatePath, options: dict[str, str]) -> QComboBox:
        '''A fixed choice between options (stored value -> shown text).'''
        values = list(options)
        current = self.get(path)
        if current not in options:
            values.append(current)
        combobox = QComboBox()
        combobox.addItems([options.get(value, str(value)) for value in values])
        combobox.setCurrentIndex(values.index(current))
        combobox.currentIndexChanged.connect(lambda index: self.set(path, values[index]))
        self.add_row(path, combobox)
        return combobox

    def number(self, *path: str | int) -> QLineEdit:
        '''A text entry for a positive number - anything else is undone when editing finishes.'''
        entry = QLineEdit(str(self.get(path)))

        def save():
            old = self.get(path)
            try:
                value = float(entry.text())
            except ValueError:
                value = 0
            if value <= 0:
                entry.setText(str(old))
                return
            self.set(path, int(value) if isinstance(old, int) and value.is_integer() else value)

        entry.editingFinished.connect(save)
        self.add_row(path, entry)
        return entry


class SettingsOverlayButton(ImportantButton):
    '''
    A button opening an overlay of SettingsSection columns side by side -
    subclasses build them in populate.
    '''

    def __init__(self, context: Context):
        super().__init__(context)
        Overlay(context.root, context, self, self.populate_overlay)

    def populate_overlay(self, overlay: Overlay):
        row = QHBoxLayout()
        row.setSpacing(self.context.style.igap)
        overlay.layout().addLayout(row)
        self.columns = row
        self.populate(overlay)

    def section(self, title: str) -> SettingsSection:
        section = SettingsSection(self.context, title)
        self.columns.addWidget(section, 0, Qt.AlignmentFlag.AlignTop)
        return section

    def populate(self, overlay: Overlay):
        pass
