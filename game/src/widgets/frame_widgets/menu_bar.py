from ...app_core import Context
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QComboBox, QFrame, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QWidget
from ..popup import message
from typing import Callable

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

    def add_tooltip(self, widget, key: str):
        self.context.style.add_tooltip(widget, "menu_bar_tooltips", key)

    def add_button(self, label: str = "_default", function: Callable | None = None) -> QPushButton:
        button = QPushButton(self.context.labels.get("menu_bar_buttons", label))
        button.setFont(self.style.get_font())
        if function is not None:
            self._connect(button, function)
        self.row.addWidget(button)
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
        called with whichever one the user picks.
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
        self.row.addWidget(dropdown)
        return dropdown

    # Panel Buttons

    def minimize_button(self, frame_widget: QWidget | None = None, pane: QWidget | None = None):
        '''
        Adds a button that hides frame_widget and shrinks pane down to its
        minimum size, or restores both - and auto-minimizes/restores as
        the user drags pane's containing Panes sash past that minimum,
        mirroring the old <Configure>-driven auto-minimize.
        '''
        minimize_text = self.context.labels.get("menu_bar_buttons", "minimize")
        maximize_text = self.context.labels.get("menu_bar_buttons", "maximize")
        button = self.add_button("minimize")
        remembered_size = None

        def shrink_pane():
            nonlocal remembered_size
            if pane is None:
                return
            splitter = pane.parent()
            index = splitter.indexOf(pane)
            sizes = splitter.sizes()
            remembered_size = sizes[index]
            min_size = self.style.PANE_MIN_HEIGHT if splitter.orientation() == Qt.Orientation.Vertical else self.style.PANE_MIN_WIDTH
            sizes[index] = min_size
            splitter.setSizes(sizes)

        def grow_pane():
            if pane is None:
                return
            splitter = pane.parent()
            index = splitter.indexOf(pane)
            sizes = splitter.sizes()
            sizes[index] = remembered_size if remembered_size else self.style.PANE_BIG
            splitter.setSizes(sizes)

        def click_minimize(already_shrunk: bool = False):
            button.clicked.disconnect()
            self._connect(button, click_maximize)
            button.setText(maximize_text)
            if not already_shrunk:
                shrink_pane()
            if frame_widget is not None:
                frame_widget.hide()

        def click_maximize():
            button.clicked.disconnect()
            self._connect(button, click_minimize)
            button.setText(minimize_text)
            grow_pane()
            if frame_widget is not None:
                frame_widget.show()

        def on_sash_moved(pos=None, index=None):
            if pane is None:
                return
            splitter = pane.parent()
            min_size = self.style.PANE_MIN_HEIGHT if splitter.orientation() == Qt.Orientation.Vertical else self.style.PANE_MIN_WIDTH
            current = pane.height() if splitter.orientation() == Qt.Orientation.Vertical else pane.width()
            if current <= min_size + self.style.igap:
                click_minimize(already_shrunk=True)

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
