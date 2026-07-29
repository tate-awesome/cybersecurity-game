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
from customtkinter import CTkButton, CTkEntry, CTkFrame, CTkLabel

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

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

    def __init__(self, style, left_parent, right_parent, get_url_fn, on_hvac_anomaly=None):
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