from typing import TYPE_CHECKING

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QComboBox, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QScrollArea,
                               QSplitter, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget)

from ...widgets import PANELS

if TYPE_CHECKING:
    from .config_editor import ConfigEditor

ORIENTATION_NAMES = {"horizontal": "Side by side", "vertical": "Stacked"}
PREFIXES = {"horizontal": "h_panes", "vertical": "v_panes"}
# Sibling groups need different names in JSON - named by position, like "v_panes_left"
POSITION_NAMES = {
    "horizontal": {2: ["left", "right"], 3: ["left", "middle", "right"]},
    "vertical": {2: ["top", "bottom"], 3: ["top", "middle", "bottom"]},
}


class LayoutEditor:
    '''
    The workspace editor's two layout tabs, sharing one pane tree - the
    positional tree PageManager.parse_panes makes:
    {"orientation", "children": [{"weight", "panes": {...}} | {"weight", "widget": "<panel type>"}]}

      - shape_tab: the tree's groups and panels, with buttons to add
        panels and groups, remove them, reorder them, and flip a group's
        direction, beside a preview of the result.
      - weights_tab: a full-size preview whose dividers can be dragged to
        resize panes, beside every weight as a number.

    A spot in the tree is a path: child indexes from the top group, so ()
    is the top group itself. authored() turns the tree back into the
    h_panes/v_panes layout a config file holds.
    '''

    def __init__(self, editor: "ConfigEditor", panes: dict | None):
        self.editor = editor
        self.style = editor.style
        self.root_weight = 1
        tree = editor.pages.parse_panes(panes) if isinstance(panes, dict) else None
        if isinstance(panes, dict):
            for key, group in panes.items():
                if editor.pages.pane_group(key) and isinstance(group, dict):
                    self.root_weight = group.get("weight", 1)
        self.root = {"weight": self.root_weight, "panes": tree or {"orientation": "horizontal", "children": []}}
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
                             "or a panel to add right after it. A group can't hold the same panel type twice.")
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
        controls.addWidget(self.button("Add Panel", lambda: self.add({"widget": self.panel_type.currentText()})), 0, 2)
        controls.addWidget(self.button("Add Side-by-Side Group", lambda: self.add({"panes": {"orientation": "horizontal", "children": []}})), 1, 0)
        controls.addWidget(self.button("Add Stacked Group", lambda: self.add({"panes": {"orientation": "vertical", "children": []}})), 1, 1)
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
            text = self.entry_name(entry)
            if "widget" in entry:
                text = f"{text}  ({entry['widget']})"
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

    def add(self, new: dict):
        # Inside a selected group, or right after a selected panel
        if self.is_group(self.selected):
            parent_path, index = self.selected, len(self.entry(self.selected)["panes"]["children"])
        else:
            parent_path, index = self.selected[:-1], self.selected[-1] + 1
        siblings = self.entry(parent_path)["panes"]["children"]
        if "widget" in new and any(child.get("widget") == new["widget"] for child in siblings):
            self.editor.set_status(f"This group already has a {new['widget']} - a group can't hold the same panel type twice.", "red")
            return
        weights = [child["weight"] for child in siblings]
        new["weight"] = round(sum(weights) / len(weights), 2) if weights else 1
        siblings.insert(index, new)
        self.changed(select=parent_path + (index,))

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
        group = self.entry(path)["panes"]
        group["orientation"] = "vertical" if group["orientation"] == "horizontal" else "horizontal"
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
        grid = QGridLayout(body)
        grid.setColumnStretch(1, 1)
        grid.setAlignment(Qt.AlignmentFlag.AlignTop)
        row = 0
        def add(path: tuple, depth: int):
            nonlocal row
            entry = self.entry(path)
            if path != ():
                label = QLabel("    " * (depth - 1) + self.entry_name(entry))
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
            box = QLabel(self.entry_name(entry))
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
    def authored(self) -> tuple[dict, list[str]]:
        '''The layout as a config file's "panes" - one h_panes/v_panes group - plus any problems with it.'''
        errors = []
        def group(panes: dict, weight) -> dict:
            out = {"weight": weight}
            children = panes["children"]
            if not children:
                errors.append(f"An empty {ORIENTATION_NAMES[panes['orientation']].lower()} group - add a panel to it or remove it.")
            groups = [child for child in children if "panes" in child]
            names = iter(POSITION_NAMES[panes["orientation"]].get(len(groups), [str(i) for i in range(1, len(groups) + 1)]))
            for child in children:
                if "widget" in child:
                    out[child["widget"]] = child["weight"]
                else:
                    prefix = PREFIXES[child["panes"]["orientation"]]
                    key = prefix if len(groups) == 1 else f"{prefix}_{next(names)}"
                    out[key] = group(child["panes"], child["weight"])
            return out
        top = self.root["panes"]
        return {PREFIXES[top["orientation"]]: group(top, self.root_weight)}, errors
