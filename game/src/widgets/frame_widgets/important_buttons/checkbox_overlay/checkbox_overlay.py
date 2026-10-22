from .....app_core import Context
from ...overlay import Overlay
from ...drag_drop import DragHandle, DragPayload, ListZone
from PySide6.QtWidgets import QCheckBox, QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout


class CheckboxOverlay:
    '''
    Binds a button to open and close an overlay listing one chip per key in a
    context.states settings category, persisted there, with a translated
    label per chip (via context.labels) and a category title above them. Each
    chip has a checkbox for whether that form/column shows. It only writes
    context.states - whatever shows those forms/columns polls the same
    category from its own animation callback and follows along.

    With reorderable=True the chips can be dragged to reorder them, and the
    new order is written back as the key order of the same settings category
    (mutated in place, so the checkboxes' autosave keeps working); a panel
    that lays its forms out in that category's order then follows the drag.

    Used for hacking-panel and modbus-panel form visibility - those only
    ever differed in which settings category to read/write (state_key) and
    what to title the column (category_label). Packet-console columns have
    their own overlay (see PacketColumnsOverlay).

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
        for key in box_slots:
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
        # everywhere else. box_slots is the live category dict; a reorder
        # mutates that same dict in place (see persist_order), so this keeps
        # writing to the right place afterwards.
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
        Rewrites the settings category's key order to the chips' order,
        mutating the live dict in place (clear + re-insert) so the checkboxes'
        autosave closures - which hold that same dict - keep working. Keys
        with no chip (filtered-out/unavailable forms) keep their value and
        trail the end.
        '''
        live = self.context.states.get(self.state_key)
        ordered = {chip.key: live.get(chip.key, "0") for chip in self.zone.items}
        for existing_key, existing_value in live.items():
            if existing_key not in ordered:
                ordered[existing_key] = existing_value
        live.clear()
        live.update(ordered)
