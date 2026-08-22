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
from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkEntry

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# UI blocks shared with DefenderV0 (submarine mode)
from ._shared_blocks import (
    SliderDef, build_encryption_block, build_ap_communication_block,
    build_slider_block, sync_sliders, reset_slider_defaults,
)

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

    # Set by _shared_blocks.build_encryption_block()/build_ap_communication_block()
    # via setattr(target, ...) - declared here so pyright can see them.
    _enc_label: CTkLabel
    _enc_button: CTkButton
    _enc_key_entry: CTkEntry
    _filter_label: CTkLabel
    _filter_button: CTkButton

    MAX_POINTS = 300     # rolling window cap
    MAX_AGE_S  = 300.0    # ...and a 5-minute time cap, whichever trims more

    # Slider definitions: (title, min, max, default, attr_name, decimals, data_key)
    HVAC_SLIDER_DEFS: list[SliderDef] = [
        SliderDef("Sensor Noise Variance", 0.0, 1.0, 0.1, "sensor_noise_variance", 2, "hvac_sensor_noise_variance"),
        SliderDef("Kalman Expected Sensor Variance", 0.0, 1.0, 0.1, "kalman_expected_sensor_variance", 2, "hvac_kalman_expected_sensor_variance"),
        SliderDef("State Error Threshold", 0.0, 10.0, 5.0, "state_error_threshold", 1, "hvac_state_error_threshold"),
    ]

    def __init__(self, style, left_parent, right_parent, get_url_fn, context, on_hvac_anomaly=None, on_kalman_filter_change=None):
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
        self._on_kalman_filter_change = on_kalman_filter_change

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
        self._hvac_kalman_filter_enabled = True

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
        build_encryption_block(self.style, parent, parent, self._context, self)

    def _toggle_encryption(self):
        if not self._encryption_on:
            self._enc_key_entry.configure(state="disabled")
            self._enc_button.configure(text="Disable Encryption")
            self._encryption_on = True
        else:
            self._enc_key_entry.configure(state="normal")
            self._enc_button.configure(text="Enable Encryption")
            self._encryption_on = False

        self._push_hvac_controls()

    def _build_AP_communication_block(self, parent):
        build_ap_communication_block(self.style, parent, self, self._toggle_AP_communication)

    def _toggle_AP_communication(self):
        self._AP_communication_on = not self._AP_communication_on
        self._push_hvac_controls()

    def _toggle_hvac_kalman_filter(self):
        self._hvac_kalman_filter_enabled = (
            not self._hvac_kalman_filter_enabled
        )

        if self._on_kalman_filter_change is not None:
            self._on_kalman_filter_change(
                self._hvac_kalman_filter_enabled
            )

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
        "encryption_key": self._enc_key_entry.get().strip(),
        "AP_communication": self._AP_communication_on,
        "sensor_noise_variance": self.sensor_noise_variance,
        "hvac_kalman_expected_sensor_variance": self.kalman_expected_sensor_variance,
        "hvac_state_error_threshold": self.state_error_threshold,
        "hvac_kalman_filter_enabled": self._hvac_kalman_filter_enabled,
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
        self._sliders, self._slider_value_labels = build_slider_block(
            self.style, parent, "HVAC SETTINGS", self.HVAC_SLIDER_DEFS,
            self, self._push_hvac_controls, self._reset_slider_defaults,
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
        sync_sliders(self, data, self.HVAC_SLIDER_DEFS, self._sliders, self._slider_value_labels)

    def _reset_slider_defaults(self):
        reset_slider_defaults(self, self.HVAC_SLIDER_DEFS, self._sliders, self._slider_value_labels, self._push_hvac_controls)

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