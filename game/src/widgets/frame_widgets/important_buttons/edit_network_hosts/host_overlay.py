from .....app_core import Context
from ...overlay import Overlay
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QCheckBox, QFrame, QGridLayout, QLabel, QLineEdit, QPushButton, QScrollArea


class HostOverlay:
    '''
    Binds a button to open and close an overlay with a row for every MAC
    and IP address the network graph has seen (context.buffer.network),
    editing its nickname and hide fields in context.states["network_hosts"].
    It only writes context.states - the network graph polls them every
    frame and follows along.

    An address only gets an entry in network_hosts once one of its fields
    is edited, so the saved setting doesn't fill up with every host ever seen.
    '''
    # Past this share of the screen's height, the rows scroll
    MAX_SCREEN_HEIGHT = 0.7
    # An address's fields before it's edited
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

        macs, ips, host_ips = self.context.buffer.network.get_hosts()
        # The other way around too, for the IP rows' "Seen with"
        ip_hosts = {ip: [mac for mac in macs if ip in host_ips.get(mac, [])] for ip in ips}

        if not macs and not ips:
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

        # Address Rows, MACs then IPs, each under its section's name
        sections = (("macs", macs, host_ips), ("ips", ips, ip_hosts))
        for kind, addresses, seen_with in sections:
            section_label = QLabel(self.context.labels.get(f"network_hosts_sections_{kind}"))
            section_label.setFont(med)
            grid.addWidget(section_label, row, col)
            row += 1

            for address in addresses:
                address_label = QLabel(address)
                address_label.setFont(mono)
                grid.addWidget(address_label, row, col)
                col += 1
                seen_label = QLabel("\n".join(seen_with.get(address, [])))
                seen_label.setFont(mono)
                grid.addWidget(seen_label, row, col)
                col += 1
                # "nickname": "",
                nick_entry = QLineEdit()
                nick_entry.setFont(med)
                grid.addWidget(nick_entry, row, col)
                self.enrich_entry(nick_entry, kind, address, "nickname")
                nick_entries.append(nick_entry)
                col += 1
                # "hide": "0"
                hide_checkbox = QCheckBox()
                grid.addWidget(hide_checkbox, row, col)
                self.enrich_checkbox(hide_checkbox, kind, address, "hide")
                hide_checkboxes.append(hide_checkbox)

                col = 0
                row += 1

        # Do All buttons
        def connect(button, function):
            button.clicked.connect(lambda checked=False, function=function: function())

        # Reset All
        def reset_all():
            self.clear_entries(nick_entries)
            self.deselect_all(hide_checkboxes)
        button = QPushButton("Reset All")
        button.setFont(med)
        connect(button, reset_all)
        grid.addWidget(button, row + 1, col)
        col += 2
        # Nicknames
        button = QPushButton("Clear All")
        button.setFont(med)
        connect(button, lambda: self.clear_entries(nick_entries))
        grid.addWidget(button, row + 1, col)
        col += 1
        # Hide
        button = QPushButton("Select All")
        button.setFont(med)
        connect(button, lambda: self.select_all(hide_checkboxes))
        grid.addWidget(button, row, col)
        button = QPushButton("Deselect All")
        button.setFont(med)
        connect(button, lambda: self.deselect_all(hide_checkboxes))
        grid.addWidget(button, row + 1, col)

        # A busy network has more addresses than fit on screen
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
        overlay.layout().addWidget(scroll)

    def save(self, kind: str, address: str, key: str, value: str):
        '''
        Sets one of this address's fields in network_hosts - giving it an
        entry first if it has none, unless the value is the default anyway.
        '''
        saved = self.context.states.get("network_hosts", kind)
        if address not in saved:
            if value == self.DEFAULTS[key]:
                return
            saved[address] = dict(self.DEFAULTS)
        saved[address][key] = value

    def saved(self, kind: str, address: str, key: str):
        return self.context.states.get("network_hosts", kind).get(address, {}).get(key, self.DEFAULTS[key])

    def enrich_entry(self, entry: QLineEdit, kind: str, address: str, key: str):
        # Bind autosave
        def autosave(text, kind=kind, address=address, key=key):
            self.save(kind, address, key, text)
        entry.textEdited.connect(autosave)
        # clear_entries needs to trigger this same save when it sets text
        # programmatically, since textEdited (deliberately) doesn't fire for that.
        entry.autosave = lambda: autosave(entry.text())

        # Load saved entry input
        entry.setText(str(self.saved(kind, address, key)))

    def enrich_checkbox(self, checkbox: QCheckBox, kind: str, address: str, key: str):
        # Load previous input before connecting, so restoring it doesn't itself trigger autosave
        value = self.saved(kind, address, key)
        checkbox.setChecked(value == "1" or value == 1)

        # Stored as "1"/"0", like every other checkbox setting
        def autosave(checked: bool, kind=kind, address=address, key=key):
            self.save(kind, address, key, "1" if checked else "0")
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
