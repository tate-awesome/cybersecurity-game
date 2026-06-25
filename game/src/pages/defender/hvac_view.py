"""
Read-only HVAC test dashboard for DefenderV0.

DefenderV0 owns the connection, polling, and mode detection (reading
submarine_mode from AP_ESP32.ino). This module only knows how to render
whatever HVAC fields it's handed via update(), and how to push a manual
setpoint to the AP's /set_hvac_target test endpoint. It has no opinion
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

    def __init__(self, style, left_parent, right_parent, get_url_fn):
        """
        style        - the Style object DefenderV0 already uses (self.style)
        left_parent  - container to build the setpoint/readout cards into
        right_parent - container to build the trajectory graph into
        get_url_fn   - callable returning the current base server URL,
                       shared with DefenderV0 so both hit the same AP
        """
        self.style    = style
        self._get_url = get_url_fn

        self._t0            = time.monotonic()
        self._times          = []
        self._room_temps     = []
        self._target_temps   = []

        self._build_left(left_parent)
        self._build_graph(right_parent)

    # ════════════════════════════════════════════════════════════════════
    #  Construction
    # ════════════════════════════════════════════════════════════════════

    def _build_left(self, parent):
        self._left_root = CTkFrame(parent, fg_color="transparent")

        # ── Setpoint card ──────────────────────────────────────────────
        setpoint_card = CTkFrame(self._left_root, fg_color=self.style.color("widget"))
        setpoint_card.pack(fill="x", padx=self.style.igap, pady=self.style.igap)

        CTkLabel(setpoint_card, text="HVAC SETPOINT", font=self.style.get_font()).pack(
            anchor="w", padx=self.style.igap, pady=(self.style.igap, 0)
        )
        CTkLabel(setpoint_card, text="Test rig — sets target_temp on AP_ESP32",
                 font=self.style.get_font("small"), text_color="gray").pack(
            anchor="w", padx=self.style.igap
        )

        CTkLabel(setpoint_card, text="Target Temperature (°F)",
                 font=self.style.get_font("small"), text_color="gray").pack(
            anchor="w", padx=self.style.igap, pady=(self.style.igap, 0)
        )
        self._setpoint_entry = CTkEntry(setpoint_card, font=self.style.get_font(),
                                        placeholder_text="e.g. 75.2")
        self._setpoint_entry.pack(fill="x", padx=self.style.igap, pady=(2, 4))

        CTkButton(setpoint_card, text="Set Temperature", font=self.style.get_font(),
                  command=self._send_setpoint).pack(
            fill="x", padx=self.style.igap, pady=(0, 4)
        )

        self._setpoint_status = CTkLabel(setpoint_card, text="Status: Not set",
                                         font=self.style.get_font(), text_color="gray")
        self._setpoint_status.pack(anchor="w", padx=self.style.igap, pady=self.style.gapbot)

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
    #  Network — manual setpoint push
    # ════════════════════════════════════════════════════════════════════

    def _send_setpoint(self):
        raw = self._setpoint_entry.get().strip()
        try:
            value = float(raw)
        except ValueError:
            self._setpoint_status.configure(text="Status: Invalid input", text_color="red")
            return

        if not (0.0 <= value <= 150.0):
            self._setpoint_status.configure(text="Status: Out of range (0–150°F)",
                                            text_color="red")
            return

        def _request():
            try:
                resp = requests.post(
                    f"{self._get_url()}/set_hvac_target",
                    json={"target_temp": value},
                    timeout=3,
                )
                if resp.ok:
                    self._setpoint_status.after(0, lambda: self._setpoint_status.configure(
                        text=f"Status: Set to {value:.1f}°F", text_color="green"
                    ))
                else:
                    self._setpoint_status.after(0, lambda: self._setpoint_status.configure(
                        text=f"Status: Server error {resp.status_code}", text_color="red"
                    ))
            except Exception:
                self._setpoint_status.after(0, lambda: self._setpoint_status.configure(
                    text="Status: Connection failed", text_color="red"
                ))

        threading.Thread(target=_request, daemon=True).start()

    # ════════════════════════════════════════════════════════════════════
    #  Data — DefenderV0 feeds the polled /api/data JSON straight through
    # ════════════════════════════════════════════════════════════════════

    def update(self, data: dict):
        current_temp = data.get("current_temp")
        target_temp  = data.get("target_temp")
        heater_on    = data.get("heater_on")

        if current_temp is not None:
            self._current_label.configure(text=f"{float(current_temp):.1f}°F")
        if target_temp is not None:
            self._target_label.configure(text=f"{float(target_temp):.1f}°F")
        if heater_on is not None:
            on = bool(heater_on)
            self._heater_label.configure(text="ON" if on else "OFF",
                                         text_color="green" if on else "gray")

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
