'''
Example panels for the theme editor's gallery (see ThemeEditorPage): every
kind of panel body the app has - a packet treeview, a console, a text
table, strip charts, the submarine map, the HVAC model, the network
diagram, forms and alerts - built from the same pieces the real panels
use, so a theme looks the same here as on a workspace. The canvases are
the real ones, drawing made-up data from the small stand-ins below
instead of the capture buffers, so nothing here can start a network
action or touch captured data - which leaves every control free to hover,
click and select, showing those colors too.

Titles are "menu_bar_titles_example_<name>" labels.
'''
import math

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QCheckBox, QComboBox, QLabel, QLineEdit, QPlainTextEdit, QPushButton, QSlider, QTableWidget,
                               QTableWidgetItem, QTabWidget, QWidget)

from ...app_core import Context
from ..canvases.house import House
from ..canvases.network_diagram import NetworkDiagramCanvas
from ..canvases.strip_chart import StripChart
from ..canvases.world_map import WorldMap
from ..frame_widgets.scrollable import Scrollable
from .base_form import BaseForm
from .packet_console.treeview import PacketTreeview
from .panel import Panel

# How many seconds of history the sample strip charts hold
CHART_SECONDS = 60


class PassWheel:
    '''Mixed into the sample canvases: the wheel scrolls the gallery instead of zooming them.'''

    def wheelEvent(self, event):
        event.ignore()


# Stand-ins for the capture buffers' channels - just the getters each canvas calls
class SampleSubmarine:
    '''A boat weaving across the map ("in") and its spoofed copy drifting off course ("out").'''

    def __init__(self):
        self.paths = {"in": [], "out": []}
        for step in range(80):
            x = 20 + step * 2
            self.paths["in"].append((x, 100 + 40 * math.sin(step / 12)))
            self.paths["out"].append((x, 100 + 40 * math.sin(step / 12) - step * 0.6))

    def get_simple_path(self, direction: str) -> list[tuple[float, float]]:
        return self.paths[direction]

    def get_position(self, direction: str) -> tuple[float, float]:
        return self.paths[direction][-1]

    def get_bearing(self, direction: str) -> float:
        (x1, y1), (x2, y2) = self.paths[direction][-2:]
        return math.atan2(y2 - y1, x2 - x1)


class SampleHVAC:
    '''A room a little cold, with the heater on.'''

    def get_temperature(self, direction: str) -> float:
        return 68.4 if direction == "in" else 71.0

    def get_heater(self, direction: str) -> float:
        return 1


class SampleNetwork:
    '''Five hosts in a ring - this machine among them - with traffic between a few.'''

    def __init__(self, own_mac: str):
        self.macs = [own_mac, "a4:cf:12:8e:01:3c", "b8:27:eb:44:10:9a", "3c:71:bf:02:7d:e1", "dc:a6:32:5f:88:04"]

    def get_host_positions(self) -> dict:
        count = len(self.macs)
        return {mac: (math.cos(2 * math.pi * i / count), math.sin(2 * math.pi * i / count)) for i, mac in enumerate(self.macs)}

    def get_arrows_this_tick(self) -> dict:
        return {"a": (self.macs[0], self.macs[1]), "b": (self.macs[2], self.macs[1]), "c": (self.macs[0], self.macs[3])}


class SamplePackets:
    def get_selected(self):
        return None


class SampleWorldMap(PassWheel, WorldMap):
    def __init__(self, master: QWidget, context: Context):
        super().__init__(master, context)
        self.buffer = SampleSubmarine()


class SampleHouse(PassWheel, House):
    def __init__(self, master: QWidget, context: Context):
        super().__init__(master, context)
        self.buffer = SampleHVAC()


class SampleNetworkDiagram(PassWheel, NetworkDiagramCanvas):
    def __init__(self, master: QWidget, context: Context):
        super().__init__(master, context)
        self.network = SampleNetwork(self.mac_address)
        self.packets = SamplePackets()


# The panels
class PacketsExample(Panel):
    '''The packet console's treeview, with a selected row.'''
    COLUMNS = ["number", "time_word", "ip_src", "ip_dst", "protocol", "length", "summary"]
    HOSTS = ["192.168.4.1", "192.168.4.2", "192.168.4.10", "192.168.4.23"]
    PROTOCOLS = [("TCP", "502 > 51544 [PSH, ACK] Modbus/TCP"), ("ARP", "Who has 192.168.4.10? Tell 192.168.4.2"),
                 ("UDP", "DNS query A ap-config.local"), ("TCP", "Read Holding Registers 0-14")]

    def __init__(self, master: QWidget, context: Context):
        super().__init__(master, context, "example_packets")
        self.menu_bar.add_dropdown(["Live", "Paused"])
        self.menu_bar.add_button("example_filter")
        treeview = PacketTreeview(self, context)
        treeview.set_visible_columns(self.COLUMNS)
        for number in range(1, 41):
            protocol, summary = self.PROTOCOLS[number % len(self.PROTOCOLS)]
            row = {"number": number, "time_word": f"{number * 0.137:.3f}", "ip_src": self.HOSTS[number % 4],
                   "ip_dst": self.HOSTS[(number + 1) % 4], "protocol": protocol, "length": 60 + (number * 37) % 140,
                   "summary": summary}
            treeview.submit(str(number), [str(row.get(column, "")) for column in treeview.columns])
        treeview.select("12")


class StatusExample(Panel):
    '''The status console's text area.'''
    LINES = [
        "0.000 [wifi] Connecting to AP-Config...", "1.204 [wifi] Connected to AP-Config",
        "2.881 [nmap] Scanning 192.168.4.0/24", "6.512 [nmap] 3 hosts up: .1 .2 .10",
        "8.030 [arp] Spoofing 192.168.4.2 <-> 192.168.4.10", "8.031 [sniff] Sniffing on wlan0",
        "12.774 [nfq] Rewriting holding register 3 (52 -> 90)", "14.006 [sniff] 1,204 packets captured",
        "15.220 [json] Saved capture_0412.jsonl",
    ]

    def __init__(self, master: QWidget, context: Context):
        super().__init__(master, context, "example_status")
        self.menu_bar.add_checkbox("Auto-Scroll", True)
        text = QPlainTextEdit("\n\n".join(self.LINES))
        text.setFont(self.style.get_font("mono"))
        text.setReadOnly(True)
        text.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.layout().addWidget(text, 1)


class RegistersExample(Panel):
    '''A text table in a form card, like the ModBus table.'''
    ROWS = [("Speed", "52", "90", "NFQ"), ("Rudder", "-12", "-12", "-"), ("Heading", "271", "271", "-"),
            ("Temperature", "68.4", "71.0", "NFQ"), ("Heater", "1", "1", "-"), ("Setpoint", "72", "72", "-")]

    def __init__(self, master: QWidget, context: Context):
        super().__init__(master, context, "example_registers")
        self.menu_bar.add_button("example_clear")
        scrollable = Scrollable(self, context)
        form = BaseForm(None, context)
        for column in range(4):
            form.grid_layout.setColumnStretch(column, 1)
        form.add_header("ModBus Readings")
        for row in [("Variable", "Received", "Sent", "Source"), *self.ROWS]:
            for column, text in enumerate(row):
                label = QLabel(text)
                label.setFont(self.style.get_font("mono"))
                label.setAlignment(Qt.AlignmentFlag.AlignLeft if column == 0 else Qt.AlignmentFlag.AlignCenter)
                form.grid_layout.addWidget(label, form.current_row, column)
            form.current_row += 1
        scrollable.grid_layout.addWidget(form, 0, 0)
        scrollable.add_deadspace()


class ChartsExample(Panel):
    '''Two strip charts sharing a time axis - one series, then three.'''

    def __init__(self, master: QWidget, context: Context):
        super().__init__(master, context, "example_charts")
        self.menu_bar.add_button("pause")
        scrollable = Scrollable(self, context)
        scrollable.columnconfigure(0, weight=1)
        scrollable.columnconfigure(1, weight=1)
        times = [second / 2 for second in range(CHART_SECONDS * 2 + 1)]
        temperature = {"": [(t, 66 + 6 * (1 - math.exp(-t / 20)) + 0.3 * math.sin(t)) for t in times]}
        motion = {
            "in": [(t, 50 + 30 * math.sin(t / 6)) for t in times],
            "out": [(t, 50 + 30 * math.sin(t / 6) + t * 0.5) for t in times],
            "target": [(t, 60.0) for t in times],
        }
        time_offset = [0.0]
        for column, (title, units, histories) in enumerate([("Temperature", "°F", temperature), ("Speed", "knots", motion)]):
            chart = StripChart(scrollable, context, (0, column), lambda title=title: title, lambda units=units: units,
                               lambda: 1, lambda histories=histories: histories, time_offset=time_offset,
                               now_getter=lambda: CHART_SECONDS)
            chart.start_animation()


class MapExample(Panel):
    def __init__(self, master: QWidget, context: Context):
        super().__init__(master, context, "example_map")
        self.menu_bar.add_dropdown(["Sniffed Map", "Defender Map"])
        SampleWorldMap(self, context)


class HouseExample(Panel):
    def __init__(self, master: QWidget, context: Context):
        super().__init__(master, context, "example_house")
        SampleHouse(self, context)


class NetworkExample(Panel):
    def __init__(self, master: QWidget, context: Context):
        super().__init__(master, context, "example_network")
        SampleNetworkDiagram(self, context)


class ControlsExample(Panel):
    '''Form cards with every kind of control, in their different states.'''

    def __init__(self, master: QWidget, context: Context):
        super().__init__(master, context, "example_controls")
        scrollable = Scrollable(self, context)

        connection = BaseForm(None, context)
        connection.add_header("ARP Spoofing")
        self.row(connection, "Target IP:", self.entry("192.168.4.2"))
        self.row(connection, "Host IP:", self.entry("", "192.168.4.10"))
        status, button = connection.add_button("ARP Spoofer is off", "Start Attack")
        status.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        scrollable.grid_layout.addWidget(connection, 0, 0)

        options = BaseForm(None, context)
        options.add_header("Options")
        checked = QCheckBox("Rewrite packets")
        checked.setChecked(True)
        self.row(options, checked, QCheckBox("Log to file"))
        dropdown = QComboBox()
        dropdown.addItems(["Holding register 3", "Holding register 4", "Coil 1"])
        self.row(options, "Register:", dropdown)
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setValue(65)
        self.row(options, "Noise:", slider)
        disabled = QPushButton("Unavailable")
        disabled.setEnabled(False)
        self.row(options, disabled, QPushButton("Apply"))
        scrollable.grid_layout.addWidget(options, 1, 0)
        scrollable.add_deadspace()

    def entry(self, text: str, placeholder: str = "") -> QLineEdit:
        entry = QLineEdit(text)
        entry.setPlaceholderText(placeholder)
        return entry

    def row(self, form: BaseForm, left, right: QWidget):
        '''One row of a form: a label (text) or control on the left, a control on the right.'''
        if isinstance(left, str):
            left = QLabel(left)
        for widget in (left, right):
            widget.setFont(self.style.get_font())
        form.grid_layout.addWidget(left, form.current_row, 0, 1, 2)
        form.grid_layout.addWidget(right, form.current_row, 2)
        form.current_row += 1


class FlagsExample(Panel):
    '''Status cards with colored text, like the defender flags.'''

    def __init__(self, master: QWidget, context: Context):
        super().__init__(master, context, "example_flags")
        scrollable = Scrollable(self, context)
        cards = [
            ("Error Detection", [("● State threshold surpassed", "bad"), ("● Speed threshold surpassed", "text"),
                                 ("● Rudder threshold surpassed", "text")]),
            ("Kalman Filter", [("Status: ON", "good")]),
            ("Encryption", [("Status: OFF", "warning"), ("Key: (none)", "text")]),
        ]
        for row, (title, lines) in enumerate(cards):
            card = BaseForm(None, context)
            header = QLabel(title.upper())
            header.setFont(self.style.get_font())
            card.grid_layout.addWidget(header, card.current_row, 0, 1, -1)
            card.current_row += 1
            for text, color in lines:
                line = QLabel(text)
                line.setFont(self.style.get_font("small"))
                self.style.live_style(line, lambda color=color: f"QLabel {{ color: {self.style.color(color)}; }}")
                card.grid_layout.addWidget(line, card.current_row, 0, 1, -1)
                card.current_row += 1
            scrollable.grid_layout.addWidget(card, row, 0)
        scrollable.add_deadspace()


class TabsExample(Panel):
    '''Tabs holding an editable table and a free-text area.'''
    HOSTS = [("192.168.4.1", "a4:cf:12:8e:01:3c", "Espressif", "80, 502"),
             ("192.168.4.2", "b8:27:eb:44:10:9a", "Raspberry Pi", "22, 502"),
             ("192.168.4.10", "3c:71:bf:02:7d:e1", "Espressif", "502"),
             ("192.168.4.23", "dc:a6:32:5f:88:04", "Raspberry Pi", "22")]

    def __init__(self, master: QWidget, context: Context):
        super().__init__(master, context, "example_tabs")
        tabs = QTabWidget()
        tabs.setFont(self.style.get_font())

        table = QTableWidget(len(self.HOSTS), 4)
        table.setFont(self.style.get_font("mono"))
        table.setHorizontalHeaderLabels(["Host", "MAC", "Vendor", "Open Ports"])
        table.setAlternatingRowColors(True)
        table.horizontalHeader().setStretchLastSection(True)
        for row, host in enumerate(self.HOSTS):
            for column, text in enumerate(host):
                table.setItem(row, column, QTableWidgetItem(text))
        table.resizeColumnsToContents()
        table.selectRow(1)
        tabs.addTab(table, "Hosts")

        notes = QPlainTextEdit("Target: the AP's Modbus server on 192.168.4.10:502.\n\n"
                               "Holding register 3 is the boat's speed - rewrite it in transit and watch the map drift.")
        notes.setFont(self.style.get_font())
        tabs.addTab(notes, "Notes")
        self.layout().addWidget(tabs, 1)


# The gallery's grid: each example's (row, column, row span, column span)
EXAMPLE_PANELS: list[tuple[type[Panel], tuple[int, int, int, int]]] = [
    (PacketsExample, (0, 0, 1, 2)),
    (StatusExample, (0, 2, 1, 1)),
    (MapExample, (1, 0, 2, 1)),
    (ChartsExample, (1, 1, 1, 2)),
    (HouseExample, (2, 1, 1, 1)),
    (NetworkExample, (2, 2, 1, 1)),
    (ControlsExample, (3, 0, 1, 2)),
    (FlagsExample, (3, 2, 1, 1)),
    (RegistersExample, (4, 0, 1, 1)),
    (TabsExample, (4, 1, 1, 2)),
]
