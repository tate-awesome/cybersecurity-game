from PySide6.QtCore import Qt
from PySide6.QtWidgets import QAbstractItemView, QHeaderView, QTreeWidget, QTreeWidgetItem, QWidget

from ....app_core import Context


class PacketTreeview:
    """
    Wraps a QTreeWidget into a small row-oriented API, so callers never need
    to import or touch QTreeWidget directly. QTreeWidget already provides
    its own scrollbars and (via the app-wide stylesheet built in Style) its
    own theming, so this needs none of the manual ttk.Style/scrollbar wiring
    the tkinter version did.
    """

    def __init__(self, parent: QWidget, context: Context):
        self.context = context
        self.style = context.style
        packet_columns = context.labels.get("packet_columns")
        if not isinstance(packet_columns, dict):
            # A malformed labels file shouldn't take the whole packet console
            # down at construction - fall back to no columns instead.
            packet_columns = {}
        self.columns = list(packet_columns.keys())

        self._items: dict[str, QTreeWidgetItem] = {}
        self.frame = self._tree = self._build(parent)

    # ------------------------------------------------------------------
    # Construction / styling
    # ------------------------------------------------------------------
    def _build(self, parent: QWidget) -> QTreeWidget:
        tree = QTreeWidget()
        tree.setFont(self.style.get_font("treeview"))
        tree.setStyleSheet(self.style.themed("QTreeWidget::item { padding: 4px; }"))
        tree.setAlternatingRowColors(True)

        tree.setColumnCount(len(self.columns))
        tree.setHeaderLabels([self.context.labels.get("packet_columns", col) for col in self.columns])
        tree.setRootIsDecorated(False)  # flat table, no expand arrows - matches show="headings"
        tree.setUniformRowHeights(True)
        tree.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        tree.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        header = tree.header()
        header.setMinimumSectionSize(50)
        for i, col in enumerate(self.columns):
            tree.setColumnWidth(i, int(self.style.get_column_width(col)))
            if col == "Info":
                header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)

        # Stretch 1: see Scrollable.__init__ for why (same Panel-body/
        # trailing-filler interaction).
        parent.layout().addWidget(tree, 1)
        return tree

    # ------------------------------------------------------------------
    # Selection
    # ------------------------------------------------------------------
    def bind_select(self, callback):
        self._tree.itemSelectionChanged.connect(callback)

    def selection(self):
        return [item.data(0, Qt.ItemDataRole.UserRole) for item in self._tree.selectedItems()]

    def select(self, row_id):
        item = self._items.get(row_id)
        if item is not None:
            self._tree.setCurrentItem(item)
            self._tree.scrollToItem(item)

    def select_last(self):
        row_ids = self.get_ids()
        if row_ids:
            self.select(row_ids[-1])

    # ------------------------------------------------------------------
    # Columns
    # ------------------------------------------------------------------
    def set_visible_columns(self, columns):
        visible = set(columns)
        for i, col in enumerate(self.columns):
            self._tree.setColumnHidden(i, col not in visible)

    # ------------------------------------------------------------------
    # Row CRUD
    # ------------------------------------------------------------------
    def get_ids(self):
        return [self._tree.topLevelItem(i).data(0, Qt.ItemDataRole.UserRole) for i in range(self._tree.topLevelItemCount())]

    def get(self, row_id):
        item = self._items[row_id]
        return [item.text(i) for i in range(len(self.columns))]

    def create(self, row_id, values, index="end"):
        item = QTreeWidgetItem([str(v) for v in values])
        item.setData(0, Qt.ItemDataRole.UserRole, row_id)
        if index == "end":
            self._tree.addTopLevelItem(item)
        else:
            self._tree.insertTopLevelItem(index, item)
        self._items[row_id] = item

    def submit(self, row_id, values, sort_column_index=0):
        """
        Insert a row, keeping rows sorted (descending) by the given column,
        assuming rows are usually appended in order already.
        """
        try:
            new_val = float(values[sort_column_index])
        except (ValueError, TypeError):
            new_val = values[sort_column_index]

        insert_index = "end"

        # Search from the bottom up (since packets usually arrive sequentially)
        ids = self.get_ids()
        for position in range(len(ids) - 1, -1, -1):
            current_val_str = self._items[ids[position]].text(sort_column_index)

            try:
                current_val = float(current_val_str)
            except (ValueError, TypeError):
                current_val = current_val_str

            # If the existing row is smaller than or equal to our new row,
            # it means our row belongs right AFTER this row.
            if current_val <= new_val:
                insert_index = position + 1
                break

        self.create(row_id, values, index=insert_index)

    def edit(self, row_id, values):
        item = self._items[row_id]
        for i, value in enumerate(values):
            item.setText(i, str(value))

    def delete(self, row_id):
        item = self._items.pop(row_id, None)
        if item is not None:
            index = self._tree.indexOfTopLevelItem(item)
            self._tree.takeTopLevelItem(index)

    def clear(self):
        self._tree.clear()
        self._items.clear()

    def count(self):
        return self._tree.topLevelItemCount()

    def trim_oldest(self, overflow_count):
        row_ids = self.get_ids()
        for i in range(overflow_count):
            self.delete(row_ids[i])

    # ------------------------------------------------------------------
    # Scrolling
    # ------------------------------------------------------------------
    def scroll_to_bottom(self):
        self._tree.scrollToBottom()
