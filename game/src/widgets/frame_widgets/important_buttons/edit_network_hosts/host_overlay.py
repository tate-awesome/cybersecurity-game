from .....app_core import Context
from ...overlay import Overlay
from .....network.buffer.channels.network_graph import MAX_NICKNAME_LENGTH
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QCheckBox, QFrame, QGridLayout, QLabel, QLineEdit, QPushButton, QScrollArea


class HostOverlay:
    '''
    Binds a button to open and close an overlay with a row for every host
    (device - MAC address) the network graph has seen
    (context.buffer.network), with the IPs seen on it, editing its nickname
    and hide fields - kept in preferences, across workspaces (see
    Preferences.network_hosts). The network graph polls them every frame
    and follows along.

    A search box above the rows narrows them to the MACs, IPs or nicknames
    containing what's typed - and the Select/Clear All buttons only touch
    the rows still showing.

    A MAC only gets an entry once one of its fields is edited, so
    preferences don't fill up with every host ever seen.
    '''
    # Past this share of the screen's height, the rows scroll
    MAX_SCREEN_HEIGHT = 0.7
    # A MAC's fields before it's edited
    DEFAULTS = {"nickname": "", "hide": "0"}

    def __init__(self, button: QPushButton, context: Context):
        self.context = context
        self.style = context.style
        self.overlay = Overlay(self.context.root, context, button, self.populate_overlay, "east")

    def populate_overlay(self, overlay: Overlay):
        med = self.style.get_font()
        mono = self.style.get_font("mono")
        frame = QFrame()
        # Part of the overlay's background - follows the "overlay" surface, not "widget"
        self.style.set_material(frame, "overlay_card")
        grid = QGridLayout(frame)
        grid.setContentsMargins(self.style.igap, self.style.igap, self.style.igap, self.style.igap)
        grid.setVerticalSpacing(self.style.cgap * 2)
        grid.setHorizontalSpacing(self.style.igap)

        macs, host_ips = self.context.buffer.network.get_hosts()

        if not macs:
            label = QLabel(self.context.labels.get("network_hosts_none_seen"))
            label.setFont(med)
            grid.addWidget(label, 0, 0)
            overlay.layout().addWidget(frame)
            return

        row = 0
        col = 0

        # Top Row
        top_labels = self.context.labels.group("network_hosts_settings")
        for key, text in top_labels.items():
            top_label = QLabel(text)
            top_label.setFont(med)
            grid.addWidget(top_label, row, col)
            col += 1
        col = 0
        row += 1

        nick_entries = []
        hide_checkboxes = []
        # Each row's widgets and the text the search looks through besides
        # its nickname (see search)
        rows = []

        # Host Rows
        for mac in macs:
            ips = host_ips.get(mac, [])
            mac_label = QLabel(mac)
            mac_label.setFont(mono)
            grid.addWidget(mac_label, row, col)
            col += 1
            ips_label = QLabel("\n".join(ips))
            ips_label.setFont(mono)
            grid.addWidget(ips_label, row, col)
            col += 1
            # "nickname": "",
            nick_entry = QLineEdit()
            nick_entry.setFont(med)
            # As long as fits a chip on the network graph
            nick_entry.setMaxLength(MAX_NICKNAME_LENGTH)
            grid.addWidget(nick_entry, row, col)
            self.enrich_entry(nick_entry, mac, "nickname")
            nick_entries.append(nick_entry)
            col += 1
            # "hide": "0"
            hide_checkbox = QCheckBox()
            grid.addWidget(hide_checkbox, row, col)
            self.enrich_checkbox(hide_checkbox, mac, "hide")
            hide_checkboxes.append(hide_checkbox)

            rows.append(((mac_label, ips_label, nick_entry, hide_checkbox), nick_entry, " ".join([mac] + ips)))
            col = 0
            row += 1

        # Do All buttons, for the rows the search left showing
        def connect(button, function):
            button.clicked.connect(lambda checked=False, function=function: function())
        def shown(widgets):
            return [widget for widget in widgets if not widget.isHidden()]

        # Reset All
        def reset_all():
            self.clear_entries(shown(nick_entries))
            self.deselect_all(shown(hide_checkboxes))
        button = QPushButton("Reset All")
        button.setFont(med)
        connect(button, reset_all)
        grid.addWidget(button, row + 1, col)
        col += 2
        # Nicknames
        button = QPushButton("Clear All")
        button.setFont(med)
        connect(button, lambda: self.clear_entries(shown(nick_entries)))
        grid.addWidget(button, row + 1, col)
        col += 1
        # Hide
        button = QPushButton("Select All")
        button.setFont(med)
        connect(button, lambda: self.select_all(shown(hide_checkboxes)))
        grid.addWidget(button, row, col)
        button = QPushButton("Deselect All")
        button.setFont(med)
        connect(button, lambda: self.deselect_all(shown(hide_checkboxes)))
        grid.addWidget(button, row + 1, col)
        # The menu keeps its size while searching - the space the hidden
        # rows leave goes below the rest, instead of between them
        grid.setRowStretch(row + 2, 1)

        # A busy network has more hosts than fit on screen
        scroll = QScrollArea()
        self.style.set_material(scroll, "none")
        scroll.setWidget(frame)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        frame.ensurePolished()
        content = frame.sizeHint()
        max_height = int(self.context.root.screen().availableGeometry().height() * self.MAX_SCREEN_HEIGHT)
        scrollbar_width = scroll.verticalScrollBar().sizeHint().width()
        scroll.setFixedSize(content.width() + (scrollbar_width if content.height() > max_height else 0),
                            min(content.height(), max_height))

        # Above the scrolling rows, so it stays put while they scroll
        search_entry = QLineEdit()
        search_entry.setFont(med)
        search_entry.setPlaceholderText(self.context.labels.get("network_hosts_search"))
        search_entry.setClearButtonEnabled(True)
        search_entry.textChanged.connect(lambda text: self.search(text, rows))
        overlay.layout().addWidget(search_entry)
        overlay.layout().addWidget(scroll)
        search_entry.setFocus()

    def search(self, text: str, rows: list):
        '''Shows just the rows whose MAC, IPs or nickname contain text (any case).'''
        text = text.strip().lower()
        for widgets, nick_entry, searched in rows:
            matches = text in searched.lower() or text in nick_entry.text().lower()
            for widget in widgets:
                widget.setVisible(matches)

    def save(self, mac: str, key: str, value: str):
        '''Sets one of this MAC's fields (see Preferences.set_host_field).'''
        self.context.preferences.set_host_field(mac, key, value)

    def saved(self, mac: str, key: str):
        return self.context.preferences.host_field(mac, key)

    def enrich_entry(self, entry: QLineEdit, mac: str, key: str):
        # Bind autosave
        def autosave(text, mac=mac, key=key):
            self.save(mac, key, text)
        entry.textEdited.connect(autosave)
        # clear_entries needs to trigger this same save when it sets text
        # programmatically, since textEdited (deliberately) doesn't fire for that.
        entry.autosave = lambda: autosave(entry.text())

        # Load saved entry input
        entry.setText(str(self.saved(mac, key)))

    def enrich_checkbox(self, checkbox: QCheckBox, mac: str, key: str):
        # Load previous input before connecting, so restoring it doesn't itself trigger autosave
        value = self.saved(mac, key)
        checkbox.setChecked(value == "1" or value == 1)

        # Stored as "1"/"0", like every other checkbox setting
        def autosave(checked: bool, mac=mac, key=key):
            self.save(mac, key, "1" if checked else "0")
        checkbox.toggled.connect(autosave)

    def select_all(self, checkboxes: list[QCheckBox]):
        for checkbox in checkboxes:
            checkbox.setChecked(True)

    def deselect_all(self, checkboxes: list[QCheckBox]):
        for checkbox in checkboxes:
            checkbox.setChecked(False)

    def clear_entries(self, entries: list[QLineEdit]):
        for entry in entries:
            entry.setText("")
            entry.autosave()
