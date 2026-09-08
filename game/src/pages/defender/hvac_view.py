"""
Read-only HVAC test dashboard for DefenderV0.

Fully self-contained: owns its own AP poller lookup, animation_manager
registration, and submarine/HVAC visibility, all read straight from
context.buffer.defender_status/defender_modbus - the AP poller process
(context.process_manager) is the only thing outside this class it depends
on, and DefenderV0 never has to call into it at all once constructed.
"""

import threading

import requests
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget

import matplotlib
matplotlib.use("QtAgg")
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from ...widgets import popup, ShiftWheelSlider

# Hardcoded dark-theme colors matching AP_ESP32.ino's config page palette.
# Not pulled from the app's Style object on purpose — CTk colors can be
# light/dark-mode tuples, and matplotlib needs a single concrete color string.
_FIG_BG      = "#16213e"
_AXES_BG     = "#0a0a1a"
_GRID        = "#0f3460"
_TEXT        = "#e0e0e0"
_ROOM_LINE   = "#4caf50"   # green
_TARGET_LINE = "#e94560"   # accent pink/red, matches the AP's accent color

# QSlider only steps through integers - each slider's own float min/max is
# mapped onto this many integer positions (see _to_slider_pos/_from_slider_pos).
SLIDER_RESOLUTION = 1000


class HVACView:

    MAX_POINTS = 300     # how many trailing buffer samples the graph plots

    def __init__(self, style, left_parent, right_parent, context):
        """
        style        - the Style object DefenderV0 already uses (self.style)
        left_parent  - container to build the readout cards into
        right_parent - container to build the trajectory graph into

        Fully self-contained: owns its own kalman-filter toggle (nothing
        outside this class needs to know about it) and reaches the AP poller
        process through context.process_manager instead of being handed a
        URL closure, so nothing has to construct or wire this up beyond
        passing context - the same context every widget already gets.
        """
        self.style    = style
        self._context = context

        self._ui_master = left_parent
        self.sensor_noise_variance = 0.1
        self.kalman_expected_sensor_variance = 0.1
        self.state_error_threshold = 5.0
        self._syncing_sliders = False
        self._hvac_kalman_filter_enabled = True
        self._submarine_mode = True

        self._build_left(left_parent)
        self._build_graph(right_parent)

        # Starts hidden - submarine mode (the assumed initial state, matching
        # _submarine_mode above) shows DefenderV0's own submarine widgets
        # instead. Unlike Tk, where a constructed-but-never-packed widget is
        # already invisible, Qt shows a widget as soon as it's added to a
        # layout - so this needs to be explicit, or HVAC content would flash
        # visible for one frame before _refresh_visibility ever runs.
        self._left_root.hide()
        self._graph_root.hide()

        self._push_hvac_controls()
        self._context.animation_manager.add_callback(f"HVACView_{id(self)}", self.refresh)
        self.refresh()

    def _get_url(self) -> str:
        return self._context.process_manager.get_process("ap_poll").url

    # ════════════════════════════════════════════════════════════════════
    #  Construction
    # ════════════════════════════════════════════════════════════════════

    def _section(self, parent: QWidget, title: str | None = None) -> QWidget:
        '''
        A titled card: a widget-colored panel with an optional bold title
        label at the top, added into parent's layout. Mirrors the repeated
        CTkFrame(fg_color="widget")+CTkLabel(title) pattern this file used
        throughout.
        '''
        section = QWidget()
        section.setStyleSheet(self.style.themed(f"background-color: {self.style.color('widget')};", section))
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

    def _build_left(self, parent: QWidget):
        self._left_root = QWidget()
        self._left_root.setLayout(QVBoxLayout())
        self._left_root.layout().setContentsMargins(0, 0, 0, 0)
        self._left_root.layout().setSpacing(self.style.igap)
        parent.layout().addWidget(self._left_root)

        # ── Live readout card ──────────────────────────────────────────
        readout_card = self._section(self._left_root, "LIVE STATUS")

        self._current_label = self._readout_row(readout_card, "Current Temp")
        self._target_label  = self._readout_row(readout_card, "Target Temp")
        self._heater_label  = self._readout_row(readout_card, "Heater")

        self._build_encryption_block(self._left_root)
        self._build_AP_communication_block(self._left_root)
        self._build_kalman_block(self._left_root)
        self._build_slider_block(self._left_root)

    def _build_encryption_block(self, parent: QWidget):
        section = self._section(parent, "ENCRYPTION")

        self._enc_label = QLabel("Status: OFF")
        self._enc_label.setFont(self.style.get_font())
        self._enc_label.setStyleSheet("color: gray;")
        section.layout().addWidget(self._enc_label)

        # Key entry
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
            if not self._context.buffer.defender_status.get("encryption_status", False):
                # Encryption is off - try to turn it on
                if self._enc_key_entry.text().strip() == "":
                    # Empty key — show error
                    popup.message(parent, self._context, "Please enter an encryption key before enabling encryption.")
                elif not str.isascii(self._enc_key_entry.text().strip()):
                    # Non-ASCII key — show error
                    popup.message(parent, self._context, "Encryption key must be ASCII.")
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

    def _toggle_encryption(self):
        # Shared with DefenderV0's own encryption block through
        # defender_status.encryption_status - it's the same AP-level
        # feature (same endpoint, same field names) shown twice, not two
        # independent toggles, so both read/write the one confirmed value.
        status = self._context.buffer.defender_status
        new_state = not status.get("encryption_status", False)

        if new_state:
            self._enc_key_entry.setEnabled(False)
            self._enc_button.setText("Disable Encryption")
        else:
            self._enc_key_entry.setEnabled(True)
            self._enc_button.setText("Enable Encryption")

        status.put("encryption_status", new_state)
        self._push_hvac_controls()

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

    def _build_kalman_block(self, parent: QWidget):
        '''
        HVAC's own Kalman Filter button+label - previously built by
        DefenderV0 and wired back here through an on_kalman_filter_change
        callback just to keep a label DefenderV0 owned in sync. Owning both
        outright removes that callback entirely.
        '''
        section = self._section(parent, "KALMAN FILTER")

        self._hvac_kalman_label = QLabel("Status: ON")
        self._hvac_kalman_label.setFont(self.style.get_font())
        self._hvac_kalman_label.setStyleSheet("color: green;")
        section.layout().addWidget(self._hvac_kalman_label)

        self._hvac_kalman_button = QPushButton("Toggle Kalman Filter")
        self._hvac_kalman_button.setFont(self.style.get_font())
        self._wire_button(self._hvac_kalman_button, self._toggle_hvac_kalman_filter)
        section.layout().addWidget(self._hvac_kalman_button)

    def _toggle_AP_communication(self):
        # Shared with DefenderV0's own AP-tunnel block through
        # defender_status.ap_communication - see _toggle_encryption.
        status = self._context.buffer.defender_status
        status.put("ap_communication", not status.get("ap_communication", False))
        self._push_hvac_controls()

    def _toggle_hvac_kalman_filter(self):
        # Unlike encryption/AP-tunnel, HVAC's kalman toggle posts a
        # different field (hvac_kalman_filter_enabled) than the submarine
        # one (kalman_filter_enabled) and the AP's poll response only ever
        # echoes the latter - so there's no confirmed HVAC value to read
        # back, and this stays local to the one button/label that owns it.
        self._hvac_kalman_filter_enabled = not self._hvac_kalman_filter_enabled

        if self._hvac_kalman_filter_enabled:
            self._hvac_kalman_label.setText("Kalman Filter Status: ON")
            self._hvac_kalman_label.setStyleSheet("color: green;")
        else:
            self._hvac_kalman_label.setText("Kalman Filter Status: OFF")
            self._hvac_kalman_label.setStyleSheet("color: gray;")

        self._push_hvac_controls()

    def _refresh_encryption_ui(self):
        if self._context.buffer.defender_status.get("encryption_status", False):
            self._enc_label.setText("Status: ON")
            self._enc_label.setStyleSheet("color: green;")
            self._enc_button.setText("Disable Encryption")
            self._enc_key_entry.setEnabled(False)
        else:
            self._enc_label.setText("Status: OFF")
            self._enc_label.setStyleSheet("color: gray;")
            self._enc_button.setText("Enable Encryption")
            self._enc_key_entry.setEnabled(True)

    def _refresh_AP_communication_ui(self):
        if self._context.buffer.defender_status.get("ap_communication", False):
            self._filter_label.setText("Status: ON")
            self._filter_label.setStyleSheet("color: green;")
            self._filter_button.setText("Disable Communication Through AP")
        else:
            self._filter_label.setText("Status: OFF")
            self._filter_label.setStyleSheet("color: gray;")
            self._filter_button.setText("Enable Communication Through AP")

    def _refresh_hvac_controls_ui(self):
        self._refresh_encryption_ui()
        self._refresh_AP_communication_ui()

    def _push_hvac_controls(self):
        status = self._context.buffer.defender_status
        payload = {
        "encryption_status": status.get("encryption_status", False),
        "encryption_key": self._enc_key_entry.text().strip(),
        "AP_communication": status.get("ap_communication", False),
        "sensor_noise_variance": self.sensor_noise_variance,
        "hvac_kalman_expected_sensor_variance": self.kalman_expected_sensor_variance,
        "hvac_state_error_threshold": self.state_error_threshold,
        "hvac_kalman_filter_enabled": self._hvac_kalman_filter_enabled,
        }

        def _request():
            try:
                requests.post(
                    f"{self._get_url()}/set_hvac_settings",
                    json=payload,
                    timeout=3,
                )
            except Exception:
                pass

        # No UI update on the response here - unlike Tk's after(0, ...),
        # which safely marshals a callback onto the main thread, touching
        # widgets directly from this background thread would be unsafe
        # under Qt. refresh() already reconciles this UI every animation
        # tick on the main thread (see below), which is the same ~100ms
        # latency this app already uses everywhere else for background
        # work reaching the GUI.
        threading.Thread(target=_request, daemon=True).start()

    def _to_slider_pos(self, value: float, lo: float, hi: float) -> int:
        if hi == lo:
            return 0
        return int(round((value - lo) / (hi - lo) * SLIDER_RESOLUTION))

    def _from_slider_pos(self, pos: int, lo: float, hi: float) -> float:
        return lo + (pos / SLIDER_RESOLUTION) * (hi - lo)

    def _build_slider_block(self, parent: QWidget):
        section = self._section(parent, "HVAC SETTINGS")

        slider_defs = [
            ("Sensor Noise Variance", 0.0, 1.0, 0.1, "sensor_noise_variance", 2),
            ("Kalman Expected Sensor Variance", 0.0, 1.0, 0.1, "kalman_expected_sensor_variance", 2),
            ("State Error Threshold", 0.0, 10.0, 5.0, "state_error_threshold", 1),
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

            slider = ShiftWheelSlider(Qt.Orientation.Horizontal)
            slider.setRange(0, SLIDER_RESOLUTION)
            slider.setValue(self._to_slider_pos(default, min_val, max_val))

            def slider_callback(pos, lbl=value_label, attr=attr_name, d=decimals, lo=min_val, hi=max_val):
                value = self._from_slider_pos(pos, lo, hi)
                setattr(self, attr, value)
                lbl.setText(f"{value:.{d}f}")

                if not self._syncing_sliders:
                    self._push_hvac_controls()

            slider.valueChanged.connect(slider_callback)
            section.layout().addWidget(slider)

            self._sliders[title] = slider
            self._slider_value_labels[title] = value_label
            self._slider_ranges[title] = (min_val, max_val)

        reset_button = QPushButton("Reset to Defaults")
        reset_button.setFont(self.style.get_font())
        self._wire_button(reset_button, self._reset_slider_defaults)
        section.layout().addWidget(reset_button)

    def _readout_row(self, parent: QWidget, label_text: str) -> QLabel:
        row = QWidget()
        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(0, 0, 0, 0)
        parent.layout().addWidget(row)

        label = QLabel(f"{label_text}:")
        label.setFont(self.style.get_font("small"))
        label.setStyleSheet("color: gray;")
        row_layout.addWidget(label)
        row_layout.addStretch()

        value = QLabel("—")
        value.setFont(self.style.get_font("small"))
        row_layout.addWidget(value)
        return value

    def _build_graph(self, parent: QWidget):
        self._graph_root = QWidget()
        self._graph_root.setStyleSheet(self.style.themed(f"background-color: {self.style.color('widget')};", self._graph_root))
        self._graph_root.setLayout(QVBoxLayout())
        self._graph_root.layout().setContentsMargins(8, 8, 8, 8)
        parent.layout().addWidget(self._graph_root)

        fig = Figure(figsize=(5, 4), dpi=100)
        fig.patch.set_facecolor(_FIG_BG)
        ax = fig.add_subplot(111)
        ax.set_facecolor(_AXES_BG)
        ax.set_title("Temperature Trajectory Over Time", color=_TEXT, fontsize=11)
        ax.set_xlabel("Time (s)", color=_TEXT)
        ax.set_ylabel("Temperature (°F)", color=_TEXT)
        ax.tick_params(colors=_TEXT)
        ax.grid(True, color=_GRID, linewidth=0.6)
        ax.margins(0,0.2)
        for spine in ax.spines.values():
            spine.set_color(_GRID)

        (self._room_line,) = ax.plot([], [], color=_ROOM_LINE, linewidth=1.8,
                                      label="Room Temp")
        (self._target_line,) = ax.plot([], [], color=_TARGET_LINE, linewidth=1.8,
                                        linestyle="--", label="Target Setpoint")
        legend = ax.legend(loc="upper left", facecolor=_FIG_BG, edgecolor=_GRID,
                           fontsize=8)
        for text in legend.get_texts():
            text.set_color(_TEXT)
        fig.tight_layout()

        self._fig = fig
        self._ax  = ax
        self._canvas = FigureCanvasQTAgg(fig)
        self._graph_root.layout().addWidget(self._canvas)
        self._canvas.draw()

    def _sync_hvac_sliders(self):
        status = self._context.buffer.defender_status
        values = {
            "Sensor Noise Variance":
                status.get("hvac_sensor_noise_variance"),

            "Kalman Expected Sensor Variance":
                status.get("hvac_kalman_expected_sensor_variance"),

            "State Error Threshold":
                status.get("hvac_state_error_threshold"),
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

                lo, hi = self._slider_ranges[title]
                slider.setValue(self._to_slider_pos(value, lo, hi))

                attr_map = {
                    "Sensor Noise Variance":
                        "sensor_noise_variance",

                    "Kalman Expected Sensor Variance":
                        "kalman_expected_sensor_variance",

                    "State Error Threshold":
                        "state_error_threshold",
                }

                setattr(self, attr_map[title], value)

                if label is not None:
                    decimals = 1 if title == "State Error Threshold" else 2
                    label.setText(f"{value:.{decimals}f}")

        finally:
            self._syncing_sliders = False

    def _reset_slider_defaults(self):
        defaults = {
            "Sensor Noise Variance": (
                0.1, "sensor_noise_variance", 2
            ),
            "Kalman Expected Sensor Variance": (
                0.1, "kalman_expected_sensor_variance", 2
            ),
            "State Error Threshold": (
                5.0, "state_error_threshold", 1
            ),
        }

        self._syncing_sliders = True

        try:
            for title, (value, attr, decimals) in defaults.items():

                setattr(self, attr, value)

                lo, hi = self._slider_ranges[title]
                self._sliders[title].setValue(self._to_slider_pos(value, lo, hi))

                self._slider_value_labels[title].setText(f"{value:.{decimals}f}")

        finally:
            self._syncing_sliders = False

        self._push_hvac_controls()

    # ════════════════════════════════════════════════════════════════════
    #  Visibility — self-managed from defender_status.submarine_mode, not
    #  driven by DefenderV0, so this class doesn't need anything outside
    #  itself to know when to show or hide.
    # ════════════════════════════════════════════════════════════════════

    def show(self):
        self._left_root.show()
        self._graph_root.show()

    def hide(self):
        self._left_root.hide()
        self._graph_root.hide()

    def _refresh_visibility(self):
        submarine_mode = bool(self._context.buffer.defender_status.get("submarine_mode", True))
        if submarine_mode == self._submarine_mode:
            return
        self._submarine_mode = submarine_mode
        self.hide() if submarine_mode else self.show()

    # ════════════════════════════════════════════════════════════════════
    #  Data — reads straight from context.buffer; DefenderV0 only tells the
    #  shared animation_manager when to tick, it never hands us poll data.
    # ════════════════════════════════════════════════════════════════════

    def refresh(self):
        self._refresh_visibility()
        self._sync_hvac_sliders()
        self._refresh_hvac_controls_ui()

        modbus = self._context.buffer.defender_modbus
        status = self._context.buffer.defender_status

        current_temp = modbus.get_single("temperature", "client_clean")
        target_temp  = modbus.get_single("temperature", "target")
        heater_on    = status.get("heater_on")

        if current_temp is not None:
            self._current_label.setText(f"{float(current_temp):.1f}°F")
        if target_temp is not None:
            self._target_label.setText(f"{float(target_temp):.1f}°F")
        if heater_on is not None:
            on = bool(heater_on)
            self._heater_label.setText("ON" if on else "OFF")
            self._heater_label.setStyleSheet(f"color: {'green' if on else 'gray'};")

        if current_temp is None and target_temp is None:
            return  # nothing worth plotting yet

        self._redraw_graph()

    def _redraw_graph(self):
        modbus = self._context.buffer.defender_modbus
        room_history = modbus.get_history("temperature", "client_clean")[-self.MAX_POINTS:]
        target_history = modbus.get_history("temperature", "target")[-self.MAX_POINTS:]

        if not room_history and not target_history:
            return
        t0 = (room_history or target_history)[0][0]

        room_times, room_values = zip(*room_history) if room_history else ((), ())
        target_times, target_values = zip(*target_history) if target_history else ((), ())

        self._room_line.set_data([t - t0 for t in room_times], room_values)
        self._target_line.set_data([t - t0 for t in target_times], target_values)
        self._ax.relim()
        self._ax.autoscale_view()

        y_min, y_max = self._ax.get_ylim()
        center = (y_min + y_max) / 2
        min_range = 150.0
        if (y_max - y_min) < min_range:
            half_range = min_range / 2
            self._ax.set_ylim(center - half_range, center + half_range)

        self._canvas.draw_idle()
