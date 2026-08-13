"""
Read-only HVAC test dashboard for DefenderV0.

DefenderV0 owns the connection, polling, and mode detection (reading
submarine_mode from AP_ESP32.ino). This module only knows how to render
whatever HVAC fields it's handed via update(). It has no opinion
about Submarine mode and doesn't touch any Submarine-only state.
"""

import threading
import time

import requests
from customtkinter import CTkButton, CTkEntry, CTkFrame, CTkLabel, CTkSlider

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from ...widgets import popup

# Hardcoded dark-theme colors matching AP_ESP32.ino's config page palette.
# Not pulled from the app's Style object on purpose — CTk colors can be
# light/dark-mode tuples, and matplotlib needs a single concrete color string.
_FIG_BG      = "#16213e"
_AXES_BG     = "#0a0a1a"
_GRID        = "#0f3460"
_TEXT        = "#e0e0e0"
_ROOM_LINE   = "#4caf50"   # green
_TARGET_LINE = "#e94560"   # accent pink/red, matches the AP's accent color


class HVACView:

    MAX_POINTS = 300     # rolling window cap
    MAX_AGE_S  = 300.0    # ...and a 5-minute time cap, whichever trims more

    def __init__(self, style, left_parent, right_parent, get_url_fn, context, on_hvac_anomaly=None):
        """
        style        - the Style object DefenderV0 already uses (self.style)
        left_parent  - container to build the readout cards into
        right_parent - container to build the trajectory graph into
        get_url_fn   - callable returning the current base server URL,
                       shared with DefenderV0 so both hit the same AP
        """
        self.style    = style
        self._get_url = get_url_fn
        self._on_hvac_anomaly = on_hvac_anomaly

        self._t0            = time.monotonic()
        self._times          = []
        self._room_temps     = []
        self._target_temps   = []
        self._HVAC_anomaly = False
        self._encryption_on = False
        self._context = context
        self._AP_communication_on = False
        self._ui_master = left_parent
        self.sensor_noise_variance = 0.1
        self.kalman_expected_sensor_variance = 0.1
        self.state_error_threshold = 5.0
        self._syncing_sliders = False

        self._build_left(left_parent)
        self._build_graph(right_parent)

    # ════════════════════════════════════════════════════════════════════
    #  Construction
    # ════════════════════════════════════════════════════════════════════

    def _build_left(self, parent):
        self._left_root = CTkFrame(parent, fg_color="transparent")

        # ── Live readout card ──────────────────────────────────────────
        readout_card = CTkFrame(self._left_root, fg_color=self.style.color("widget"))
        readout_card.pack(fill="x", padx=self.style.igap, pady=self.style.igap)

        CTkLabel(readout_card, text="LIVE STATUS", font=self.style.get_font()).pack(
            anchor="w", padx=self.style.igap, pady=(self.style.igap, 4)
        )

        self._current_label = self._readout_row(readout_card, "Current Temp")
        self._target_label  = self._readout_row(readout_card, "Target Temp")
        self._heater_label  = self._readout_row(readout_card, "Heater")

        CTkFrame(readout_card, fg_color="transparent", height=self.style.igap).pack()

        self._build_encryption_block(self._left_root)
        self._build_AP_communication_block(self._left_root)
        self._build_slider_block(self._left_root)

    def _build_encryption_block(self, parent):
        section = CTkFrame(parent, fg_color=self.style.color("widget"))
        section.pack(fill="x", padx=self.style.igap, pady=self.style.igap)

        CTkLabel(section, text="ENCRYPTION", font=self.style.get_font()).pack(
            anchor="w", padx=self.style.igap, pady=(self.style.igap, 0)
        )
        self._enc_label = CTkLabel(section, text="Status: OFF",
                                    font=self.style.get_font(), text_color="gray")
        self._enc_label.pack(anchor="w", padx=self.style.igap)

        # Key entry
        CTkLabel(section, text="Encryption Key", font=self.style.get_font("small"),
                    text_color="gray").pack(anchor="w", padx=self.style.igap, pady=self.style.gaptop)
        self._enc_key_entry = CTkEntry(section, font=self.style.get_font(),
                                        placeholder_text="Enter key…")
        self._enc_key_entry.pack(fill="x", padx=self.style.igap, pady=(2, 4))

        self._enc_button = CTkButton(section, text="Enable Encryption",
                                        font=self.style.get_font())
        def enc_button():
            if not self._encryption_on:
                # Encryption is off - try to turn it on
                if self._enc_key_entry.get().strip() == "":
                    # Empty key — show error
                    popup.message(parent, self._context, "Please enter an encryption key before enabling encryption.")
                elif not str.isascii(self._enc_key_entry.get().strip()):
                    # Non-ASCII key — show error
                    popup.message(parent, self._context, "Encryption key must be ASCII.")
                else:
                    # Key looks good — toggle encryption on behavior
                    self._enc_key_entry.configure(state="disabled")
                    self._enc_button.configure(text="Disable Encryption")
                    self._toggle_encryption()
            else:
                # Encryption is on - turn it off
                self._enc_key_entry.configure(state="normal")
                self._enc_key_entry.delete(0, "end")
                self._enc_button.configure(text="Enable Encryption")
                self._toggle_encryption()

        self._enc_button.configure(command=enc_button)

        self._enc_button.pack(fill="x", padx=self.style.igap, pady=self.style.gapbot)

    def _toggle_encryption(self):
        if not self._encryption_on:
            self._enc_key_entry.configure(state="disabled")
            self._enc_button.configure(text="Disable Encryption")
            self._encryption_on = True
        else:
            self._enc_key_entry.configure(state="normal")
            self._enc_key_entry.delete(0, "end")
            self._enc_key_entry.insert(0, "1234")
            self._enc_button.configure(text="Enable Encryption")
            self._encryption_on = False

        self._push_hvac_controls()

    def _build_AP_communication_block(self, parent):
        section = CTkFrame(parent, fg_color=self.style.color("widget"))
        section.pack(fill="x", padx=self.style.igap, pady=self.style.igap)

        CTkLabel(section, text="COMMUNICATE VIA ACCESS POINT", font=self.style.get_font()).pack(
            anchor="w", padx=self.style.igap, pady=(self.style.igap, 0)
        )
        self._filter_label = CTkLabel(section, text="Status: OFF",
                                    font=self.style.get_font(), text_color="gray")
        self._filter_label.pack(anchor="w", padx=self.style.igap)

        self._filter_button = CTkButton(section, text="Enable Communication Through AP",
                                        font=self.style.get_font(),
                                        command=self._toggle_AP_communication)
        self._filter_button.pack(fill="x", padx=self.style.igap, pady=self.style.gapbot)

    def _toggle_AP_communication(self):
        self._AP_communication_on = not self._AP_communication_on
        self._push_hvac_controls()

    def _refresh_encryption_ui(self):
        if self._encryption_on:
            self._enc_label.configure(text="Status: ON", text_color="green")
            self._enc_button.configure(text="Disable Encryption")
            self._enc_key_entry.configure(state="disabled")
        else:
            self._enc_label.configure(text="Status: OFF", text_color="gray")
            self._enc_button.configure(text="Enable Encryption")
            self._enc_key_entry.configure(state="normal")

    def _refresh_AP_communication_ui(self):
        if self._AP_communication_on:
            self._filter_label.configure(text="Status: ON", text_color="green")
            self._filter_button.configure(text="Disable Communication Through AP")
        else:
            self._filter_label.configure(text="Status: OFF", text_color="gray")
            self._filter_button.configure(text="Enable Communication Through AP")

    def _refresh_hvac_controls_ui(self):
        self._refresh_encryption_ui()
        self._refresh_AP_communication_ui()

    def _push_hvac_controls(self):
        payload = {
        "encryption_status": self._encryption_on,
        "encryption_key": self._enc_key_entry.get().strip() if self._encryption_on else "1234",
        "AP_communication": self._AP_communication_on,
        "sensor_noise_variance": self.sensor_noise_variance,
        "hvac_kalman_expected_sensor_variance": self.kalman_expected_sensor_variance,
        "hvac_state_error_threshold": self.state_error_threshold,
        }

        def _request():
            try:
                resp = requests.post(
                    f"{self._get_url()}/set_hvac_settings",
                    json=payload,
                    timeout=3,
                )
                if resp.ok:
                    self._ui_master.after(0, self._refresh_hvac_controls_ui)
            except Exception:
                pass

        threading.Thread(target=_request, daemon=True).start()

    def _build_slider_block(self, parent):
        section = CTkFrame(parent, fg_color=self.style.color("widget"))
        section.pack(fill="x", padx=self.style.igap, pady=self.style.igap)

        CTkLabel(
            section,
            text="HVAC SETTINGS",
            font=self.style.get_font()
        ).pack(anchor="w", padx=self.style.igap, pady=(self.style.igap, 8))

        slider_defs = [
            ("Sensor Noise Variance", 0.0, 1.0, 0.1, "sensor_noise_variance", 2),
            ("Kalman Expected Sensor Variance", 0.0, 1.0, 0.1, "kalman_expected_sensor_variance", 2),
            ("State Error Threshold", 0.0, 10.0, 5.0, "state_error_threshold", 1),
        ]

        self._sliders = {}
        self._slider_value_labels = {}

        for title, min_val, max_val, default, attr_name, decimals in slider_defs:
            header = CTkFrame(section, fg_color="transparent")
            header.pack(fill="x", padx=self.style.igap)

            CTkLabel(
                header,
                text=title,
                font=self.style.get_font("small")
            ).pack(side="left")

            value_label = CTkLabel(
                header,
                text=f"{default:.{decimals}f}",
                font=self.style.get_font("small"),
                text_color="gray"
            )
            value_label.pack(side="right")

            def slider_callback(value, lbl=value_label, attr=attr_name, d=decimals):
                value = float(value)

                setattr(self, attr, value)
                lbl.configure(text=f"{value:.{d}f}")

                if not self._syncing_sliders:
                    self._push_hvac_controls()

            slider = CTkSlider(
                section,
                from_=min_val,
                to=max_val,
                command=slider_callback
            )
            slider.set(default)
            slider.pack(fill="x", padx=self.style.igap, pady=(0, 8))

            self._sliders[title] = slider
            self._slider_value_labels[title] = value_label

        reset_button = CTkButton(
            section,
            text="Reset to Defaults",
            font=self.style.get_font(),
            command=self._reset_slider_defaults
        )
        reset_button.pack(
            fill="x",
            padx=self.style.igap,
            pady=self.style.igap
        )
    
    def _readout_row(self, parent, label_text):
        row = CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", padx=self.style.igap, pady=2)
        CTkLabel(row, text=f"{label_text}:", font=self.style.get_font("small"),
                 text_color="gray", anchor="w").pack(side="left")
        value = CTkLabel(row, text="—", font=self.style.get_font("small"), anchor="e")
        value.pack(side="right")
        return value

    def _build_graph(self, parent):
        self._graph_root = CTkFrame(parent, fg_color=self.style.color("widget"))

        fig = Figure(figsize=(5, 4), dpi=100)
        fig.patch.set_facecolor(_FIG_BG)
        ax = fig.add_subplot(111)
        ax.set_facecolor(_AXES_BG)
        ax.set_title("Temperature Trajectory Over Time", color=_TEXT, fontsize=11)
        ax.set_xlabel("Time (s)", color=_TEXT)
        ax.set_ylabel("Temperature (°F)", color=_TEXT)
        ax.tick_params(colors=_TEXT)
        ax.grid(True, color=_GRID, linewidth=0.6)
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
        self._canvas = FigureCanvasTkAgg(fig, master=self._graph_root)
        self._canvas.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=8)
        self._canvas.draw()

    def _sync_hvac_sliders(self, data: dict):
        values = {
            "Sensor Noise Variance":
                data.get("hvac_sensor_noise_variance"),

            "Kalman Expected Sensor Variance":
                data.get("hvac_kalman_expected_sensor_variance"),

            "State Error Threshold":
                data.get("hvac_state_error_threshold"),
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

                slider.set(value)

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
                    label.configure(
                        text=f"{value:.{decimals}f}"
                    )

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

                self._sliders[title].set(value)

                self._slider_value_labels[title].configure(
                    text=f"{value:.{decimals}f}"
                )

        finally:
            self._syncing_sliders = False

        self._push_hvac_controls()

    # ════════════════════════════════════════════════════════════════════
    #  Visibility — DefenderV0 calls these on mode change
    # ════════════════════════════════════════════════════════════════════

    def show(self):
        self._left_root.pack(fill="x")
        self._graph_root.pack(fill="both", expand=True, padx=20, pady=20)

    def hide(self):
        self._left_root.pack_forget()
        self._graph_root.pack_forget()

    # ════════════════════════════════════════════════════════════════════
    #  Data — DefenderV0 feeds the polled /api/data JSON straight through
    # ════════════════════════════════════════════════════════════════════

    def update(self, data: dict):
        self._sync_hvac_sliders(data)

        current_temp = data.get("current_temp")
        target_temp  = data.get("target_temp")
        heater_on    = data.get("heater_on")
        HVAC_anomaly = data.get("HVAC_anomaly_detected")

        if current_temp is not None:
            self._current_label.configure(text=f"{float(current_temp):.1f}°F")
        if target_temp is not None:
            self._target_label.configure(text=f"{float(target_temp):.1f}°F")
        if heater_on is not None:
            on = bool(heater_on)
            self._heater_label.configure(text="ON" if on else "OFF",
                                         text_color="green" if on else "gray")
        if HVAC_anomaly is not None:
            self._HVAC_anomaly = bool(HVAC_anomaly)
            if self._on_hvac_anomaly is not None:
                self._on_hvac_anomaly(self._HVAC_anomaly)

        if current_temp is None and target_temp is None:
            return  # nothing worth plotting yet

        t = time.monotonic() - self._t0
        self._times.append(t)
        self._room_temps.append(float(current_temp) if current_temp is not None else float("nan"))
        self._target_temps.append(float(target_temp) if target_temp is not None else float("nan"))

        # Trim to a rolling window so the graph doesn't grow unbounded
        cutoff = t - self.MAX_AGE_S
        while self._times and (self._times[0] < cutoff or len(self._times) > self.MAX_POINTS):
            self._times.pop(0)
            self._room_temps.pop(0)
            self._target_temps.pop(0)

        self._room_line.set_data(self._times, self._room_temps)
        self._target_line.set_data(self._times, self._target_temps)
        self._ax.relim()
        self._ax.autoscale_view()
        self._canvas.draw_idle()

    def get_hvac_anomaly(self):
        return self._HVAC_anomaly