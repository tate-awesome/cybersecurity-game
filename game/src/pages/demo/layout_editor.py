from typing import TYPE_CHECKING

from PySide6.QtCore import QPoint, Qt
from PySide6.QtWidgets import QApplication, QFrame, QHBoxLayout, QLabel, QScrollArea, QVBoxLayout, QWidget

from ...widgets import PANELS, DockArea, GenericPanel

if TYPE_CHECKING:
    from .config_editor import ConfigEditor


class PanelChip(QFrame):
    '''
    One panel type in the layout editor's list: its name, picked up and
    dragged into the preview to add a copy of it there (see LayoutEditor.pick_up).
    '''

    def __init__(self, layout_editor: "LayoutEditor", panel: str):
        super().__init__()
        self.layout_editor = layout_editor
        self.panel = panel
        style = layout_editor.style
        style.set_material(self, "card", rounded=True, outlined=True)
        row = QHBoxLayout(self)
        gap = style.cgap * 2
        row.setContentsMargins(gap * 2, gap, gap * 2, gap)
        name = QLabel(layout_editor.panel_name(panel))
        name.setFont(style.get_font("default"))
        name.setWordWrap(True)
        name.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        row.addWidget(name, 1)
        self.setToolTip(layout_editor.panel_details(panel))
        self.setCursor(Qt.CursorShape.OpenHandCursor)
        self.pressed_at: QPoint | None = None

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.pressed_at = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        at = event.globalPosition().toPoint()
        if self.pressed_at is not None and (at - self.pressed_at).manhattanLength() >= QApplication.startDragDistance():
            self.pressed_at = None
            self.layout_editor.pick_up(self.panel, at)

    def mouseReleaseEvent(self, event):
        self.pressed_at = None


class LayoutEditor:
    '''
    The workspace editor's Layout tab: every panel type down the left - a
    scrollable list to pick panels up from - beside a preview of the
    layout on the right. The preview is a DockArea, the same as a
    workspace's, with a stand-in for each panel: drag a panel from the
    list into it to add one, drag a panel by its menu bar to move it (or
    onto another, as a tab), drag one back onto the list to remove it, and
    drag the dividers to resize. Every copy of a panel gets its own
    numbered id ("status_panel_2"), so one panel type can appear any
    number of times - up to its MAX_COPIES, if it has one.

    authored() turns the preview back into the layout_shape and
    layout_weights a config file holds.
    '''

    def __init__(self, editor: "ConfigEditor", shape: dict | None, weights: dict | None):
        self.editor = editor
        self.style = editor.style
        self.context = editor.context
        self.tree = editor.pages.layout_tree(shape, weights)
        self.shape = shape
        self.weights = weights if isinstance(weights, dict) else {}
        # Only once the preview's been changed is the layout read back off it - until then, it's saved as it was written
        self.touched = False
        self.tab = self.build_tab()

    # Panel names and explanations, from _default_notes.json's "panels"
    def panel_note(self, panel: str) -> dict:
        note = self.editor.notes.get("panels", {}).get(panel)
        return note if isinstance(note, dict) else {}

    def panel_name(self, panel: str) -> str:
        return self.panel_note(panel).get("name") or self.editor.labels.data.get(f"menu_bar_titles_{panel}", panel)

    def panel_details(self, panel: str) -> str:
        return self.panel_note(panel).get("details", "")

    def panel_keys(self) -> list[str]:
        '''Every panel type, in _default_notes.json's "panels" order, then any it doesn't list.'''
        listed = [key for key in self.editor.notes.get("panels", {}) if key in PANELS]
        return listed + [key for key in PANELS if key not in listed]

    # The tab
    def build_tab(self) -> QWidget:
        tab = QWidget()
        row = QHBoxLayout(tab)
        row.setSpacing(self.style.igap)

        left = QVBoxLayout()
        row.addLayout(left, 1)
        explanation = QLabel("Drag a panel from here into the preview to add it. In the preview, drag a panel by its "
                             "title bar to move it: onto the middle of another panel to share its pane as a tab, or onto "
                             "an edge to split that pane. Drag one back here to remove it, and drag the dividers to resize.")
        explanation.setFont(self.style.get_font("small"))
        explanation.setWordWrap(True)
        left.addWidget(explanation)
        self.buffet = QScrollArea()
        self.buffet.setWidgetResizable(True)
        self.buffet.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.buffet.setStyleSheet("QScrollArea { background-color: transparent; border: none; }")
        chips = QWidget()
        self.editor.paint_root(chips)
        column = QVBoxLayout(chips)
        column.setSpacing(self.style.cgap * 3)
        column.setAlignment(Qt.AlignmentFlag.AlignTop)
        for panel in self.panel_keys():
            column.addWidget(PanelChip(self, panel))
        self.buffet.setWidget(chips)
        left.addWidget(self.buffet, 1)

        preview = QWidget()
        preview.setLayout(QVBoxLayout())
        preview.layout().setContentsMargins(0, 0, 0, 0)
        row.addWidget(preview, 3)
        self.dock = DockArea(preview, self.context, self.tree, self.stand_in, discard=self.buffet,
                             empty_text="No panels yet - drag one in from the list.")
        self.dock.changed.connect(self.changed)
        return tab

    def stand_in(self, panel_id: str, master: QWidget) -> QWidget:
        '''A panel's stand-in in the preview: its menu bar, and its id and what it's for.'''
        panel = self.editor.pages.panel_type(panel_id)
        stand_in = GenericPanel(master, self.context, panel if panel in PANELS else "_default")
        text = QLabel(f"{panel_id}\n\n{self.panel_details(panel)}".strip())
        text.setFont(self.style.get_font("small"))
        text.setWordWrap(True)
        text.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        text.setContentsMargins(0, self.style.igap, 0, 0)
        stand_in.layout().addWidget(text, 1)
        return stand_in

    def pick_up(self, panel: str, at: QPoint):
        '''Starts dragging a new copy of a panel type from the list - see PanelChip.'''
        panel_id = self.next_id(panel)
        if panel_id is None:
            self.editor.set_status(f"A layout can only hold {PANELS[panel].MAX_COPIES} of {self.panel_name(panel)}.", "bad")
            return
        self.dock.begin_drag(panel_id, at, new=True)

    def changed(self):
        self.touched = True
        self.editor.mark_dirty()
        self.editor.refresh_usage()

    # The layout
    def numbers(self, kind: str) -> list[int]:
        '''The numbers in use by a panel type's ids.'''
        return [int(panel_id.rpartition("_")[2]) for panel_id in self.dock.panel_ids()
                if self.editor.pages.panel_type(panel_id) == kind]

    def next_id(self, kind: str) -> str | None:
        '''
        A new id for a panel type: one past the highest number it already
        has - or, for a panel type with a MAX_COPIES (its settings are per
        copy, like ModbusModel's model_panels), the lowest number from 1 to
        MAX_COPIES not in use yet, and None once they all are.
        '''
        limit = getattr(PANELS.get(kind), "MAX_COPIES", None)
        if limit is None:
            return f"{kind}_{max(self.numbers(kind), default=0) + 1}"
        free = [number for number in range(1, limit + 1) if number not in self.numbers(kind)]
        return f"{kind}_{free[0]}" if free else None

    def all_ids(self) -> list[str]:
        '''Every panel id in the layout.'''
        return self.dock.panel_ids()

    def panel_types(self) -> list[str]:
        '''The panel types in the layout, in layout order, each once.'''
        found = []
        for panel_id in self.dock.panel_ids():
            panel = self.editor.pages.panel_type(panel_id)
            if panel not in found:
                found.append(panel)
        return found

    # Saving
    def authored(self) -> tuple[dict | None, dict, list[str]]:
        '''The layout as a config file's "layout_shape" and "layout_weights", plus any problems with it.'''
        pages = self.editor.pages
        tree = self.dock.layout_tree() if self.touched else self.tree
        if tree is None:
            return None, {}, ["The layout has no panels - drag at least one into the preview."]
        errors = []
        for panel_id in pages.layout_panel_ids(tree):
            limit = getattr(PANELS.get(pages.panel_type(panel_id)), "MAX_COPIES", None)
            number = panel_id.rpartition("_")[2]
            if limit is not None and number.isdigit() and not 1 <= int(number) <= limit:
                errors.append(f'"{panel_id}": this panel\'s ids only go from 1 to {limit}.')
        if not self.touched:
            return self.shape, self.weights, errors
        return pages.layout_shape_of(tree), pages.authored_weights(tree, self.weights), errors
