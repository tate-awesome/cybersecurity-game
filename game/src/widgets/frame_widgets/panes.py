from PySide6.QtCore import Qt
from PySide6.QtWidgets import QSplitter, QVBoxLayout, QWidget
from ...app_core import Context

class Panes(QSplitter):

    def __init__(self, master: QWidget, context: Context, direction = "horizontal", child_count: int = 3, child_sizes: list[int] = [4, 3, 2], pad_around = True):
        '''
        Args:
            child_sizes: pane size is (approximately) proportional to 1/child_size[i],
            used as this QSplitter's initial stretch factors - e.g. child_size = [3, 2, 1]
            means the first pane starts smallest and the last starts biggest. Purely a
            starting point: the user can drag any sash afterwards (see get_weights, which
            is how a dragged layout gets remembered across sessions).
        '''
        if not direction in ["horizontal", "vertical"] or child_count < 2:
            raise ValueError(
                f"Invalid Panes args: direction={direction!r} (must be 'horizontal' or 'vertical'), "
                f"child_count={child_count!r} (must be >= 2)"
            )

        orientation = Qt.Orientation.Horizontal if direction == "horizontal" else Qt.Orientation.Vertical
        super().__init__(orientation, master)

        self.panels = []
        self.context = context
        self.direction = direction
        style = context.style

        master.layout().addWidget(self)
        margin = style.igap if pad_around else 0
        master.layout().setContentsMargins(margin, margin, margin, margin)

        self.setHandleWidth(style.igap)
        color = style.color("root")
        self.setStyleSheet(style.themed(f"QSplitter::handle {{ background-color: {color}; }} QSplitter > QWidget {{ background-color: {color}; }}"))

        min_size = style.PANE_MIN_WIDTH if direction == "horizontal" else style.PANE_MIN_HEIGHT
        initial_sizes = []
        for i in range(child_count):
            pane = QWidget()
            pane.setLayout(QVBoxLayout())
            pane.layout().setContentsMargins(0, 0, 0, 0)
            if direction == "horizontal":
                pane.setMinimumWidth(min_size)
            else:
                pane.setMinimumHeight(min_size)

            self.addWidget(pane)
            self.setCollapsible(i, False)
            stretch = max(1, round(1000 / child_sizes[i]))
            self.setStretchFactor(i, stretch)
            initial_sizes.append(stretch)
            self.panels.append(pane)

        # setStretchFactor alone only governs how a *later* resize
        # distributes new space - the initial split needs an explicit
        # setSizes() call. Qt normalizes these proportionally to whatever
        # real width/height the splitter ends up with, so the exact
        # numbers don't matter, only their ratios.
        self.setSizes(initial_sizes)

    def pane(self, index: int):
        if hasattr(self, "panels"):
            return self.panels[index]

    def get_weights(self) -> dict:
        '''
        Reads this Panes' current sash-adjusted sizes back out as a
        {"orientation", "children": [{"weight": ..., "panes": {...}}]}
        tree in the same shape as a page's own pane-tree config, so it
        can be saved and later merged back on top of that page's
        defaults (matched by position, not by any "key" - see
        PageManager.merge_pane_weights). Recurses into any pane whose
        sole child is itself a nested Panes, found from the live widget
        hierarchy rather than any separately tracked structure.
        '''
        sizes = self.sizes()
        children = []
        for i, pane in enumerate(self.panels):
            child = {"weight": sizes[i]}
            nested = next(iter(pane.findChildren(Panes, options=Qt.FindChildOption.FindDirectChildrenOnly)), None)
            if nested is not None:
                child["panes"] = nested.get_weights()
            children.append(child)
        return {"orientation": self.direction, "children": children}