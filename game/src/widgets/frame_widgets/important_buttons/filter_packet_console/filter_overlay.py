import copy
import ipaddress
import re

from PySide6.QtCore import QEvent, QObject, QPointF, QRectF, QStringListModel, Qt, QTimer, Signal
from PySide6.QtGui import QColor, QFont, QFontMetrics, QPainter, QPen
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QCompleter, QFrame, QGridLayout, QHBoxLayout, QLabel,
                               QPushButton, QScrollArea, QVBoxLayout, QWidget)

from .....app_core import Context
from .....network.buffer.packet_filter import (BY_NAME, FIELDS, FilterError, conjugate, empty_state, join_pair, parse,
                                                quote, split_pair, to_state)
from ....popup import ButtonPopup
from ...text_area import TextArea

# A box's states, in the order a click steps through them (see CycleBox)
NEUTRAL, INCLUDE, EXCLUDE, HIDDEN = "neutral", "include", "exclude", "hidden"
# How wide a host or register combobox is, in average characters - and each of a pair's two
COMBO_WIDTH_CHARS = 16
PAIR_COMBO_WIDTH_CHARS = 12
# How wide the description panel on the right is, in average characters
DESCRIPTION_WIDTH_CHARS = 30
# How long typing in the filter text waits for a pause before reading it
TYPING_PAUSE_MS = 300
# A field with more options than this splits them into columns, by section
OPTIONS_PER_COLUMN = {"type": 8, "meta": 3}
# Room the popup leaves for everything but its boxes (title, filter text,
# buttons, margins and shadow; the description panel beside them) when
# capping their size to the screen - see fit
CHROME_HEIGHT = 400
CHROME_WIDTH = 140


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
    A column of editable comboboxes, each row with a CycleBox in front:
    filling in the last row adds an empty one under it, so a field can take
    as many values as it needs. Emptied rows (but the last) go away once
    left. Typed text matches as-is; a picked option's value is its text, or
    for "Speed (hreg_3)" the register in the parentheses.

    With pair=True each row is two comboboxes side by side, one host each,
    and its value is the two joined ("A<>B" - see packet_filter.join_pair).
    '''
    changed = Signal()

    def __init__(self, context: Context, options: list[str], placeholders: list[str], on_resize, pair: bool = False):
        super().__init__()
        self.context = context
        self.style = context.style
        self.options = options
        self.placeholders = placeholders
        self.on_resize = on_resize
        self.pair = pair
        # Each row: its box, its comboboxes (two for a pair), and the row itself
        self.rows: list[tuple[CycleBox, list[QComboBox], QWidget]] = []
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.layout_ = QVBoxLayout(self)
        self.layout_.setContentsMargins(0, 0, 0, 0)
        self.layout_.setSpacing(self.style.cgap * 2)
        self.width = QFontMetrics(self.style.get_font()).averageCharWidth() * (PAIR_COMBO_WIDTH_CHARS if pair else COMBO_WIDTH_CHARS)
        self.add_row()

    @staticmethod
    def value_of(text: str) -> str:
        text = text.strip()
        register = re.search(r"\((hreg_\d+)\)\s*$", text)
        return register.group(1) if register else text

    def text_for(self, value: str) -> str:
        '''The option showing value - "Speed (hreg_3)" for hreg_3 - or value itself (a pair's, as it is).'''
        if self.pair:
            return value
        return next((option for option in self.options if self.value_of(option) == value), value)

    def combo(self, text: str, placeholder: str) -> QComboBox:
        combo = QComboBox()
        combo.setEditable(True)
        combo.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        combo.setFont(self.style.get_font())
        combo.setFixedWidth(self.width)
        combo.addItems(self.options)
        combo.lineEdit().setPlaceholderText(placeholder)
        # Suggestions containing what's typed anywhere, in a list - not filled in as you type
        completer = QCompleter(QStringListModel(self.options), combo)
        completer.setFilterMode(Qt.MatchFlag.MatchContains)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        combo.setCompleter(completer)
        combo.setCurrentIndex(-1)
        combo.setEditText(text)
        return combo

    def add_row(self, text: str = "", state: str = INCLUDE):
        # Parented from the start: showing a part of a parentless widget makes
        # it a window of its own
        row = QWidget(self)
        layout = QHBoxLayout(row)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(self.style.cgap * 3)
        box = CycleBox(self.context, (INCLUDE, EXCLUDE, NEUTRAL), state)
        layout.addWidget(box)
        texts = list(split_pair(text)) if self.pair else [text]
        combos = []
        for i, part in enumerate(texts):
            if i:
                between = QLabel("\u21c4")
                between.setFont(self.style.get_font())
                self.style.set_tone(between, "muted")
                layout.addWidget(between)
            combo = self.combo(part, self.placeholders[i])
            layout.addWidget(combo)
            combos.append(combo)
        self.layout_.addWidget(row)
        entry = (box, combos, row)
        # Blank on an empty row, which filters nothing - keeping its place, so the rows line up
        box.set_blank(not self.filled(entry))
        self.rows.append(entry)
        box.changed.connect(lambda state: self.changed.emit())
        for combo in combos:
            combo.lineEdit().textEdited.connect(lambda text, entry=entry: self.edited(entry))
            combo.activated.connect(lambda index, entry=entry: self.edited(entry))
            combo.lineEdit().editingFinished.connect(lambda entry=entry: self.tidy(entry))
        return entry

    @staticmethod
    def filled(entry) -> bool:
        return any(combo.currentText().strip() for combo in entry[1])

    def value(self, entry) -> str:
        if self.pair:
            return join_pair(*(combo.currentText() for combo in entry[1])) if self.filled(entry) else ""
        return self.value_of(entry[1][0].currentText())

    def edited(self, entry):
        entry[0].set_blank(not self.filled(entry))
        # Filling in the last row opens a new one under it
        if entry is self.rows[-1] and self.filled(entry):
            self.add_row()
            self.on_resize()
        self.changed.emit()

    def tidy(self, entry):
        if entry in self.rows and entry is not self.rows[-1] and not self.filled(entry):
            focused = QApplication.focusWidget()
            if focused is not None and entry[2].isAncestorOf(focused):
                return  # still moving between its two comboboxes
            self.rows.remove(entry)
            entry[2].deleteLater()
            QTimer.singleShot(0, self, self.on_resize)

    def values(self) -> tuple[list[str], list[str]]:
        '''The (included, excluded) values - rows left empty or set to not filter aren't either.'''
        include, exclude = [], []
        for entry in self.rows:
            value = self.value(entry)
            if value and entry[0].state in (INCLUDE, EXCLUDE):
                (include if entry[0].state == INCLUDE else exclude).append(value)
        return include, exclude

    def set_values(self, include: list[str], exclude: list[str]):
        if self.values() == (include, exclude):
            return  # already showing them - and the row being typed in stays put
        focused = QApplication.focusWidget()
        if focused is not None and self.isAncestorOf(focused):
            # Rather than fall back to wherever, once the focused widget is deleted
            self.setFocus()
        for _, _, row in self.rows:
            row.deleteLater()
        self.rows = []
        for value in include:
            self.add_row(self.text_for(value), INCLUDE)
        for value in exclude:
            self.add_row(self.text_for(value), EXCLUDE)
        self.add_row()


class FilterPopup(QObject):
    '''
    Opens the packet filter editor, in a popup: checkboxes
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

    A panel on the right describes the section, field or option under the
    mouse: what it is, how a packet is checked against it, and how it's
    written in the filter (see describe).
    '''

    def __init__(self, context: Context):
        popup = ButtonPopup(context, context.labels.get("packet_filter_overlay_title"))
        super().__init__(popup)  # goes with the popup
        self.popup = popup
        self.context = context
        self.style = context.style
        self.labels = context.labels
        self.loading = False
        self.state = empty_state()
        self.options: dict[str, dict[str, CycleOption]] = {}
        self.combos: dict[str, ComboColumn] = {}
        self.populate()
        popup.show()

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
    def populate(self):
        style = self.style
        self.developer = self.context.preferences.is_developer()
        self.options, self.combos, self.availability = {}, {}, []
        gap = style.cgap * 2

        column = QVBoxLayout()
        column.setSpacing(gap * 2)
        self.popup.body.addLayout(column)

        # The boxes scroll if they'd make the popup taller than the screen (see fit)
        self.boxes = QWidget()
        style.set_material(self.boxes, "none")
        boxes = QVBoxLayout(self.boxes)
        boxes.setContentsMargins(0, 0, 0, 0)
        boxes.setSpacing(style.igap)
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setStyleSheet("QScrollArea { background-color: transparent; border: none; }")
        self.scroll.setWidget(self.boxes)
        body = QHBoxLayout()
        body.setSpacing(style.igap)
        body.addWidget(self.scroll, 0, Qt.AlignmentFlag.AlignTop)
        body.addWidget(self.build_description())
        column.addLayout(body)
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
        self.editor = TextArea()
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
        paste = QPushButton(self.labels.get("packet_filter_overlay_paste"))
        paste.setFont(style.get_font())
        paste.clicked.connect(lambda checked=False: self.paste())
        footer.addWidget(paste)
        clear = QPushButton(self.labels.get("packet_filter_overlay_clear"))
        clear.setFont(style.get_font())
        clear.clicked.connect(lambda checked=False: self.editor.setPlainText(""))
        footer.addWidget(clear)
        column.addLayout(footer)

        self.read_text(save=False)
        self.describe(None)
        self.fit()

    def muted(self, text: str, wrap: bool = False) -> QLabel:
        label = QLabel(text)
        label.setFont(self.style.get_font("small"))
        label.setWordWrap(wrap)
        self.style.set_tone(label, "muted")
        return label

    def heading(self, text: str, key: str, topic: tuple, section: bool = False) -> QWidget:
        '''
        A section's name (bold, in the text color) or a field's (small and
        muted, like a column header) - for developers, a checkbox for whether
        students get it. Pointing at it describes it (see describe).
        '''
        font = QFont(self.style.get_font())
        font.setBold(True)
        if self.developer:
            widget = QCheckBox(text)
            widget.setChecked(self.available(key))
            widget.setToolTip(self.labels.get("packet_filter_overlay_available_tooltip"))
            widget.toggled.connect(lambda checked, key=key: self.set_available(key, checked))
        else:
            widget = QLabel(text)
        widget.setFont(font if section else self.style.get_font("small"))
        if not section:
            self.style.set_tone(widget, "muted")
        self.watch(widget, topic)
        return widget

    def watch(self, widget: QWidget, topic: tuple):
        '''Describes topic in the panel on the right whenever the mouse comes onto widget.'''
        widget.filter_topic = topic
        widget.installEventFilter(self)

    def eventFilter(self, watched, event):
        if event.type() == QEvent.Type.Enter and hasattr(watched, "filter_topic"):
            self.describe(watched.filter_topic)
        return False

    def card(self, name: str) -> tuple[QFrame, QVBoxLayout]:
        card = QFrame()
        self.style.set_material(card, "card", rounded=True, outlined=True)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(self.style.igap, self.style.igap, self.style.igap, self.style.igap)
        layout.setSpacing(self.style.cgap * 3)
        layout.addWidget(self.heading(self.labels.get(f"packet_filter_sections_{name}"), f"section.{name}", ("section", name),
                                      section=True))
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
                        grid.addWidget(self.field_heading(field), row + 1, 0, 1, 3)
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
                    field_column.addWidget(self.field_heading(field))
            field_column.addStretch(1)
            row.addLayout(field_column)
        row.addStretch(1)
        layout.addLayout(row)
        return card

    def field_heading(self, field) -> QWidget:
        return self.heading(self.labels.get(f"packet_filter_fields_{label_key(field.name)}"), field.name, ("field", field.name, None))

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
                self.watch(option, ("field", field.name, value))
                option.box.changed.connect(lambda state, field=field.name, value=value: self.option_changed(field, value, state))
                made[value] = option
            self.options[field.name] = made
        return list(self.options[field.name].values())

    def combo_column(self, field) -> ComboColumn:
        if field.name == "modbus.reg":
            options, placeholders = self.register_options(), [self.labels.get("packet_filter_overlay_register_placeholder")]
        elif field.name == "pair":
            options = self.host_options()
            placeholders = [self.labels.get("packet_filter_overlay_pair_left"), self.labels.get("packet_filter_overlay_pair_right")]
        else:
            options, placeholders = self.host_options(), [self.labels.get("packet_filter_overlay_host_placeholder")]
        combos = ComboColumn(self.context, options, placeholders, lambda: QTimer.singleShot(0, self, self.fit),
                             pair=field.name == "pair")
        self.watch(combos, ("field", field.name, None))
        combos.changed.connect(self.boxes_changed)
        self.combos[field.name] = combos
        return combos

    def host_options(self) -> list[str]:
        '''
        The hosts seen this session - the network graph's, since the
        workspace opened or its hosts were last cleared: the nicknames of
        those that have one, then their IP addresses, then their MACs.
        '''
        macs, host_ips = self.context.buffer.network.get_hosts()
        nicknames = {self.context.preferences.host_nickname(mac) for mac in macs} - {""}
        ips = {ip for found in host_ips.values() for ip in found}

        def ip_order(ip: str):
            try:
                address = ipaddress.ip_address(ip)
                return (address.version, int(address))
            except ValueError:
                return (9, 0)
        return sorted(nicknames, key=str.lower) + sorted(ips, key=ip_order) + sorted({mac.lower() for mac in macs} - {"-"})

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
        QTimer.singleShot(0, self, self.fit)

    def fit(self):
        '''
        Sizes the boxes' scroll area to the boxes - but no bigger than the
        screen leaves room for, scrolling the rest - then the popup to
        its contents.
        '''
        try:
            hint = self.boxes.sizeHint()
            panel = self.description["title"].parentWidget().width()
        except RuntimeError:
            return  # closed meanwhile
        screen = self.popup.screen().availableGeometry()
        room_width = max(400, screen.width() - panel - CHROME_WIDTH)
        room_height = max(200, screen.height() - CHROME_HEIGHT)
        bar = self.scroll.verticalScrollBar().sizeHint().width()
        width = min(hint.width(), room_width)
        height = min(hint.height() + (bar if width < hint.width() else 0), room_height)
        width = min(hint.width() + (bar if height < hint.height() else 0), room_width)
        self.scroll.setFixedSize(width, height)
        self.popup.adjustSize()

    # Describing what's under the mouse
    def build_description(self) -> QFrame:
        '''The panel on the right, describing the section, field or option under the mouse (see describe).'''
        style = self.style
        panel = QFrame()
        style.set_material(panel, "card", rounded=True, outlined=True)
        panel.setFixedWidth(QFontMetrics(style.get_font()).averageCharWidth() * DESCRIPTION_WIDTH_CHARS)
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(style.igap, style.igap, style.igap, style.igap)
        layout.setSpacing(style.cgap * 3)
        bold = QFont(style.get_font())
        bold.setBold(True)
        self.description: dict[str, QLabel] = {}
        for key, font, tone in (("title", bold, None), ("place", style.get_font("small"), "muted"),
                                ("about_heading", style.get_font("small"), "muted"), ("about", style.get_font(), None),
                                ("checked_heading", style.get_font("small"), "muted"), ("checked", style.get_font(), None),
                                ("typed_heading", style.get_font("small"), "muted"), ("typed", style.get_font("mono"), None),
                                ("combine", style.get_font("small"), "muted")):
            label = QLabel()
            label.setFont(font)
            label.setWordWrap(True)
            label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
            if tone:
                style.set_tone(label, tone)
            if key == "typed":
                label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            if key.endswith("_heading"):
                label.setText(self.labels.get(f"packet_filter_describe_{key[:-len('_heading')]}"))
                label.setContentsMargins(0, style.cgap * 3, 0, 0)
            layout.addWidget(label)
            self.description[key] = label
        layout.addStretch(1)
        return panel

    def describe(self, topic: tuple | None):
        '''
        Fills the description panel for topic - ("section", name), ("field",
        name, value or None) - or, with None, says how the popup works.
        For an option: what it is, how the field checks a packet, and how
        it's written to show (and hide) it.
        '''
        labels, parts = self.labels, {}
        if topic is None:
            parts["title"] = labels.get("packet_filter_overlay_hint_title")
            parts["about"] = labels.get("packet_filter_overlay_hint")
        elif topic[0] == "section":
            parts["title"] = labels.get(f"packet_filter_sections_{topic[1]}")
            parts["about"] = labels.get(f"packet_filter_about_sections_{topic[1]}")
        else:
            _, name, value = topic
            field = BY_NAME[name]
            key = label_key(name)
            field_label = labels.get(f"packet_filter_fields_{key}")
            section = labels.get(f"packet_filter_sections_{field.section}")
            if value is not None:
                parts["title"] = labels.get(value_key(name, value))
                parts["place"] = f"{section} \u203a {field_label}"
                parts["about"] = labels.get(f"packet_filter_about_{key}_{value.replace('-', '_')}")
                hide = "modbus:false" if name == "modbus" else f"-{name}:{value}"
                parts["typed"] = f"{name}:{value}\n{hide}"
            else:
                parts["title"] = field_label
                parts["place"] = section
                parts["about"] = labels.get(f"packet_filter_tips_{key}")
                examples = {"modbus.reg": "modbus.reg:hreg_4", "pair": 'pair:"10.0.0.2<>PLC"'}
                if field.kind == "combo":
                    parts["typed"] = examples.get(name, f"{name}:PLC")
                else:
                    parts["typed"] = f"{name}:{','.join(field.values[:2])}"
            parts["checked"] = labels.get(f"packet_filter_eval_{key}")
            if field.kind == "combo" or len(field.values) > 1:
                parts["combine"] = labels.get("packet_filter_describe_combine")
        for key, label in self.description.items():
            if key.endswith("_heading"):
                label.setVisible(bool(parts.get(key[:-len("_heading")])))
            else:
                label.setText(parts.get(key, ""))
                label.setVisible(bool(parts.get(key)))

    def paste(self):
        '''Puts the clipboard's filter in place of the one in the text box, and reads it at once.'''
        self.editor.setPlainText(QApplication.clipboard().text().strip())
        self.typing.stop()
        self.read_text()

    def show_status(self, text: str | None, bad: bool = False):
        self.status.setText(text or "")
        self.style.set_tone(self.status, "bad" if bad else "muted")

    def copy(self, button: QPushButton):
        QApplication.clipboard().setText(self.editor.toPlainText().strip())
        button.setText(self.labels.get("packet_filter_overlay_copied"))
        QTimer.singleShot(1200, button, lambda: button.setText(self.labels.get("packet_filter_overlay_copy")))
