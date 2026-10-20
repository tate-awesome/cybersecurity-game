'''
Docking: panels a user can pick up by their menu bar and drop somewhere
else in the same layout - beside another panel (splitting its pane), or
onto it as a tab (stacking them in one pane), like an IDE's editor groups.

Three pieces:

  - The layout model: plain dicts, converted from and back to the
    layout_tree PageManager.layout_tree makes from a page config's
    "layout_shape" and "layout_weights". A split {"id", "weight",
    "orientation", "children"} holds splits and leaves; a leaf {"id",
    "weight", "panels", "current"} is one pane, holding one panel (its id
    is that panel's) or a tab stack of several (its id is "tabs_<n>").
    split_at/add_tab/remove_panel change it, and normalize keeps it
    minimal: no empty or one-child splits, no split inside one running the
    same way. Any layout can be built from drops alone.
  - TabbedPane: what fills each leaf's pane - its panels stacked, only
    the current one showing. With more than one, each panel's menu bar
    shows a TabStrip in its title's place: every tab's title, its own
    highlighted, and "···" for those there's no room for.
  - DockArea: builds the Panes/TabbedPane skeleton for a layout, holds
    every panel (built once, moved from skeleton to skeleton as the layout
    changes), and runs the drag: pressing a panel's menu bar (its empty
    space, its title or a tab) and moving picks the panel up - it leaves
    the layout, and a chip with its title follows the mouse - and
    releasing it over a pane docks it there. While it's held, a
    see-through rectangle shows where it'd land (see DockArea.target_at).
    It also minimizes panes, a pane at a time or whole groups laid flat
    (see DockArea's Minimizing section).

Like drag_drop's drags, it's plain mouse events and widgets floating over
the window, not the system's drag and drop - so it works the same on every
platform and window system, and as root under sudo.
'''
import copy
from collections.abc import Callable
from dataclasses import dataclass

from PySide6.QtCore import QEvent, QObject, QPoint, QRect, QSize, Qt, QTimer, Signal
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import QAbstractButton, QApplication, QHBoxLayout, QLabel, QPushButton, QStackedLayout, QVBoxLayout, QWidget

from ...app_core import Context
from ...app_core.context.style import PANEL_BORDER_WIDTH
from .overlay import Overlay
from .panes import Panes
from .window_chrome import WindowBarButton

EDGES = ("left", "right", "top", "bottom")
SPLIT_PREFIXES = {"horizontal": "h_panes", "vertical": "v_panes"}
TAB_PREFIX = "tabs"
# A pane's tab hitbox is its middle, this far in from each edge (as a share
# of its width/height); the rest is four trapezoids, one per edge, that split it
CENTER_INSET = 0.25
# How thick each band along a pane's edge is that docks beside a whole
# group the pane's edge runs along, instead of the pane itself (see target_at)
GROUP_BAND = 18
# The tab strip's "more tabs" button
MORE_TABS = "···"
# A menu bar button's height, by font (see TabbedPane.thickness)
_BUTTON_HEIGHTS: dict[str, int] = {}


# Qt's "no maximum" size
QWIDGETSIZE_MAX = (1 << 24) - 1


# Layout model

def from_tree(tree: dict) -> dict:
    '''A layout_tree (see PageManager.layout_tree) as a split - see the module docstring.'''
    def split(node: dict, weight: float) -> dict:
        children = []
        for child in node.get("children", []):
            if "panes" in child:
                children.append(split(child["panes"], child["weight"]))
            else:
                panels = list(child["tabs"]) if "tabs" in child else [child["id"]]
                children.append(leaf(panels, child["id"], child["weight"]))
        return {"id": node["id"], "weight": weight, "orientation": node["orientation"], "children": children}
    return split(tree, 1)


def to_tree(root: dict) -> dict:
    '''A split back as a layout_tree.'''
    children = []
    for child in root["children"]:
        if "children" in child:
            children.append({"id": child["id"], "weight": child["weight"], "panes": to_tree(child)})
        elif len(child["panels"]) > 1:
            children.append({"id": child["id"], "weight": child["weight"], "tabs": list(child["panels"])})
        else:
            panel_id = child["panels"][0]
            children.append({"id": panel_id, "weight": child["weight"], "widget": panel_type(panel_id)})
    return {"id": root["id"], "orientation": root["orientation"], "children": children}


def leaf(panels: list[str], leaf_id: str | None = None, weight: float = 1) -> dict:
    return {"id": leaf_id or panels[0], "weight": weight, "panels": panels, "current": panels[0]}


def panel_type(panel_id: str) -> str:
    '''The panel type a layout id names - see PageManager.panel_type.'''
    base, _, number = panel_id.rpartition("_")
    return base if base and number.isdigit() else panel_id


def is_split(node: dict) -> bool:
    return "children" in node


def walk(node: dict, parents: tuple = ()):
    '''Every node from node down, each with its parents (outermost first).'''
    yield node, parents
    if is_split(node):
        for child in node["children"]:
            yield from walk(child, parents + (node,))


def find(root: dict, node_id: str) -> tuple[dict | None, tuple]:
    for node, parents in walk(root):
        if node["id"] == node_id:
            return node, parents
    return None, ()


def leaf_of(root: dict, panel_id: str) -> dict | None:
    for node, _ in walk(root):
        if not is_split(node) and panel_id in node["panels"]:
            return node
    return None


def panel_ids(root: dict | None) -> list[str]:
    if root is None:
        return []
    return [panel for node, _ in walk(root) if not is_split(node) for panel in node["panels"]]


def new_id(root: dict | None, prefix: str) -> str:
    '''prefix plus one past the highest number in use with it.'''
    numbers = [0]
    for node, _ in walk(root) if root is not None else ():
        for node_id in [node["id"], *node.get("panels", ())]:
            base, _, number = node_id.rpartition("_")
            if base == prefix and number.isdigit():
                numbers.append(int(number))
    return f"{prefix}_{max(numbers) + 1}"


def normalize(root: dict | None) -> dict | None:
    '''
    The smallest layout showing the same thing (see the module docstring),
    with a split on top - or None, with no panels left. A leaf's id follows
    its panels: the panel's own for one, a tabs_<n> id for several.
    '''
    def tidy(node: dict) -> dict | None:
        if not is_split(node):
            if not node["panels"]:
                return None
            if node["current"] not in node["panels"]:
                node["current"] = node["panels"][0]
            return node
        children = []
        for child in node["children"]:
            child = tidy(child)
            if child is None:
                continue
            if is_split(child) and child["orientation"] == node["orientation"]:
                # Running the same way: its children are this split's, in its share of it
                total = sum(grandchild["weight"] for grandchild in child["children"]) or 1
                for grandchild in child["children"]:
                    grandchild["weight"] = grandchild["weight"] / total * child["weight"]
                children.extend(child["children"])
            else:
                children.append(child)
        if not children:
            return None
        if len(children) == 1:
            children[0]["weight"] = node["weight"]
            return children[0]
        node["children"] = children
        return node

    root = tidy(root) if root is not None else None
    if root is None:
        return None
    if not is_split(root):
        root = {"id": new_id(root, SPLIT_PREFIXES["horizontal"]), "weight": 1, "orientation": "horizontal", "children": [root]}
    for node, _ in walk(root):
        if not is_split(node):
            if len(node["panels"]) == 1:
                node["id"] = node["panels"][0]
            elif panel_type(node["id"]) != TAB_PREFIX:
                node["id"] = new_id(root, TAB_PREFIX)
    return root


def remove_panel(root: dict, panel_id: str) -> dict | None:
    node = leaf_of(root, panel_id)
    if node is not None:
        index = node["panels"].index(panel_id)
        node["panels"].remove(panel_id)
        if node["current"] == panel_id and node["panels"]:
            # The tab beside it shows instead
            node["current"] = node["panels"][min(index, len(node["panels"]) - 1)]
    return normalize(root)


def add_tab(root: dict, leaf_id: str, panel_id: str, index: int | None = None) -> dict:
    node, _ = find(root, leaf_id)
    index = len(node["panels"]) if index is None else max(0, min(index, len(node["panels"])))
    node["panels"].insert(index, panel_id)
    node["current"] = panel_id
    return normalize(root)


def split_at(root: dict | None, target_id: str | None, edge: str, panel_id: str) -> dict:
    '''
    Docks panel_id in a new pane on one edge of the node target_id (a pane
    or a whole group), splitting it: the new pane takes half its room.
    With no layout at all, the panel is the whole layout.
    '''
    new = leaf([panel_id])
    if root is None:
        return normalize(new)
    orientation = "horizontal" if edge in ("left", "right") else "vertical"
    before = edge in ("left", "top")
    target, parents = find(root, target_id)
    parent = parents[-1] if parents else None
    if parent is not None and parent["orientation"] == orientation:
        index = parent["children"].index(target)
        target["weight"] = new["weight"] = target["weight"] / 2
        parent["children"].insert(index if before else index + 1, new)
    else:
        split = {"id": new_id(root, SPLIT_PREFIXES[orientation]), "weight": target["weight"], "orientation": orientation,
                 "children": [new, target] if before else [target, new]}
        target["weight"] = new["weight"] = 1
        if parent is None:
            root = split
        else:
            parent["children"][parent["children"].index(target)] = split
    return normalize(root)


def drain_evenly(sizes: list[float], floors: list[float], amount: float) -> list[float]:
    '''
    Takes up to amount from sizes in all, never one below its floor -
    always from the biggest first, in lockstep, like water draining off the
    tallest bars evenly: two that started at different sizes end up level
    (or at a floor) before either drops further. How a restored pane takes
    its room back from its neighbours (see DockArea.lay_out_split).
    '''
    sizes = [float(size) for size in sizes]
    remaining = float(amount)
    while remaining > 1e-6:
        room = [i for i in range(len(sizes)) if sizes[i] - floors[i] > 1e-6]
        if not room:
            break
        tallest = max(sizes[i] for i in room)
        top = [i for i in room if abs(sizes[i] - tallest) < 1e-6]
        lower = [size for size in sizes if size < tallest - 1e-6]
        boundary = max(max(lower) if lower else min(floors[i] for i in top), min(floors[i] for i in top))
        take = min((tallest - boundary) * len(top), remaining)
        if take <= 1e-9:
            break
        for i in top:
            sizes[i] -= take / len(top)
        remaining -= take
    return sizes


# Panes

class TabStrip(QWidget):
    '''
    The tabs of a TabbedPane, in one of its panels' menu bars in the
    title's place (see MenuBar.set_title_widget): every panel's title, the
    menu bar's own panel highlighted. Clicking another calls select with
    its panel id. Too narrow for them all, it shows what fits - always its
    own - and MORE_TABS, which lists the rest.
    '''

    def __init__(self, context: Context, tabs: list[tuple[str, str]], own: str, select: Callable[[str], None]):
        super().__init__()
        self.context = context
        self.style = context.style
        self.own = own
        self.select = select
        row = QHBoxLayout(self)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(self.style.cgap * 2)
        self.buttons: dict[str, QPushButton] = {}
        for panel_id, title in tabs:
            button = WindowBarButton(title)
            button.setFont(self.style.get_font())
            button.setProperty("dock_panel_id", panel_id)
            active = panel_id == own
            self.style.live_style(button, lambda active=active: self.tab_sheet(active))
            if not active:
                button.clicked.connect(lambda checked=False, panel_id=panel_id: self.select(panel_id))
            row.addWidget(button, 0, Qt.AlignmentFlag.AlignVCenter)
            self.buttons[panel_id] = button
        self.more = WindowBarButton(MORE_TABS)
        self.more.setFont(self.style.get_font())
        self.more.setToolTip(context.labels.get("menu_bar_tooltips_more_tabs"))
        row.addWidget(self.more, 0, Qt.AlignmentFlag.AlignVCenter)
        row.addStretch()
        self.more_overlay = Overlay(context.root, context, self.more, self.populate_more, closed_text=MORE_TABS, open_text=MORE_TABS)
        self.hidden: list[str] = []
        self.fit()

    def tab_sheet(self, active: bool) -> str:
        '''A tab reads as text, not a button - the menu bar's own panel's underlined in the accent.'''
        text = self.style.color("text")
        if active:
            return (f"QPushButton {{ background: transparent; border: none; border-radius: 0px; color: {text};"
                    f" border-bottom: 2px solid {self.style.color('accent')}; padding: 0px 4px; }}")
        muted = QColor(text)
        muted.setAlphaF(0.6)
        return (f"QPushButton {{ background: transparent; border: none; color: {muted.name(QColor.NameFormat.HexArgb)};"
                f" border-bottom: 2px solid transparent; padding: 0px 4px; }}"
                f" QPushButton:hover {{ color: {text}; }}")

    def sizeHint(self) -> QSize:
        # Its own tab and MORE_TABS - the menu bar's buttons squash before
        # this does (see MenuBar._update_squashing), and it stretches into
        # whatever room they leave
        spacing = self.layout().spacing()
        own = self.buttons[self.own].sizeHint()
        width = own.width() + spacing + self.more.sizeHint().width()
        return QSize(width, max(own.height(), self.more.sizeHint().height()))

    def minimumSizeHint(self) -> QSize:
        return self.sizeHint()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.fit()

    def fit(self):
        '''Shows the tabs that fit, in order - its own always - and MORE_TABS if any don't.'''
        spacing = self.layout().spacing()
        widths = {panel_id: button.sizeHint().width() + spacing for panel_id, button in self.buttons.items()}
        room = self.width()
        if sum(widths.values()) <= room:
            shown = set(self.buttons)
        else:
            room -= widths[self.own] + self.more.sizeHint().width()
            shown = {self.own}
            for panel_id in self.buttons:
                if panel_id != self.own and widths[panel_id] <= room:
                    shown.add(panel_id)
                    room -= widths[panel_id]
        self.hidden = [panel_id for panel_id in self.buttons if panel_id not in shown]
        for panel_id, button in self.buttons.items():
            button.setVisible(panel_id in shown)
        self.more.setVisible(bool(self.hidden))

    def populate_more(self, overlay: Overlay):
        for panel_id in self.hidden:
            button = QPushButton(self.buttons[panel_id].text())
            button.setFont(self.style.get_font())
            button.clicked.connect(lambda checked=False, panel_id=panel_id: (overlay.close_chain(), self.select(panel_id)))
            overlay.layout().addWidget(button)

    def insert_index(self, pos: QPoint) -> int:
        '''Where a tab dropped at pos (in this strip) would go among them all.'''
        order = list(self.buttons)
        for panel_id in order:
            button = self.buttons[panel_id]
            if button.isVisible() and pos.x() < button.geometry().center().x():
                return order.index(panel_id)
        shown = [panel_id for panel_id in order if self.buttons[panel_id].isVisible()]
        return order.index(shown[-1]) + 1 if shown else len(order)

    def insert_x(self, index: int) -> int:
        '''Where in this strip (x) the gap a tab dropped at index would go in is.'''
        order = list(self.buttons)
        shown = [panel_id for panel_id in order if self.buttons[panel_id].isVisible()]
        after = [panel_id for panel_id in shown if order.index(panel_id) >= index]
        if after:
            return self.buttons[after[0]].geometry().left() - self.layout().spacing() // 2
        return self.buttons[shown[-1]].geometry().right() + self.layout().spacing() // 2 if shown else 0


class _SideTitle(QWidget):
    '''A panel's title, turned to read down a sideways strip (see _SideStrip).'''

    def __init__(self, context: Context, text: str, current: bool):
        super().__init__()
        self.style = context.style
        self.text = text
        self.current = current
        self.setFont(self.style.get_font())
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def sizeHint(self) -> QSize:
        metrics = self.fontMetrics()
        pad = self.style.igap
        return QSize(metrics.height(), metrics.horizontalAdvance(self.text) + pad)

    def minimumSizeHint(self) -> QSize:
        return QSize(self.fontMetrics().height(), 0)

    def paintEvent(self, event):
        painter = QPainter(self)
        color = QColor(self.style.color("text"))
        if not self.current:
            color.setAlphaF(0.6)
        painter.setPen(color)
        # A quarter turn clockwise: it reads top to bottom
        painter.translate(self.width(), 0)
        painter.rotate(90)
        painter.drawText(QRect(0, 0, self.height(), self.width()),
                         Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, self.text)
        painter.end()


class _SideStrip(QWidget):
    '''
    A minimized pane laid flat the other way (see DockArea.lay_out_minimized):
    a thin upright panel with its restore button at the top and its tabs'
    titles turned sideways below - each a handle to pick its panel up by,
    or click to peek at it (see DockArea.peek).
    '''

    def __init__(self, context: Context, tabs: list[tuple[str, str]], current: str, restore: Callable[[str | None], None],
                 watch: Callable[[QWidget, str], None] | None):
        super().__init__()
        self.style = context.style
        self.setProperty("shadowed", True)
        column = QVBoxLayout(self)
        left, top, right, bottom = self.style.panel_margins()
        border = PANEL_BORDER_WIDTH
        gap = self.style.igap // 2
        column.setContentsMargins(left + border, top + border + gap, right + border, bottom + border + gap)
        column.setSpacing(self.style.igap)
        from .menu_bar import RESTORE_ICON, bare_icon  # here - menu_bar imports this module's package
        button = bare_icon(context, WindowBarButton(self.style.icon(RESTORE_ICON)))
        button.setToolTip(context.labels.get("menu_bar_buttons_maximize"))
        button.clicked.connect(lambda checked=False: restore(None))
        column.addWidget(button, 0, Qt.AlignmentFlag.AlignHCenter)
        for panel_id, title in tabs:
            label = _SideTitle(context, title, panel_id == current)
            column.addWidget(label, 0, Qt.AlignmentFlag.AlignHCenter)
            if watch is not None:
                watch(label, panel_id)
        column.addStretch()

    def minimumSizeHint(self) -> QSize:
        return QSize(0, 0)

    def paintEvent(self, event):
        from ..panels.panel import paint_panel  # here - panels import this module's package
        painter = QPainter(self)
        paint_panel(painter, self.style, self.width(), self.height())
        painter.end()


class _LentPlaceholder(QWidget):
    '''Where a minimized panel's bar was while it's out being peeked at (see TabbedPane.lend): its title, faint.'''

    def __init__(self, context: Context, title: str):
        super().__init__()
        self.style = context.style
        self.title = title
        self.setFont(self.style.get_font())

    def minimumSizeHint(self) -> QSize:
        return QSize(0, 0)

    def paintEvent(self, event):
        from ..panels.panel import paint_panel  # here - panels import this module's package
        painter = QPainter(self)
        paint_panel(painter, self.style, self.width(), self.height())
        color = QColor(self.style.color("text"))
        color.setAlphaF(0.45)
        painter.setPen(color)
        left, top, right, bottom = self.style.panel_margins()
        room = self.rect().adjusted(left + self.style.igap * 2, top, -right, -bottom)
        painter.drawText(room, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, self.title)
        painter.end()


class TabbedPane(QWidget):
    '''
    Fills a pane with one or more panels, stacked - only the current one
    showing. With more than one, each panel's menu bar shows a TabStrip
    for switching between them.

    A pane is shown in one of three forms (see set_form): "open"; "bar" -
    minimized to just its menu bar, bodies hidden; or "side" - minimized
    the other way, a _SideStrip of its titles turned sideways.

    panels are (panel id, panel) pairs; watch(widget, panel id) is called
    on every tab, so whoever made this can make it a handle to pick that
    panel up by (see DockArea); switched(panel id) on every switch, and
    restore(panel id or None) when a sideways title or its button's clicked.
    '''

    def __init__(self, master: QWidget, context: Context, panels: list[tuple[str, QWidget]], current: str | None = None,
                 switched: Callable[[str], None] | None = None, watch: Callable[[QWidget, str], None] | None = None,
                 restore: Callable[[str | None], None] | None = None):
        super().__init__(master)
        self.context = context
        self.style = context.style
        self.switched = switched
        self.watch = watch
        self.restore = restore
        master.layout().addWidget(self, 1)
        self.stack = QStackedLayout(self)
        self.stack.setContentsMargins(0, 0, 0, 0)
        self.panels: dict[str, QWidget] = {}
        for panel_id, panel in panels:
            self.panels[panel_id] = panel
            self.stack.addWidget(panel)
        self.tabs = [(panel_id, panel.menu_bar.title()) for panel_id, panel in panels if getattr(panel, "menu_bar", None) is not None]
        for panel_id, panel in panels:
            menu_bar = getattr(panel, "menu_bar", None)
            if menu_bar is None:
                continue
            if len(panels) > 1:
                strip = TabStrip(context, self.tabs, panel_id, self.set_current)
                menu_bar.set_title_widget(strip)
                if watch is not None:
                    watch(strip, panel_id)
                    for tab_id, button in strip.buttons.items():
                        watch(button, tab_id)
            else:
                menu_bar.set_title_widget(None)
        self.form = "open"
        self.side: _SideStrip | None = None
        self.lent: QWidget | None = None
        self.current = None
        self.set_current(current if current in self.panels else next(iter(self.panels)))

    def minimumSizeHint(self):
        # Like the pane it's in (see _PaneContainer): only the pane's own floor counts
        return QSize(0, 0)

    def set_current(self, panel_id: str):
        if panel_id == self.current:
            return
        self.current = panel_id
        if self.form == "side":
            self.set_form("side")  # its titles show which is current
        else:
            self.stack.setCurrentWidget(self.panels[panel_id])
        if self.switched is not None:
            self.switched(panel_id)

    def current_panel(self) -> QWidget:
        return self.panels[self.current]

    def set_form(self, form: str):
        '''Shows the pane "open", minimized as a "bar" (its menu bar), or minimized to the "side" (see the class docstring).'''
        self.form = form
        for panel in self.panels.values():
            menu_bar = getattr(panel, "menu_bar", None)
            if menu_bar is not None:
                menu_bar.show_minimized(form != "open")
        if self.side is not None:
            self.stack.removeWidget(self.side)
            self.side.deleteLater()
            self.side = None
        if form == "side":
            self.side = _SideStrip(self.context, self.tabs, self.current, self.restore or (lambda panel_id: None), self.watch)
            self.stack.addWidget(self.side)
            self.stack.setCurrentWidget(self.side)
        else:
            self.stack.setCurrentWidget(self.panels[self.current])

    def lend(self, panel_id: str) -> QWidget:
        '''Takes a panel out to be shown somewhere else for a while (see DockArea.peek) - give it back with take_back.'''
        panel = self.panels[panel_id]
        self.stack.removeWidget(panel)
        if self.form != "side":
            # Its menu bar's gone with it - a stand-in keeps the pane's place
            title = panel.menu_bar.title() if getattr(panel, "menu_bar", None) is not None else ""
            self.lent = _LentPlaceholder(self.context, title)
            self.stack.addWidget(self.lent)
            self.stack.setCurrentWidget(self.lent)
        return panel

    def take_back(self, panel_id: str):
        if self.lent is not None:
            self.stack.removeWidget(self.lent)
            self.lent.deleteLater()
            self.lent = None
        self.stack.insertWidget(list(self.panels).index(panel_id), self.panels[panel_id])
        self.set_form(self.form)

    def thickness(self) -> int:
        '''
        How thick it is minimized, either way: a panel menu bar's height
        (its buttons' and the room around them - the same for every panel,
        so minimized panes line up, and measurable while hidden) and the
        panel's frame around it.
        '''
        font = self.style.get_font()
        key = font.toString()
        if key not in _BUTTON_HEIGHTS:
            sample = QPushButton("Ag")
            sample.setFont(font)
            sample.ensurePolished()
            _BUTTON_HEIGHTS[key] = sample.sizeHint().height()
            sample.deleteLater()
        _, top, _, bottom = self.style.panel_margins()
        bar = _BUTTON_HEIGHTS[key] + 4 * self.style.cgap
        return bar + top + bottom + 2 * PANEL_BORDER_WIDTH + self.style.setting("panel_frame")


# Dragging

class _Grip(QObject):
    '''
    Watches the widgets a panel can be picked up by - its menu bar, title
    and tabs, each marked with the "dock_panel_id" it picks up - and starts
    a DockArea drag once one's pressed and the mouse moves past the
    platform's drag distance - or, pressed and let go without moving, tells
    it the title was clicked.
    '''

    def __init__(self, area: "DockArea"):
        super().__init__(area)
        self.area = area
        self.pressed: tuple[QPoint, str, QObject] | None = None

    def eventFilter(self, watched, event):
        kind = event.type()
        if kind == QEvent.Type.MouseButtonPress and event.button() == Qt.MouseButton.LeftButton:
            panel_id = watched.property("dock_panel_id")
            # The same press, passed up from a title to its menu bar, keeps the title's
            if panel_id and (self.pressed is None or self.pressed[1] != panel_id or event.globalPosition().toPoint() != self.pressed[0]):
                self.pressed = (event.globalPosition().toPoint(), panel_id, watched)
        elif kind == QEvent.Type.MouseMove and event.buttons() & Qt.MouseButton.LeftButton and self.pressed is not None:
            at = event.globalPosition().toPoint()
            if (at - self.pressed[0]).manhattanLength() >= QApplication.startDragDistance():
                _, panel_id, source = self.pressed
                self.pressed = None
                if isinstance(source, QAbstractButton):
                    source.setDown(False)  # a tab: it's picked up, not clicked
                self.area.begin_drag(panel_id, at)
                return True
        elif kind == QEvent.Type.MouseButtonRelease and self.pressed is not None:
            # A click, not a drag: on a minimized pane's title, it peeks at the panel (see DockArea.peek)
            _, panel_id, source = self.pressed
            self.pressed = None
            if event.button() == Qt.MouseButton.LeftButton and not isinstance(source, QAbstractButton):
                QTimer.singleShot(0, lambda: self.area.title_clicked(panel_id, source))
        return False


class _SashGrip(QObject):
    '''Remembers every open pane's size when a divider is pressed - what one dragged down to minimized goes back to.'''

    def __init__(self, area: "DockArea"):
        super().__init__(area)
        self.area = area

    def eventFilter(self, watched, event):
        if event.type() == QEvent.Type.MouseButtonPress and self.area.root is not None:
            self.area.remember_open_sizes(self.area.collapsed())
        return False


class _Chip(QLabel):
    '''
    What follows the mouse while a panel's held: its title on a card.
    Holds the mouse and keyboard until it's dropped, so it gets every move
    wherever the mouse goes - the menu bar it was picked up by is gone.
    '''

    def __init__(self, area: "DockArea", title: str):
        super().__init__(title, area.window())
        self.area = area
        style = area.style
        self.setFont(style.get_font("default"))
        gap = style.cgap * 4
        self.setContentsMargins(gap * 2, gap, gap * 2, gap)
        style.set_material(self, "card", rounded=True, outlined=True)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
        self.adjustSize()
        self.setCursor(Qt.CursorShape.ClosedHandCursor)

    def follow(self, at: QPoint):
        # Just below and right of the pointer, so it doesn't hide where it's pointing
        offset = QPoint(self.area.style.igap, self.area.style.igap)
        pos = self.parentWidget().mapFromGlobal(at) + offset
        # Kept in the window - it's just as easily read flipped to the pointer's other side
        room = self.parentWidget().rect()
        if pos.x() + self.width() > room.right():
            pos.setX(pos.x() - self.width() - 2 * offset.x())
        if pos.y() + self.height() > room.bottom():
            pos.setY(pos.y() - self.height() - 2 * offset.y())
        self.move(pos)

    def mouseMoveEvent(self, event):
        self.area.drag_to(event.globalPosition().toPoint())

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.area.end_drag(event.globalPosition().toPoint(), drop=True)

    def event(self, event):
        # Esc is the pause menu's shortcut (see KeyBinds) - while a panel's
        # held, it puts the panel back instead
        if event.type() == QEvent.Type.ShortcutOverride and event.key() == Qt.Key.Key_Escape:
            event.accept()
            return True
        return super().event(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.area.end_drag(QPoint(), drop=False)


class _DropPreview(QWidget):
    '''Over the whole window while a panel's held: a see-through rectangle where it'd land, and for a tab, the gap it'd go in.'''

    def __init__(self, area: "DockArea"):
        super().__init__(area.window())
        self.area = area
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.rect_at: QRect | None = None
        self.line_at: QRect | None = None
        self.setGeometry(self.parentWidget().rect())

    def show_target(self, rect: QRect | None, line: QRect | None):
        if rect != self.rect_at or line != self.line_at:
            self.rect_at, self.line_at = rect, line
            self.update()

    def paintEvent(self, event):
        if self.rect_at is None:
            return
        style = self.area.style
        accent = QColor(style.color("accent"))
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        fill = QColor(accent)
        fill.setAlphaF(0.22)
        edge = QColor(accent)
        edge.setAlphaF(0.8)
        painter.setPen(QPen(edge, 2))
        painter.setBrush(fill)
        radius = style.PANEL_RADIUS
        painter.drawRoundedRect(self.rect_at.adjusted(2, 2, -2, -2), radius, radius)
        if self.line_at is not None:
            painter.fillRect(self.line_at, accent)
        painter.end()


class _Peek(QWidget):
    '''
    A minimized panel, lent out of its pane and shown open in a popup by
    it (see DockArea.peek) - to look at or use without restoring the pane.
    Closes like any popup, on a click outside it or Esc, and hands the
    panel back.
    '''

    def __init__(self, area: "DockArea", panel: QWidget, closed: Callable[[], None]):
        super().__init__(area.window(), Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.style = area.style
        self.closed = closed
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(panel)
        panel.show()

    def paintEvent(self, event):
        # The page's window material under the panel, as on the page - a
        # see-through panel would otherwise show whatever's under the popup
        from ..panels.panel import paint_panel  # here - panels import this module's package
        painter = QPainter(self)
        paint_panel(painter, self.style, self.width(), self.height(), on_window=True)
        painter.end()

    def hideEvent(self, event):
        super().hideEvent(event)
        closed, self.closed = self.closed, None
        if closed is not None:
            closed()


@dataclass
class DropTarget:
    '''
    Where a held panel would land: kind "tab" (into leaf node_id's tabs at
    index), "split" (a new pane on edge of node node_id - a pane or a
    group) or "fill" (the whole, empty layout). rect is where it'd show,
    and line where its tab would go, both in the DockArea.
    '''
    kind: str
    node_id: str | None
    rect: QRect
    edge: str | None = None
    index: int | None = None
    line: QRect | None = None


class DockArea(QWidget):
    '''
    A layout of panels the user can rearrange by dragging them (see the
    module docstring), filling master. tree is a layout_tree (see
    PageManager.layout_tree) or None for none; make_panel(panel id, parent)
    builds a panel - each once, kept for as long as it's in the layout.

    discard is a widget that takes panels dropped on it out of the layout
    for good (the layout editor's panel list); without one, a panel
    dropped anywhere it can't go goes back to where it was. changed is
    emitted whenever the layout's rearranged or a pane's resized.
    '''

    changed = Signal()

    def __init__(self, master: QWidget, context: Context, tree: dict | None, make_panel: Callable[[str, QWidget], QWidget],
                 transparent: bool = False, discard: QWidget | None = None, empty_text: str = ""):
        super().__init__(master)
        self.context = context
        self.style = context.style
        self.make_panel = make_panel
        self.transparent = transparent
        self.discard = discard
        self.empty_text = empty_text
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        if master.layout() is not None:
            master.layout().addWidget(self, 1)

        # Where panels wait while their skeleton's rebuilt, or while held
        self.shelf = QWidget(self)
        self.shelf.setLayout(QVBoxLayout())
        self.shelf.hide()
        self.grip = _Grip(self)
        self.sash_grip = _SashGrip(self)
        # The panel being peeked at, its pane and its popup (see peek)
        self.peeking: tuple[str, TabbedPane, _Peek] | None = None

        self.root = from_tree(tree) if tree else None
        self.panels: dict[str, QWidget] = {}
        for panel_id in panel_ids(self.root):
            self.add_panel(panel_id)

        self.host: QWidget | None = None
        self.root_panes: Panes | None = None
        self.splits: dict[str, Panes] = {}
        self.tabbed: dict[str, TabbedPane] = {}

        # While a panel's held: its id, whether it's new (see begin_drag), the layout to go back to, and what's drawn
        self.held: str | None = None
        self.held_new = False
        self.held_at = QPoint()
        self._relayout_queued = False
        self.before: dict | None = None
        self.chip: _Chip | None = None
        self.preview: _DropPreview | None = None
        self.build()

    # Panels
    def add_panel(self, panel_id: str) -> QWidget:
        panel = self.make_panel(panel_id, self.shelf)
        self.panels[panel_id] = panel
        menu_bar = getattr(panel, "menu_bar", None)
        if menu_bar is not None:
            for widget in (menu_bar, menu_bar.game_label):
                self.watch(widget, panel_id)
            menu_bar.minimize_clicked.connect(lambda panel_id=panel_id: self.toggle_minimized(panel_id))
        return panel

    def watch(self, widget: QWidget, panel_id: str):
        '''Makes widget a handle to pick panel_id up by.'''
        widget.setProperty("dock_panel_id", panel_id)
        widget.installEventFilter(self.grip)

    def panel_ids(self) -> list[str]:
        return panel_ids(self.root)

    # Building
    def build(self):
        '''Builds the skeleton for self.root and moves every panel into its place in it.'''
        for panel in self.panels.values():
            panel.setParent(self.shelf)
        if self.host is not None:
            self.layout().removeWidget(self.host)
            self.host.hide()
            self.host.deleteLater()
        self.host = QWidget()
        self.host.setLayout(QVBoxLayout())
        self.host.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(self.host)
        self.splits, self.tabbed = {}, {}
        if self.root is None:
            self.root_panes = None
            empty = QLabel(self.empty_text)
            empty.setFont(self.style.get_font("default"))
            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty.setWordWrap(True)
            self.host.layout().addWidget(empty)
        else:
            self.root_panes = self.build_split(self.root, self.host)
        # Minimized panes, once the new skeleton's in place
        self.relayout_soon()

    def build_split(self, node: dict, master: QWidget) -> Panes:
        children = node["children"]
        total = sum(child["weight"] for child in children) or 1
        divisors = [total / max(child["weight"], 1e-6) for child in children]
        panes = Panes(master, self.context, node["orientation"], len(children), divisors, False,
                      transparent=self.transparent, ids=[child["id"] for child in children])
        panes.splitterMoved.connect(lambda *_, node=node: (self.sash_moved(node), self.changed.emit()))
        for index in range(1, panes.count()):
            panes.handle(index).installEventFilter(self.sash_grip)
        self.splits[node["id"]] = panes
        for index, child in enumerate(children):
            pane = panes.pane(index)
            if is_split(child):
                self.build_split(child, pane)
            else:
                self.tabbed[child["id"]] = TabbedPane(
                    pane, self.context, [(panel_id, self.panels[panel_id]) for panel_id in child["panels"]], child["current"],
                    switched=lambda panel_id, child=child: child.__setitem__("current", panel_id), watch=self.watch,
                    restore=lambda panel_id, child=child: self.restore(child, panel_id))
        return panes

    # Reading it back
    def capture_sizes(self):
        '''
        Takes every pane's live size as its weight - what the user's dragged
        its sash to. Not a group that hasn't been laid out yet (just built,
        or never shown - the layout editor's preview on a tab not opened):
        its sizes are Qt's placeholders, and its weights are still right.
        '''
        if self.root is None:
            return
        collapsed = self.collapsed()
        for node, _ in walk(self.root):
            panes = self.splits.get(node["id"]) if is_split(node) else None
            if panes is None or not panes.isVisible() or panes.testAttribute(Qt.WidgetAttribute.WA_PendingResizeEvent):
                continue
            if collapsed[node["id"]] or any(collapsed[child["id"]] for child in node["children"]):
                continue  # minimized panes' sizes aren't theirs to keep - see minimize
            sizes = panes.sizes()
            if len(sizes) == len(node["children"]) and all(size > 0 for size in sizes):
                for child, size in zip(node["children"], sizes):
                    child["weight"] = size

    def layout_tree(self) -> dict | None:
        '''The layout as it is now, as a layout_tree - its weights each pane's live size.'''
        self.capture_sizes()
        return to_tree(self.root) if self.root is not None else None

    # Minimizing
    #
    # A pane minimizes along the group it's in, to just its menu bar,
    # handing its room to the open panes beside it evenly - and restoring,
    # takes back the size it had from them. Once every pane in a group is
    # minimized, the group minimizes the other way, along the group it's in
    # in turn: flat, its panes turned to sideways strips of titles (see
    # TabbedPane's "side" form). Restoring one pane in it opens the group
    # back up to its own size, that pane taking all the room its minimized
    # neighbours leave. A layout's top group never minimizes - nothing's
    # left to take its room.

    def toggle_minimized(self, panel_id: str):
        self.end_peek()
        node = leaf_of(self.root, panel_id) if self.root is not None else None
        if node is not None:
            self.minimize(node, not node.get("minimized", False))

    def restore(self, node: dict, panel_id: str | None = None):
        '''Restores a minimized pane - showing panel_id, if given.'''
        self.end_peek()
        if panel_id is not None and node["id"] in self.tabbed:
            self.tabbed[node["id"]].set_current(panel_id)
        self.minimize(node, False)

    def minimize(self, node: dict, minimized: bool):
        before = self.collapsed()
        self.remember_open_sizes(before)
        node["minimized"] = minimized
        self.lay_out_minimized(before)

    def collapsed(self) -> dict[str, bool]:
        '''Which nodes are minimized: a minimized pane, or a group (not the top one) whose panes all are.'''
        found = {}
        def visit(node: dict, top: bool) -> bool:
            if is_split(node):
                children = [visit(child, False) for child in node["children"]]
                found[node["id"]] = not top and all(children)
            else:
                found[node["id"]] = bool(node.get("minimized"))
            return found[node["id"]]
        if self.root is not None:
            visit(self.root, True)
        return found

    def thin_axis(self, parents: tuple, collapsed: dict[str, bool]) -> str:
        '''The way a minimized node is flattened: along the innermost group above it that's still open.'''
        for parent in reversed(parents):
            if not collapsed[parent["id"]]:
                return parent["orientation"]
        return parents[0]["orientation"] if parents else "vertical"

    def thickness(self, node: dict, axis: str) -> int:
        '''How thick a minimized node is along axis, the way it's flattened.'''
        if not is_split(node):
            tabbed = self.tabbed.get(node["id"])
            return tabbed.thickness() if tabbed is not None else self.style.igap * 4
        sizes = [self.thickness(child, axis) for child in node["children"]]
        if node["orientation"] == axis:
            panes = self.splits.get(node["id"])
            handle = panes.handleWidth() if panes is not None else 0
            return sum(sizes) + handle * (len(sizes) - 1)
        return max(sizes)

    def remember_open_sizes(self, collapsed: dict[str, bool]):
        '''Each open pane's size in its open group - what it goes back to when restored.'''
        for node, _ in walk(self.root) if self.root is not None else ():
            panes = self.splits.get(node["id"]) if is_split(node) else None
            if panes is None or collapsed[node["id"]] or panes.testAttribute(Qt.WidgetAttribute.WA_PendingResizeEvent):
                continue
            for child, size in zip(node["children"], panes.sizes()):
                if not collapsed[child["id"]] and size > 0:
                    child["open_size"] = size

    def sash_moved(self, node: dict):
        '''
        A divider in node's group was dragged: a pane dragged down to its
        title bar's thickness minimizes - and a group dragged that thin
        (across the way it stacks its panes) minimizes all its panes,
        laying it flat.
        '''
        before = self.collapsed()
        panes = self.splits.get(node["id"])
        if panes is None or before.get(node["id"]):
            return
        axis = node["orientation"]
        shrunk = [child for child, size in zip(node["children"], panes.sizes())
                  if not before[child["id"]] and self.can_minimize(child) and size <= self.thickness(child, axis) + self.style.igap]
        if not shrunk:
            return
        for child in shrunk:
            for inner, _ in walk(child):
                if not is_split(inner):
                    inner["minimized"] = True
        self.lay_out_minimized(before)

    def can_minimize(self, node: dict) -> bool:
        '''Whether every panel in node has a minimize button to restore it with (the layout editor's stand-ins don't).'''
        return all(getattr(getattr(self.panels.get(panel_id), "menu_bar", None), "minimize", None) is not None
                   for panel_id in panel_ids(node))

    def relayout_soon(self):
        if not self._relayout_queued:
            self._relayout_queued = True
            QTimer.singleShot(0, self._relayout)

    def _relayout(self):
        self._relayout_queued = False
        # Not until it's on screen with its real size - see showEvent
        if self.root is not None and self.isVisible() and not self.testAttribute(Qt.WidgetAttribute.WA_PendingResizeEvent):
            # Even with nothing minimized: every pane's floor is its title bar (see lay_out_split)
            self.lay_out_minimized(self.collapsed())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.relayout_soon()

    def showEvent(self, event):
        super().showEvent(event)
        self.relayout_soon()

    def lay_out_minimized(self, before: dict[str, bool]):
        '''
        Sizes every group's panes for which are minimized now, coming from
        before (which were then), and shows each pane in its form.
        '''
        if self.root is None or self.root_panes is None:
            return
        after = self.collapsed()
        self.lay_out_split(self.root, (), self.width(), self.height(), before, after)
        for node, parents in walk(self.root):
            tabbed = self.tabbed.get(node["id"])
            if tabbed is None:
                continue
            if not after[node["id"]]:
                form = "open"
            else:
                form = "bar" if self.thin_axis(parents, after) == "vertical" else "side"
            if form != tabbed.form:
                tabbed.set_form(form)

    def lay_out_split(self, node: dict, parents: tuple, width: int, height: int, before: dict, after: dict):
        panes = self.splits[node["id"]]
        children = node["children"]
        axis = node["orientation"]
        horizontal = axis == "horizontal"
        room = (width if horizontal else height) - panes.handleWidth() * (len(children) - 1)
        floor = self.style.PANE_MIN_WIDTH if horizontal else self.style.PANE_MIN_HEIGHT
        current = [float(size) for size in panes.sizes()]
        total = sum(current)
        if len(current) != len(children) or total <= 0 or panes.testAttribute(Qt.WidgetAttribute.WA_PendingResizeEvent):
            # Not laid out yet: its sizes are Qt's placeholders
            current = [float(child["weight"]) for child in children]
            total = sum(current) or 1
        current = [size / total * room for size in current]

        # Flattened along this group's own direction, a minimized pane is
        # just its thickness - but in a group minimized the other way, its
        # panes share the group's length, in their open proportions
        sharing = after[node["id"]] and self.thin_axis(parents + (node,), after) != axis
        kinds, sizes = [], []
        for child, size in zip(children, current):
            if after[child["id"]] and not sharing:
                kinds.append("flat")
                sizes.append(float(self.thickness(child, axis)))
            elif sharing:
                kinds.append("share")
                sizes.append(float(child.get("open_size") or child["weight"]))
            elif before.get(child["id"]):
                kinds.append("opened")  # restored: back to the size it had
                sizes.append(float(child.get("open_size") or size))
            else:
                kinds.append("open")
                sizes.append(size)

        if sharing:
            flat = sum(size for kind, size in zip(kinds, sizes) if kind == "flat")
            shares = sum(size for kind, size in zip(kinds, sizes) if kind == "share") or 1
            sizes = [size if kind == "flat" else size / shares * (room - flat) for kind, size in zip(kinds, sizes)]
        else:
            spare = room - sum(sizes)
            takers = [i for i, kind in enumerate(kinds) if kind == "open"] or [i for i, kind in enumerate(kinds) if kind == "opened"]
            if spare > 0 and takers:
                # Freed room goes to the open panes evenly
                for i in takers:
                    sizes[i] += spare / len(takers)
            elif spare < 0:
                # A restored pane takes its room back from the open panes, tallest first
                for group in ([i for i, kind in enumerate(kinds) if kind == "open"], [i for i, kind in enumerate(kinds) if kind == "opened"]):
                    if not group or spare >= 0:
                        continue
                    drained = drain_evenly([sizes[i] for i in group], [floor] * len(group), -spare)
                    spare += sum(sizes[i] for i in group) - sum(drained)
                    for i, size in zip(group, drained):
                        sizes[i] = size

        for index, (child, kind, size) in enumerate(zip(children, kinds, sizes)):
            pane = panes.pane(index)
            if kind == "flat":
                low, high = int(size), int(size)
            else:
                # Open, a pane can be dragged down to its title bar - which minimizes it (see sash_moved)
                low = self.thickness(child, axis) if self.can_minimize(child) else floor
                low, high = min(low, int(size)), QWIDGETSIZE_MAX
            if horizontal:
                pane.setMinimumWidth(low)
                pane.setMaximumWidth(high)
            else:
                pane.setMinimumHeight(low)
                pane.setMaximumHeight(high)
        panes.setSizes([max(0, round(size)) for size in sizes])

        for child, size in zip(children, sizes):
            if is_split(child):
                self.lay_out_split(child, parents + (node,), round(size) if horizontal else width,
                                   height if horizontal else round(size), before, after)

    # Peeking
    def title_clicked(self, panel_id: str, source: QWidget):
        node = leaf_of(self.root, panel_id) if self.root is not None else None
        if node is not None and node.get("minimized") and self.held is None:
            self.peek(panel_id)

    def peek(self, panel_id: str):
        '''
        Shows a minimized panel open in a popup beside its strip - the
        panel itself, lent out of its pane until the popup closes - to
        glance at or use (flip a form on, say) without restoring the pane.
        '''
        self.end_peek()
        node = leaf_of(self.root, panel_id)
        tabbed = self.tabbed.get(node["id"]) if node is not None else None
        if tabbed is None:
            return
        # Its open size the way it's flattened: what the minimized group it's in - or it - had open
        collapsed = self.collapsed()
        _, parents = find(self.root, node["id"])
        flattened = node
        for parent in reversed(parents):
            if not collapsed[parent["id"]]:
                break
            flattened = parent
        anchor = QRect(tabbed.mapToGlobal(QPoint(0, 0)), tabbed.size())
        side = tabbed.form == "side"
        panel = tabbed.lend(panel_id)
        menu_bar = getattr(panel, "menu_bar", None)
        if menu_bar is not None:
            menu_bar.show_body(True)
        popup = _Peek(self, panel, lambda: self.end_peek(closing=True))
        self.peeking = (panel_id, tabbed, popup)

        # Its size open along the way it's minimized, within reason - and beside its strip
        window = QRect(self.window().mapToGlobal(QPoint(0, 0)), self.window().size())
        open_size = int(flattened.get("open_size") or 0)
        # ...and across, the room its strip has, or what it had open in its own group
        own = int(node.get("open_size") or 0)
        width = open_size if side else anchor.width()
        height = max(anchor.height(), own) if side else open_size
        width = max(360, min(width or 480, window.width() * 2 // 3))
        height = max(280, min(height or 360, window.height() * 2 // 3))
        if side:
            x = anchor.right() if anchor.right() + width <= window.right() else anchor.left() - width
            y = anchor.top()
        else:
            x = anchor.left()
            y = anchor.bottom() if anchor.bottom() + height <= window.bottom() else anchor.top() - height
        x = max(window.left(), min(x, window.right() - width))
        y = max(window.top(), min(y, window.bottom() - height))
        popup.setGeometry(x, y, width, height)
        popup.show()

    def end_peek(self, closing: bool = False):
        '''Hands a peeked-at panel back to its pane (see peek).'''
        if self.peeking is None:
            return
        panel_id, tabbed, popup = self.peeking
        self.peeking = None
        panel = self.panels.get(panel_id)
        if panel is not None:
            panel.setParent(self.shelf)
            if self.tabbed.get(leaf_of(self.root, panel_id)["id"]) is tabbed:
                tabbed.take_back(panel_id)
            else:
                self.build()  # its pane was rebuilt meanwhile
        if not closing:
            popup.closed = None
            popup.close()
        popup.deleteLater()

    # Dragging
    def begin_drag(self, panel_id: str, at: QPoint, new: bool = False):
        '''
        Picks panel_id up: it leaves the layout and its chip follows the
        mouse from at. new is for a panel that isn't in the layout yet (the
        layout editor's list) - built now, and dropped anywhere but the
        layout, it's gone again.
        '''
        if self.held is not None:
            return
        self.end_peek()
        self.capture_sizes()
        self.before = copy.deepcopy(self.root)
        self.held, self.held_new = panel_id, new
        if new:
            self.add_panel(panel_id)
        elif self.root is not None:
            self.root = remove_panel(self.root, panel_id)
        self.build()
        panel = self.panels[panel_id]
        menu_bar = getattr(panel, "menu_bar", None)
        title = menu_bar.title() if menu_bar is not None else panel_id
        self.preview = _DropPreview(self)
        self.preview.show()
        self.chip = _Chip(self, title)
        self.chip.show()
        self.chip.raise_()
        self.chip.follow(at)
        self.chip.grabMouse()
        self.chip.grabKeyboard()
        # The new layout's pane sizes come in once it's laid out
        self.held_at = at
        QTimer.singleShot(0, lambda: self.drag_to(self.held_at))

    def drag_to(self, at: QPoint):
        if self.held is None or self.chip is None:
            return
        self.held_at = at
        self.chip.follow(at)
        target = self.target_at(at)
        if target is None:
            self.preview.show_target(None, None)
            return
        origin = self.mapTo(self.window(), QPoint(0, 0))
        line = target.line.translated(origin) if target.line is not None else None
        self.preview.show_target(target.rect.translated(origin), line)

    def end_drag(self, at: QPoint, drop: bool):
        if self.held is None:
            return
        panel_id, new = self.held, self.held_new
        target = self.target_at(at) if drop else None
        for widget in (self.chip, self.preview):
            if widget is not None:
                widget.releaseMouse()
                widget.releaseKeyboard()
                widget.hide()
                widget.deleteLater()
        self.chip = self.preview = None
        self.held = None
        if target is not None:
            self.capture_sizes()
            if target.kind == "tab":
                self.root = add_tab(self.root, target.node_id, panel_id, target.index)
            else:
                self.root = split_at(self.root, target.node_id, target.edge or "right", panel_id)
        elif new or (drop and self.over_discard(at)):
            # Out of the layout for good
            panel = self.panels.pop(panel_id)
            panel.hide()
            panel.deleteLater()
        else:
            self.root = self.before
        self.before = None
        self.build()
        self.changed.emit()

    def over_discard(self, at: QPoint) -> bool:
        return self.discard is not None and self.discard.isVisible() and self.discard.rect().contains(self.discard.mapFromGlobal(at))

    # Where a drop lands
    def node_rect(self, node: dict) -> QRect | None:
        widget = self.splits.get(node["id"]) if is_split(node) else self.tabbed.get(node["id"])
        if widget is None:
            return None
        return QRect(widget.mapTo(self, QPoint(0, 0)), widget.size())

    def target_at(self, at: QPoint) -> DropTarget | None:
        '''
        Where a panel dropped at at (global) would land, if anywhere: the
        pane under it is cut into a middle square - onto it as a tab - and
        four trapezoids, one per edge - beside it, splitting it. A tab
        stack's tab row takes it as a tab at that spot in the row. And in
        thin bands along a pane's edge, where that edge is also a whole
        group's (stacked or side by side the other way), it docks beside
        that whole group - the outermost group's band the closest to the
        edge - so any layout can be built. With no layout at all, it fills it.
        '''
        pos = self.mapFromGlobal(at)
        if not self.rect().contains(pos):
            return None
        if self.root is None:
            return DropTarget("fill", None, self.rect())
        for node, parents in walk(self.root):
            if is_split(node):
                continue
            rect = self.node_rect(node)
            if rect is None or not rect.contains(pos):
                continue
            return self.tab_row_target(node, rect, pos) or self.group_target(node, parents, rect, pos) or self.pane_target(node, rect, pos)
        return None

    def tab_row_target(self, node: dict, rect: QRect, pos: QPoint) -> DropTarget | None:
        if len(node["panels"]) < 2:
            return None
        tabbed = self.tabbed[node["id"]]
        menu_bar = getattr(tabbed.current_panel(), "menu_bar", None)
        strip = menu_bar._title_widget if menu_bar is not None else None
        if not isinstance(strip, TabStrip):
            return None
        bar = QRect(menu_bar.mapTo(self, QPoint(0, 0)), menu_bar.size())
        if not bar.contains(pos):
            return None
        local = strip.mapFrom(self, pos)
        index = strip.insert_index(local)
        x = strip.mapTo(self, QPoint(strip.insert_x(index), 0)).x()
        top = strip.mapTo(self, QPoint(0, 0)).y()
        line = QRect(x - 1, top, 3, strip.height())
        return DropTarget("tab", node["id"], rect, index=index, line=line)

    def group_target(self, node: dict, parents: tuple, rect: QRect, pos: QPoint) -> DropTarget | None:
        for edge in EDGES:
            distance = {"left": pos.x() - rect.left(), "right": rect.right() - pos.x(),
                        "top": pos.y() - rect.top(), "bottom": rect.bottom() - pos.y()}[edge]
            if distance >= GROUP_BAND * len(parents):
                continue
            orientation = "horizontal" if edge in ("left", "right") else "vertical"
            # Groups this edge is also an edge of, outermost first - those
            # running the same way as the split would just end up beside this pane
            groups = []
            for group in parents:
                group_rect = self.node_rect(group)
                if group_rect is None or group["orientation"] == orientation:
                    continue
                if self.edge_of(group_rect, edge) == self.edge_of(rect, edge):
                    groups.append((group, group_rect))
            band = distance // GROUP_BAND
            if band < len(groups):
                group, group_rect = groups[band]
                return DropTarget("split", group["id"], self.half(group_rect, edge), edge=edge)
        return None

    def pane_target(self, node: dict, rect: QRect, pos: QPoint) -> DropTarget:
        u = (pos.x() - rect.left()) / max(rect.width(), 1)
        v = (pos.y() - rect.top()) / max(rect.height(), 1)
        inner = CENTER_INSET
        if inner <= u <= 1 - inner and inner <= v <= 1 - inner:
            return DropTarget("tab", node["id"], rect, index=None)
        if u < inner and u <= v <= 1 - u:
            edge = "left"
        elif u > 1 - inner and 1 - u <= v <= u:
            edge = "right"
        elif v < 0.5:
            edge = "top"
        else:
            edge = "bottom"
        return DropTarget("split", node["id"], self.half(rect, edge), edge=edge)

    @staticmethod
    def edge_of(rect: QRect, edge: str) -> int:
        return {"left": rect.left(), "right": rect.right(), "top": rect.top(), "bottom": rect.bottom()}[edge]

    @staticmethod
    def half(rect: QRect, edge: str) -> QRect:
        '''The half of rect on edge - where a pane split off that edge goes.'''
        if edge == "left":
            return QRect(rect.left(), rect.top(), rect.width() // 2, rect.height())
        if edge == "right":
            return QRect(rect.left() + rect.width() - rect.width() // 2, rect.top(), rect.width() // 2, rect.height())
        if edge == "top":
            return QRect(rect.left(), rect.top(), rect.width(), rect.height() // 2)
        return QRect(rect.left(), rect.top() + rect.height() - rect.height() // 2, rect.width(), rect.height() // 2)
