from typing import TYPE_CHECKING

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QComboBox, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QScrollArea,
                               QSplitter, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget)

from ...widgets import PANELS

if TYPE_CHECKING:
    from .config_editor import ConfigEditor

ORIENTATION_NAMES = {"horizontal": "Side by side", "vertical": "Stacked"}
PREFIXES = {"horizontal": "h_panes", "vertical": "v_panes"}


class LayoutEditor:
    '''
    The workspace editor's two layout tabs, sharing one pane tree - the
    positional tree PageManager.layout_tree makes:
    {"id", "orientation", "children": [{"id", "weight", "panes": {...}} | {"id", "weight", "widget": "<panel type>"}]}

      - shape_tab: the tree's groups and panels, with buttons to add
        panels and groups, remove them, reorder them, and flip a group's
        direction, beside a preview of the result.
      - weights_tab: a full-size preview whose dividers can be dragged to
        resize panes, beside every weight as a number.

    A spot in the tree is a path: child indexes from the top group, so ()
    is the top group itself. Every panel and group has an id - its type
    plus a number, like "status_panel_2" - so one panel type can appear
    any number of times. authored() turns the tree back into the
    layout_shape and layout_weights a config file holds.
    '''

    def __init__(self, editor: "ConfigEditor", shape: dict | None, weights: dict | None):
        self.editor = editor
        self.style = editor.style
        tree = editor.pages.layout_tree(shape, weights)
        tree = tree or {"id": "h_panes_1", "orientation": "horizontal", "children": []}
        self.root = {"id": tree["id"], "weight": 1, "panes": tree}
        self.selected: tuple = ()
        self.syncing = False

        self.shape_tab = self.build_shape_tab()
        self.weights_tab = self.build_weights_tab()
        self.refresh()

    # Tree access
    def entry(self, path: tuple) -> dict:
        '''The {"weight", "panes"|"widget"} entry at path.'''
        entry = self.root
        for index in path:
            entry = entry["panes"]["children"][index]
        return entry

    def is_group(self, path: tuple) -> bool:
        return "panes" in self.entry(path)

    def all_ids(self, entry: dict | None = None) -> list[str]:
        entry = entry or self.root
        ids = [entry["id"]]
        if "panes" in entry:
            for child in entry["panes"]["children"]:
                ids += self.all_ids(child)
        return ids

    def next_id(self, kind: str) -> str:
        '''A new id for a panel type or group prefix: one past the highest number it already has.'''
        numbers = [int(pane_id.rpartition("_")[2]) for pane_id in self.all_ids()
                   if self.editor.pages.panel_type(pane_id) == kind and pane_id.rpartition("_")[2].isdigit()]
        return f"{kind}_{max(numbers, default=0) + 1}"

    def entry_name(self, entry: dict) -> str:
        if "panes" in entry:
            return ORIENTATION_NAMES[entry["panes"]["orientation"]]
        panel = entry["widget"]
        label = f"menu_bar_titles_{panel}"
        return self.editor.labels.data.get(label, panel)

    # Shape tab
    def build_shape_tab(self) -> QWidget:
        tab = QWidget()
        row = QHBoxLayout(tab)
        row.setSpacing(self.style.igap)
        left = QVBoxLayout()
        row.addLayout(left, 2)

        explanation = QLabel("The workspace's panels and how they're grouped. Select a group to add inside it, "
                             "or a panel to add right after it. A panel type can be added as many times as you like - "
                             "each copy gets its own numbered id, so its weight is kept separately.")
        explanation.setFont(self.style.get_font("small"))
        explanation.setWordWrap(True)
        left.addWidget(explanation)

        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.setFont(self.style.get_font("default"))
        self.tree.setStyleSheet(self.style.themed(
            f"QTreeWidget {{ background-color: {self.style.color('field')}; color: {self.style.color('field_text')}; border: none; }}"))
        self.tree.currentItemChanged.connect(self.on_select)
        left.addWidget(self.tree, 1)

        controls = QGridLayout()
        left.addLayout(controls)
        self.panel_type = QComboBox()
        self.panel_type.setFont(self.style.get_font("default"))
        self.panel_type.addItems(list(PANELS))
        controls.addWidget(self.panel_type, 0, 0, 1, 2)
        controls.addWidget(self.button("Add Panel", lambda: self.add({"id": self.next_id(self.panel_type.currentText()), "widget": self.panel_type.currentText()})), 0, 2)
        controls.addWidget(self.button("Add Side-by-Side Group", lambda: self.add_group("horizontal")), 1, 0)
        controls.addWidget(self.button("Add Stacked Group", lambda: self.add_group("vertical")), 1, 1)
        controls.addWidget(self.button("Flip Direction", self.flip), 1, 2)
        controls.addWidget(self.button("Move Up", lambda: self.move(-1)), 2, 0)
        controls.addWidget(self.button("Move Down", lambda: self.move(1)), 2, 1)
        controls.addWidget(self.button("Remove", self.remove), 2, 2)

        self.shape_preview = QVBoxLayout()
        self.shape_preview.setContentsMargins(0, 0, 0, 0)
        row.addLayout(self.shape_preview, 3)
        return tab

    def button(self, text: str, function) -> QPushButton:
        button = QPushButton(text)
        button.setFont(self.style.get_font("default"))
        button.clicked.connect(lambda checked=False: function())
        return button

    def on_select(self):
        if self.syncing:
            return
        item = self.tree.currentItem()
        self.selected = tuple(item.data(0, Qt.ItemDataRole.UserRole)) if item is not None else ()
        self.build_preview(self.shape_preview, interactive=False)

    def fill_tree(self):
        self.syncing = True
        self.tree.clear()
        current = None
        def add(parent, path: tuple):
            nonlocal current
            entry = self.entry(path)
            text = f"{self.entry_name(entry)}  ({entry['id']})"
            item = QTreeWidgetItem([text])
            item.setData(0, Qt.ItemDataRole.UserRole, path)
            if parent is None:
                self.tree.addTopLevelItem(item)
            else:
                parent.addChild(item)
            if path == self.selected:
                current = item
            if "panes" in entry:
                for index in range(len(entry["panes"]["children"])):
                    add(item, path + (index,))
        add(None, ())
        self.tree.expandAll()
        if current is not None:
            self.tree.setCurrentItem(current)
        self.syncing = False

    # Shape changes
    def changed(self, select: tuple | None = None):
        if select is not None:
            self.selected = select
        self.editor.mark_dirty()
        self.refresh()
        self.editor.refresh_usage()

    def add(self, new: dict):
        # Inside a selected group, or right after a selected panel
        if self.is_group(self.selected):
            parent_path, index = self.selected, len(self.entry(self.selected)["panes"]["children"])
        else:
            parent_path, index = self.selected[:-1], self.selected[-1] + 1
        siblings = self.entry(parent_path)["panes"]["children"]
        weights = [child["weight"] for child in siblings]
        average = round(sum(weights) / len(weights), 2) if weights else 1
        new["weight"] = int(average) if average == int(average) else average
        siblings.insert(index, new)
        self.changed(select=parent_path + (index,))

    def add_group(self, orientation: str):
        group_id = self.next_id(PREFIXES[orientation])
        self.add({"id": group_id, "panes": {"id": group_id, "orientation": orientation, "children": []}})

    def remove(self):
        if self.selected == ():
            self.editor.set_status("The top group can't be removed.", "red")
            return
        parent_path, index = self.selected[:-1], self.selected[-1]
        del self.entry(parent_path)["panes"]["children"][index]
        self.changed(select=parent_path)

    def move(self, step: int):
        if self.selected == ():
            return
        parent_path, index = self.selected[:-1], self.selected[-1]
        siblings = self.entry(parent_path)["panes"]["children"]
        target = index + step
        if not 0 <= target < len(siblings):
            return
        siblings[index], siblings[target] = siblings[target], siblings[index]
        self.changed(select=parent_path + (target,))

    def flip(self):
        path = self.selected if self.is_group(self.selected) else self.selected[:-1]
        entry = self.entry(path)
        group = entry["panes"]
        group["orientation"] = "vertical" if group["orientation"] == "horizontal" else "horizontal"
        # The id names the direction, so it changes with it
        entry["id"] = group["id"] = self.next_id(PREFIXES[group["orientation"]])
        self.changed(select=path)

    # Weights tab
    def build_weights_tab(self) -> QWidget:
        tab = QWidget()
        row = QHBoxLayout(tab)
        row.setSpacing(self.style.igap)
        self.weight_preview = QVBoxLayout()
        self.weight_preview.setContentsMargins(0, 0, 0, 0)
        row.addLayout(self.weight_preview, 3)

        right = QVBoxLayout()
        row.addLayout(right, 2)
        explanation = QLabel("Drag the dividers in the preview to resize panes, or type a weight. "
                             "Weights are shares of the group a pane sits in - a pane with weight 2 gets "
                             "twice the room of a weight-1 neighbour.")
        explanation.setFont(self.style.get_font("small"))
        explanation.setWordWrap(True)
        right.addWidget(explanation)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(self.style.themed("QScrollArea { background-color: transparent; border: none; }"))
        right.addWidget(scroll, 1)
        self.weight_scroll = scroll
        return tab

    def fill_weight_rows(self):
        body = QWidget()
        self.editor.paint_root(body)
        grid = QGridLayout(body)
        grid.setColumnStretch(1, 1)
        grid.setAlignment(Qt.AlignmentFlag.AlignTop)
        row = 0
        def add(path: tuple, depth: int):
            nonlocal row
            entry = self.entry(path)
            if path != ():
                label = QLabel("    " * (depth - 1) + f"{self.entry_name(entry)}  ({entry['id']})")
                label.setFont(self.style.get_font("default"))
                grid.addWidget(label, row, 0)
                weight = QLineEdit(f"{entry['weight']:g}")
                weight.setFont(self.style.get_font("default"))
                weight.setMaximumWidth(140)
                weight.editingFinished.connect(lambda path=path, weight=weight: self.type_weight(path, weight))
                grid.addWidget(weight, row, 1, Qt.AlignmentFlag.AlignLeft)
                row += 1
            if "panes" in entry:
                for index in range(len(entry["panes"]["children"])):
                    add(path + (index,), depth + 1)
        add((), 0)
        self.weight_scroll.setWidget(body)

    def type_weight(self, path: tuple, entry_box: QLineEdit):
        entry = self.entry(path)
        try:
            weight = float(entry_box.text())
        except ValueError:
            weight = 0
        if weight <= 0:
            self.editor.set_status(f'A weight must be a number above 0, not "{entry_box.text()}".', "red")
            entry_box.setText(f"{entry['weight']:g}")
            return
        weight = int(weight) if weight == int(weight) else weight
        if weight != entry["weight"]:
            entry["weight"] = weight
            self.editor.mark_dirty()
            self.build_preview(self.shape_preview, interactive=False)
            self.build_preview(self.weight_preview, interactive=True)

    def drag(self, path: tuple, splitter: QSplitter):
        '''A divider in the weights preview moved: each pane's weight becomes its percentage of the group.'''
        sizes = splitter.sizes()
        total = sum(sizes)
        if total <= 0:
            return
        for child, size in zip(self.entry(path)["panes"]["children"], sizes):
            child["weight"] = max(1, round(size / total * 100))
        self.editor.mark_dirty()
        self.fill_weight_rows()
        self.build_preview(self.shape_preview, interactive=False)

    # Previews
    def build_preview(self, holder: QVBoxLayout, interactive: bool):
        '''A mock of the layout: nested splitters, with a labelled box per panel.'''
        while holder.count():
            old = holder.takeAt(0).widget()
            if old is not None:
                # Out of the layout but not deleted until the event loop gets to it - hide it
                # now, or it's drawn loose over whatever's at the top-left of the tab until then
                old.hide()
                old.deleteLater()
        holder.addWidget(self.preview_widget((), interactive))

    def preview_widget(self, path: tuple, interactive: bool) -> QWidget:
        entry = self.entry(path)
        if "widget" in entry:
            selected = not interactive and path == self.selected
            box = QLabel(f"{self.entry_name(entry)}\n{entry['id']}")
            box.setFont(self.style.get_font("default"))
            box.setAlignment(Qt.AlignmentFlag.AlignCenter)
            box.setWordWrap(True)
            border = self.style.color("accent") if selected else self.style.color("widget")
            box.setStyleSheet(f"background-color: {self.style.color('panel')}; color: {self.style.color('text')};"
                              f" border: 3px solid {border}; border-radius: {self.style.PANEL_RADIUS}px;")
            return box
        group = entry["panes"]
        orientation = Qt.Orientation.Horizontal if group["orientation"] == "horizontal" else Qt.Orientation.Vertical
        splitter = QSplitter(orientation)
        splitter.setChildrenCollapsible(False)
        splitter.setHandleWidth(self.style.igap)
        if not interactive and path == self.selected:
            splitter.setStyleSheet(f"QSplitter {{ border: 3px solid {self.style.color('accent')}; }}")
        children = group["children"]
        if not children:
            empty = QLabel(f"Empty {ORIENTATION_NAMES[group['orientation']].lower()} group - add a panel to it")
            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty.setWordWrap(True)
            empty.setStyleSheet(f"color: {self.style.color('red')};")
            splitter.addWidget(empty)
            return splitter
        for index in range(len(children)):
            splitter.addWidget(self.preview_widget(path + (index,), interactive))
        splitter.setSizes([max(1, int(child["weight"] * 1000)) for child in children])
        for index in range(1, splitter.count()):
            splitter.handle(index).setEnabled(interactive)
        if interactive:
            splitter.splitterMoved.connect(lambda *_, path=path, splitter=splitter: self.drag(path, splitter))
        return splitter

    def refresh(self):
        self.fill_tree()
        self.fill_weight_rows()
        self.build_preview(self.shape_preview, interactive=False)
        self.build_preview(self.weight_preview, interactive=True)

    # Saving
    def authored(self) -> tuple[dict, dict, list[str]]:
        '''The layout as a config file's "layout_shape" and "layout_weights", plus any problems with it.'''
        errors = []
        weights = {}
        def group(panes: dict) -> list:
            children = panes["children"]
            if not children:
                errors.append(f"An empty {ORIENTATION_NAMES[panes['orientation']].lower()} group - add a panel to it or remove it.")
            out = []
            for child in children:
                weights[child["id"]] = child["weight"]
                out.append(child["id"] if "widget" in child else {child["id"]: group(child["panes"])})
            return out
        shape = {self.root["id"]: group(self.root["panes"])}
        ids = self.all_ids()
        for duplicate in sorted({pane_id for pane_id in ids if ids.count(pane_id) > 1}):
            errors.append(f'The id "{duplicate}" is used more than once.')
        return shape, weights, errors
