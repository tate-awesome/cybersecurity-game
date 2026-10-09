from PySide6.QtCore import Qt
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import QCheckBox, QComboBox, QFrame, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSlider, QWidget
from collections.abc import Callable
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
        # Part of the overlay's background - follows the "overlay" surface, not "widget"
        self.setStyleSheet(self.style.themed(f"background-color: {self.style.surface('overlay', 'widget')};", self))
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

    def button(self, text: str, function: Callable, tooltip: str | None = None) -> QPushButton:
        '''A full-width button that runs function - for choices applied in one click.'''
        button = QPushButton(text)
        button.setFont(self.style.get_font())
        if tooltip:
            button.setToolTip(tooltip)
        button.clicked.connect(lambda checked=False: function())
        self.grid.addWidget(button, self.row, 0, 1, 2)
        self.row += 1
        return button

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

    def toggle(self, path: StatePath, checked: bool, changed: Callable[[bool], None]) -> QCheckBox:
        '''
        A checkbox for a setting that isn't in context.states (e.g. a style
        preference) - path only names its label/tooltip.
        '''
        checkbox = QCheckBox()
        # Load before connecting, so restoring it doesn't itself trigger a save
        checkbox.setChecked(checked)
        checkbox.toggled.connect(changed)
        self.add_row(path, checkbox)
        return checkbox

    def choice(self, path: StatePath, options: dict[str, str], current: str, changed: Callable[[str], None]) -> QComboBox:
        '''
        A fixed choice (stored value -> shown text) for a setting that isn't
        in context.states (e.g. a style preference) - path only names its
        label/tooltip. changed gets the stored value.
        '''
        values = list(options)
        if current not in options:
            values.append(current)
        combobox = QComboBox()
        combobox.addItems([options.get(value, str(value)) for value in values])
        combobox.setCurrentIndex(values.index(current))
        combobox.currentIndexChanged.connect(lambda index: changed(values[index]))
        self.add_row(path, combobox)
        return combobox

    def integer(self, path: StatePath, value: int, minimum: int, maximum: int, changed: Callable[[int], None]) -> QLineEdit:
        '''
        A text entry for a whole number in [minimum, maximum], for a setting
        that isn't in context.states - path only names its label/tooltip.
        Anything else is undone when editing finishes.
        '''
        entry = QLineEdit(str(value))
        entry.setValidator(QIntValidator(minimum, maximum, entry))
        current = [value]

        def save():
            try:
                new_value = int(entry.text())
            except ValueError:
                new_value = None
            if new_value is None or not minimum <= new_value <= maximum:
                entry.setText(str(current[0]))
                return
            if new_value != current[0]:
                current[0] = new_value
                changed(new_value)

        entry.editingFinished.connect(save)
        self.add_row(path, entry)
        return entry

    def slider(self, path: StatePath, value: int, minimum: int, maximum: int, changed: Callable[[int], None],
               suffix: str = "") -> QSlider:
        '''
        A slider for a setting that isn't in context.states (e.g. a style
        preference) - path only names its label/tooltip. changed runs on
        every move, so the setting can apply live. The current value is
        shown beside it, followed by suffix.
        '''
        row = QWidget()
        layout = QHBoxLayout(row)
        layout.setContentsMargins(0, 0, 0, 0)
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(minimum, maximum)
        slider.setValue(value)
        slider.setMinimumWidth(160)
        readout = QLabel(f"{value}{suffix}")
        readout.setFont(self.style.get_font())
        # Wide enough for the longest value, so the slider doesn't shift as it changes
        readout.setMinimumWidth(readout.fontMetrics().horizontalAdvance(f"{maximum}{suffix}") + 4)
        readout.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(slider, 1)
        layout.addWidget(readout)

        def on_change(new_value: int):
            readout.setText(f"{new_value}{suffix}")
            changed(new_value)

        slider.valueChanged.connect(on_change)
        self.add_row(path, row)
        return slider

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
