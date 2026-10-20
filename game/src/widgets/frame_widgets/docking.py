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


class TabbedPane(QWidget):
    '''
    Fills a pane with one or more panels, stacked - only the current one
    showing. With more than one, each panel's menu bar shows a TabStrip
    for switching between them. A panel that's minimized (see
    MenuBar.minimize_button) passes that on to whichever tab replaces it,
    so the pane keeps its size.

    panels are (panel id, panel) pairs; watch(widget, panel id) is called
    on every tab, so whoever made this can make it a handle to pick that
    panel up by (see DockArea); switched(panel id) on every switch.
    '''

    def __init__(self, master: QWidget, context: Context, panels: list[tuple[str, QWidget]], current: str | None = None,
                 switched: Callable[[str], None] | None = None, watch: Callable[[QWidget, str], None] | None = None):
        super().__init__(master)
        self.context = context
        self.switched = switched
        master.layout().addWidget(self, 1)
        self.stack = QStackedLayout(self)
        self.stack.setContentsMargins(0, 0, 0, 0)
        self.panels: dict[str, QWidget] = {}
        for panel_id, panel in panels:
            self.panels[panel_id] = panel
            self.stack.addWidget(panel)
        tabs = [(panel_id, panel.menu_bar.title()) for panel_id, panel in panels if getattr(panel, "menu_bar", None) is not None]
        for panel_id, panel in panels:
            menu_bar = getattr(panel, "menu_bar", None)
            if menu_bar is None:
                continue
            if len(panels) > 1:
                strip = TabStrip(context, tabs, panel_id, self.set_current)
                menu_bar.set_title_widget(strip)
                if watch is not None:
                    watch(strip, panel_id)
                    for tab_id, button in strip.buttons.items():
                        watch(button, tab_id)
            else:
                menu_bar.set_title_widget(None)
        self.current = None
        self.set_current(current if current in self.panels else next(iter(self.panels)))

    def minimumSizeHint(self):
        # Like the pane it's in (see _PaneContainer): only the pane's own floor counts
        return QSize(0, 0)

    def set_current(self, panel_id: str):
        old = self.panels.get(self.current)
        new = self.panels[panel_id]
        if new is old:
            return
        minimized = old is not None and getattr(old, "menu_bar", None) is not None and old.menu_bar.is_minimized()
        if minimized:
            old.menu_bar.set_minimized(False)
        self.current = panel_id
        self.stack.setCurrentWidget(new)
        if minimized and getattr(new, "menu_bar", None) is not None:
            new.menu_bar.set_minimized(True)
        if self.switched is not None:
            self.switched(panel_id)

    def current_panel(self) -> QWidget:
        return self.panels[self.current]


# Dragging

class _Grip(QObject):
    '''
    Watches the widgets a panel can be picked up by - its menu bar, title
    and tabs, each marked with the "dock_panel_id" it picks up - and starts
    a DockArea drag once one's pressed and the mouse moves past the
    platform's drag distance.
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
        elif kind == QEvent.Type.MouseButtonRelease:
            self.pressed = None
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
        current = {node["current"] for node, _ in walk(self.root) if not is_split(node)} if self.root else set()
        for panel_id, panel in self.panels.items():
            if hasattr(panel, "redocked"):
                panel.redocked(keep_minimized=panel_id in current)

    def build_split(self, node: dict, master: QWidget) -> Panes:
        children = node["children"]
        total = sum(child["weight"] for child in children) or 1
        divisors = [total / max(child["weight"], 1e-6) for child in children]
        panes = Panes(master, self.context, node["orientation"], len(children), divisors, False,
                      transparent=self.transparent, ids=[child["id"] for child in children])
        panes.splitterMoved.connect(lambda *_: self.changed.emit())
        self.splits[node["id"]] = panes
        for index, child in enumerate(children):
            pane = panes.pane(index)
            if is_split(child):
                self.build_split(child, pane)
            else:
                self.tabbed[child["id"]] = TabbedPane(
                    pane, self.context, [(panel_id, self.panels[panel_id]) for panel_id in child["panels"]], child["current"],
                    switched=lambda panel_id, child=child: child.__setitem__("current", panel_id), watch=self.watch)
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
        for node, _ in walk(self.root):
            panes = self.splits.get(node["id"]) if is_split(node) else None
            if panes is None or not panes.isVisible() or panes.testAttribute(Qt.WidgetAttribute.WA_PendingResizeEvent):
                continue
            sizes = panes.sizes()
            if len(sizes) == len(node["children"]) and all(size > 0 for size in sizes):
                for child, size in zip(node["children"], sizes):
                    child["weight"] = size

    def layout_tree(self) -> dict | None:
        '''The layout as it is now, as a layout_tree - its weights each pane's live size.'''
        self.capture_sizes()
        return to_tree(self.root) if self.root is not None else None

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
