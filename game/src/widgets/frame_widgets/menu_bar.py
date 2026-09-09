from ...app_core import Context
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QComboBox, QFrame, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QWidget
from ..popup import message
from .overlay import Overlay
from typing import Callable


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


class MenuBar(QFrame):
    '''
    The main Widget for the menu bar.
    Comes with a label and has a button maker.
    Inherits QFrame.
    '''

    def __init__(self, master: QWidget, context: Context, title_label: str = "_default"):
        super().__init__(master)
        self.context = context
        self.style = context.style

        master.layout().addWidget(self)
        self.setStyleSheet(self.style.themed(f"background-color: {self.style.color('widget')};", self))
        self.setContentsMargins(self.style.igap, self.style.cgap, self.style.igap, self.style.cgap)
        # Qt widgets default to a vertical size policy that's willing to
        # grow into whatever leftover space its layout has - the old
        # CTkFrame only ever got fill="x" (not expand=True), so it never
        # grew past its natural height, leaving Panes to claim the rest.
        # Maximum reproduces that: this frame can shrink but never grow
        # past its own sizeHint.
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)

        self.row = QHBoxLayout(self)
        self.row.setContentsMargins(self.style.igap, self.style.cgap, self.style.igap, self.style.cgap)

        self.game_label = QLabel(self.context.labels.get("menu_bar_titles", title_label))
        self.game_label.setFont(self.style.get_font())
        self.row.addWidget(self.game_label, 0, Qt.AlignmentFlag.AlignVCenter)
        self.row.addStretch()

        # Button overflow overlay - see update_squashing/_populate_overflow_overlay.
        # Always the rightmost widget in the row (add_button/add_dropdown
        # insert new entries just before it), hidden until squashing finds
        # something to put in it.
        self._entries: list[dict] = []
        self._squashed_entries: list[dict] = []
        self.the_overflow_button = QPushButton("...")
        self.the_overflow_button.setFont(self.style.get_font())
        self.row.addWidget(self.the_overflow_button)
        self.the_overflow_button.hide()
        self.overflow_overlay = Overlay(self.context.root, self.context, self.the_overflow_button, self._populate_overflow_overlay)

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
        become narrow again. Reporting the true floor instead - the label
        plus every dropdown (neither ever squashes) plus the overflow
        button alone - keeps that floor constant regardless of history, so
        the window/pane can always still be shrunk down to it, which is
        what actually lets squashing kick back in.
        '''
        margins = self.row.contentsMargins()
        spacing = self.row.spacing()
        width = margins.left() + margins.right()
        width += self.game_label.sizeHint().width()
        for entry in self._entries:
            if entry["kind"] == "dropdown":
                width += spacing + entry["widget"].sizeHint().width()
        width += spacing + self.the_overflow_button.sizeHint().width()
        return QSize(width, self.sizeHint().height())

    def add_tooltip(self, widget, key: str):
        self.context.style.add_tooltip(widget, "menu_bar_tooltips", key)

    def add_button(self, label: str = "_default", function: Callable | None = None) -> QPushButton:
        button = QPushButton(self.context.labels.get("menu_bar_buttons", label))
        button.setFont(self.style.get_font())
        if function is not None:
            self._connect(button, function)
        self._insert_entry(button, "button")
        return button

    def _connect(self, button: QPushButton, function: Callable):
        '''
        clicked emits a "checked" bool that none of these callbacks expect
        (see TitleMenu.button for the bug this avoids) - drop it before
        calling through.
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

    # Button overflow overlay
    #
    # Ported from the CTk version's update_squashing/overflow_button/
    # clone_button/populate_overflow_overlay: when the menu bar isn't wide
    # enough to fit every button, the ones that don't fit are hidden and an
    # overflow ("...") button appears with clones of them in a popup.

    def _insert_entry(self, widget: QWidget, kind: str):
        # Insert just before the overflow button so it stays the rightmost
        # widget in the row no matter how many buttons/dropdowns get added.
        index = self.row.indexOf(self.the_overflow_button)
        self.row.insertWidget(index, widget)
        self._entries.append({"widget": widget, "kind": kind})
        self._update_squashing()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_squashing()

    def _update_squashing(self):
        try:
            margins = self.row.contentsMargins()
            spacing = self.row.spacing()
            available_width = self.width() - margins.left() - margins.right()
            available_width -= self.game_label.sizeHint().width() + spacing

            fine = []
            squashed = []
            for entry in self._entries:
                available_width -= entry["widget"].sizeHint().width() + spacing
                if entry["kind"] != "button" or available_width >= 0:
                    fine.append(entry)
                else:
                    squashed.append(entry)

            self._squashed_entries = squashed
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
        for entry in self._squashed_entries:
            button = entry["widget"]
            proxy = QPushButton(button.text())
            proxy.setFont(self.style.get_font())
            # Replays a real click on the (hidden) original button rather
            # than capturing its callback at insert time, so a proxy always
            # reflects whatever label/handler the button currently has -
            # including buttons like minimize/reversible_button that swap
            # their text and handler dynamically after creation.
            proxy.clicked.connect(lambda checked=False, b=button: b.click())
            overlay.layout().addWidget(proxy)

    # Panel Buttons

    def minimize_button(self, frame_widget: QWidget | None = None, pane: QWidget | None = None):
        '''
        Adds a button that hides frame_widget and shrinks pane down to just
        this menu bar's own height, or restores both - and auto-minimizes
        as the user drags pane's containing Panes sash down to its normal
        floor (PANE_MIN_HEIGHT/WIDTH), mirroring the old <Configure>-driven
        auto-minimize.

        Space freed by shrinking is handed to the sibling panes evenly.
        Restoring takes it back from whichever sibling is currently
        tallest first (leveling siblings down together once they match),
        growing pane back to its authored share of the splitter - see
        Panes.default_stretch - rather than an arbitrary fixed size.
        '''
        minimize_text = self.context.labels.get("menu_bar_buttons", "minimize")
        maximize_text = self.context.labels.get("menu_bar_buttons", "maximize")
        button = self.add_button("minimize")
        is_minimized = False
        normal_min_extent = None  # pane's PANE_MIN_HEIGHT/WIDTH floor, remembered while it's lowered

        def shrink_pane():
            nonlocal normal_min_extent
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

        def grow_pane():
            nonlocal normal_min_extent
            if pane is None:
                return
            splitter = pane.parent()
            index = splitter.indexOf(pane)
            vertical = splitter.orientation() == Qt.Orientation.Vertical

            # Restore this pane's normal floor before asking the splitter
            # for more room - otherwise it's still pinned at the minimized
            # (menu-bar-only) height from shrink_pane.
            if normal_min_extent is not None:
                if vertical:
                    pane.setMinimumHeight(normal_min_extent)
                else:
                    pane.setMinimumWidth(normal_min_extent)
                normal_min_extent = None

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

        def click_maximize():
            nonlocal is_minimized
            if not is_minimized:
                return
            is_minimized = False
            button.clicked.disconnect()
            self._connect(button, click_minimize)
            button.setText(minimize_text)
            grow_pane()
            if frame_widget is not None:
                frame_widget.show()

        def on_sash_moved(pos=None, index=None):
            if pane is None or is_minimized:
                return
            splitter = pane.parent()
            min_size = self.style.PANE_MIN_HEIGHT if splitter.orientation() == Qt.Orientation.Vertical else self.style.PANE_MIN_WIDTH
            current = pane.height() if splitter.orientation() == Qt.Orientation.Vertical else pane.width()
            if current <= min_size + self.style.igap:
                click_minimize()

        self._connect(button, click_minimize)
        if pane is not None:
            pane.parent().splitterMoved.connect(on_sash_moved)

        return button

    def reversible_button(self, start_func: Callable, stop_func: Callable, inactive_label: str, active_label: str, start_active: bool = False):
        inactive_name = self.context.labels.get("menu_bar_buttons", inactive_label)
        active_name = self.context.labels.get("menu_bar_buttons", active_label)
        button = self.add_button(inactive_label)

        def stop():
            stop_func()
            button.clicked.disconnect()
            self._connect(button, start)
            button.setText(inactive_name)

        def start():
            start_func()
            button.clicked.disconnect()
            self._connect(button, stop)
            button.setText(active_name)

        # Sync the button's initial text/command to whatever state start_func/stop_func
        # already represent, without re-invoking either (they're already in that state).
        if start_active:
            self._connect(button, stop)
            button.setText(active_name)
        else:
            self._connect(button, start)
            button.setText(inactive_name)
        return button

    # Page Buttons

    def quit_button(self):
        button = self.add_button("quit_button", self.context.router.quit)
        self.add_tooltip(button, "quit_button")

    def refresh_button(self):
        button = self.add_button("refresh_button", self.context.router.refresh)
        self.add_tooltip(button, "refresh_button")

    def reset_button(self):
        button = self.add_button("reset_button", self.context.reset_data)
        self.add_tooltip(button, "reset_button")

    def back_button(self):
        button = self.add_button("back_button", self.context.router.go_back)
        self.add_tooltip(button, "back_button")

    def toggle_button(self):
        button = self.add_button("toggle_button", self.context.style.toggle_mode)
        self.add_tooltip(button, "toggle_button")

    def theme_button(self):
        button = self.add_button("theme_button", self.context.style.select_theme)
        self.add_tooltip(button, "theme_button")

    def pcap_button(self):
        button = self.add_button("pcap_button", self.context.buffer.loader.load_pcap)
        self.add_tooltip(button, "pcap_button")

    def save_button(self):
        button = self.add_button("save_button", self.context.buffer.replay.save_json)

    def load_button(self):
        button = self.add_button("load_button", self.context.buffer.replay.load_json)

    def stream_button(self):
        button = self.reversible_button(
            self.context.buffer.file_stream.start,
            self.context.buffer.file_stream.stop,
            "stream_button",
            "stream_button_active",
        )
        self.add_tooltip(button, "stream_button")

    def preset_button(self):
        button = self.add_button("preset_button", self.context.states.select)
        self.add_tooltip(button, "preset_button")

    def labels_button(self):
        button = self.add_button("labels_button", self.context.labels.select)
        self.add_tooltip(button, "labels_button")

    def help_button(self):
        button = self.add_button("help_button", lambda: message(self, self.context, self.context.help_message()))
        self.add_tooltip(button, "help_button")

    def data_button(self):
        button = self.add_button("fields_button", self.context.states.save_inputs)
        self.add_tooltip(button, "fields_button")

    def page_button(self):
        button = self.add_button("page_button", self.context.preferences.save_page)
        self.add_tooltip(button, "page_button")

    def page_buttons(self):
        self.quit_button()
        self.refresh_button()
        self.reset_button()
        self.back_button()
        self.help_button()
        self.toggle_button()
        self.theme_button()
        self.pcap_button()
        self.save_button()
        self.load_button()
        self.stream_button()
        self.preset_button()
        self.labels_button()
        self.data_button()
        self.page_button()
