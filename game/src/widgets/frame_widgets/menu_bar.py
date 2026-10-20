from ...app_core import Context
from ...app_core.context.style import Style
from PySide6.QtCore import QEvent, QObject, QSize, Qt, QTimer
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QCheckBox, QComboBox, QFrame, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QSplitter, QWidget
from .important_buttons import (ButtonGroup, ConfigureThisWorkspace, DeleteAllUserData, DeleteAllWorkspaceSavedData,
                                EditWorkspaceAvailability, ImportantButton, LoadLocalizationLabelsFile, MENU_BAR_BUTTONS,
                                OpenAccessPointConfigInBrowser, OpenSettingsPage, OpenWorkspaceEditor, OpenWorkspaceSorter,
                                RefreshCurrentPage, SaveLayoutShapeAsDefault, SaveLayoutWeightsAsDefault,
                                SelectBackground, SelectColorTheme, ToggleDebugLabels, ToggleWorkspaceBackground,
                                ToggleFullscreen, ToggleLightDarkMode)
from .important_buttons.button_group import offered_sections
from .overlay import Overlay
from .window_chrome import (SquareButtons, WindowBarButton, WindowControls, WindowDrag, draw_window_bar_line, window_bar_button_height,
                            window_bar_height, window_bar_room)
from collections.abc import Callable

# A page's menu bar has three zones (see MenuBar.build_page_zones):
#   left   - home (the pause menu), back, forward, the page's title, its bookmark and refresh
#   center - the page's own tools: the buttons its config's "menu_bar" names
#   right  - the same on every page: Quick Settings, Help and the window controls
# Everything but the page's own tools is on every page's menu bar by itself -
# a page config only chooses those.

# The page's own tools in the center zone, left to right: each group key
# ("menu_bar_buttons_<key>" labels its button) maps to its sections, top to
# bottom - (header key or None, button names - keys of
# important_buttons.MENU_BAR_BUTTONS). A page config's "menu_bar" only says
# which buttons a page gets (see MenuBar.add_config_buttons): a group with
# none of them is left out, and a group with just one shows that button in
# the group's place instead.
MENU_BAR_GROUPS: dict[str, list[tuple[str | None, list[str]]]] = {
    "captures_button_group": [
        ("load_fast", ["pcap_button", "load_json_fast_button"]),
        ("load_real_time", ["stream_pcap_button", "load_button"]),
        ("save", ["save_button", "stream_button"]),
        ("current_capture", ["clear_status_button", "clear_packet_console_button", "clear_modbus_button", "clear_all_button"]),
    ],
    "modbus_button_group": [
        ("registers_and_models", ["registers_button", "register_preset_button"]),
    ],
    "view_button_group": [
        ("model_display", ["model_style_button", "strip_chart_style_button"]),
    ],
    "workspace_button_group": [
        ("reload", ["clear_inputs_button", "reset_layout_button", "reset_button"]),
        ("customize", ["preset_button"]),
        ("show_hide", ["network_forms_button", "modbus_forms_button", "defender_forms_button", "packet_columns_button"]),
    ],
    "links_button_group": [
        ("links", ["ap_config_button"]),
    ],
}

# Every config button name in layout order - the order the workspace editor lists them in
MENU_BAR_BUTTON_ORDER: list[str] = [name for sections in MENU_BAR_GROUPS.values() for _, names in sections for name in names]
assert sorted(MENU_BAR_BUTTON_ORDER) == sorted(MENU_BAR_BUTTONS), "every menu bar button needs exactly one place in MENU_BAR_GROUPS"

# The right zone's dropdowns, the same on every page, each shown as just its
# icon. Quick Settings has what's changed most often - everything else is
# on the settings page it links to - and, in developer mode
# (preferences.json "is_developer"), the debug tools (see DEVELOPER_SECTIONS)
RIGHT_ZONE_GROUPS: dict[str, list[tuple[str | None, list[type[ImportantButton]]]]] = {
    "quick_settings_button_group": [
        ("general", [ToggleFullscreen, LoadLocalizationLabelsFile]),
        ("appearance", [ToggleLightDarkMode, SelectColorTheme, SelectBackground,
                        ToggleWorkspaceBackground]),
        ("navigation", [OpenAccessPointConfigInBrowser, OpenSettingsPage]),
        ("debug_tools", [DeleteAllUserData, DeleteAllWorkspaceSavedData, OpenWorkspaceEditor,
                         OpenWorkspaceSorter, ConfigureThisWorkspace, SaveLayoutShapeAsDefault, SaveLayoutWeightsAsDefault,
                         EditWorkspaceAvailability, ToggleDebugLabels]),
    ],
}
RIGHT_ZONE_ICONS: dict[str, str] = {
    "quick_settings_button_group": "adjustments-horizontal",
}

# The overflow button's text, closed and open (see MenuBar._update_squashing)
OVERFLOW_CLOSED = Style.icon("chevrons-right")
OVERFLOW_OPEN = Style.icon("x")

# What the hand-built game pages (attacker, defender) get (see MenuBar.page_buttons)
PAGE_BUTTON_NAMES: list[str] = [
    "ap_config_button", "reset_button", "preset_button",
    "pcap_button", "load_button", "save_button", "stream_button",
]


def _pane_is_minimized(widget: QWidget, vertical: bool, style) -> bool:
    '''
    A minimized pane has had its own floor lowered below the splitter's
    normal PANE_MIN_HEIGHT/WIDTH (down to just its menu bar's height - see
    minimize_button.shrink_pane), and nothing else in Panes ever sets a
    smaller floor - so a floor below that normal value reliably means "this
    pane is currently minimized," with no extra bookkeeping needed.
    '''
    normal_floor = style.PANE_MIN_HEIGHT if vertical else style.PANE_MIN_WIDTH
    current_floor = widget.minimumHeight() if vertical else widget.minimumWidth()
    return current_floor < normal_floor


def _drain_evenly(sizes: list[float], floors: list[float], amount: float) -> list[float]:
    '''
    Removes up to `amount` total from `sizes` (never taking an entry below
    its matching `floors` value), always draining whichever entries are
    currently tallest first and in lockstep - like water draining off the
    tallest bars evenly - so two entries that started at different heights
    end up equal (or at a floor) before either drops further. Used by
    minimize_button's maximize path: the growing pane takes height from its
    single biggest sibling until they're level with the next-biggest, then
    takes from all of them evenly, the same way a human would rebalance a
    row of panes by hand.
    '''
    sizes = [float(s) for s in sizes]
    floors = [float(f) for f in floors]
    remaining = float(amount)
    n = len(sizes)

    while remaining > 1e-6:
        room = [i for i in range(n) if sizes[i] - floors[i] > 1e-6]
        if not room:
            break
        tallest_height = max(sizes[i] for i in room)
        tallest = [i for i in room if abs(sizes[i] - tallest_height) < 1e-6]

        lower_heights = [sizes[i] for i in range(n) if sizes[i] < tallest_height - 1e-6]
        next_height = max(lower_heights) if lower_heights else None
        floor_ceiling = min(floors[i] for i in tallest)
        boundary = floor_ceiling if next_height is None else max(next_height, floor_ceiling)

        headroom = (tallest_height - boundary) * len(tallest)
        take = min(headroom, remaining)
        if take <= 1e-9:
            break
        share = take / len(tallest)
        for i in tallest:
            sizes[i] -= share
        remaining -= take

    return sizes


def icon_button(context: Context, button: ImportantButton, icon: str | None = None,
                active_icon: str | None = None) -> ImportantButton:
    '''
    Shows a solo button as a bare symbol - its own ICON unless told
    otherwise (see ImportantButton.show_icon) - no background or border,
    just the icon in the text color (the accent on hover), its label as its
    tooltip. Faint while disabled.
    '''
    style = context.style
    button.show_icon(icon, active_icon)
    button.setCursor(Qt.CursorShape.PointingHandCursor)
    button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
    name = f"_icon_button_{id(button)}"
    button.setObjectName(name)

    def sheet() -> str:
        faint = QColor(style.color("text"))
        faint.setAlpha(80)
        return (f"QPushButton#{name} {{ background: transparent; border: none; padding: 0px {style.igap // 2}px;"
                f" {style.icon_css()}"
                f" color: {style.color('text')}; }}"
                f" QPushButton#{name}:hover {{ color: {style.color('accent')}; }}"
                f" QPushButton#{name}:pressed {{ color: {style.color('text')}; }}"
                f" QPushButton#{name}:disabled {{ color: {faint.name(QColor.NameFormat.HexArgb)}; }}")
    style.live_style(button, sheet)
    return button


def global_buttons(context: Context) -> QWidget:
    '''
    The buttons at the top right of every page, left of the window
    controls: Quick Settings, then Help - a page's menu bar has them (see MenuBar.build_right_zone), and so
    do the title pages, which have none (see CornerControls).
    '''
    from .important_buttons import ShowHelpMessage
    holder = QWidget()
    row = QHBoxLayout(holder)
    row.setContentsMargins(0, 0, 0, 0)
    # Square, side by side, like the window controls (see SquareButtons)
    row.setSpacing(0)
    for group_key, group_sections in RIGHT_ZONE_GROUPS.items():
        group = ButtonGroup(context, group_key, offered_sections(context, group_sections))
        row.addWidget(icon_button(context, group, RIGHT_ZONE_ICONS[group_key]))
    row.addWidget(icon_button(context, ShowHelpMessage(context)))
    # As tall as what holds them - the window bar's whole height but its line (see window_bar_room) - and as wide
    for button in holder.findChildren(QPushButton):
        button.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
    SquareButtons(holder)
    return holder


class _RightZoneRoom(QWidget):
    '''
    A page menu bar's right zone's place in its row - holding the zone's
    width there, while the zone itself (a child of the bar, not of this)
    spans the bar's whole height, up through the room above the row (see
    window_bar_room) to the window's top edge, and down to just above its line.
    '''

    def __init__(self, bar: QWidget, zone: QWidget):
        super().__init__()
        self.bar = bar
        self.zone = zone
        zone.setParent(bar)
        zone.installEventFilter(self)

    def sizeHint(self):
        return QSize(self.zone.sizeHint().width(), 0)

    def minimumSizeHint(self):
        return QSize(self.zone.minimumSizeHint().width(), 0)

    def eventFilter(self, watched, event):
        if event.type() == QEvent.Type.LayoutRequest:
            self.updateGeometry()  # The zone's width changed (e.g. the window controls hid for fullscreen)
        return False

    def place_zone(self):
        self.zone.setGeometry(self.x(), 0, self.width(), window_bar_button_height(self.bar.height()))
        self.zone.raise_()

    def moveEvent(self, event):
        self.place_zone()

    def resizeEvent(self, event):
        self.place_zone()


class _FollowResize(QObject):
    '''Calls back whenever a widget resizes - a page's menu bar isn't in its layout, so it places itself.'''
    def __init__(self, widget: QWidget, callback):
        super().__init__(widget)
        self.callback = callback
        widget.installEventFilter(self)

    def eventFilter(self, watched, event):
        if event.type() == QEvent.Type.Resize:
            self.callback()
        return False


class MenuBar(QFrame):
    '''
    The main Widget for the menu bar.
    Comes with a label and has a button maker.
    Inherits QFrame.

    A page's menu bar (master is a Page) is also the window's title bar -
    the window is borderless (see MainWindow). It runs edge to edge along
    the top of the window, floating over the page like the Footer does
    along the bottom, and has three zones (see MENU_BAR_GROUPS): the left
    and right ones the same on every page, the center the page's own
    buttons (add_button, add_config_buttons...). Its empty space moves the
    window. A panel's menu bar is just its title and its buttons.
    '''

    def __init__(self, master: QWidget, context: Context, title_label: str = "_default"):
        super().__init__(master)
        self.context = context
        self.style = context.style
        from ...pages.page import Page
        self.page_bar = isinstance(master, Page)

        # No background of its own: a page's shows the page (and its
        # background visual) up to the window's edge, and a panel's is
        # part of the panel's drawer - one material with the frame around
        # its contents (see themes' module docstring)
        self.style.set_material(self, "none")
        # Qt widgets default to a vertical size policy that's willing to
        # grow into whatever leftover space its layout has - the old
        # CTkFrame only ever got fill="x" (not expand=True), so it never
        # grew past its natural height, leaving Panes to claim the rest.
        # Maximum reproduces that: this frame can shrink but never grow
        # past its own sizeHint.
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        self.row = QHBoxLayout(self)
        if self.page_bar:
            # Flush with the window's edges - the window controls fill the
            # top right corner, so that's where a mouse flung there lands
            self.setContentsMargins(0, 0, 0, 0)
            # Room above and below all but the right zone, which spans it (see _RightZoneRoom)
            room = window_bar_room(context)
            self.row.setContentsMargins(self.style.igap // 2, room, 0, room)
            # Left out of page transitions (see Page.appear_targets) - it's
            # the same from page to page, so it stays put
            self.setProperty("page_bar", True)
        else:
            master.layout().addWidget(self)
            self.setContentsMargins(self.style.igap, self.style.cgap, self.style.igap, self.style.cgap)
            self.row.setContentsMargins(self.style.igap, self.style.cgap, self.style.igap, self.style.cgap)

        # Everything in the row that isn't an entry - room squashing never takes (see _update_squashing)
        self._fixed: list[QWidget] = []
        # What shows in the title's place instead of it, if anything (see set_title_widget)
        self._title_widget: QWidget | None = None
        # A panel's minimize button's state and controls (see minimize_button)
        self._minimizer: dict | None = None
        self.back_arrow = None
        self.window_controls = None

        if self.page_bar:
            self.left_zone = self.build_left_zone()
            self.row.addWidget(self.left_zone, 0, Qt.AlignmentFlag.AlignVCenter)
            self._fixed.append(self.left_zone)

        self.game_label = QLabel(self.context.labels.get(f"menu_bar_titles_{title_label}"))
        self.game_label.setFont(self.style.get_font("page_title" if self.page_bar else "default"))
        # A title is a name, never markup - "<b>" in one should show as typed
        self.game_label.setTextFormat(Qt.TextFormat.PlainText)
        if self.page_bar:
            # Dragging the title moves the window, like the bar's empty space
            # (see WindowDrag) - a QLabel keeps the mouse moves after a press
            # to itself, so the bar never saw the drag
            self.game_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.row.addWidget(self.game_label, 0, Qt.AlignmentFlag.AlignVCenter)
        self._fixed.append(self.game_label)

        if self.page_bar:
            from .important_buttons import ToggleBookmark
            self.bookmark = self.icon_button(ToggleBookmark(context))
            self.refresh = self.icon_button(RefreshCurrentPage(context))
            for button in (self.bookmark, self.refresh):
                self.row.addWidget(button, 0, Qt.AlignmentFlag.AlignVCenter)
                self._fixed.append(button)
        self.row.addStretch()

        # Button overflow overlay - see update_squashing/_populate_overflow_overlay.
        # Sits just left of every button (add_button/add_dropdown append new
        # entries after it), where the buttons squashed into it would have
        # been, hidden until squashing finds something to put in it.
        self._entries: list[dict] = []
        self._squashed_entries: list[dict] = []
        self.the_overflow_button = WindowBarButton()
        self.the_overflow_button.setFont(self.style.get_font())
        self.add_tooltip(self.the_overflow_button, "overflow")
        self.row.addWidget(self.the_overflow_button)
        self.the_overflow_button.hide()
        self.overflow_overlay = Overlay(self.context.root, self.context, self.the_overflow_button, self._populate_overflow_overlay,
                                        closed_text=OVERFLOW_CLOSED, open_text=OVERFLOW_OPEN)

        if self.page_bar:
            # The center zone's entries go between the two stretches (see _insert_entry)
            self.row.addStretch()
            self.right_zone = self.build_right_zone()
            self.row.addWidget(_RightZoneRoom(self, self.right_zone))
            self._fixed.append(self.right_zone)
            WindowDrag(self, context.root)
            context.root.fullscreen_changed.connect(self._on_fullscreen_changed)
            self._top_padding: int | None = None
            _FollowResize(master, self.place)
            self.place()

    # Page menu bar zones

    def build_left_zone(self) -> QWidget:
        '''Home (the pause menu), back and forward - back's and forward's tooltips name where they go.'''
        from .important_buttons import GoBackToPreviousPage, GoForwardToNextPage, OpenPauseMenu
        zone = QWidget()
        row = QHBoxLayout(zone)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(0)
        router = self.context.router
        self.home = self.icon_button(OpenPauseMenu(self.context))
        self.back_arrow = self.icon_button(GoBackToPreviousPage(self.context))
        self.forward_arrow = self.icon_button(GoForwardToNextPage(self.context))
        stack = router.navigation_stack
        self.where_to(self.back_arrow, stack[-2] if len(stack) >= 2 else None, "back_to")
        self.where_to(self.forward_arrow, router.forward_stack[-1] if router.forward_stack else None, "forward_to")
        for button in (self.home, self.back_arrow, self.forward_arrow):
            row.addWidget(button, 0, Qt.AlignmentFlag.AlignVCenter)
        return zone

    def where_to(self, button: QPushButton, key: str | None, label: str):
        '''
        Names the page a back/forward button leads to in its tooltip - or,
        with nowhere to go, disables it (kept in place, so the buttons
        after it never move).
        '''
        if key is None:
            button.setEnabled(False)
            return
        name = self.context.router.page_name(key)
        button.setToolTip(self.context.labels.get(f"menu_bar_tooltips_{label}").replace("{page}", name))

    def build_right_zone(self) -> QWidget:
        '''The buttons every page has at its top right (see global_buttons), then the window controls.'''
        zone = QWidget()
        row = QHBoxLayout(zone)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(0)  # Square buttons, side by side up to the window's corner (see SquareButtons)
        row.addWidget(global_buttons(self.context))
        # The whole height of the bar, up into the window's top right corner
        self.window_controls = WindowControls(self.context, zone)
        row.addWidget(self.window_controls)
        return zone

    def icon_button(self, button: ImportantButton, icon: str | None = None, active_icon: str | None = None) -> ImportantButton:
        '''A solo button as a bare symbol - see icon_button.'''
        return icon_button(self.context, button, icon, active_icon)

    def bar_height(self) -> int:
        '''
        A page menu bar's height: the same on every page (see
        window_bar_height) - taller only if something in it is.
        '''
        return max(window_bar_height(self.context), self.sizeHint().height() + 4 * self.style.cgap)

    def place(self):
        '''
        A page menu bar: along the top of the page, over it - and the page
        given that much more top margin, so nothing of its own is covered.
        '''
        try:
            page = self.parentWidget()
            height = self.bar_height()
            self.setGeometry(0, 0, page.width(), height)
            self.raise_()
            if self._top_padding != height:
                margins = page.contentsMargins()
                top = margins.top() - (self._top_padding or 0) + height
                page.setContentsMargins(margins.left(), top, margins.right(), margins.bottom())
                self._top_padding = height
        except RuntimeError:
            pass  # deleted with its page, with the resize still queued

    def _on_fullscreen_changed(self, *args):
        try:
            self._update_squashing()
        except RuntimeError:
            pass  # deleted with its page, with the signal still connected

    def fixed_width(self) -> int:
        '''Room the row's fixed items take (see _fixed) - the right zone's less maximize while it's hidden (fullscreen).'''
        spacing = self.row.spacing()
        return sum(widget.sizeHint().width() + spacing for widget in self._fixed)

    def tool_buttons(self) -> list[QPushButton]:
        '''The page's own buttons in the center zone, left to right - squashed ones too (see _update_squashing).'''
        return [entry["widget"] for entry in self._entries if entry["kind"] == "button"]

    def minimumSizeHint(self):
        '''
        Qt's default minimumSizeHint for a QHBoxLayout is the sum of every
        currently *visible* item's own size - which for this row means
        "however many buttons happen to be squashed away right now", not
        "as many as squashing could ever hide". That default makes the
        window's own minimum size track whatever's currently unsquashed:
        widen the window enough to unsquash everything, and the reported
        minimum locks in near that width, since nothing ever gets narrow
        enough again to trigger _update_squashing back down - a bar (and
        the whole window containing it) that was ever wide can never
        become narrow again. Reporting the true floor instead - the fixed
        items plus every dropdown (neither ever squashes) plus the overflow
        button alone - keeps that floor constant regardless of history, so
        the window/pane can always still be shrunk down to it, which is
        what actually lets squashing kick back in.
        '''
        margins = self.row.contentsMargins()
        spacing = self.row.spacing()
        width = margins.left() + margins.right()
        width += self.fixed_width()
        for entry in self._entries:
            if entry["kind"] in ("dropdown", "checkbox"):
                width += spacing + entry["widget"].sizeHint().width()
        width += spacing + self.the_overflow_button.sizeHint().width()
        return QSize(width, self.sizeHint().height())

    def add_tooltip(self, widget, key: str):
        self.context.style.add_tooltip(widget, "menu_bar_tooltips", key)

    def add_button(self, label: str = "_default", function: Callable | None = None) -> QPushButton:
        button = WindowBarButton(self.context.labels.get(f"menu_bar_buttons_{label}"))
        button.setFont(self.style.get_font())
        if function is not None:
            self._connect(button, function)
        self._insert_entry(button, "button")
        return button

    def _connect(self, button: QPushButton, function: Callable):
        '''
        clicked emits a "checked" bool that none of these callbacks expect
        (a callback's own default-valued argument would silently get
        clobbered by it) - drop it before calling through.
        '''
        button.clicked.connect(lambda checked=False, function=function: function())

    def add_dropdown(self, values: list[str], command: Callable[[str], None] | None = None, default: str | None = None) -> QComboBox:
        '''
        A button-row dropdown (e.g. ModbusModel's hvac/submarine picker) -
        values/default are already-localized display text, command is
        called with whichever one the user picks. Doesn't participate in
        the overflow overlay (see _update_squashing/_populate_overflow_overlay)
        - it's always kept visible, since cloning a combo box's current
        selection into the overlay isn't as simple as replaying a click.
        '''
        dropdown = QComboBox()
        dropdown.setFont(self.style.get_font())
        dropdown.addItems(values)
        if default is not None:
            index = dropdown.findText(default)
            if index >= 0:
                dropdown.setCurrentIndex(index)
        if command is not None:
            dropdown.currentTextChanged.connect(command)
        self._insert_entry(dropdown, "dropdown")
        return dropdown

    def add_checkbox(self, label: str, checked: bool = False, command: Callable[[bool], None] | None = None) -> QCheckBox:
        '''
        A button-row checkbox (e.g. ModbusModel's Auto-Switch toggle) -
        never squashed into the overflow overlay, same as add_dropdown and
        for the same reason (nothing here clones a checkbox's live checked
        state into the overlay). command is called with the new checked
        state on every toggle, including programmatic ones (checkbox.setChecked).
        '''
        checkbox = QCheckBox(label)
        checkbox.setFont(self.style.get_font())
        checkbox.setChecked(checked)
        if command is not None:
            checkbox.toggled.connect(command)
        self._insert_entry(checkbox, "checkbox")
        return checkbox

    # Button overflow overlay
    #
    # Ported from the CTk version's update_squashing/overflow_button/
    # clone_button/populate_overflow_overlay: when the menu bar isn't wide
    # enough to fit every button, the ones that don't fit are hidden and an
    # overflow ("»") button appears with clones of them in a popup.

    def _insert_entry(self, widget: QWidget, kind: str):
        # Entries fill in left to right after the overflow button - on a
        # page's menu bar, before the stretch that ends the center zone
        if self.page_bar:
            self.row.insertWidget(self.row.count() - 2, widget)
        else:
            self.row.addWidget(widget)
        self._entries.append({"widget": widget, "kind": kind})
        self._update_squashing()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_squashing()

    def paintEvent(self, event):
        super().paintEvent(event)
        # A page's menu bar is underlined (see draw_window_bar_line)
        if self.page_bar:
            draw_window_bar_line(self, self.context)

    def _update_squashing(self):
        try:
            margins = self.row.contentsMargins()
            spacing = self.row.spacing()
            available_width = self.width() - margins.left() - margins.right()
            available_width -= self.fixed_width()

            # Fit buttons in from the right, so the leftmost ones squash
            # first - a bar's most important buttons (back, quit, a panel's
            # minimize) go last, on the right, and stay visible longest.
            def split(width: int) -> tuple[list[dict], list[dict]]:
                # Dropdowns/checkboxes never squash, so their room comes off the top
                # before any button is fitted - wherever they sit in the row
                for entry in self._entries:
                    if entry["kind"] != "button":
                        width -= entry["widget"].sizeHint().width() + spacing
                fine = []
                squashed = []
                for entry in reversed(self._entries):
                    if entry["kind"] != "button":
                        fine.append(entry)
                        continue
                    width -= entry["widget"].sizeHint().width() + spacing
                    if width >= 0:
                        fine.append(entry)
                    else:
                        squashed.append(entry)
                return fine, squashed

            fine, squashed = split(available_width)
            if squashed:
                # The overflow button itself takes room once it's showing
                fine, squashed = split(available_width - self.the_overflow_button.sizeHint().width() - spacing)

            # Back in left-to-right order for the overflow overlay
            self._squashed_entries = squashed[::-1]
            for entry in fine:
                entry["widget"].setVisible(True)
            for entry in squashed:
                entry["widget"].setVisible(False)
            self.the_overflow_button.setVisible(len(squashed) > 0)
        except RuntimeError:
            # A destroyed widget mid-navigation with this resizeEvent still
            # queued raises RuntimeError (the underlying C++ object is
            # already gone) - safe to just skip this stale redraw.
            pass

    def _populate_overflow_overlay(self, overlay: Overlay):
        proxies: list[tuple[QPushButton, QPushButton]] = []
        for entry in self._squashed_entries:
            button = entry["widget"]
            proxy = QPushButton(button.text())
            proxy.setFont(self.style.get_font())
            # Its overlay opens on hover once a sibling's is open (see Overlay._switch_to_hovered)
            proxy.setProperty("opens_overlay", button.property("opens_overlay"))
            # Replays a real click on the (hidden) original button rather
            # than capturing its callback at insert time, so a proxy always
            # reflects whatever label/handler the button currently has -
            # including buttons like minimize/ToggleButton that swap
            # their text and handler dynamically after creation.
            proxy.clicked.connect(lambda checked=False, b=button, p=proxy: self._replay_click(b, p))
            overlay.layout().addWidget(proxy)
            proxies.append((button, proxy))

        # QPushButton has no text-changed signal, and a button's label can
        # change from anywhere (a ToggleButton click, an overlay it opens
        # closing, a pane's sash being dragged to minimize it) - so poll
        # labels across while this overlay is open, then stop.
        callback_name = f"overflow_proxies_{id(self)}"

        def sync_proxies():
            try:
                if not overlay.isVisible():
                    self.context.animation_manager.remove_callback(callback_name)
                    return
                for button, proxy in proxies:
                    if proxy.text() != button.text():
                        proxy.setText(button.text())
            except RuntimeError:
                # This menu bar (or a proxy) was destroyed mid-navigation
                self.context.animation_manager.remove_callback(callback_name)
        self.context.animation_manager.add_callback(callback_name, sync_proxies)

    def _replay_click(self, button: QPushButton, proxy: QPushButton):
        '''
        Clicks the hidden original button, recording the proxy as the
        widget the click really came from for the duration - an Overlay
        that button opens anchors itself to that proxy (see
        Overlay.click_open), since the hidden original has no on-screen
        position to anchor to.
        '''
        button.click_proxy = proxy
        try:
            button.click()
        finally:
            button.click_proxy = None
        # Show the new label right away rather than on the next sync_proxies poll
        try:
            proxy.setText(button.text())
        except RuntimeError:
            pass  # the click navigated away, destroying the button or proxy

    # Panel Buttons

    def minimize_button(self, frame_widget: QWidget | None = None):
        '''
        Adds a button that hides frame_widget and shrinks the pane this
        menu bar's panel sits in down to just this menu bar's own height,
        or restores both - and auto-minimizes as the user drags that pane's
        Panes sash down to its normal floor (PANE_MIN_HEIGHT/WIDTH),
        mirroring the old <Configure>-driven auto-minimize.

        The pane is looked up whenever it's needed (see pane), not fixed
        when the panel is built - a panel can be docked somewhere else
        (see DockArea), which calls redocked to follow it there.

        Space freed by shrinking is handed to the sibling panes evenly.
        Restoring takes it back from whichever sibling is currently
        tallest first (leveling siblings down together once they match),
        growing the pane back to its authored share of the splitter - see
        Panes.default_stretch - rather than an arbitrary fixed size.
        '''
        minimize_text = self.context.labels.get("menu_bar_buttons_minimize")
        maximize_text = self.context.labels.get("menu_bar_buttons_maximize")
        button = self.add_button("minimize")
        is_minimized = False
        normal_min_extent = None  # pane's PANE_MIN_HEIGHT/WIDTH floor, remembered while it's lowered
        watched_splitter = None  # the Panes whose sash moves on_sash_moved follows (see attach)

        def shrink_pane():
            nonlocal normal_min_extent
            pane = self.pane()
            if pane is None:
                return
            splitter = pane.parent()
            index = splitter.indexOf(pane)
            vertical = splitter.orientation() == Qt.Orientation.Vertical

            sizes = [float(s) for s in splitter.sizes()]
            current = sizes[index]
            target = min(float(self.sizeHint().height() if vertical else self.sizeHint().width()), current)

            # Lower this pane's hard floor so the splitter will actually
            # allow it down to the menu bar's own height - its normal
            # floor is PANE_MIN_HEIGHT/WIDTH, set once in Panes.__init__.
            normal_min_extent = pane.minimumHeight() if vertical else pane.minimumWidth()
            if vertical:
                pane.setMinimumHeight(int(target))
            else:
                pane.setMinimumWidth(int(target))

            freed = current - target
            siblings = [i for i in range(splitter.count()) if i != index]
            # A sibling that's already minimized has its own floor lowered
            # the same way (see above) - handing it a share of the freed
            # space would grow it past that floor, since a floor only ever
            # stops a pane from getting *smaller*. Left out of the
            # recipients, it stays exactly at its own minimized height
            # instead of ballooning back up with nothing to fill but blank
            # space under its own menu bar.
            growable = [i for i in siblings if not _pane_is_minimized(splitter.widget(i), vertical, self.style)]
            if growable and freed > 0:
                share = freed / len(growable)
                for i in growable:
                    sizes[i] += share
                sizes[index] = target
            # else: every other pane in this splitter is already minimized
            # too, so there's no one left to hand the freed space to -
            # leave this pane's own allocated size alone rather than
            # shrinking it into space Qt would just renormalize back out
            # across every pane (silently un-minimizing all of them). Its
            # body is still hidden and its menu bar still pins to the top
            # of that space (see Panel's AlignTop), so the extra room just
            # collects as blank space below it - the last minimized pane in
            # a splitter ends up holding whatever's left over instead of
            # everyone floating apart.
            splitter.setSizes([round(s) for s in sizes])

        def restore_floor():
            '''
            Restores this pane's normal PANE_MIN_HEIGHT/WIDTH floor if
            shrink_pane lowered it - shared by grow_pane's click-to-restore
            path and on_sash_moved's drag-to-restore path below, since only
            one of them (grow_pane) also needs to resize the pane afterward.
            '''
            nonlocal normal_min_extent
            pane = self.pane()
            if pane is None or normal_min_extent is None:
                return
            splitter = pane.parent()
            vertical = splitter.orientation() == Qt.Orientation.Vertical
            if vertical:
                pane.setMinimumHeight(normal_min_extent)
            else:
                pane.setMinimumWidth(normal_min_extent)
            normal_min_extent = None

        def grow_pane():
            pane = self.pane()
            if pane is None:
                return
            splitter = pane.parent()
            index = splitter.indexOf(pane)
            vertical = splitter.orientation() == Qt.Orientation.Vertical

            # Restore this pane's normal floor before asking the splitter
            # for more room - otherwise it's still pinned at the minimized
            # (menu-bar-only) height from shrink_pane.
            restore_floor()

            sizes = [float(s) for s in splitter.sizes()]
            current = sizes[index]

            default_weight = getattr(pane, "default_stretch", None)
            if default_weight is not None:
                total_weight = sum(
                    getattr(splitter.widget(i), "default_stretch", default_weight)
                    for i in range(splitter.count())
                )
                target = (default_weight / total_weight) * sum(sizes) if total_weight else self.style.PANE_BIG
            else:
                target = self.style.PANE_BIG
            target = max(target, current)
            needed = target - current

            siblings = [i for i in range(splitter.count()) if i != index]
            sibling_sizes = [sizes[i] for i in siblings]
            sibling_floors = [
                (splitter.widget(i).minimumHeight() if vertical else splitter.widget(i).minimumWidth())
                for i in siblings
            ]
            drained = _drain_evenly(sibling_sizes, sibling_floors, needed)
            actually_taken = sum(sibling_sizes) - sum(drained)

            for offset, i in enumerate(siblings):
                sizes[i] = drained[offset]
            sizes[index] = current + actually_taken
            splitter.setSizes([round(s) for s in sizes])

        def click_minimize():
            nonlocal is_minimized
            if is_minimized:
                return
            is_minimized = True
            button.clicked.disconnect()
            self._connect(button, click_maximize)
            button.setText(maximize_text)
            shrink_pane()
            if frame_widget is not None:
                frame_widget.hide()

        def unminimize(resize: bool):
            '''
            Shared by click_maximize (button click - also resizes the pane
            back out to its authored share) and on_sash_moved (the user
            already dragged the pane to whatever size they wanted, so this
            only needs to reveal frame_widget in place, not also resize it
            out from under them).
            '''
            nonlocal is_minimized
            if not is_minimized:
                return
            is_minimized = False
            button.clicked.disconnect()
            self._connect(button, click_minimize)
            button.setText(minimize_text)
            if resize:
                grow_pane()
            else:
                restore_floor()
            if frame_widget is not None:
                frame_widget.show()

        def click_maximize():
            unminimize(resize=True)

        def on_sash_moved(pos=None, index=None):
            pane = self.pane()
            if pane is None or not self.isVisible():
                return  # a tab behind another (see TabbedPane) doesn't follow its pane
            splitter = pane.parent()
            min_size = self.style.PANE_MIN_HEIGHT if splitter.orientation() == Qt.Orientation.Vertical else self.style.PANE_MIN_WIDTH
            current = pane.height() if splitter.orientation() == Qt.Orientation.Vertical else pane.width()
            big_enough = current > min_size + self.style.igap
            if not is_minimized and not big_enough:
                click_minimize()
            elif is_minimized and big_enough:
                # The user dragged this pane back open by hand - show
                # frame_widget in place instead of requiring an explicit
                # click on the now-hidden Maximize button, the same way
                # dragging it down to its floor auto-minimizes above.
                unminimize(resize=False)

        def attach():
            '''Follows the sash of whichever Panes the pane is in now (see redocked).'''
            nonlocal watched_splitter
            pane = self.pane()
            splitter = pane.parent() if pane is not None else None
            if splitter is watched_splitter:
                return
            if watched_splitter is not None:
                try:
                    watched_splitter.splitterMoved.disconnect(on_sash_moved)
                except (RuntimeError, TypeError):
                    pass  # deleted with its old layout
            watched_splitter = splitter
            if splitter is not None:
                splitter.splitterMoved.connect(on_sash_moved)

        def redocked(keep: bool):
            '''
            After the panel moves to another pane (see DockArea): starts
            following that one, and - if it was minimized and keep - shrinks
            it there too, once the new layout has its sizes. Otherwise it
            comes back open (a tab behind another, or a pane that's gone).
            '''
            nonlocal is_minimized, normal_min_extent
            was_minimized = is_minimized
            if is_minimized:
                # Its old pane - and the floor lowered on it - are gone: start over open
                is_minimized = False
                normal_min_extent = None
                button.clicked.disconnect()
                self._connect(button, click_minimize)
                button.setText(minimize_text)
                if frame_widget is not None:
                    frame_widget.show()
            attach()
            if was_minimized and keep:
                QTimer.singleShot(0, lambda: self.pane() is not None and click_minimize())

        def set_minimized(minimized: bool):
            if minimized:
                click_minimize()
            else:
                unminimize(resize=False)

        self._connect(button, click_minimize)
        attach()
        self._minimizer = {"is": lambda: is_minimized, "set": set_minimized, "redocked": redocked}

        return button

    def pane(self) -> QWidget | None:
        '''
        The pane this menu bar's panel sits in right now - the nearest
        widget up from it that's directly in a splitter (a Panes) - or None.
        '''
        widget = self.parentWidget()
        while widget is not None and not isinstance(widget.parentWidget(), QSplitter):
            widget = widget.parentWidget()
        return widget

    def is_minimized(self) -> bool:
        return self._minimizer is not None and self._minimizer["is"]()

    def set_minimized(self, minimized: bool):
        '''Minimizes or restores in place (no resize) - for a panel with a minimize button.'''
        if self._minimizer is not None:
            self._minimizer["set"](minimized)

    def redocked(self, keep_minimized: bool = True):
        '''The panel has moved to another pane - see minimize_button's redocked.'''
        if self._minimizer is not None:
            self._minimizer["redocked"](keep_minimized)

    # Title or tabs

    def set_title_widget(self, widget: QWidget | None):
        '''
        Shows widget (e.g. a TabStrip) where the title is, stretched over
        the room the buttons leave - or, with None, the title again. The
        widget it replaces, if not the title, is deleted.
        '''
        current = self._title_widget or self.game_label
        if widget is current or (widget is None and self._title_widget is None):
            return
        index = self.row.indexOf(current)
        self._fixed[self._fixed.index(current)] = widget or self.game_label
        if self._title_widget is not None:
            self.row.removeWidget(self._title_widget)
            self._title_widget.hide()
            self._title_widget.deleteLater()
        if widget is None:
            self.game_label.show()
        else:
            self.game_label.hide()
            self.row.insertWidget(index, widget, 1)
        self._title_widget = widget
        self._update_squashing()

    def title(self) -> str:
        return self.game_label.text()

    # Important Buttons

    def add_important(self, button_class: type[ImportantButton], *args) -> ImportantButton | None:
        '''
        Adds an important button (see important_buttons) - args are passed
        through to its constructor after context. Returns the button, or
        None if it isn't available right now (see is_available).
        '''
        if not button_class.is_available(self.context):
            return None
        button = button_class(self.context, *args)
        self._insert_entry(button, "button")
        return button

    def add_config_buttons(self, names: list[str]):
        '''
        Adds the named menu bar buttons (a page config's "menu_bar" - keys of
        important_buttons.MENU_BAR_BUTTONS), grouped and ordered by
        MENU_BAR_GROUPS rather than by names' own order. Buttons that aren't
        available right now (see is_available) don't count toward a group.
        Everything else a page's menu bar has, it has by itself - see MenuBar.
        '''
        for name in names:
            if name not in MENU_BAR_BUTTONS:
                print(f"MenuBar has no button named {name!r}, skipping")
        wanted = set(names)
        for group_key, sections in MENU_BAR_GROUPS.items():
            present = []
            for header, section_names in sections:
                button_classes = [MENU_BAR_BUTTONS[name] for name in section_names
                                  if name in wanted and MENU_BAR_BUTTONS[name].is_available(self.context)]
                if button_classes:
                    present.append((header, button_classes))
            button_classes = [button_class for _, section in present for button_class in section]
            if len(button_classes) == 1:
                self.add_important(button_classes[0])
            elif button_classes:
                self.add_important(ButtonGroup, group_key, present)

    def page_buttons(self):
        '''Every standard page button - see PAGE_BUTTON_NAMES.'''
        self.add_config_buttons(PAGE_BUTTON_NAMES)
