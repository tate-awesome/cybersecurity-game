from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (QGridLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
                               QSizePolicy, QToolButton, QWidget)
from collections.abc import Callable
from ...app_core import Context
from ...network.process import Process

# A process's lifecycle as a flat card shows it. is_stopping takes priority
# over is_starting over is_running, so a process only has to flag the
# transitional phases during their window (see Process.is_starting).
PHASE_STOPPED = "stopped"
PHASE_STARTING = "starting"
PHASE_RUNNING = "running"
PHASE_STOPPING = "stopping"


class ElidingLabel(QLabel):
    '''
    A label that shows "…" instead of hard-clipping when it's narrower than
    its text, and keeps the full text as a tooltip. Used for flat card
    titles, which share their row with the button and so can run out of room
    in a narrow card. It still *prefers* its full width (so the card grows to
    fit the title up to the card's max width), but reports a tiny minimum so
    it can shrink and elide once the card is capped or the panel is narrow.
    '''

    def __init__(self, text: str = "", parent: QWidget | None = None):
        super().__init__(text, parent)
        self._full_text = text
        self.setToolTip(text)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

    def sizeHint(self) -> QSize:
        # Report the FULL text's width, not the elided text currently shown -
        # otherwise the card would keep shrinking to fit its own ellipsis.
        # This is what lets the layout size columns to the widest real title.
        return QSize(self.fontMetrics().horizontalAdvance(self._full_text) + 2,
                     super().sizeHint().height())

    def minimumSizeHint(self) -> QSize:
        # A plain QLabel's minimum is its full text width, which would keep
        # the card from ever shrinking the title. Allow it down to an
        # ellipsis' width so the row can give the title whatever's left.
        return QSize(self.fontMetrics().horizontalAdvance("…") + 4,
                     super().minimumSizeHint().height())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        elided = self.fontMetrics().elidedText(self._full_text, Qt.TextElideMode.ElideRight, self.width())
        # QLabel.setText (not self.setText) - this is display-only, the full
        # text is kept in _full_text for the next resize and the tooltip.
        QLabel.setText(self, elided)

class BaseForm(QWidget):
    '''
    Shared by network_action_panel's and modbus_panel's process/action forms. The two
    differ only in how they source display text and lay out the process
    button row:
      - network_action_panel forms pass a `key` and look their text up via
        context.labels (i18n), and track game_progress on start.
      - modbus_panel forms pass no `key` (defaults to None) and build their
        text directly from `process_noun` (not translated).

    The process button is optimistic: clicking it immediately shows the
    target state's text with no command (so it can't be double-clicked
    mid-transition), and add_process_button polls process_status_func on the
    animation loop to reconcile the button/status label with whatever the
    process or AP actually confirms - which may lag behind the click for
    network-backed forms, or land immediately for local processes.
    '''
    def __init__(self, master: QWidget, context: Context, process_noun: str = "Process", key: str | None = None,
                 flat: bool = False, title_dot: bool = True):
        '''
        process_noun is used like "start sniffer" "start DoS attack" "stopping NFQ" "ARP Spoofer is running" "NFQ is on"
        key, if given, selects the "network_action_forms"/"network_action_panels" i18n text
        for this form instead of building plain text from process_noun.

        flat (network_action_panel only) gives the card the compact layout:
        the header, a status dot and the start/stop button share one row
        (no separate status line), each entry's prompt becomes its
        placeholder, and the card can be minimized to hide its entries. The
        grid is still the layout underneath - the header bar and each entry
        just span all its columns - so forms that add their own grid rows
        (e.g. ap_connect's connection label) keep working unchanged.
        '''
        super().__init__(master)

        self.style = context.style
        self.context = context
        self.key = key
        self.process_noun = process_noun
        self.flat = flat
        self.title_dot = title_dot
        self.has_process_button = False

        # Flat-layout widgets, filled in by add_header/add_labeled_entry/
        # add_process_row as the form builds itself.
        self.header_bar: QWidget | None = None
        self.header_bar_layout: QHBoxLayout | None = None
        self.status_dot: QLabel | None = None
        self.caret_button: QToolButton | None = None
        self._entry_widgets: list[QWidget] = []  # per-entry rows, for minimize
        self.entry_dots: list[QLabel] = []  # a per-entry status dot, when asked for
        self._minimized = False

        self.style.set_material(self, "card")

        self.grid_layout = QGridLayout(self)
        # No left/right margin - the CTk version never padded the frame
        # itself (see add_label_row's padx=nogap), only individual rows
        # like add_labeled_entry/add_process_row padded their own widgets
        # via padx=gap. A blanket horizontal margin here would inset every
        # row, including the ones meant to reach the form's edges.
        self.grid_layout.setContentsMargins(self.style.igap, self.style.igap, self.style.igap, self.style.igap)
        self.grid_layout.setVerticalSpacing(self.style.igap)
        self.grid_layout.setHorizontalSpacing(self.style.igap)
        self.grid_layout.setColumnStretch(0, 0)
        self.grid_layout.setColumnStretch(1, 1)
        self.grid_layout.setColumnStretch(2, 0)

        # Resolve attack labels
        if self.key is not None:
            self.status_on_text = self.context.labels.get(f"network_action_forms_{self.key}_on")
            self.status_off_text = self.context.labels.get(f"network_action_forms_{self.key}_off")
            self.start_process_text = self.context.labels.get(f"network_action_forms_{self.key}_start")
            self.stop_process_text = self.context.labels.get(f"network_action_forms_{self.key}_stop")
        else:
            self.status_on_text = f"{self.process_noun} is on"
            self.status_off_text = f"{self.process_noun} is off"
            self.start_process_text = f"Start {self.process_noun}"
            self.stop_process_text = f"Stop {self.process_noun}"

        # The flat button restates only the verb, with a play/stop glyph -
        # what it acts on is already the card's title. The full label text
        # ("Start Spoofer") stays the button text everywhere else.
        if self.flat:
            self.start_button_text = f"{self.style.icon('player-play')}  Start"
            self.stop_button_text = f"{self.style.icon('square')}  Stop"
            # Shown while the process is between states (see the phase model).
            self.starting_button_text = "Starting"
            self.stopping_button_text = "Stopping"
            # Shown on the start button while any entry is still empty.
            self.input_needed_text = f"{self.style.icon('alert-triangle')}  Input"
        else:
            self.start_button_text = self.start_process_text
            self.stop_button_text = self.stop_process_text
            # Non-flat (modbus) keeps its old optimistic look: the button jumps
            # to the target state's text immediately, with no dedicated
            # transitional wording.
            self.starting_button_text = self.stop_process_text
            self.stopping_button_text = self.start_process_text
            self.input_needed_text = self.start_process_text

        self.current_row = 0
        self.entry_index = 0
        self.entries: list[QLineEdit] = []
        self.start_process = lambda: None
        self.stop_process = lambda: None
        self._process_button_connected = False

    def wire_button(self, button: QPushButton, function: Callable):
        '''
        clicked emits a "checked" bool that none of these callbacks expect -
        drop it before calling through. Reusable by subclasses (e.g. Modify)
        that wire up their own buttons outside of add_process_row/add_button.
        '''
        button.clicked.connect(lambda checked=False, function=function: function())

    def fixed_width_wrapper(self, widget: QWidget, alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignLeft) -> QWidget:
        '''
        Wraps `widget` (expected to already have its own setFixedWidth) in
        an ordinarily-growable QWidget, so the grid cell can be given this
        wrapper instead of `widget` itself. A grid column sizes itself to
        match whatever's placed in it - handing it a fixed-width widget
        directly locks that ENTIRE COLUMN to that width everywhere it's
        used, which in a multi-row form sharing columns (e.g. Modify's
        multiplier/offset table) rigidly locks every row's column instead
        of just the one widget that's supposed to be fixed-size. The
        wrapper has no size of its own, so it stretches/shrinks with the
        column normally while `widget` stays visually locked within
        whatever room that leaves, pinned to `alignment` (an explicit
        stretch on the far side rather than Qt's own alignment handling -
        a lone item with nothing else competing for space in a box layout
        gets centered by default, not pinned to a specific side).
        '''
        wrapper = QWidget()
        layout = QHBoxLayout(wrapper)
        layout.setContentsMargins(0, 0, 0, 0)
        if alignment != Qt.AlignmentFlag.AlignLeft:
            layout.addStretch()
        layout.addWidget(widget)
        if alignment != Qt.AlignmentFlag.AlignRight:
            layout.addStretch()
        return wrapper

    def get_process(self, process_class: type[Process], *args, capability: str | None = None,
                    tags: list[str] | None = None, **kwargs) -> Process:
        '''
        Retrieves this form's process from context.process_manager, creating
        and registering it under `key` on first visit. Since forms are
        recreated on every refresh, this is how a form regains control of a
        still-running process instead of losing track of it.
        Requires `key` to have been set - it doubles as the process's name.
        tags is passed through to ProcessManager.add_process on first visit
        (e.g. "stop_last") - ignored on later visits, since the process is
        already registered by then.

        capability, if given and currently hosted by the privileged helper
        (see network/helper), makes this a proxy to the helper's copy
        instead of an in-process instance - decided on first visit, so a
        still-running process keeps its home until the page is rebuilt.
        '''
        assert self.key is not None, "get_process() requires key to be set"
        process = self.context.process_manager.get_process(self.key)
        if process is None:
            if capability is not None and self.context.helper.hosts(capability):
                process = self.context.helper.proxy(capability)
            else:
                process = process_class(self.context.buffer, self.context, *args, **kwargs)
            self.context.process_manager.add_process(self.key, process, tags)
        return process

    def add_header(self, text: str | None = None):
        '''
        text: explicit header text (modbus_panel forms). If omitted,
        network_action_panel forms look their header up via context.labels using
        `key` (must be set).
        '''
        if text is None:
            assert self.key is not None, "add_header() with no text requires key to be set"
            text = str(self.context.labels.get(f"hacking_forms_{self.key}"))
        if self.flat:
            return self._add_flat_header(text)
        self.header = QLabel(text)
        self.header.setFont(self.style.get_font())
        # columnSpan=-1 spans to the layout's actual last column (as
        # declared by the setColumnStretch calls in __init__) instead of a
        # hardcoded 10 - that hardcoded span was wider than the 3 columns
        # this form ever really uses, so Qt treated the row as having 7
        # extra phantom columns past the real content, each still adding
        # its own horizontal spacing and stealing width the actual columns
        # should have gotten, which is what left a gap on the form's right
        # edge.
        self.grid_layout.addWidget(self.header, self.current_row, 0, 1, -1, Qt.AlignmentFlag.AlignCenter)
        self.current_row += 1

    def _add_flat_header(self, text: str):
        '''
        The flat card's top row: a status dot, the left-aligned title, then
        (appended later) a minimize caret and the start/stop button. The row
        is one widget spanning every grid column, so entries and any extra
        rows a form adds still sit below it in the grid as usual.
        '''
        self.header_bar = QWidget()
        self.header_bar_layout = QHBoxLayout(self.header_bar)
        self.header_bar_layout.setContentsMargins(0, 0, 0, 0)
        self.header_bar_layout.setSpacing(self.style.igap // 2)

        # Status dot - idle until the process confirms it's running (see
        # _set_dot_tone). "⬤" is drawn in the dot's text color, which set_tone
        # keeps on the theme's material: muted off, yellow mid-transition,
        # green running. A form can opt out (title_dot=False, e.g. wifi, which
        # shows per-entry dots instead).
        if self.title_dot:
            self.status_dot = QLabel("⬤")
            self.status_dot.setFont(self.style.get_font("small"))
            self.style.set_tone(self.status_dot, "muted")
            self.header_bar_layout.addWidget(self.status_dot)

        self.header = ElidingLabel(text)
        header_font = QFont(self.style.get_font("default"))
        header_font.setBold(True)
        self.header.setFont(header_font)
        self.header.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        # The title takes the row's slack (stretch 1) and elides when there
        # isn't enough, so the caret and button stay pinned to the right.
        self.header_bar_layout.addWidget(self.header, 1)

        self.grid_layout.addWidget(self.header_bar, self.current_row, 0, 1, -1)
        self.current_row += 1
        return self.header

    def _ensure_caret(self):
        '''
        Adds the minimize caret to the header the first time the card gets
        an entry - entry-less cards never grow one, so they stay as small as
        a minimized card already is.
        '''
        if self.caret_button is not None or self.header_bar_layout is None:
            return
        self.caret_button = QToolButton()
        self.caret_button.setAutoRaise(True)
        self.caret_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.caret_button.setFont(self.style.get_font("icon"))
        self.caret_button.setText(self.style.icon("chevron-down"))
        self.caret_button.setToolTip("Hide inputs")
        self.caret_button.clicked.connect(lambda checked=False: self.toggle_minimized())
        # Sits just left of where the start/stop button lands (added last).
        self.header_bar_layout.addWidget(self.caret_button)

    def toggle_minimized(self, minimized: bool | None = None):
        '''Collapses/expands the card's entry rows (flat cards only).'''
        if not self.flat:
            return
        self._minimized = (not self._minimized) if minimized is None else minimized
        for widget in self._entry_widgets:
            widget.setVisible(not self._minimized)
        if self.caret_button is not None:
            self.caret_button.setText(self.style.icon("chevron-right" if self._minimized else "chevron-down"))
            self.caret_button.setToolTip("Show inputs" if self._minimized else "Hide inputs")

    def unit_height(self) -> int:
        '''
        How tall this flat card is with just its header and button - no
        entries or extra rows. The network action panel's grid cell height
        (see FlowLayout).
        '''
        rows = [w for w in (self.header_bar, getattr(self, "process_button", None)) if w is not None]
        margins = self.grid_layout.contentsMargins()
        return (margins.top() + margins.bottom() + sum(w.sizeHint().height() for w in rows)
                + self.grid_layout.verticalSpacing() * max(len(rows) - 1, 0))

    def _set_dot_tone(self, tone: str):
        '''Colors the title status dot (if this card has one) - see _add_flat_header.'''
        if self.status_dot is not None:
            self.style.set_tone(self.status_dot, tone)

    def add_label_row(self, label_slot: str, label_keys: list[str]) -> list[QLabel]:
        column = 0
        output = []
        for key in label_keys:
            text = self.context.labels.get(f"{label_slot}_{key}")
            label = QLabel(text)
            label.setFont(self.style.get_font("mono"))
            if column == 0:
                label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            else:
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.grid_layout.addWidget(label, self.current_row, column)
            column += 1
            output.append(label)
        self.current_row += 1
        return output

    def add_labeled_entry(self, label: str, autosave: bool = True, dot: bool = False):
        '''
        Adds a labeled entry for the curent row in the form.
        With autosave, the entry saves and reloads its text input from the
        page's states - without, the form fills and saves it itself (e.g.
        WifiForm's, which live in app-wide preferences instead).
        With dot (flat cards only), a status dot sits to the left of the
        entry, collected in self.entry_dots for the form to color (wifi uses
        one per network to show which it's on).
        Requires `key` to have been set (network_action_forms forms only).
        '''

        assert self.key is not None, "add_labeled_entry() requires key to be set"

        # Create widgets
        label_widget = QLabel(label)
        label_widget.setFont(self.style.get_font())
        label_widget.setAlignment(Qt.AlignmentFlag.AlignLeft)

        entry = QLineEdit()
        entry.setAlignment(Qt.AlignmentFlag.AlignLeft)
        entry.setFont(self.style.get_font())

        if self.flat:
            # Flat card: the prompt lives inside the entry as placeholder
            # text, and the entry spans the card full-width. Tracked so the
            # minimize caret can hide it. The label widget is still returned
            # for callers that unpack it, just never placed.
            entry.setPlaceholderText(label.rstrip(":").strip())
            if dot:
                row = QWidget()
                row_layout = QHBoxLayout(row)
                row_layout.setContentsMargins(0, 0, 0, 0)
                row_layout.setSpacing(self.style.igap // 2)
                entry_dot = QLabel("⬤")
                entry_dot.setFont(self.style.get_font("small"))
                self.style.set_tone(entry_dot, "muted")
                # Fixed to the glyph's width so blanking it (empty text) still
                # reserves the space - the entries stay aligned either way.
                entry_dot.setFixedWidth(entry_dot.fontMetrics().horizontalAdvance("⬤"))
                self.entry_dots.append(entry_dot)
                row_layout.addWidget(entry_dot)
                row_layout.addWidget(entry, 1)
                self.grid_layout.addWidget(row, self.current_row, 0, 1, -1)
                self._entry_widgets.append(row)
            else:
                self.grid_layout.addWidget(entry, self.current_row, 0, 1, -1)
                self._entry_widgets.append(entry)
            self._ensure_caret()
        else:
            self.grid_layout.addWidget(label_widget, self.current_row, 1)
            # QLineEdit's default horizontal size policy is Expanding - even
            # sitting in column 2 (stretch=0, see __init__), its own policy
            # still lets it balloon to fill whatever room that column ends up
            # with. A fixed width overrides that, and fixed_width_wrapper keeps
            # it from also locking the whole column to that width.
            entry.setFixedWidth(self.style.igap * 16)
            self.grid_layout.addWidget(self.fixed_width_wrapper(entry), self.current_row, 2, Qt.AlignmentFlag.AlignRight)
        self.entries.append(entry)
        self.current_row += 1
        if not autosave:
            return label_widget, entry

        # Bind autosave
        save_slots = self.context.states.get("network_action_form_inputs", self.key)
        def autosave(text, e=entry, idx=self.entry_index):
            save_slots[idx] = text
        entry.textEdited.connect(autosave)

        # Load saved entry input
        entry.setText(save_slots[self.entry_index])

        # Update current index
        self.entry_index += 1

        return label_widget, entry

    def add_process_row(self, start_func: Callable, stop_func: Callable, status_func: Callable[[], bool],
                        default_status: str = "", starting_func: Callable[[], bool] | None = None,
                        stopping_func: Callable[[], bool] | None = None):

        if self.has_process_button:
            return

        # Create widgets
        self.process_status = QLabel(default_status)
        self.process_status.setFont(self.style.get_font())
        self.process_button = QPushButton("")
        self.process_button.setFont(self.style.get_font())
        self.place_process_row()

        # Set function definitions
        self.start_process = start_func
        self.stop_process = stop_func
        self.status_func = status_func
        # The transitional-phase checks: taken as given, else from the Process
        # behind status_func (so forms don't have to pass them), else never.
        process = getattr(status_func, "__self__", None)
        self.starting_func = starting_func or (process.is_starting if isinstance(process, Process) else (lambda: False))
        self.stopping_func = stopping_func or (process.is_stopping if isinstance(process, Process) else (lambda: False))

        # Phase as of the last refresh (None forces the first refresh below to
        # configure the button/status regardless of state)
        self.process_phase = None
        self.refresh_process_button()

        # Return submits the form - a no-op for modbus_panel forms, which never populate self.entries
        for entry in self.entries:
            entry.returnPressed.connect(self.click_start)

        # Update current index
        self.current_row += 1

        self.has_process_button = True

        # Polled so the optimistic text/command set by click_start/click_stop
        # gets reconciled with reality once the underlying process or AP
        # actually confirms the new state.
        self.context.animation_manager.add_callback(f"process_button_{id(self)}", self.refresh_process_button)

    def place_process_row(self):
        '''
        Puts process_status and process_button into the grid on current_row
        - overridden by forms that lay that row out differently (e.g.
        CombinedTable, which has more buttons beside it).
        '''
        if self.flat:
            # The button is a full-width bar across the bottom of the card,
            # below the entries. The header row carries only the dot, title
            # and minimize caret; the status line is dropped - the dot and
            # the button's own icon carry the state instead. process_status
            # is kept as a detached label so apply_phase can still set its
            # text without special-casing.
            # The button's row takes any height the card is stretched past its
            # natural size (the network action panel sizes cards to whole grid
            # cells - see FlowLayout), with the button pinned to its bottom so
            # the slack opens up between the entries and the button.
            self.process_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            self.grid_layout.setRowStretch(self.current_row, 1)
            self.grid_layout.addWidget(self.process_button, self.current_row, 0, 1, -1, Qt.AlignmentFlag.AlignBottom)
            return
        self.process_status.setAlignment(Qt.AlignmentFlag.AlignLeft)
        if self.key is not None:
            self.grid_layout.addWidget(self.process_status, self.current_row, 1, 1, 1)
        else:
            self.grid_layout.addWidget(self.process_status, self.current_row, 0, 1, 2)
        self.grid_layout.addWidget(self.fixed_width_wrapper(self.process_button), self.current_row, 2, Qt.AlignmentFlag.AlignRight)

    def refresh_process_button(self):
        '''
        Reconcile the button, status text and indicator dot with the process's
        current phase (see Process.is_starting / the PHASE_* constants). Polled,
        so the optimistic text/dot a click sets gets corrected once the process
        confirms the new state.
        '''
        phase = self.current_phase()
        if phase != self.process_phase:
            self.process_phase = phase
            self.apply_phase(phase)
        # While stopped, a flat card warns on the button when an entry is still
        # empty - polled, since entries are edited after apply_phase ran.
        if self.flat and phase == PHASE_STOPPED:
            self.refresh_input_warning()

    def current_phase(self) -> str:
        '''stopping > starting > running > stopped - see the PHASE_* constants.'''
        if self.stopping_func():
            return PHASE_STOPPING
        if self.starting_func():
            return PHASE_STARTING
        if self.status_func():
            return PHASE_RUNNING
        return PHASE_STOPPED

    def apply_phase(self, phase: str):
        '''
        Sets the button text + click action, the (non-flat) status label, and
        the dot's color for a phase. Running is green and offers Stop, stopped
        is muted and offers Start, and the two transitions are yellow: starting
        offers Stop (cancel), stopping offers Start.
        '''
        self._disconnect_process_button()
        if phase == PHASE_RUNNING:
            self.wire_button(self.process_button, self.click_stop)
            self.process_button.setText(self.stop_button_text)
            self.process_status.setText(self.status_on_text)
            self._set_dot_tone("good")
        elif phase == PHASE_STARTING:
            self.wire_button(self.process_button, self.click_stop)  # click cancels the start
            self.process_button.setText(self.starting_button_text)
            self.process_status.setText(self.status_on_text)
            self._set_dot_tone("warning")
        elif phase == PHASE_STOPPING:
            self.wire_button(self.process_button, self.click_start)
            self.process_button.setText(self.stopping_button_text)
            self.process_status.setText(self.status_off_text)
            self._set_dot_tone("warning")
        else:  # PHASE_STOPPED
            self.wire_button(self.process_button, self.click_start)
            self.process_button.setText(self.start_button_text)
            self.process_status.setText(self.status_off_text)
            self._set_dot_tone("muted")
        self._process_button_connected = True

    def entries_filled(self) -> bool:
        '''Whether every entry on this form has (non-whitespace) text.'''
        return all(entry.text().strip() for entry in self.entries)

    def refresh_input_warning(self):
        '''
        Flat start button: "⚠ Input" while any entry is empty, else the normal
        start text. No-op for a card with no entries (nothing to fill).
        '''
        if not self.flat or not self.entries:
            return
        text = self.start_button_text if self.entries_filled() else self.input_needed_text
        if self.process_button.text() != text:
            self.process_button.setText(text)

    def click_start(self):
        '''Optimistically show the "starting" state, then kick off the start.'''
        if self.key is not None:
            self.context.states.set("game_progress", self.key, value=1)
        self.process_button.setText(self.starting_button_text)
        self._set_dot_tone("warning")
        self._disconnect_process_button()
        # Clear the confirmed phase so the next poll always reconciles, even if
        # start_process() fails and the phase reads the same as before the click.
        self.process_phase = None
        self.process_button.repaint()  # paint the optimistic text now, in case start_process() blocks briefly
        self.start_process()

    def click_stop(self):
        if not self.has_process_button:
            return
        self.process_button.setText(self.stopping_button_text)
        self._set_dot_tone("warning")
        self._disconnect_process_button()
        self.process_phase = None
        self.process_button.repaint()
        self.stop_process()

    def _disconnect_process_button(self):
        # Tracked explicitly rather than relying on disconnect() to raise
        # when nothing's connected - PySide6 only logs a RuntimeWarning in
        # that case (not a catchable RuntimeError), which would otherwise
        # spam the console on every form's first build.
        if self._process_button_connected:
            self.process_button.clicked.disconnect()
            self._process_button_connected = False

    def add_button(self, default_status: str = "", button_text: str = "", button_func: Callable | None = None):
        # Create widgets
        status = QLabel(default_status)
        status.setFont(self.style.get_font())
        status.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.grid_layout.addWidget(status, self.current_row, 1)

        button = QPushButton(button_text)
        button.setFont(self.style.get_font())
        if button_func is not None:
            self.wire_button(button, button_func)
        self.grid_layout.addWidget(button, self.current_row, 2)

        # Update current index
        self.current_row += 1

        return status, button
