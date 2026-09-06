from ...app_core import Context

# Widgets
from ...widgets import Panes, MenuBar, Scrollable
from ...widgets import popup
from ...widgets.map import Map
from ...drawing.viewport import ViewPort
from ..page import Page

# HVAC test dashboard, shown in place of the Submarine widgets when AP_ESP32
# reports submarine_mode == False
from .hvac_view import HVACView

# Network
from ...network.hardware import APPoller

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QButtonGroup, QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSlider, QVBoxLayout, QWidget,
)

import threading
import requests
import time

# QSlider only steps through integers - each slider's own float min/max is
# mapped onto this many integer positions (see _to_slider_pos/_from_slider_pos).
SLIDER_RESOLUTION = 1000


class DefenderV0(Page):
    '''
    Page constructor for defender/defenderv0.
    '''

    POLL_INTERVAL_MS = 2000

    # Flag definitions — (key, display label).
    HVAC_FLAG_DEFS = [
            ("HVAC_filter_flag", "State Filtering Threshold Surpassed")
        ]

    SUBMARINE_FLAG_DEFS = [
        ("state_filter_flag", "State Filtering Threshold Surpassed"),
        ("speed_filter_flag", "Speed Filtering Treshold Surpassed"),
        ("rudder_filter_flag", "Rudder Filtering Treshold Surpassed")
    ]

    def __init__(self, context: Context):
        super().__init__(context)

        # ── Internal state FIRST (map callback fires immediately) ────────────
        # Everything the AP actually reports, and everything this page pushes
        # back to it (encryption/AP-tunnel/kalman-enabled status, positions,
        # flags, settings, temperatures...) lives in context.buffer.
        # defender_modbus/defender_map/defender_status - see _refresh_*
        # below. What's left here is genuinely local, single-widget UI state:
        # the log toggle and in-progress slider drags.
        self._log_source    = "client"   # "client" or "server"
        self._submarine_mode = True
        self.sensor_noise_variance = 8.3
        self.kalman_expected_sensor_variance = 8.3
        self.rudder_error_threshold = 2.75
        self.speed_error_threshold = 2.0
        self._syncing_sliders = False
        self._submarine_pending_revision = 0

        # ── AP poller process — a background thread that has to survive a
        # page refresh, so it's owned by context.process_manager the same
        # way a network_action_panel form owns its attack process, and
        # regained here rather than recreated whenever this page rebuilds.
        self._ap_poller = self.context.process_manager.get_process("ap_poll")
        if self._ap_poller is None:
            self._ap_poller = APPoller(self.context.buffer, self.context)
            self.context.process_manager.add_process("ap_poll", self._ap_poller)

        # ── Menu bar ─────────────────────────────────────────────────────────
        menu_bar = MenuBar(self, context, "defender")
        menu_bar.page_buttons()

        # ── Three-pane layout ────────────────────────────────────────────────
        trifold = Panes(self, context, "horizontal", 3, [4, 3, 2], True)
        left_p = Scrollable(trifold.pane(0), context)
        middle_p = trifold.pane(1)
        right_p = trifold.pane(2)

        # left_p is a Scrollable (QScrollArea) - its own grid_layout is where
        # content goes (see widgets/frame_widgets/scrollable.py), one widget
        # at (0, 0), so everything below can just use ordinary
        # parent.layout().addWidget(...) self-placement from there on.
        left_content = QWidget()
        left_content.setLayout(QVBoxLayout())
        left_content.layout().setContentsMargins(0, 0, 0, 0)
        left_p.grid_layout.addWidget(left_content, 0, 0)

        # ── Left pane ────────────────────────────────────────────────────────
        self._build_connection_block(left_content)   # mode-agnostic — always visible
        self._mode_content_left = QWidget()
        self._mode_content_left.setLayout(QVBoxLayout())
        self._mode_content_left.layout().setContentsMargins(0, 0, 0, 0)
        left_content.layout().addWidget(self._mode_content_left)

        self._submarine_left = QWidget()
        self._submarine_left.setLayout(QVBoxLayout())
        self._submarine_left.layout().setContentsMargins(0, 0, 0, 0)
        self._mode_content_left.layout().addWidget(self._submarine_left)
        self._build_encryption_block(self._submarine_left)
        self._build_AP_communication_block(self._submarine_left)
        self._build_slider_block(self._submarine_left)
        self._build_values_block(self._submarine_left)

        self._hvac_view = HVACView(self.style, self._mode_content_left, right_p, context)

        left_p.add_deadspace()

        # ── Middle pane ──────────────────────────────────────────────────────
        self._submarine_middle = QWidget()
        self._submarine_middle.setLayout(QVBoxLayout())
        self._submarine_middle.layout().setContentsMargins(0, 0, 0, 0)
        middle_p.layout().addWidget(self._submarine_middle)

        self._build_packet_log(self._submarine_middle)
        self._build_flags_block(self._submarine_middle, "SUBMARINE ERROR DETECTION FLAGS [MODBUS]", self.SUBMARINE_FLAG_DEFS, "_submarine_flag_labels",)
        # ── Kalman Filter block ─────────────────────────────────────────────
        kalman_section = self._section(self._submarine_middle, "KALMAN FILTER")

        self._submarine_kalman_label = QLabel("Status: ON")
        self._submarine_kalman_label.setFont(self.style.get_font())
        self._submarine_kalman_label.setStyleSheet("color: green;")
        kalman_section.layout().addWidget(self._submarine_kalman_label)

        self._submarine_kalman_button = QPushButton("Toggle Kalman Filter")
        self._submarine_kalman_button.setFont(self.style.get_font())
        self._wire_button(self._submarine_kalman_button, self._toggle_submarine_kalman_filter)
        kalman_section.layout().addWidget(self._submarine_kalman_button)

        self._hvac_middle = QWidget()
        self._hvac_middle.setLayout(QVBoxLayout())
        self._hvac_middle.layout().setContentsMargins(0, 0, 0, 0)
        middle_p.layout().addWidget(self._hvac_middle)
        self._build_flags_block(self._hvac_middle, "HVAC ERROR DETECTION FLAG", self.HVAC_FLAG_DEFS, "_hvac_flag_labels",)
        # HVAC's own Kalman Filter block lives entirely inside HVACView now
        # (see hvac_view.py's _build_kalman_block) - it owns the button, the
        # label, and the toggle state, so there's no callback threaded back
        # into this page just to update a label this class doesn't build.

        self._build_mode_block(middle_p)       # mode-agnostic — always visible

        # middle_p is a plain Panes pane (no Scrollable/add_deadspace of its
        # own) - without this, leftover vertical space has nowhere dedicated
        # to go and distributes into the actual section widgets instead,
        # stretching them past their natural size (the same root cause as
        # the MenuBar sizing bug found earlier in this migration).
        middle_p.layout().addStretch()

        self._refresh_mode_ui()

        self._post_slider_settings()

        self._map_container = QWidget()
        self._map_container.setLayout(QVBoxLayout())
        self._map_container.layout().setContentsMargins(0, 0, 0, 0)
        right_p.layout().addWidget(self._map_container)

        def draw_defender_map(canvas, draw_lock, scale, offset):
            draw = ViewPort(canvas, scale, offset)
            with draw_lock:
                draw.grid_lines()
                positions = self.context.buffer.defender_map.get_path("client_clean")
                if len(positions) < 1:
                    return
                draw.line(positions, "red")
                bearing = self.context.buffer.defender_modbus.get_single("theta", "client_clean")
                if bearing is None:
                    return
                draw.boat(positions[-1], bearing, "white", "black")

        self._map = Map(self._map_container, context, draw_defender_map,
                        framerate_ms=self.POLL_INTERVAL_MS, padding=20)

        # ── Page updaters — each repaints itself from context.buffer on the
        # shared animation_manager tick, the same way MitmTable/canvases do,
        # instead of one central method reaching into every other widget's
        # update method. That's what makes it possible to lift each of these
        # into its own panel later without carrying the others along.
        self.context.animation_manager.add_callback(f"DefenderConnection_{id(self)}", self._refresh_connection)
        self.context.animation_manager.add_callback(f"DefenderSubmarineValues_{id(self)}", self._refresh_submarine_values)
        self.context.animation_manager.add_callback(f"DefenderFlags_{id(self)}", self._refresh_flags)

        # ── Start polling ────────────────────────────────────────────────────
        self._poll()

    # ════════════════════════════════════════════════════════════════════════
    #  UI builder helpers
    # ════════════════════════════════════════════════════════════════════════

    def _section(self, parent: QWidget, title: str | None = None) -> QWidget:
        '''
        A titled card: a widget-colored panel with an optional bold title
        label at the top, added into parent's layout. Mirrors the repeated
        CTkFrame(fg_color="widget")+CTkLabel(title) pattern this file used
        throughout.
        '''
        section = QWidget()
        section.setStyleSheet(f"background-color: {self.style.color('widget')};")
        layout = QVBoxLayout(section)
        layout.setContentsMargins(self.style.igap, self.style.igap, self.style.igap, self.style.igap)
        layout.setSpacing(4)
        parent.layout().addWidget(section)

        if title is not None:
            label = QLabel(title)
            label.setFont(self.style.get_font())
            layout.addWidget(label)

        return section

    def _wire_button(self, button: QPushButton, function):
        # clicked emits a "checked" bool that none of these callbacks expect.
        button.clicked.connect(lambda checked=False, function=function: function())

    def _to_slider_pos(self, value: float, lo: float, hi: float) -> int:
        if hi == lo:
            return 0
        return int(round((value - lo) / (hi - lo) * SLIDER_RESOLUTION))

    def _from_slider_pos(self, pos: int, lo: float, hi: float) -> float:
        return lo + (pos / SLIDER_RESOLUTION) * (hi - lo)

    def _build_connection_block(self, parent: QWidget):
        section = self._section(parent, "SERVER URL")

        self._url_entry = QLineEdit()
        self._url_entry.setFont(self.style.get_font())
        self._url_entry.setPlaceholderText("http://192.168.8.141")
        self._url_entry.setText("http://192.168.4.1")
        section.layout().addWidget(self._url_entry)

        connect_button = QPushButton("Connect")
        connect_button.setFont(self.style.get_font())
        self._wire_button(connect_button, self._poll)
        section.layout().addWidget(connect_button)

        self._conn_status = QLabel("⬤  Not connected")
        self._conn_status.setFont(self.style.get_font())
        self._conn_status.setStyleSheet("color: gray;")
        section.layout().addWidget(self._conn_status)

    def _build_encryption_block(self, parent: QWidget):
        section = self._section(parent, "ENCRYPTION")

        self._enc_label = QLabel("Status: OFF")
        self._enc_label.setFont(self.style.get_font())
        self._enc_label.setStyleSheet("color: gray;")
        section.layout().addWidget(self._enc_label)

        key_label = QLabel("Encryption Key")
        key_label.setFont(self.style.get_font("small"))
        key_label.setStyleSheet("color: gray;")
        section.layout().addWidget(key_label)

        self._enc_key_entry = QLineEdit()
        self._enc_key_entry.setFont(self.style.get_font())
        self._enc_key_entry.setPlaceholderText("Enter key…")
        section.layout().addWidget(self._enc_key_entry)

        self._enc_button = QPushButton("Enable Encryption")
        self._enc_button.setFont(self.style.get_font())

        def enc_button():
            if not self.context.buffer.defender_status.get("encryption_status", False):
                # Encryption is off - try to turn it on
                if self._enc_key_entry.text().strip() == "":
                    # Empty key — show error
                    popup.message(self, self.context, "Please enter an encryption key before enabling encryption.")
                elif not str.isascii(self._enc_key_entry.text().strip()):
                    # Non-ASCII key — show error
                    popup.message(self, self.context, "Encryption key must be ASCII.")
                else:
                    # Key looks good — toggle encryption on behavior
                    self._enc_key_entry.setEnabled(False)
                    self._enc_button.setText("Disable Encryption")
                    self._toggle_encryption()
            else:
                # Encryption is on - turn it off
                self._enc_key_entry.setEnabled(True)
                self._enc_key_entry.clear()
                self._enc_button.setText("Enable Encryption")
                self._toggle_encryption()

        self._wire_button(self._enc_button, enc_button)
        section.layout().addWidget(self._enc_button)

    def _build_AP_communication_block(self, parent: QWidget):
        section = self._section(parent, "COMMUNICATE VIA ACCESS POINT")

        self._filter_label = QLabel("Status: OFF")
        self._filter_label.setFont(self.style.get_font())
        self._filter_label.setStyleSheet("color: gray;")
        section.layout().addWidget(self._filter_label)

        self._filter_button = QPushButton("Enable Communication Through AP")
        self._filter_button.setFont(self.style.get_font())
        self._wire_button(self._filter_button, self._toggle_AP_communication)
        section.layout().addWidget(self._filter_button)

    def _build_mode_block(self, parent: QWidget):
        section = self._section(parent, "OPERATION MODE")

        # Read-only — this just reflects whatever submarine_mode AP_ESP32.ino
        # is currently reporting. Mode is changed on the AP itself, not here.
        self._mode_label = QLabel("Mode: SUBMARINE")
        self._mode_label.setFont(self.style.get_font())
        self._mode_label.setStyleSheet("color: green;")
        section.layout().addWidget(self._mode_label)

    def _refresh_mode_ui(self):
        if not hasattr(self, '_mode_label'):
            return
        try:
            if self._submarine_mode:
                self._mode_label.setText("Mode: SUBMARINE")
                self._mode_label.setStyleSheet("color: green;")
                self._hvac_middle.hide()

                self._submarine_left.show()
                self._submarine_middle.show()
                self._map_container.show()
            else:
                self._mode_label.setText("Mode: HVAC")
                self._mode_label.setStyleSheet("color: orange;")
                self._submarine_left.hide()
                self._submarine_middle.hide()
                self._map_container.hide()

                self._hvac_middle.show()
        except Exception as e:
            print("refresh_mode_ui:", e)

    def _build_values_block(self, parent: QWidget):
        """Client values card and Server values card, side by side."""
        outer = QWidget()
        outer_layout = QHBoxLayout(outer)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        parent.layout().addWidget(outer)

        fields = ["x", "y", "theta", "speed", "rudder"]
        self._val_labels = {"client": {}, "server": {}}

        for source in ["client", "server"]:
            card = QWidget()
            card.setStyleSheet(f"background-color: {self.style.color('widget')};")
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(self.style.igap, self.style.igap, self.style.igap, self.style.igap)
            outer_layout.addWidget(card, 1)

            title_label = QLabel(f"{source.capitalize()} Values")
            title_label.setFont(self.style.get_font())
            card_layout.addWidget(title_label)

            for field in fields:
                row_frame = QWidget()
                row_layout = QHBoxLayout(row_frame)
                row_layout.setContentsMargins(0, 0, 0, 0)
                card_layout.addWidget(row_frame)

                field_label = QLabel(f"{field} =")
                field_label.setFont(self.style.get_font("small"))
                field_label.setStyleSheet("color: gray;")
                row_layout.addWidget(field_label)

                lbl = QLabel("—")
                lbl.setFont(self.style.get_font("small"))
                row_layout.addWidget(lbl, 1)
                self._val_labels[source][field] = lbl

    def _build_packet_log(self, parent: QWidget):
        """Header with CLIENT | SERVER segmented toggle, then scrollable rows."""
        header_frame = self._section(parent)

        title_row = QWidget()
        title_row_layout = QHBoxLayout(title_row)
        title_row_layout.setContentsMargins(0, 0, 0, 0)
        header_frame.layout().addWidget(title_row)

        title_label = QLabel("PACKET LOG  (last 10)")
        title_label.setFont(self.style.get_font())
        title_row_layout.addWidget(title_label)
        title_row_layout.addStretch()

        toggle_group = QButtonGroup(title_row)
        toggle_group.setExclusive(True)
        for value in ["CLIENT", "SERVER"]:
            btn = QPushButton(value)
            btn.setFont(self.style.get_font("small"))
            btn.setCheckable(True)
            title_row_layout.addWidget(btn)
            toggle_group.addButton(btn)
        toggle_group.buttons()[0].setChecked(True)
        toggle_group.buttonClicked.connect(lambda btn: self._on_log_source_change(btn.text()))

        cols = ["Time", "X (m)", "Y (m)", "Theta", "Speed", "Rudder"]
        col_frame = QWidget()
        col_frame.setStyleSheet(f"background-color: {self.style.color('panel')};")
        col_layout = QGridLayout(col_frame)
        parent.layout().addWidget(col_frame)
        for i, col in enumerate(cols):
            col_label = QLabel(col)
            col_label.setFont(self.style.get_font("small"))
            col_label.setStyleSheet("color: gray;")
            col_layout.addWidget(col_label, 0, i)
            col_layout.setColumnStretch(i, 1)

        self._log_frame = Scrollable(parent, self.context, 240, "x", False)
        for i in range(len(cols)):
            self._log_frame.columnconfigure(i, weight=1)

        self._log_rows = []

    def _build_flags_block(self, parent: QWidget, title: str, defs, label_attr: str):
        section = self._section(parent, title)

        labels = {}
        for key, label_text in defs:
            row = QWidget()
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(0, 0, 0, 0)
            section.layout().addWidget(row)

            dot = QLabel("●")
            dot.setFont(self.style.get_font("small"))
            dot.setStyleSheet("color: gray;")
            row_layout.addWidget(dot)

            text_label = QLabel(label_text)
            text_label.setFont(self.style.get_font("small"))
            row_layout.addWidget(text_label, 1)
            labels[key] = dot

        setattr(self, label_attr, labels)

    def _build_slider_block(self, parent: QWidget):
        section = self._section(parent, "SUBMARINE SETTINGS")

        slider_defs = [
            ("Sensor Noise Variance", 0.0, 20, 8.3, "sensor_noise_variance", 2),
            ("Kalman Expected Sensor Variance", 0.0, 20, 8.3, "kalman_expected_sensor_variance", 2),
            ("Rudder Error Threshold", 0.0, 10, 2.75, "rudder_error_threshold", 1),
            ("Speed Error Threshold", 0.0, 10, 2.0, "speed_error_threshold", 1),
        ]

        self._sliders = {}
        self._slider_value_labels = {}
        self._slider_ranges = {}

        for title, min_val, max_val, default, attr_name, decimals in slider_defs:
            header = QWidget()
            header_layout = QHBoxLayout(header)
            header_layout.setContentsMargins(0, 0, 0, 0)
            section.layout().addWidget(header)

            title_label = QLabel(title)
            title_label.setFont(self.style.get_font("small"))
            header_layout.addWidget(title_label)
            header_layout.addStretch()

            value_label = QLabel(f"{default:.{decimals}f}")
            value_label.setFont(self.style.get_font("small"))
            value_label.setStyleSheet("color: gray;")
            header_layout.addWidget(value_label)

            slider = QSlider(Qt.Orientation.Horizontal)
            slider.setRange(0, SLIDER_RESOLUTION)
            slider.setValue(self._to_slider_pos(default, min_val, max_val))

            def slider_callback(pos, lbl=value_label, attr=attr_name, d=decimals, lo=min_val, hi=max_val):
                value = self._from_slider_pos(pos, lo, hi)

                setattr(self, attr, value)
                lbl.setText(f"{value:.{d}f}")

                # Only POST when the USER moved the slider.
                if not self._syncing_sliders:
                    self._post_slider_settings()

            slider.valueChanged.connect(slider_callback)
            section.layout().addWidget(slider)

            self._sliders[title] = slider
            self._slider_value_labels[title] = value_label
            self._slider_ranges[title] = (min_val, max_val)

        reset_button = QPushButton("Reset to Defaults")
        reset_button.setFont(self.style.get_font())
        self._wire_button(reset_button, self._reset_slider_defaults)
        section.layout().addWidget(reset_button)

    def _post_slider_settings(self):
        payload = {
            "sensor_noise_variance": self.sensor_noise_variance,
            "kalman_expected_sensor_variance": self.kalman_expected_sensor_variance,
            "rudder_error_threshold": self.rudder_error_threshold,
            "speed_error_threshold": self.speed_error_threshold,
            "kalman_filter_enabled": self.context.buffer.defender_status.get("kalman_filter_enabled", True),
        }

        def _request():
            try:
                resp = requests.post(
                    f"{self._ap_poller.url}/set_settings",
                    json=payload,
                    timeout=3,
                )
                if resp.ok:
                    body = resp.json()
                    self._submarine_pending_revision = int(
                        body.get("settings_revision", 0)
                    )
                    print(
                        "Settings posted, revision:",
                        self._submarine_pending_revision
                    )
            except Exception as e:
                print("post_slider_settings:", e)

        threading.Thread(target=_request, daemon=True).start()

    def _sync_submarine_sliders(self):
        status = self.context.buffer.defender_status

        client_revision = int(
            status.get("client_settings_revision", 0) or 0
        )

        server_revision = int(
            status.get("server_settings_revision", 0) or 0
        )

        if self._submarine_pending_revision > 0:

            if (
                client_revision < self._submarine_pending_revision
                or server_revision < self._submarine_pending_revision
            ):
                return

            self._submarine_pending_revision = 0

        values = {
            "Sensor Noise Variance":
                status.get("sensor_noise_variance"),

            "Kalman Expected Sensor Variance":
                status.get("kalman_expected_sensor_variance"),

            "Rudder Error Threshold":
                status.get("rudder_error_threshold"),

            "Speed Error Threshold":
                status.get("speed_error_threshold"),
        }

        self._syncing_sliders = True

        try:
            for title, value in values.items():
                if value is None:
                    continue

                slider = self._sliders.get(title)
                label = self._slider_value_labels.get(title)

                if slider is None:
                    continue

                value = float(value)

                # Move the UI slider to the MCU's current value.
                lo, hi = self._slider_ranges[title]
                slider.setValue(self._to_slider_pos(value, lo, hi))

                # Keep the Python-side variable synchronized too.
                attr_map = {
                    "Sensor Noise Variance": "sensor_noise_variance",
                    "Kalman Expected Sensor Variance":
                        "kalman_expected_sensor_variance",
                    "Rudder Error Threshold":
                        "rudder_error_threshold",
                    "Speed Error Threshold":
                        "speed_error_threshold",
                }

                setattr(self, attr_map[title], value)

                if label is not None:
                    decimals = 1 if title in (
                        "Rudder Error Threshold",
                        "Speed Error Threshold"
                    ) else 2

                    label.setText(f"{value:.{decimals}f}")

        finally:
            self._syncing_sliders = False

    def _reset_slider_defaults(self):
        defaults = {
            "Sensor Noise Variance": (
                8.3, "sensor_noise_variance", 2
            ),
            "Kalman Expected Sensor Variance": (
                8.3, "kalman_expected_sensor_variance", 2
            ),
            "Rudder Error Threshold": (
                2.75, "rudder_error_threshold", 1
            ),
            "Speed Error Threshold": (
                2.0, "speed_error_threshold", 1
            ),
        }

        # Prevent each slider's setValue() from generating its own POST
        self._syncing_sliders = True

        try:
            for title, (value, attr, decimals) in defaults.items():

                # Update Python variable
                setattr(self, attr, value)

                # Move slider
                lo, hi = self._slider_ranges[title]
                self._sliders[title].setValue(self._to_slider_pos(value, lo, hi))

                # Update displayed number
                self._slider_value_labels[title].setText(f"{value:.{decimals}f}")

        finally:
            self._syncing_sliders = False

        self._post_slider_settings()

    # ════════════════════════════════════════════════════════════════════════
    #  Network actions
    # ════════════════════════════════════════════════════════════════════════

    def _get_url(self) -> str:
        # Falls back to the poller's own last-known URL (which defaults to
        # 192.168.4.1 itself) rather than a second hardcoded default here.
        return self._url_entry.text().strip().rstrip("/") or self._ap_poller.url

    def _toggle_encryption(self):
        new_state = not self.context.buffer.defender_status.get("encryption_status", False)
        enc_key   = self._enc_key_entry.text().strip()

        def _request():
            try:
                resp = requests.post(
                    f"{self._ap_poller.url}/set_encryption",
                    json={"encryption_status": new_state, "encryption_key": enc_key},
                    timeout=3,
                )
                if resp.ok:
                    # Written straight to the shared status channel instead of
                    # an instance attribute, so every widget reading
                    # encryption_status (this page's own block and HVACView's)
                    # sees the same confirmed value instead of two copies that
                    # can drift apart.
                    self.context.buffer.defender_status.put("encryption_status", new_state)
            except Exception:
                pass

        threading.Thread(target=_request, daemon=True).start()

    def _toggle_AP_communication(self):
        new_state = not self.context.buffer.defender_status.get("ap_communication", False)

        def _request():
            try:
                resp = requests.post(
                    f"{self._ap_poller.url}/set_AP_communication",
                    json={"AP_communication": new_state},
                    timeout=3,
                )
                if resp.ok:
                    # The AP never echoes AP_communication back on /api/data,
                    # so ap_communication in defender_status is this page's own
                    # confirmed-by-POST record, not something the poll unpacker
                    # ever writes - the last successful set is authoritative.
                    self.context.buffer.defender_status.put("ap_communication", new_state)
            except Exception:
                pass

        threading.Thread(target=_request, daemon=True).start()

    def _refresh_AP_communication_ui(self):
        try:
            if self.context.buffer.defender_status.get("ap_communication", False):
                self._filter_label.setText("Status: ON")
                self._filter_label.setStyleSheet("color: green;")
                self._filter_button.setText("Disable Communication Through AP")
            else:
                self._filter_label.setText("Status: OFF")
                self._filter_label.setStyleSheet("color: gray;")
                self._filter_button.setText("Enable Communication Through AP")
        except Exception as e:
            print("refresh_AP_communication_ui:", e)

    def _poll(self):
        '''
        Connect button handler, and the initial poll kickoff at the end of
        __init__. The AP poller process owns its own interval loop (it has
        to - it must keep running across a page refresh) - this just points
        it at whatever URL is currently entered and starts it if it isn't
        already running, so re-clicking Connect with a new URL redirects the
        existing poller instead of spawning a second one.
        '''
        self._ap_poller.url = self._get_url()
        if not self._ap_poller.is_running():
            self._ap_poller.start()

    def _on_log_source_change(self, value: str):
        self._log_source = value.lower()
        self._update_log()

    def _toggle_submarine_kalman_filter(self):
        new_state = not self.context.buffer.defender_status.get("kalman_filter_enabled", True)
        self.context.buffer.defender_status.put("kalman_filter_enabled", new_state)

        if new_state:
            self._submarine_kalman_label.setText("Kalman Filter Status: ON")
            self._submarine_kalman_label.setStyleSheet("color: green;")
        else:
            self._submarine_kalman_label.setText("Kalman Filter Status: OFF")
            self._submarine_kalman_label.setStyleSheet("color: gray;")

        self._post_slider_settings()

    # ════════════════════════════════════════════════════════════════════════
    #  UI update helpers
    # ════════════════════════════════════════════════════════════════════════

    def _refresh_connection(self):
        '''
        Connection/mode-level repaint: the connected dot, encryption and
        AP-tunnel status, and which top-level widget group (submarine vs
        HVAC) is visible. Registered with animation_manager in __init__ -
        HVACView repaints and shows/hides itself independently, it doesn't
        wait to be called from here.
        '''
        status = self.context.buffer.defender_status

        if self._ap_poller.connected:
            self._conn_status.setText("⬤  Connected")
            self._conn_status.setStyleSheet("color: green;")
        else:
            self._conn_status.setText("⬤  Disconnected")
            self._conn_status.setStyleSheet("color: red;")

        self._refresh_encryption_ui()
        self._refresh_AP_communication_ui()

        incoming_mode = bool(status.get("submarine_mode", True))
        if incoming_mode != self._submarine_mode:
            self._submarine_mode = incoming_mode
            self._refresh_mode_ui()

    def _refresh_submarine_values(self):
        '''
        Submarine-only repaint: value cards, packet log, slider sync. A
        no-op while the AP is in HVAC mode - registered with
        animation_manager in __init__, not gated by _refresh_connection.
        '''
        if not self._submarine_mode:
            return

        self._sync_submarine_sliders()

        self._update_value_card("client", "client_clean")
        self._update_value_card("server", "server_clean")

        # Packet log — whichever source the toggle is set to
        self._update_log()

    def _update_value_card(self, source: str, attribute: str):
        modbus = self.context.buffer.defender_modbus
        for field in ["x", "y", "theta", "speed", "rudder"]:
            raw = modbus.get_single(field, attribute)
            text = "—" if raw is None else f"{float(raw):.3f}"
            self._val_labels[source][field].setText(text)

    def _update_log(self):
        '''
        Rebuilds the last-10-rows table for whichever source the CLIENT/
        SERVER toggle is set to, by zipping together that source's x/y/
        theta/speed/rudder histories from context.buffer.defender_modbus -
        the poll unpacker always writes all five together per point, so the
        five histories stay the same length and share the same time axis.
        '''
        attribute = "client_clean" if self._log_source == "client" else "server_clean"
        modbus = self.context.buffer.defender_modbus
        fields = ["x", "y", "theta", "speed", "rudder"]
        histories = {field: modbus.get_history(field, attribute) for field in fields}
        length = min((len(history) for history in histories.values()), default=0)

        rows = []
        for i in range(max(0, length - 10), length):
            row = {"received_at": histories["x"][i][0]}
            for field in fields:
                row[field] = histories[field][i][1]
            rows.append(row)

        self._render_log(list(reversed(rows)))

    def _render_log(self, rows: list):
        cols = ["received_at", "x", "y", "theta", "speed", "rudder"]

        log_layout = self._log_frame.grid_layout
        while log_layout.count():
            item = log_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        self._log_rows = []

        for r_idx, packet in enumerate(rows):
            row_labels = []
            bg = self.style.color("widget") if r_idx % 2 == 0 else self.style.color("panel")
            for c_idx, key in enumerate(cols):
                raw = packet.get(key, "—")
                if key == "received_at":
                    # received_at is the AP's own uptime clock, in seconds
                    secs = int(float(raw))
                    text = f"{secs//3600:02d}:{(secs%3600)//60:02d}:{secs%60:02d}"
                else:
                    try:
                        text = f"{float(raw):.4f}"
                    except (ValueError, TypeError):
                        text = str(raw)

                lbl = QLabel(text)
                lbl.setFont(self.style.get_font("small"))
                lbl.setStyleSheet(f"background-color: {bg};")
                log_layout.addWidget(lbl, r_idx, c_idx)
                row_labels.append(lbl)
            self._log_rows.append(row_labels)


    def _refresh_encryption_ui(self):
        try:
            if self.context.buffer.defender_status.get("encryption_status", False):
                self._enc_label.setText("Status: ON")
                self._enc_label.setStyleSheet("color: green;")
                self._enc_button.setText("Disable Encryption")
            else:
                self._enc_label.setText("Status: OFF")
                self._enc_label.setStyleSheet("color: gray;")
                self._enc_button.setText("Enable Encryption")
        except Exception as e:
            print("refresh_encryption_ui:", e)

    def _refresh_flags(self):
        status = self.context.buffer.defender_status
        submarine_flags = {
            "state_filter_flag": bool(status.get("state_anomaly", False)),
            "speed_filter_flag": bool(status.get("speed_anomaly", False)),
            "rudder_filter_flag": bool(status.get("rudder_anomaly", False)),
        }
        hvac_flags = {"HVAC_filter_flag": bool(status.get("hvac_anomaly", False))}
        for labels, flags in (
            (getattr(self, "_submarine_flag_labels", {}), submarine_flags),
            (getattr(self, "_hvac_flag_labels", {}), hvac_flags),
        ):
            for key, dot in labels.items():
                dot.setStyleSheet(f"color: {'red' if flags.get(key, False) else 'gray'};")
