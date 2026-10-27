from .....app_core import Context
from ...overlay import Overlay
from ...drag_drop import DragHandle, DragPayload, ListZone
from PySide6.QtWidgets import QCheckBox, QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout


def form_order(context: Context, state_key: str) -> list[str]:
    '''
    state_key's keys in the order they're laid out: as listed in
    form_order[state_key] (written by a drag in a reorderable
    CheckboxOverlay), then any it doesn't list, in the category's own order.
    Kept apart from the category itself, as a list, since a page's settings
    are merged over _packages/_default.json, which keeps its own key order -
    a list is saved and merged whole.
    '''
    keys = list(context.states.get(state_key))
    listed = context.states.get("form_order").get(state_key) or []
    ordered = [key for key in listed if key in keys]
    return ordered + [key for key in keys if key not in ordered]


class CheckboxOverlay:
    '''
    Binds a button to open and close an overlay listing one chip per key in a
    context.states settings category, persisted there, with a translated
    label per chip (via context.labels) and a category title above them. Each
    chip has a checkbox for whether that form/column shows. It only writes
    context.states - whatever shows those forms/columns polls the same
    category from its own animation callback and follows along.

    With reorderable=True the chips can be dragged to reorder them, and the
    new order is written to form_order[state_key]; a panel that lays its
    forms out in that order (see form_order) then follows the drag.

    Used for hacking-panel and modbus-panel form visibility - those only
    ever differed in which settings category to read/write (state_key) and
    what to title the column (category_label). Packet-console columns have
    their own popup (see PacketColumnsPopup).

    Each chip is labeled with the labels key "<label_group>_<key>";
    label_group defaults to state_key.
    '''
    def __init__(self, button: QPushButton, context: Context,
                 state_key: str, category_label: str, visibility_key: str | None = None,
                 label_group: str | None = None, reorderable: bool = False):
        self.context = context
        self.style = context.style
        self.state_key = state_key
        self.category_label = category_label
        self.visibility_key = visibility_key
        self.label_group = label_group or state_key
        self.reorderable = reorderable
        self.zone: ListZone | None = None
        self.chips: dict[str, QFrame] = {}
        self.overlay = Overlay(self.context.root, context, button, self.populate_overlay)

    def populate_overlay(self, overlay: Overlay):
        med = self.style.get_font()

        # Create box filter widgets
        category_frame = QFrame()
        # Part of the overlay's background - follows the "overlay" surface, not "widget"
        self.style.set_material(category_frame, "overlay_card")
        category_layout = QVBoxLayout(category_frame)
        category_layout.setContentsMargins(self.style.igap, self.style.igap, self.style.igap, self.style.igap)
        category_layout.setSpacing(self.style.cgap * 2)
        overlay.layout().addWidget(category_frame)

        category_label = QLabel(self.category_label)
        category_label.setFont(med)
        category_layout.addWidget(category_label)
        if self.reorderable:
            hint = QLabel(self.context.labels.get("form_overlay_hint"))
            hint.setFont(self.style.get_font("small"))
            self.style.set_tone(hint, "muted")
            category_layout.addWidget(hint)

        # The chips live in a drop zone so they can be dragged to reorder (see
        # DragHandle / ListZone). It accepts only this overlay's own kind, so
        # chips never cross between overlays.
        self.zone = ListZone(self.context, f"{self.state_key}_chips", {self.state_key}, spacing=self.style.cgap * 2)
        if self.reorderable:
            self.zone.dropped.connect(self.on_drop)
        category_layout.addWidget(self.zone)
        self.chips = {}

        box_slots = self.context.states.get(self.state_key)
        available_forms: dict[str, int] = self.context.states.get(self.visibility_key) if self.visibility_key else None
        for key in form_order(self.context, self.state_key):
            if available_forms and (key not in available_forms or available_forms[key] == 0 or available_forms[key] == "0"):
                print(f"Form is invisible: {key!r}")
                continue
            chip = self._make_chip(key, box_slots, med)
            self.zone.insert(chip, len(self.zone.items))
            self.chips[key] = chip

    def _make_chip(self, key: str, box_slots: dict, font) -> QFrame:
        chip = QFrame()
        chip.key = key
        chip.zone = self.zone
        self.style.set_material(chip, "overlay_card", rounded=True, outlined=True)
        gap = self.style.cgap * 2
        layout = QHBoxLayout(chip)
        layout.setContentsMargins(gap * 2, gap, gap * 2, gap)
        layout.setSpacing(gap * 2)

        label = QLabel(self.context.labels.get(f"{self.label_group}_{key}"))
        label.setFont(font)
        layout.addWidget(label, 1)

        checkbox = QCheckBox()
        checkbox.setFont(font)
        # Load previous input before connecting, so restoring it doesn't itself trigger autosave
        value = box_slots[key]
        checkbox.setChecked(value == "1" or value == 1)
        # Stored as "1"/"0" - the convention this settings data already uses
        # everywhere else. box_slots is the live category dict.
        def autosave(checked: bool, value=box_slots, key=key):
            value[key] = "1" if checked else "0"
        checkbox.toggled.connect(autosave)
        layout.addWidget(checkbox)

        # The checkbox is an INTERACTIVE child, so pressing it toggles rather
        # than starting a drag; pressing anywhere else on the chip drags it.
        if self.reorderable:
            DragHandle(chip, lambda chip=chip: DragPayload(self.state_key, chip.key, self.zone.zone_id))
        return chip

    def on_drop(self, payload: DragPayload, slot: int):
        chip = self.chips.get(payload.item_id)
        if chip is None:
            return
        current = self.zone.index_of(chip)
        if slot in (current, current + 1):
            return  # dropped back where it was
        if slot > current:
            slot -= 1  # the slot was counted with the chip still in place
        self.zone.take(chip)
        self.zone.insert(chip, slot)
        self.persist_order()

    def persist_order(self):
        '''
        Writes the chips' order to form_order[state_key] - every key, those
        with no chip (unavailable forms) keeping their place after them.
        '''
        chips = [chip.key for chip in self.zone.items]
        rest = [key for key in form_order(self.context, self.state_key) if key not in chips]
        self.context.states.get("form_order")[self.state_key] = chips + rest
