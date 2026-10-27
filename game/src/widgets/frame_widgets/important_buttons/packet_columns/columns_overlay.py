from PySide6.QtCore import QEvent, QObject, QPoint, QTimer, Qt
from PySide6.QtGui import QFont, QFontMetrics
from PySide6.QtWidgets import QApplication, QCheckBox, QFrame, QHBoxLayout, QLabel, QVBoxLayout, QWidget

from .....app_core import Context
from ....popup import ButtonPopup
from ...drag_drop import INTERACTIVE, BinZone, DragHandle, DragPayload, RowZone

# The buffet's groups, each field in the order it's listed in there. A
# column in packet_columns that isn't listed here goes in the first group.
COLUMN_CATEGORIES: dict[str, list[str]] = {
    "packet": ["number", "time_word", "time_delta", "length", "protocol", "info", "summary", "layers_word"],
    "addresses": ["src", "dst", "src_host", "dst_host", "ip_word", "ip_src", "ip_dst", "mac_word", "mac_src", "mac_dst"],
    "transport": ["src_port", "dst_port", "service", "tcp_flags", "ttl", "payload_length"],
    "capture": ["direction", "hack", "observer", "purpose"],
    "modbus": ["modbus_word", "command_word", "command", "command_type", "variables", "values",
               "is_modbus", "is_useful", "is_primary"],
}
# What a chip's drag carries (see DragPayload) - only this popup's zones take it
CHIP_KIND = "packet_column"
# How wide the buffet and tray are, and the description beside them, in average characters
CHIPS_WIDTH_CHARS = 64
DESCRIPTION_WIDTH_CHARS = 28


def column_position(value) -> int:
    '''
    A packet_columns value as its place in the tray: 1 is the leftmost
    column, 0 not shown. Older saves stored "1"/"0" for shown/not shown,
    which still read as shown (in the default order - see tray_columns).
    '''
    try:
        return max(0, int(float(value)))
    except (TypeError, ValueError):
        return 0


def is_column_available(context: Context, key: str) -> bool:
    '''Whether students get this column at all (packet_columns_available - every column is, by default).'''
    return context.states.get("packet_columns_available").get(key, 1) in (1, "1", True)


def tray_columns(context: Context) -> list[str]:
    '''The columns in the tray, left to right - available to students or not. Ties keep the default order.'''
    columns = context.states.get("packet_columns")
    order = {key: i for i, key in enumerate(columns)}
    return sorted((key for key, value in columns.items() if column_position(value) > 0),
                  key=lambda key: (column_position(columns[key]), order[key]))


def shown_columns(context: Context) -> list[str]:
    '''The packet console's columns, left to right: the tray's, but only those students are given.'''
    return [key for key in tray_columns(context) if is_column_available(context, key)]


def column_category(key: str) -> str:
    return next((category for category, keys in COLUMN_CATEGORIES.items() if key in keys), next(iter(COLUMN_CATEGORIES)))


class PacketColumnsPopup(QObject):
    '''
    Opens the packet console's columns popup: a buffet of every field a column can show, as chips in groups (see
    COLUMN_CATEGORIES), above a tray of the columns that show. Dragging a
    chip into the tray shows that column, and the tray's order, left to
    right, is the console's; dragging it back out (or clicking a chip)
    moves it across. Pointing at a chip describes its field, in the panel
    on the right.

    The buffet is one drop target (a BinZone): while a tray chip is over
    it, it fades, rather than showing a place to drop, since a chip always
    goes back to its own group.

    Writes the tray to packet_columns as each column's place in it (1 is
    the leftmost, 0 not shown) - positions rather than key order, since a
    page's settings are merged over _packages/_default.json, which keeps
    its own key order. The packet console polls that and follows along.

    Only fields students are given (packet_columns_available) are offered.
    In developer mode every field is, each chip with a checkbox for whether
    students get it.
    '''

    def __init__(self, context: Context):
        popup = ButtonPopup(context, context.labels.get("packet_column_overlay_title"))
        super().__init__(popup)  # goes with the popup
        self.popup = popup
        self.context = context
        self.style = context.style
        self.labels = context.labels
        self.developer = False
        self.chips: dict[str, QFrame] = {}
        self.buffet: dict[str, RowZone] = {}
        self.tray: RowZone | None = None
        # The chip a click started on, and where
        self.pressed: QFrame | None = None
        self.pressed_at = QPoint()
        self.populate()
        popup.show()

    # Building
    def populate(self):
        style = self.style
        font = style.get_font()
        gap = style.cgap * 2
        self.developer = self.context.preferences.is_developer()
        columns = self.context.states.get("packet_columns")
        keys = [key for key in columns if self.developer or is_column_available(self.context, key)]
        chips_width = self.char_width(CHIPS_WIDTH_CHARS)

        body = QHBoxLayout()
        body.setSpacing(style.igap)
        self.popup.body.addLayout(body)
        chips_column = QVBoxLayout()
        chips_column.setSpacing(gap)
        body.addLayout(chips_column)

        # The buffet: one area to drop on (it fades while a tray chip is
        # over it), wherever in it the chip goes back to its own group (see
        # on_buffet_drop) - so its groups' zones take no drops themselves
        buffet = BinZone(self.context, "packet_columns_buffet", {CHIP_KIND},
                         takes=lambda payload: self.chips[payload.item_id] in self.tray.items, spacing=gap)
        buffet.dropped.connect(self.on_buffet_drop)
        chips_column.addWidget(buffet)
        self.buffet = {}
        for category in COLUMN_CATEGORIES:
            if not any(column_category(key) == category for key in keys):
                continue
            buffet.layout().addWidget(self.heading(f"packet_column_categories_{category}"))
            zone = RowZone(self.context, f"packet_columns_{category}", set(), spacing=gap)
            zone.setFixedWidth(chips_width)
            buffet.layout().addWidget(zone)
            self.buffet[category] = zone

        chips_column.addSpacing(style.igap)
        chips_column.addWidget(self.heading("packet_column_overlay_tray"))
        self.tray = RowZone(self.context, "packet_columns_tray", {CHIP_KIND}, spacing=gap)
        style.set_material(self.tray, "card", rounded=True, outlined=True)
        self.tray.setContentsMargins(gap * 2, gap * 2, gap * 2, gap * 2)
        self.tray.setFixedWidth(chips_width)
        self.tray.dropped.connect(self.on_tray_drop)
        chips_column.addWidget(self.tray)
        chips_column.addStretch(1)

        body.addWidget(self.build_description())

        self.chips = {key: self.make_chip(key, font) for key in keys}
        in_tray = [key for key in tray_columns(self.context) if key in self.chips]
        for key in keys:
            if key not in in_tray:
                self.send_home(self.chips[key])
        for key in in_tray:
            self.tray.insert(self.chips[key], len(self.tray.items))
        self.describe(None)

    def heading(self, label_key: str) -> QLabel:
        label = QLabel(self.labels.get(label_key))
        label.setFont(self.style.get_font("small"))
        self.style.set_tone(label, "muted")
        return label

    def char_width(self, chars: int) -> int:
        return QFontMetrics(self.style.get_font()).averageCharWidth() * chars

    def build_description(self) -> QFrame:
        '''The panel on the right, describing the field under the mouse (see describe).'''
        style = self.style
        panel = QFrame()
        style.set_material(panel, "card", rounded=True, outlined=True)
        panel.setFixedWidth(self.char_width(DESCRIPTION_WIDTH_CHARS))
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(style.igap, style.igap, style.igap, style.igap)
        layout.setSpacing(style.cgap * 2)

        self.description_name = QLabel()
        name_font = QFont(style.get_font())
        name_font.setBold(True)
        self.description_name.setFont(name_font)
        self.description_name.setWordWrap(True)
        layout.addWidget(self.description_name)

        self.description_category = QLabel()
        self.description_category.setFont(style.get_font("small"))
        style.set_tone(self.description_category, "muted")
        layout.addWidget(self.description_category)

        self.description_text = QLabel()
        self.description_text.setFont(style.get_font())
        self.description_text.setWordWrap(True)
        self.description_text.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.description_text)

        self.description_hidden = QLabel(self.labels.get("packet_column_overlay_unavailable"))
        self.description_hidden.setFont(style.get_font("small"))
        self.description_hidden.setWordWrap(True)
        style.set_tone(self.description_hidden, "muted")
        layout.addWidget(self.description_hidden)
        layout.addStretch(1)
        return panel

    def make_chip(self, key: str, font) -> QFrame:
        chip = QFrame()
        chip.key = key
        self.style.set_material(chip, "overlay_card", rounded=True, outlined=True)
        gap = self.style.cgap * 2
        layout = QHBoxLayout(chip)
        layout.setContentsMargins(gap * 2, gap, gap * 2, gap)
        layout.setSpacing(gap * 2)

        label = QLabel(self.labels.get(f"packet_columns_{key}"))
        label.setFont(font)
        layout.addWidget(label)

        if self.developer:
            # Developers: whether students get this field at all. Ints, like
            # _default.json's, so the autosave's diff against it stays clean
            available = QCheckBox()
            available.setChecked(is_column_available(self.context, key))
            available.setToolTip(self.labels.get("packet_column_overlay_available_tooltip"))
            def autosave(checked: bool, key=key):
                self.context.states.get("packet_columns_available")[key] = 1 if checked else 0
                self.describe(key)
            available.toggled.connect(autosave)
            layout.addWidget(available)

        # The checkbox is INTERACTIVE, so pressing it toggles rather than
        # starting a drag (or a click - see eventFilter)
        chip.drag = DragHandle(chip, lambda chip=chip: DragPayload(CHIP_KIND, chip.key, self.zone_of(chip).zone_id))
        for widget in [chip, *chip.findChildren(QWidget)]:
            if not isinstance(widget, INTERACTIVE):
                widget.installEventFilter(self)
        return chip

    # Pointing and clicking
    def eventFilter(self, watched, event):
        kind = event.type()
        chip = self.chip_of(watched)
        if chip is None:
            return False
        if kind == QEvent.Type.Enter:
            self.describe(chip.key)
        elif kind == QEvent.Type.MouseButtonPress and event.button() == Qt.MouseButton.LeftButton:
            self.pressed = chip
            self.pressed_at = event.globalPosition().toPoint()
        elif kind == QEvent.Type.MouseButtonRelease and event.button() == Qt.MouseButton.LeftButton:
            # A press and release in place, not a drag (this sees the release
            # before the chip's DragHandle finishes one)
            moved = (event.globalPosition().toPoint() - self.pressed_at).manhattanLength() if self.pressed is chip else 0
            if self.pressed is chip and chip.drag.dragging is None and moved < QApplication.startDragDistance():
                # After this event - moving the chip reparents it
                QTimer.singleShot(0, self, lambda chip=chip: self.toggle(chip))
            self.pressed = None
        return False

    def chip_of(self, widget: QWidget) -> QFrame | None:
        chips = set(map(id, self.chips.values()))
        while widget is not None and id(widget) not in chips:
            widget = widget.parentWidget()
        return widget

    def describe(self, key: str | None):
        '''Shows what key's field is in the description panel - or, with None, how the popup works.'''
        if key is None:
            self.description_name.setText(self.labels.get("packet_column_overlay_hint_title"))
            self.description_category.hide()
            self.description_text.setText(self.labels.get("packet_column_overlay_hint"))
            self.description_hidden.hide()
            return
        self.description_name.setText(self.labels.get(f"packet_columns_{key}"))
        self.description_category.setText(self.labels.get(f"packet_column_categories_{column_category(key)}"))
        self.description_category.show()
        self.description_text.setText(self.labels.get(f"packet_column_descriptions_{key}"))
        self.description_hidden.setVisible(self.developer and not is_column_available(self.context, key))

    # Moving chips
    def zone_of(self, chip: QFrame) -> RowZone:
        return self.tray if chip in self.tray.items else self.buffet[column_category(chip.key)]

    def send_home(self, chip: QFrame):
        '''Puts chip in its own group in the buffet, in that group's order.'''
        category = column_category(chip.key)
        zone = self.buffet[category]
        rank = {key: i for i, key in enumerate(COLUMN_CATEGORIES[category])}
        mine = rank.get(chip.key, len(rank))
        zone.insert(chip, sum(1 for other in zone.items if rank.get(other.key, len(rank)) <= mine))

    def toggle(self, chip: QFrame):
        '''A click: into the tray (at its right end), or back out of it.'''
        if chip in self.tray.items:
            self.tray.take(chip)
            self.send_home(chip)
        else:
            self.zone_of(chip).take(chip)
            self.tray.insert(chip, len(self.tray.items))
        self.changed()

    def on_tray_drop(self, payload: DragPayload, slot: int):
        chip = self.chips.get(payload.item_id)
        if chip is None:
            return
        if chip in self.tray.items:
            current = self.tray.index_of(chip)
            if slot in (current, current + 1):
                return  # dropped back where it was
            if slot > current:
                slot -= 1  # the slot was counted with the chip still in place
        self.zone_of(chip).take(chip)
        self.tray.insert(chip, slot)
        self.changed()

    def on_buffet_drop(self, payload: DragPayload, slot: None):
        '''Wherever in the buffet it's dropped, a chip goes back to its own group.'''
        chip = self.chips.get(payload.item_id)
        if chip is None or chip not in self.tray.items:
            return
        self.tray.take(chip)
        self.send_home(chip)
        self.changed()

    def changed(self):
        '''Writes the tray's order to packet_columns (see the class docstring), and fits the popup to its chips again.'''
        tray = [chip.key for chip in self.tray.items]
        live = self.context.states.get("packet_columns")
        for key in live:
            live[key] = tray.index(key) + 1 if key in tray else 0
        self.popup.adjustSize()
