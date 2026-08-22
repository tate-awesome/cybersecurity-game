from tkinter import ttk
from tkinter import font as tkfont

from ....app_core import Context


class PacketTreeview:
    """
    Wraps a styled ttk.Treeview (plus its scrollbars) into a small row-oriented
    API, so callers never need to import or touch ttk.Treeview directly.
    """

    def __init__(self, parent, context: Context):
        self.context = context
        self.style = context.style
        packet_columns = context.labels.get("packet_columns")
        if not isinstance(packet_columns, dict):
            # A malformed labels file shouldn't take the whole packet console
            # down at construction - fall back to no columns instead.
            packet_columns = {}
        self.columns = list(packet_columns.keys())

        self.frame, self._tree = self._build(parent)

    # ------------------------------------------------------------------
    # Construction / styling
    # ------------------------------------------------------------------
    def _build(self, parent):
        style = ttk.Style()
        style.theme_use('clam')
        style.layout("Treeview", [
            ('Treeview.treearea', {'sticky': 'nswe', 'border': '0'})
        ])
        style.configure("TFrame", borderwidth=0, relief="flat")
        tree_font = tkfont.Font(
            family="Consolas",
            size=self.style.get_font_size("treeview")
        )
        row_height = tree_font.metrics("linespace") * 2 + 6

        # 1. Treeview Body & Empty Rows Area
        style.configure(
            "Treeview",
            font=("Consolas", self.style.get_font_size("treeview"), "normal"),
            rowheight=row_height,
            background=self.style.color("field"),
            fieldbackground=self.style.color("field"),
            foreground=self.style.color("field_text"),
            borderwidth=0,
            relief="flat"
        )
        # Highlight colors when a cell/row is selected
        style.map(
            "Treeview",
            background=[("selected", self.style.color("accent"))],
            foreground=[("selected", self.style.color("field_text"))]
        )

        # 2. Table Headers Style
        style.configure(
            "Treeview.Heading",
            font=("Consolas", self.style.get_font_size("treeview"), "bold"),
            background=self.style.color("widget"),      # Contrasted panel color for headers
            foreground=self.style.color("field_text"),
            borderwidth=1,
            relief="flat"
        )
        style.map(
            "Treeview.Heading",
            background=[("active", self.style.color("accent"))],    # Accent color on hover
            foreground=[("active", self.style.color("field_text"))] # Text stays readable
        )

        # 3. Layout Container Frame Style
        style.configure(
            "TFrame",
            background=self.style.color("panel")  # Blends frame container with parent view
        )

        # 4. Scrollbar Track and Slider Elements
        style.configure(
            "TScrollbar",
            gripcount=0,
            background=self.style.color("scrollbar"),      # The slider handle color
            troughcolor=self.style.color("panel"),      # The tracking channel backdrop
            bordercolor=self.style.color("panel"),      # Outer slider thin border line
            arrowcolor=self.style.color("field_text"),  # Tiny arrow icons on cap ends
            lightcolor=self.style.color("panel"),       # Eliminates default 3D highlights
            darkcolor=self.style.color("panel"),
            borderwidth=0,
            thickness=self.style.get_scrollbar_size(),
            arrowsize=self.style.get_scrollbar_size()
        )
        style.map(
            "TScrollbar",
            background=[("active", self.style.color("scrollbar_hover"))] # Hover slider color shifts to accent
        )

        # Container for tree and scrollbars (Now safely targeted by TFrame styles)
        container = ttk.Frame(parent)
        container.pack(
            padx=self.style.pad_corrected(),  # Matches CustomTkinter's standard frame padding layout
            pady=self.style.pad_corrected(),
            fill="both",
            expand=True
        )

        # Treeview
        tree = ttk.Treeview(
            container,
            columns=self.columns,
            show="headings"
        )

        # Configure columns
        for col in self.columns:
            stretch = (col == "Info")

            tree.heading(col, text=self.context.labels.get("packet_columns", col))

            tree.column(
                col,
                width=self.style.get_column_width(col),
                minwidth=50,
                stretch=stretch,
                anchor="w"
            )

        # Vertical scrollbar
        y_scrollbar = ttk.Scrollbar(
            container,
            orient="vertical",
            command=tree.yview
        )

        # Horizontal scrollbar
        x_scrollbar = ttk.Scrollbar(
            container,
            orient="horizontal",
            command=tree.xview
        )

        # Connect scrollbars
        tree.configure(
            yscrollcommand=y_scrollbar.set,
            xscrollcommand=x_scrollbar.set
        )

        # Layout
        tree.grid(row=0, column=0, sticky="nsew")

        y_scrollbar.grid(row=0, column=1, sticky="ns")

        x_scrollbar.grid(row=1, column=0, sticky="ew")

        # Make tree expand
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        return container, tree

    # ------------------------------------------------------------------
    # Selection
    # ------------------------------------------------------------------
    def bind_select(self, callback):
        self._tree.bind("<<TreeviewSelect>>", callback)

    def selection(self):
        return self._tree.selection()

    def select(self, row_id):
        self._tree.selection_set(row_id)
        self._tree.see(row_id)

    def select_last(self):
        row_ids = self.get_ids()
        if row_ids:
            self.select(row_ids[-1])

    # ------------------------------------------------------------------
    # Columns
    # ------------------------------------------------------------------
    def set_visible_columns(self, columns):
        self._tree["displaycolumns"] = columns

    # ------------------------------------------------------------------
    # Row CRUD
    # ------------------------------------------------------------------
    def get_ids(self):
        return self._tree.get_children("")

    def get(self, row_id):
        return self._tree.item(row_id, "values")

    def create(self, row_id, values, index="end"):
        self._tree.insert("", index, iid=row_id, values=values)

    def submit(self, row_id, values, sort_column_index=0):
        """
        Insert a row, keeping rows sorted (descending) by the given column,
        assuming rows are usually appended in order already.
        """
        sort_key = self.columns[sort_column_index]

        try:
            new_val = float(values[sort_column_index])
        except (ValueError, TypeError):
            new_val = values[sort_column_index]

        insert_index = "end"

        # Search from the bottom up (since packets usually arrive sequentially)
        for child in reversed(self.get_ids()):
            current_val_str = self._tree.set(child, sort_key)

            try:
                current_val = float(current_val_str)
            except (ValueError, TypeError):
                current_val = current_val_str

            # If the existing row is smaller than or equal to our new row,
            # it means our row belongs right AFTER this row.
            if current_val <= new_val:
                insert_index = self._tree.index(child) + 1
                break

        self.create(row_id, values, index=insert_index)

    def edit(self, row_id, values):
        self._tree.item(row_id, values=values)

    def delete(self, row_id):
        self._tree.delete(row_id)

    def clear(self):
        self._tree.delete(*self.get_ids())

    def count(self):
        return len(self.get_ids())

    def trim_oldest(self, overflow_count):
        row_ids = self.get_ids()
        for i in range(overflow_count):
            self.delete(row_ids[i])

    # ------------------------------------------------------------------
    # Scrolling
    # ------------------------------------------------------------------
    def scroll_to_bottom(self):
        self._tree.yview_moveto(1)
