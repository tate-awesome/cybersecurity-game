from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QLabel, QLineEdit, QPushButton, QWidget
from typing import Callable
from ...app_core import Context
from ...network.process import Process

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
    def __init__(self, master: QWidget, context: Context, process_noun: str = "Process", key: str | None = None):
        '''
        process_noun is used like "start sniffer" "start DoS attack" "stopping NFQ" "ARP Spoofer is running" "NFQ is on"
        key, if given, selects the "network_action_forms"/"network_action_panels" i18n text
        for this form instead of building plain text from process_noun.
        '''
        super().__init__(master)

        self.style = context.style
        self.context = context
        self.key = key
        self.process_noun = process_noun
        self.has_process_button = False

        # A plain QWidget doesn't paint a stylesheet background at all by
        # default (unlike QFrame/QScrollArea, which do) - it stays
        # visually transparent and whatever's behind it (Scrollable's own
        # background) shows straight through, regardless of what color
        # this stylesheet says - which is also why stacked forms had no
        # visible gap between them: both the form and the gap were really
        # just Scrollable's background showing through. WA_StyledBackground
        # opts this widget into that painting.
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet(self.style.themed(f"background-color: {self.style.color('widget')};", self))

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
            self.status_on_text = self.context.labels.get("network_action_forms", f"{self.key}_on")
            self.status_off_text = self.context.labels.get("network_action_forms", f"{self.key}_off")
            self.start_process_text = self.context.labels.get("network_action_forms", f"{self.key}_start")
            self.stop_process_text = self.context.labels.get("network_action_forms", f"{self.key}_stop")
        else:
            self.status_on_text = f"{self.process_noun} is on"
            self.status_off_text = f"{self.process_noun} is off"
            self.start_process_text = f"Start {self.process_noun}"
            self.stop_process_text = f"Stop {self.process_noun}"

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

    def get_process(self, process_class: type[Process], *args, tags: list[str] | None = None, **kwargs) -> Process:
        '''
        Retrieves this form's process from context.process_manager, creating
        and registering it under `key` on first visit. Since forms are
        recreated on every refresh, this is how a form regains control of a
        still-running process instead of losing track of it.
        Requires `key` to have been set - it doubles as the process's name.
        tags is passed through to ProcessManager.add_process on first visit
        (e.g. "stop_last") - ignored on later visits, since the process is
        already registered by then.
        '''
        assert self.key is not None, "get_process() requires key to be set"
        process = self.context.process_manager.get_process(self.key)
        if process is None:
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
            text = str(self.context.labels.get("hacking_forms", self.key))
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

    def add_label_row(self, label_slot: str, label_keys: list[str]) -> list[QLabel]:
        column = 0
        output = []
        for key in label_keys:
            text = self.context.labels.get(label_slot, key)
            label = QLabel(text)
            label.setFont(self.style.get_font("mono"))
            self.grid_layout.addWidget(label, self.current_row, column)
            column += 1
            output.append(label)
        self.current_row += 1
        return output

    def add_labeled_entry(self, label: str):
        '''
        Adds a labeled entry for the curent row in the form.
        This entry has autosave and auto-loading for its text input.
        Requires `key` to have been set (network_action_forms forms only).
        '''

        assert self.key is not None, "add_labeled_entry() requires key to be set"

        # Create widgets
        label_widget = QLabel(label)
        label_widget.setFont(self.style.get_font())
        label_widget.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.grid_layout.addWidget(label_widget, self.current_row, 1)

        entry = QLineEdit()
        entry.setFont(self.style.get_font())
        self.grid_layout.addWidget(entry, self.current_row, 2)
        self.entries.append(entry)

        # Bind autosave
        save_slots = self.context.states.get("hack_forms", self.key)
        def autosave(text, e=entry, idx=self.entry_index):
            save_slots[idx] = text
        entry.textEdited.connect(autosave)

        # Load saved entry input
        entry.setText(save_slots[self.entry_index])

        # Update current index
        self.current_row += 1
        self.entry_index += 1

        return label_widget, entry

    def add_process_row(self, start_func: Callable, stop_func: Callable, status_func: Callable[[], bool], default_status: str = ""):

        if self.has_process_button:
            return

        # Create widgets
        self.process_status = QLabel(default_status)
        self.process_status.setFont(self.style.get_font())
        self.process_button = QPushButton("")
        self.process_button.setFont(self.style.get_font())

        if self.key is not None:
            self.process_status.setAlignment(Qt.AlignmentFlag.AlignLeft)
            self.grid_layout.addWidget(self.process_status, self.current_row, 1)
            self.grid_layout.addWidget(self.process_button, self.current_row, 2)
        else:
            self.process_status.setAlignment(Qt.AlignmentFlag.AlignLeft)
            self.grid_layout.addWidget(self.process_status, self.current_row, 0)
            self.grid_layout.addWidget(self.process_button, self.current_row, 2)

        # Set function definitions
        self.start_process = start_func
        self.stop_process = stop_func
        self.status_func = status_func

        # Confirmed state as of the last refresh (None forces the first
        # refresh below to configure the button/status regardless of state)
        self.process_confirmed_state = None
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

    def refresh_process_button(self):
        '''
        Refresh the process button based on the current process status.
        '''
        running = bool(self.status_func())
        if running == self.process_confirmed_state:
            return
        self.process_confirmed_state = running
        if running:
            self.configure_on()
        else:
            self.configure_off()

    def click_start(self):
        '''
        Optimistically set the process button to the "stop" state and call
        '''
        if self.key is not None:
            self.context.states.set("game_progress", self.key, value=1)
        self.process_button.setText(self.stop_process_text)
        self._disconnect_process_button()
        # Unset the confirmed state so the next poll always reconciles the
        # button, even if start_process() fails and status_func() reports
        # the same value it did before this click (e.g. still False) -
        # otherwise refresh_process_button sees "no change" and never fires.
        self.process_confirmed_state = None
        self.process_button.repaint()  # paint the optimistic text now, in case start_process() blocks briefly
        self.start_process()

    def configure_on(self):
        self._disconnect_process_button()
        self.wire_button(self.process_button, self.click_stop)
        self._process_button_connected = True
        self.process_button.setText(self.stop_process_text)
        self.process_status.setText(self.status_on_text)

    def click_stop(self):
        if not self.has_process_button:
            return
        self.process_button.setText(self.start_process_text)
        self._disconnect_process_button()
        self.process_confirmed_state = None
        self.process_button.repaint()
        self.stop_process()

    def configure_off(self):
        self._disconnect_process_button()
        self.wire_button(self.process_button, self.click_start)
        self._process_button_connected = True
        self.process_button.setText(self.start_process_text)
        self.process_status.setText(self.status_off_text)

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
