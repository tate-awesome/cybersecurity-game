import copy
import ipaddress
import re

from PySide6.QtCore import QPointF, QRectF, QStringListModel, Qt, QTimer, Signal
from PySide6.QtGui import QColor, QFontMetrics, QPainter, QPen
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QCompleter, QFrame, QGridLayout, QHBoxLayout, QLabel,
                               QPlainTextEdit, QPushButton, QScrollArea, QVBoxLayout, QWidget)

from .....app_core import Context
from .....network.buffer.packet_filter import (BY_NAME, FIELDS, FilterError, conjugate, empty_state, parse,
                                                to_state)
from ...overlay import Overlay

# A box's states, in the order a click steps through them (see CycleBox)
NEUTRAL, INCLUDE, EXCLUDE, HIDDEN = "neutral", "include", "exclude", "hidden"
# Host addresses that mean "everyone", always offered in the host comboboxes
SPECIAL_ADDRESSES = ("ff:ff:ff:ff:ff:ff", "255.255.255.255", "0.0.0.0")
# How wide a host or register combobox is, in average characters
COMBO_WIDTH_CHARS = 22
# How long typing in the filter text waits for a pause before reading it
TYPING_PAUSE_MS = 300
# A field with more options than this splits them into columns, by section
OPTIONS_PER_COLUMN = {"type": 8, "meta": 3}
# Room the overlay leaves for everything but its boxes (title, filter text,
# buttons, margins) when capping their height to the screen - see fit
CHROME_HEIGHT = 340


def label_key(field_name: str) -> str:
    return field_name.replace(".", "_")


def value_key(field_name: str, value: str) -> str:
    return f"packet_filter_values_{label_key(field_name)}_{value.replace('-', '_')}"


class CycleBox(QWidget):
    '''
    A checkbox with more than two states, a click stepping through them:
    not filtering (empty), show only these (ticked), hide these (crossed)
    - and, for developers, taken away from students (dashed). A right
    click steps back. Painted here rather than from the icon font for now.
    '''
    changed = Signal(str)

    def __init__(self, context: Context, states: tuple[str, ...], state: str = NEUTRAL):
        super().__init__()
        self.context = context
        self.style = context.style
        self.states = states
        self.state = state if state in states else states[0]
        # Drawn as nothing, and not clickable - see set_blank
        self.blank = False
        side = QFontMetrics(self.style.get_font()).height()
        self.setFixedSize(side, side)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.refresh_tooltip()

    def set_blank(self, blank: bool):
        '''Draws nothing and takes no clicks, but keeps its place - for a combobox row with nothing in it yet.'''
        if blank != self.blank:
            self.blank = blank
            self.setCursor(Qt.CursorShape.ArrowCursor if blank else Qt.CursorShape.PointingHandCursor)
            self.update()

    def set_state(self, state: str):
        self.state = state
        self.refresh_tooltip()
        self.update()

    def step(self, backward: bool = False):
        index = self.states.index(self.state) if self.state in self.states else 0
        self.set_state(self.states[(index + (-1 if backward else 1)) % len(self.states)])
        self.changed.emit(self.state)

    def refresh_tooltip(self):
        self.setToolTip(self.context.labels.get(f"packet_filter_states_{self.state}"))

    def mousePressEvent(self, event):
        if not self.blank and event.button() in (Qt.MouseButton.LeftButton, Qt.MouseButton.RightButton):
            self.step(backward=event.button() == Qt.MouseButton.RightButton)

    @staticmethod
    def ink_pen(color: QColor, width: float) -> QPen:
        pen = QPen(color, max(2.0, width / 8))
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        return pen

    def paintEvent(self, event):
        if self.blank:
            return
        style = self.style
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        box = QRectF(self.rect()).adjusted(2, 2, -2, -2)
        radius = box.width() / 5
        ink = QColor("#ffffff")
        if self.state == INCLUDE:
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor(style.color("accent")))
            painter.drawRoundedRect(box, radius, radius)
            painter.setPen(self.ink_pen(ink, box.width()))
            w, h, x, y = box.width(), box.height(), box.x(), box.y()
            painter.drawPolyline([QPointF(x + w * 0.25, y + h * 0.52), QPointF(x + w * 0.43, y + h * 0.7),
                                  QPointF(x + w * 0.76, y + h * 0.32)])
        elif self.state == EXCLUDE:
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor(style.color("bad")))
            painter.drawRoundedRect(box, radius, radius)
            painter.setPen(self.ink_pen(ink, box.width()))
            inset = box.adjusted(box.width() * 0.3, box.height() * 0.3, -box.width() * 0.3, -box.height() * 0.3)
            painter.drawLine(inset.topLeft(), inset.bottomRight())
            painter.drawLine(inset.topRight(), inset.bottomLeft())
        elif self.state == HIDDEN:
            pen = QPen(QColor(style.color("muted_text")), 1.5, Qt.PenStyle.DashLine)
            painter.setPen(pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRoundedRect(box, radius, radius)
            painter.drawLine(box.bottomLeft(), box.topRight())
        else:
            painter.setPen(QPen(QColor(style.color("muted_text")), 1.5))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRoundedRect(box, radius, radius)
        painter.end()


class CycleOption(QWidget):
    '''A CycleBox and its label, which a click anywhere on steps through (see CycleBox).'''

    def __init__(self, context: Context, text: str, states: tuple[str, ...], state: str = NEUTRAL):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(context.style.cgap * 3)
        self.box = CycleBox(context, states, state)
        layout.addWidget(self.box)
        self.label = QLabel(text)
        self.label.setFont(context.style.get_font())
        layout.addWidget(self.label)
        layout.addStretch(1)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.refresh_look()
        self.box.changed.connect(lambda state: self.refresh_look())

    def mousePressEvent(self, event):
        if event.button() in (Qt.MouseButton.LeftButton, Qt.MouseButton.RightButton):
            self.box.step(backward=event.button() == Qt.MouseButton.RightButton)

    def refresh_look(self):
        '''Labels of options taken away from students (developers only see them) are muted.'''
        self.box.context.style.set_tone(self.label, "muted" if self.box.state == HIDDEN else None)


class ComboColumn(QWidget):
    '''
    A column of editable comboboxes, each with a CycleBox in front: filling
    in the last one adds an empty one under it, so a field can take as many
    values as it needs. Emptied ones (but the last) go away once left.
    Typed text matches as-is; a picked option's value is its text, or for
    "Speed (hreg_3)" the register in the parentheses.
    '''
    changed = Signal()

    def __init__(self, context: Context, options: list[str], placeholder: str, on_resize):
        super().__init__()
        self.context = context
        self.style = context.style
        self.options = options
        self.placeholder = placeholder
        self.on_resize = on_resize
        self.rows: list[tuple[CycleBox, QComboBox, QWidget]] = []
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.layout_ = QVBoxLayout(self)
        self.layout_.setContentsMargins(0, 0, 0, 0)
        self.layout_.setSpacing(self.style.cgap * 2)
        self.width = QFontMetrics(self.style.get_font()).averageCharWidth() * COMBO_WIDTH_CHARS
        self.add_row()

    @staticmethod
    def value_of(text: str) -> str:
        text = text.strip()
        register = re.search(r"\((hreg_\d+)\)\s*$", text)
        return register.group(1) if register else text

    def text_for(self, value: str) -> str:
        '''The option showing value - "Speed (hreg_3)" for hreg_3 - or value itself.'''
        return next((option for option in self.options if self.value_of(option) == value), value)

    def add_row(self, text: str = "", state: str = INCLUDE):
        # Parented from the start: showing a part of a parentless widget makes
        # it a window of its own, and a new window closes the overlay (a popup)
        row = QWidget(self)
        layout = QHBoxLayout(row)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(self.style.cgap * 3)
        box = CycleBox(self.context, (INCLUDE, EXCLUDE, NEUTRAL), state)
        # Blank on an empty row, which filters nothing - keeping its place, so the rows line up
        box.set_blank(not text.strip())
        layout.addWidget(box)
        combo = QComboBox()
        combo.setEditable(True)
        combo.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        combo.setFont(self.style.get_font())
        combo.setFixedWidth(self.width)
        combo.addItems(self.options)
        combo.lineEdit().setPlaceholderText(self.placeholder)
        # Suggestions containing what's typed anywhere, in a list - not filled in as you type
        completer = QCompleter(QStringListModel(self.options), combo)
        completer.setFilterMode(Qt.MatchFlag.MatchContains)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        combo.setCompleter(completer)
        combo.setCurrentIndex(-1)
        combo.setEditText(text)
        layout.addWidget(combo)
        self.layout_.addWidget(row)
        entry = (box, combo, row)
        self.rows.append(entry)
        box.changed.connect(lambda state: self.changed.emit())
        combo.lineEdit().textEdited.connect(lambda text, entry=entry: self.edited(entry))
        combo.activated.connect(lambda index, entry=entry: self.edited(entry))
        combo.lineEdit().editingFinished.connect(lambda entry=entry: self.tidy(entry))
        return entry

    def edited(self, entry):
        entry[0].set_blank(not entry[1].currentText().strip())
        # Filling in the last row opens a new one under it
        if entry is self.rows[-1] and entry[1].currentText().strip():
            self.add_row()
            self.on_resize()
        self.changed.emit()

    def tidy(self, entry):
        if entry in self.rows and entry is not self.rows[-1] and not entry[1].currentText().strip():
            self.rows.remove(entry)
            entry[2].deleteLater()
            QTimer.singleShot(0, self, self.on_resize)

    def values(self) -> tuple[list[str], list[str]]:
        '''The (included, excluded) values - rows left empty or set to not filter aren't either.'''
        include, exclude = [], []
        for box, combo, _ in self.rows:
            value = self.value_of(combo.currentText())
            if value and box.state in (INCLUDE, EXCLUDE):
                (include if box.state == INCLUDE else exclude).append(value)
        return include, exclude

    def set_values(self, include: list[str], exclude: list[str]):
        if self.values() == (include, exclude):
            return  # already showing them - and the row being typed in stays put
        focused = QApplication.focusWidget()
        if focused is not None and self.isAncestorOf(focused):
            # A deleted widget's focus would fall back to the main window, closing the overlay
            self.setFocus()
        for _, _, row in self.rows:
            row.deleteLater()
        self.rows = []
        for value in include:
            self.add_row(self.text_for(value), INCLUDE)
        for value in exclude:
            self.add_row(self.text_for(value), EXCLUDE)
        self.add_row()


class FilterOverlay:
    '''
    Binds a button to open and close the packet filter editor: checkboxes
    and comboboxes by section (see packet_filter.FIELDS), above the filter
    as text. Changing a box writes the text (see packet_filter.conjugate);
    pasting or typing a filter ticks the boxes to match (to_state) - or, for
    one they can't show, sets them aside until it's cleared. Either way the
    text is saved to packet_console "filter", which the packet console
    follows.

    A box steps through not filtering, show only these and hide these.
    In developer mode it has a fourth step, taking the option away from
    students, and each section and field has a checkbox for the same
    (packet_filter_available) - what's taken away isn't built for them.
    '''

    def __init__(self, button: QPushButton, context: Context):
        self.context = context
        self.style = context.style
        self.labels = context.labels
        self.loading = False
        self.state = empty_state()
        self.options: dict[str, dict[str, CycleOption]] = {}
        self.combos: dict[str, ComboColumn] = {}
        self.overlay = Overlay(context.root, context, button, self.populate_overlay)

    # Settings
    def text(self) -> str:
        return str(self.context.states.get("packet_console").get("filter") or "")

    def save(self, text: str):
        self.context.states.get("packet_console")["filter"] = text

    def available(self, key: str) -> bool:
        return self.context.states.get("packet_filter_available").get(key, 1) not in (0, "0")

    def set_available(self, key: str, available: bool):
        settings = self.context.states.get("packet_filter_available")
        if available:
            settings.pop(key, None)
        else:
            settings[key] = 0

    def shown(self, key: str) -> bool:
        '''Whether to build this section/field/option: always for developers, otherwise if students get it.'''
        return self.developer or self.available(key)

    # Building
    def populate_overlay(self, overlay: Overlay):
        style = self.style
        self.developer = self.context.preferences.is_developer()
        self.options, self.combos, self.availability = {}, {}, []
        gap = style.cgap * 2

        frame = QFrame()
        # Part of the overlay's background - follows the "overlay" surface, not "widget"
        style.set_material(frame, "overlay_card")
        column = QVBoxLayout(frame)
        column.setContentsMargins(style.igap, style.igap, style.igap, style.igap)
        column.setSpacing(gap * 2)
        overlay.layout().addWidget(frame)

        title = QLabel(self.labels.get("packet_filter_overlay_title"))
        title.setFont(style.get_font())
        column.addWidget(title)
        column.addWidget(self.muted(self.labels.get("packet_filter_overlay_hint"), wrap=True))

        # The boxes scroll if they'd make the overlay taller than the screen (see fit)
        self.boxes = QWidget()
        style.set_material(self.boxes, "none")
        boxes = QVBoxLayout(self.boxes)
        boxes.setContentsMargins(0, 0, 0, 0)
        boxes.setSpacing(style.igap)
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setStyleSheet("QScrollArea { background-color: transparent; border: none; }")
        self.scroll.setWidget(self.boxes)
        column.addWidget(self.scroll)
        sections = {name: self.section(name) for name in ("hosts", "type", "modbus", "meta")}
        if sections["hosts"]:
            boxes.addWidget(sections["hosts"])
        # Type over Meta, beside ModBus
        lower = QHBoxLayout()
        lower.setSpacing(style.igap)
        boxes.addLayout(lower)
        for names in (("type", "meta"), ("modbus",)):
            stack = QVBoxLayout()
            stack.setSpacing(style.igap)
            for name in names:
                if sections[name]:
                    stack.addWidget(sections[name])
            stack.addStretch(1)
            lower.addLayout(stack)
        lower.addStretch(1)
        boxes.addStretch(1)

        column.addWidget(self.muted(self.labels.get("packet_filter_overlay_text")))
        self.editor = QPlainTextEdit()
        self.editor.setFont(style.get_font("mono"))
        self.editor.setFixedHeight(QFontMetrics(style.get_font("mono")).lineSpacing() * 2 + style.igap * 2)
        self.editor.setPlainText(self.text())
        column.addWidget(self.editor)
        self.typing = QTimer(self.editor)
        self.typing.setSingleShot(True)
        self.typing.setInterval(TYPING_PAUSE_MS)
        self.typing.timeout.connect(self.read_text)
        self.editor.textChanged.connect(lambda: None if self.loading else self.typing.start())

        footer = QHBoxLayout()
        self.status = self.muted("", wrap=True)
        footer.addWidget(self.status, 1)
        copy = QPushButton(self.labels.get("packet_filter_overlay_copy"))
        copy.setFont(style.get_font())
        copy.clicked.connect(lambda checked=False: self.copy(copy))
        footer.addWidget(copy)
        clear = QPushButton(self.labels.get("packet_filter_overlay_clear"))
        clear.setFont(style.get_font())
        clear.clicked.connect(lambda checked=False: self.editor.setPlainText(""))
        footer.addWidget(clear)
        column.addLayout(footer)

        self.read_text(save=False)
        self.fit()

    def muted(self, text: str, wrap: bool = False) -> QLabel:
        label = QLabel(text)
        label.setFont(self.style.get_font("small"))
        label.setWordWrap(wrap)
        self.style.set_tone(label, "muted")
        return label

    def heading(self, text: str, key: str, tooltip: str | None = None) -> QWidget:
        '''A section's or field's name - for developers, a checkbox for whether students get it.'''
        if not self.developer:
            label = self.muted(text)
            if tooltip:
                label.setToolTip(tooltip)
            return label
        checkbox = QCheckBox(text)
        checkbox.setFont(self.style.get_font("small"))
        checkbox.setChecked(self.available(key))
        checkbox.setToolTip(f"{tooltip}\n\n{self.labels.get('packet_filter_overlay_available_tooltip')}" if tooltip
                            else self.labels.get("packet_filter_overlay_available_tooltip"))
        checkbox.toggled.connect(lambda checked, key=key: self.set_available(key, checked))
        return checkbox

    def card(self, name: str) -> tuple[QFrame, QVBoxLayout]:
        card = QFrame()
        self.style.set_material(card, "card", rounded=True, outlined=True)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(self.style.igap, self.style.igap, self.style.igap, self.style.igap)
        layout.setSpacing(self.style.cgap * 3)
        layout.addWidget(self.heading(self.labels.get(f"packet_filter_sections_{name}"), f"section.{name}"))
        return card, layout

    def section(self, name: str) -> QFrame | None:
        if not self.shown(f"section.{name}"):
            return None
        fields = [field for field in FIELDS if field.section == name and self.shown(field.name)]
        if not fields:
            return None
        card, layout = self.card(name)
        if name == "modbus":
            # Two wide: each field's name, then its options two to a row
            grid = QGridLayout()
            grid.setHorizontalSpacing(self.style.igap)
            grid.setVerticalSpacing(self.style.cgap * 3)
            row = 0
            for field in fields:
                if field.kind == "check" and len(field.values) == 1:
                    # Its one option says it all ("Is ModBus") - in place of a heading
                    for option in self.field_options(field):
                        grid.addWidget(option, row, 0, 1, 3)
                    if self.developer:
                        grid.addWidget(self.heading(self.labels.get(f"packet_filter_fields_{label_key(field.name)}"),
                                                    field.name), row + 1, 0, 1, 3)
                        row += 1
                    row += 1
                    continue
                grid.addWidget(self.field_heading(field), row, 0, Qt.AlignmentFlag.AlignTop)
                if field.kind == "combo":
                    grid.addWidget(self.combo_column(field), row, 1, 1, 2)
                    row += 1
                    continue
                for i, option in enumerate(self.field_options(field)):
                    grid.addWidget(option, row + i // 2, 1 + i % 2)
                row += max(1, (len(self.field_options(field)) + 1) // 2)
            layout.addLayout(grid)
            return card
        # Every other section: a column per field, side by side
        row = QHBoxLayout()
        row.setSpacing(self.style.igap * 2)
        for field in fields:
            field_column = QVBoxLayout()
            field_column.setSpacing(self.style.cgap * 3)
            if not (field.kind == "check" and len(field.values) == 1):
                field_column.addWidget(self.field_heading(field))
            if field.kind == "combo":
                field_column.addWidget(self.combo_column(field))
            else:
                options = self.field_options(field)
                columns = QHBoxLayout()
                columns.setSpacing(self.style.igap * 2)
                per_column = OPTIONS_PER_COLUMN.get(name, len(options)) or 1
                for start in range(0, len(options), per_column):
                    stack = QVBoxLayout()
                    stack.setSpacing(self.style.cgap * 3)
                    for option in options[start:start + per_column]:
                        stack.addWidget(option)
                    stack.addStretch(1)
                    columns.addLayout(stack)
                field_column.addLayout(columns)
                if len(field.values) == 1 and self.developer:
                    # A one-option field's option is its heading - its checkbox goes under it
                    field_column.addWidget(self.heading(self.labels.get(f"packet_filter_fields_{label_key(field.name)}"),
                                                        field.name))
            field_column.addStretch(1)
            row.addLayout(field_column)
        row.addStretch(1)
        layout.addLayout(row)
        return card

    def field_heading(self, field) -> QWidget:
        return self.heading(self.labels.get(f"packet_filter_fields_{label_key(field.name)}"), field.name,
                            self.labels.get(f"packet_filter_tips_{label_key(field.name)}"))

    def field_options(self, field) -> list[CycleOption]:
        '''A check field's options (made once, then reused), skipping any students don't get.'''
        if field.name not in self.options:
            states = (NEUTRAL, INCLUDE, EXCLUDE, HIDDEN) if self.developer else (NEUTRAL, INCLUDE, EXCLUDE)
            made = {}
            for value in field.values:
                key = f"{field.name}:{value}"
                if not self.shown(key):
                    continue
                option = CycleOption(self.context, self.labels.get(value_key(field.name, value)), states,
                                     NEUTRAL if self.available(key) else HIDDEN)
                if len(field.values) == 1:
                    option.setToolTip(self.labels.get(f"packet_filter_tips_{label_key(field.name)}"))
                option.box.changed.connect(lambda state, field=field.name, value=value: self.option_changed(field, value, state))
                made[value] = option
            self.options[field.name] = made
        return list(self.options[field.name].values())

    def combo_column(self, field) -> ComboColumn:
        if field.name == "modbus.reg":
            options, placeholder = self.register_options(), self.labels.get("packet_filter_overlay_register_placeholder")
        else:
            options, placeholder = self.host_options(), self.labels.get("packet_filter_overlay_host_placeholder")
        combos = ComboColumn(self.context, options, placeholder, lambda: QTimer.singleShot(0, self.overlay, self.fit))
        combos.setToolTip(self.labels.get(f"packet_filter_tips_{label_key(field.name)}"))
        combos.changed.connect(self.boxes_changed)
        self.combos[field.name] = combos
        return combos

    def host_options(self) -> list[str]:
        '''Every host seen: nicknames, then IP addresses, MAC addresses, and the addresses that mean everyone.'''
        ips, macs = set(), set()
        packets = self.context.buffer.packets
        with packets.lock:
            seen = list(packets.buffer)
        for mpkt in seen:
            for side in ("src", "dst"):
                ip, mac = mpkt.get(f"ip_{side}"), mpkt.get(f"mac_{side}")
                if ip and ip != "-":
                    ips.add(ip)
                if mac and mac != "-":
                    macs.add(mac.lower())
        nicknames = set()
        for mac, entry in self.context.states.get("network_hosts").items():
            if isinstance(entry, dict) and "nickname" in entry and ":" in mac:
                macs.add(mac.lower())
                if entry.get("nickname"):
                    nicknames.add(entry["nickname"])

        def ip_order(ip: str):
            try:
                address = ipaddress.ip_address(ip)
                return (address.version, int(address))
            except ValueError:
                return (9, 0)
        specials = [address for address in SPECIAL_ADDRESSES]
        return (sorted(nicknames, key=str.lower) + sorted(ips - set(specials), key=ip_order)
                + sorted(macs - set(specials)) + specials)

    def register_options(self) -> list[str]:
        registers = self.context.states.get("modbus_registers")

        def number(key: str) -> int:
            return int(key.split("_")[1]) if key.split("_")[-1].isdigit() else 0
        options = []
        for key in sorted((key for key in registers if key.startswith("hreg_")), key=number):
            nickname = str((registers.get(key) or {}).get("nickname") or "").strip()
            options.append(f"{nickname} ({key})" if nickname else key)
        return options

    # Boxes -> text
    def option_changed(self, field: str, value: str, state: str):
        if self.loading:
            return
        self.set_available(f"{field}:{value}", state != HIDDEN)
        self.boxes_changed()

    def boxes_changed(self):
        if self.loading:
            return
        state = copy.deepcopy(self.state)
        for field, options in self.options.items():
            for value, option in options.items():
                for side in ("include", "exclude"):
                    if value in state[field][side]:
                        state[field][side].remove(value)
                if option.box.state in (INCLUDE, EXCLUDE):
                    state[field][option.box.state].append(value)
            # Keep the field's own order, not the order they were ticked in
            order = BY_NAME[field].values
            for side in ("include", "exclude"):
                state[field][side].sort(key=lambda value: order.index(value) if value in order else len(order))
        for field, combos in self.combos.items():
            state[field]["include"], state[field]["exclude"] = combos.values()
        self.state = state
        text = conjugate(state)
        self.loading = True
        self.editor.setPlainText(text)
        self.loading = False
        self.save(text)
        self.show_status(None)

    # Text -> boxes
    def read_text(self, save: bool = True):
        '''Reads the filter text: saves it if it can be read, and ticks the boxes to match - or sets them aside.'''
        text = self.editor.toPlainText().strip()
        try:
            tree = parse(text)
        except FilterError as error:
            self.show_status(self.labels.get("packet_filter_overlay_error").replace("{error}", str(error)), bad=True)
            return
        if save:
            self.save(text)
        state = to_state(tree)
        self.boxes.setEnabled(state is not None)
        if state is None:
            self.show_status(self.labels.get("packet_filter_overlay_custom"))
            return
        self.state = state
        self.show_status(None)
        self.loading = True
        for field, options in self.options.items():
            for value, option in options.items():
                if option.box.state == HIDDEN:
                    continue
                option.box.set_state(INCLUDE if value in state[field]["include"]
                                     else EXCLUDE if value in state[field]["exclude"] else NEUTRAL)
                option.refresh_look()
        for field, combos in self.combos.items():
            combos.set_values(state[field]["include"], state[field]["exclude"])
        self.loading = False
        QTimer.singleShot(0, self.overlay, self.fit)

    def fit(self):
        '''
        Sizes the boxes' scroll area to the boxes - but no taller than the
        screen leaves room for - then the overlay to its contents.
        '''
        try:
            hint = self.boxes.sizeHint()
        except RuntimeError:
            return  # closed meanwhile
        screen = self.overlay.screen().availableGeometry().height()
        height = min(hint.height(), max(200, screen - CHROME_HEIGHT))
        scrollbar = self.scroll.verticalScrollBar().sizeHint().width() if height < hint.height() else 0
        self.scroll.setFixedSize(hint.width() + scrollbar, height)
        self.overlay.adjustSize()

    def show_status(self, text: str | None, bad: bool = False):
        self.status.setText(text or "")
        self.style.set_tone(self.status, "bad" if bad else "muted")

    def copy(self, button: QPushButton):
        QApplication.clipboard().setText(self.editor.toPlainText().strip())
        button.setText(self.labels.get("packet_filter_overlay_copied"))
        QTimer.singleShot(1200, button, lambda: button.setText(self.labels.get("packet_filter_overlay_copy")))
