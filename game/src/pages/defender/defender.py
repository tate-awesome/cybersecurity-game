from ...app_core import Context

# Widgets
from ...widgets import Panes, MenuBar, Scrollable
from ...widgets import popup
from ...widgets.map import Map
from ...drawing.viewport import ViewPort
from ..page import Page

# Network
from ...network.network_controller import HardwareDefender

# HVAC test dashboard, shown in place of the Submarine widgets when AP_ESP32
# reports submarine_mode == False
from .hvac_view import HVACView

# customtkinter widgets
from customtkinter import (
    CTkLabel, CTkEntry, CTkButton, CTkFrame,
    CTkScrollableFrame, CTkSegmentedButton, CTkSlider
)

import threading
import requests
import math
import time


class DefenderV0(Page):
    '''
    Page constructor for defender/defenderv0. Inherits CTkFrame
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
        context.refresh_net(HardwareDefender)
        # TODO use net for lifetime management   = context.refresh_net(HardwareDefender)

        # ── Internal state FIRST (map callback fires immediately) ────────────
        self._server_url    = "http://192.168.4.1"
        self._positions     = []
        self._last_bearing  = None
        self._encryption_on = False
        self._AP_communication_on = False
        self._last_seq      = -1
        self._log_source    = "client"   # "client" or "server"
        self._last_points   = {"client": [], "server": []}
        self._submarine_mode = True
        self.sensor_noise_variance = 8.3
        self.kalman_expected_sensor_variance = 8.3
        self.rudder_error_threshold = 2.75
        self.speed_error_threshold = 2.0
        self._syncing_sliders = False
        self._submarine_pending_revision = 0
        self._submarine_kalman_filter_enabled = True

        # Flag state — all False until logic sets them
        self._submarine_flags = {key: False for key, _ in self.SUBMARINE_FLAG_DEFS}
        self._HVAC_flags = {key: False for key, _ in self.HVAC_FLAG_DEFS}

        # ── Menu bar ─────────────────────────────────────────────────────────
        menu_bar = MenuBar(self, context, "defender")
        menu_bar.page_buttons()

        # ── Three-pane layout ────────────────────────────────────────────────
        trifold = Panes(self, context, "horizontal", 3, [4, 3, 2], True)
        left_p = Scrollable(trifold.pane(0), context)
        middle_p = trifold.pane(1)
        right_p = trifold.pane(2)

        # ── Left pane ────────────────────────────────────────────────────────
        self._build_connection_block(left_p)   # mode-agnostic — always visible
        self._mode_content_left = CTkFrame(left_p, fg_color="transparent")
        self._mode_content_left.pack(fill="x")

        self._submarine_left = CTkFrame(self._mode_content_left, fg_color="transparent")
        self._submarine_left.pack(fill="x")
        self._build_encryption_block(self._submarine_left)
        self._build_AP_communication_block(self._submarine_left)
        self._build_slider_block(self._submarine_left)
        self._build_values_block(self._submarine_left)

        self._hvac_view = HVACView(self.style, self._mode_content_left, right_p, self._get_url, context, on_hvac_anomaly=self._set_hvac_flag, 
                                   on_kalman_filter_change = self._set_hvac_kalman_filter_status)

        left_p.add_deadspace()

        # ── Middle pane ──────────────────────────────────────────────────────
        self._submarine_middle = CTkFrame(middle_p, fg_color="transparent")
        self._build_packet_log(self._submarine_middle)
        self._build_flags_block(self._submarine_middle, "SUBMARINE ERROR DETECTION FLAGS [MODBUS]", self.SUBMARINE_FLAG_DEFS, "_submarine_flag_labels",)
        # ── Kalman Filter block ─────────────────────────────────────────────
        kalman_section = CTkFrame(
            self._submarine_middle,
            fg_color=self.style.color("widget")
        )
        kalman_section.pack(
            fill="x",
            padx=self.style.igap,
            pady=self.style.igap
        )

        CTkLabel(
            kalman_section,
            text="KALMAN FILTER",
            font=self.style.get_font()
        ).pack(
            anchor="w",
            padx=self.style.igap,
            pady=(self.style.igap, 0)
        )

        self._submarine_kalman_label = CTkLabel(
            kalman_section,
            text="Status: ON",
            font=self.style.get_font(),
            text_color="green"
        )
        self._submarine_kalman_label.pack(
            anchor="w",
            padx=self.style.igap
        )

        self._submarine_kalman_button = CTkButton(
            kalman_section,
            text="Toggle Kalman Filter",
            font=self.style.get_font(),
            command=self._toggle_submarine_kalman_filter
        )
        self._submarine_kalman_button.pack(
            fill="x",
            padx=self.style.igap,
            pady=self.style.gapbot
        )

        self._hvac_middle = CTkFrame(middle_p, fg_color="transparent")
        self._build_flags_block(self._hvac_middle, "HVAC ERROR DETECTION FLAG", self.HVAC_FLAG_DEFS, "_hvac_flag_labels",)
        # ── HVAC Kalman Filter block ───────────────────────────────────────
        kalman_section = CTkFrame(
            self._hvac_middle,
            fg_color=self.style.color("widget")
        )
        kalman_section.pack(
            fill="x",
            padx=self.style.igap,
            pady=self.style.igap
        )

        CTkLabel(
            kalman_section,
            text="KALMAN FILTER",
            font=self.style.get_font()
        ).pack(
            anchor="w",
            padx=self.style.igap,
            pady=(self.style.igap, 0)
        )

        self._hvac_kalman_label = CTkLabel(
            kalman_section,
            text="Status: ON",
            font=self.style.get_font(),
            text_color="green"
        )
        self._hvac_kalman_label.pack(
            anchor="w",
            padx=self.style.igap
        )

        self._hvac_kalman_button = CTkButton(
            kalman_section,
            text="Toggle Kalman Filter",
            font=self.style.get_font(),
            command=self._hvac_view._toggle_hvac_kalman_filter,
        )
        self._hvac_kalman_button.pack(
            fill="x",
            padx=self.style.igap,
            pady=self.style.gapbot
        )

        self._build_mode_block(middle_p)       # mode-agnostic — always visible
        self._refresh_mode_ui()

        self._submarine_kalman_filter_enabled = True
        self._hvac_view._hvac_kalman_filter_enabled = True

        self._post_slider_settings()
        self._hvac_view._push_hvac_controls()

        self._map_scale  = None
        self._map_offset = None
        self._map_click_xy = None

        self._map_container = CTkFrame(right_p, fg_color="transparent")
        self._map_container.pack(fill="both", expand=True)

        def draw_defender_map(canvas, draw_lock, scale, offset):
            draw = ViewPort(canvas, scale, offset)
            with draw_lock:
                self._map_scale  = scale
                self._map_offset = offset
                canvas.delete("all")
                draw.grid_lines()
                if len(self._positions) < 1:
                    return
                draw.line(self._positions, "red")
                if self._last_bearing is None:
                    return
                draw.boat(self._positions[-1], self._last_bearing, "white", "black")

        self._map = Map(self._map_container, context, draw_defender_map,
                        framerate_ms=self.POLL_INTERVAL_MS, padding=20)
        #self._map.canvas.bind("<Button-1>", self._on_map_click)

        # ── Start polling ────────────────────────────────────────────────────
        self._poll()

    # ════════════════════════════════════════════════════════════════════════
    #  UI builder helpers
    # ════════════════════════════════════════════════════════════════════════

    def _set_hvac_flag(self, value: bool):
                self._HVAC_flags["HVAC_filter_flag"] = bool(value)
                self._refresh_flags()

    def _set_hvac_kalman_filter_status(self, enabled: bool):
        enabled = bool(enabled)

        if enabled:
            self._hvac_kalman_label.configure(
                text="Kalman Filter Status: ON",
                text_color="green",
            )
        else:
            self._hvac_kalman_label.configure(
                text="Kalman Filter Status: OFF",
                text_color="gray",
            )

    def _build_connection_block(self, parent):
        section = CTkFrame(parent, fg_color=self.style.color("widget"))
        section.pack(fill="x", padx=self.style.igap, pady=self.style.igap)

        CTkLabel(section, text="SERVER URL", font=self.style.get_font()).pack(
            anchor="w", padx=self.style.igap, pady=self.style.gaptop
        )
        self._url_entry = CTkEntry(section, font=self.style.get_font(),
                                   placeholder_text="http://192.168.8.141")
        self._url_entry.pack(fill="x", padx=self.style.igap, pady=(self.style.igap, 4))
        self._url_entry.insert(0, "http://192.168.4.1")

        CTkButton(section, text="Connect", font=self.style.get_font(),
                  command=self._poll).pack(fill="x", padx=self.style.igap, pady=(0, 4))

        self._conn_status = CTkLabel(section, text="⬤  Not connected",
                                     font=self.style.get_font(), text_color="gray")
        self._conn_status.pack(anchor="w", padx=self.style.igap, pady=self.style.gapbot)

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
                    popup.message(self, self.context, "Please enter an encryption key before enabling encryption.")
                elif not str.isascii(self._enc_key_entry.get().strip()):
                    # Non-ASCII key — show error
                    popup.message(self, self.context, "Encryption key must be ASCII.")
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

    def _build_mode_block(self, parent):
        section = CTkFrame(parent, fg_color=self.style.color("widget"))
        section.pack(fill="x", padx=self.style.igap, pady=self.style.igap)

        CTkLabel(section, text="OPERATION MODE", font=self.style.get_font()).pack(
            anchor="w", padx=self.style.igap, pady=(self.style.igap, 0)
        )

        # Read-only — this just reflects whatever submarine_mode AP_ESP32.ino
        # is currently reporting. Mode is changed on the AP itself, not here.
        self._mode_label = CTkLabel(section, text="Mode: SUBMARINE",
                                    font=self.style.get_font(), text_color="green")
        self._mode_label.pack(anchor="w", padx=self.style.igap, pady=self.style.gapbot)

    def _refresh_mode_ui(self):
        if not hasattr(self, '_mode_label'):
            return
        try:
            if self._submarine_mode:
                self._mode_label.configure(text="Mode: SUBMARINE", text_color="green")
                self._hvac_view.hide()
                self._hvac_middle.pack_forget()

                self._submarine_left.pack(fill="x")
                self._submarine_middle.pack(fill="both", expand=True)
                self._map_container.pack(fill="both", expand=True)
            else:
                self._mode_label.configure(text="Mode: HVAC", text_color="orange")
                self._submarine_left.pack_forget()
                self._submarine_middle.pack_forget()
                self._map_container.pack_forget()

                self._hvac_view.show()
                self._hvac_middle.pack(fill="both", expand=True)
        except Exception as e:
            print("refresh_mode_ui:", e)

    def _build_values_block(self, parent):
        """Client values card and Server values card, side by side."""
        outer = CTkFrame(parent, fg_color="transparent")
        outer.pack(fill="x", padx=self.style.igap, pady=self.style.igap)
        outer.grid_columnconfigure(0, weight=1)
        outer.grid_columnconfigure(1, weight=1)

        fields = ["x", "y", "theta", "speed", "rudder"]
        self._val_labels = {"client": {}, "server": {}}

        for col, source in enumerate(["client", "server"]):
            card = CTkFrame(outer, fg_color=self.style.color("widget"))
            card.grid(row=0, column=col, padx=4, sticky="nsew")

            CTkLabel(card, text=f"{source.capitalize()} Values",
                     font=self.style.get_font()).pack(
                anchor="w", padx=self.style.igap, pady=(self.style.igap, 4)
            )

            for field in fields:
                row_frame = CTkFrame(card, fg_color="transparent")
                row_frame.pack(fill="x", padx=self.style.igap, pady=1)

                CTkLabel(row_frame, text=f"{field} =",
                         font=self.style.get_font("small"), text_color="gray",
                         width=60, anchor="w").pack(side="left")

                lbl = CTkLabel(row_frame, text="—",
                               font=self.style.get_font("small"), anchor="w")
                lbl.pack(side="left", fill="x", expand=True)
                self._val_labels[source][field] = lbl

            CTkFrame(card, fg_color="transparent", height=self.style.igap).pack()

    def _build_packet_log(self, parent):
        """Header with CLIENT | SERVER segmented toggle, then scrollable rows."""
        header_frame = CTkFrame(parent, fg_color=self.style.color("widget"))
        header_frame.pack(fill="x", padx=self.style.igap, pady=(self.style.igap, 0))

        title_row = CTkFrame(header_frame, fg_color="transparent")
        title_row.pack(fill="x", padx=self.style.igap, pady=self.style.igap)

        CTkLabel(title_row, text="PACKET LOG  (last 10)",
                 font=self.style.get_font()).pack(side="left")

        self._log_toggle = CTkSegmentedButton(
            title_row,
            values=["CLIENT", "SERVER"],
            command=self._on_log_source_change,
            font=self.style.get_font("small"),
        )
        self._log_toggle.set("CLIENT")
        self._log_toggle.pack(side="right")

        cols = ["Time", "X (m)", "Y (m)", "Theta", "Speed", "Rudder", "Uptime (s)"]
        col_frame = CTkFrame(parent, fg_color=self.style.color("panel"))
        col_frame.pack(fill="x", padx=self.style.igap)
        for i, col in enumerate(cols):
            CTkLabel(col_frame, text=col, font=self.style.get_font("small"),
                     text_color="gray").grid(row=0, column=i, padx=6, pady=4, sticky="w")
            col_frame.grid_columnconfigure(i, weight=1)

        self._log_frame = Scrollable(parent, self.context, 240, "x", False)
        for i in range(len(cols)):
            self._log_frame.grid_columnconfigure(i, weight=1)

        self._log_rows = []

    def _build_flags_block(self, parent, title, defs, label_attr):
        section = CTkFrame(parent, fg_color=self.style.color("widget"))
        section.pack(fill="x", padx=self.style.igap, pady=(0, self.style.igap))

        CTkLabel(section, text=title,font=self.style.get_font()).pack(
            anchor="w", padx=self.style.igap, pady=(self.style.igap, 4)
        )

        labels = {}
        for key, label_text in defs:
            row = CTkFrame(section, fg_color="transparent")
            row.pack(fill="x", padx=self.style.igap, pady=2)

            dot = CTkLabel(row, text="●", font=self.style.get_font("small"),
                        text_color="gray", width=20)
            dot.pack(side="left")

            CTkLabel(row, text=label_text,
                    font=self.style.get_font("small"), anchor="w").pack(
                side="left", fill="x", expand=True
            )
            labels[key] = dot

        setattr(self, label_attr, labels)
        CTkFrame(section, fg_color="transparent", height=self.style.igap).pack()

    def _build_slider_block(self, parent):
        section = CTkFrame(parent, fg_color=self.style.color("widget"))
        section.pack(fill="x", padx=self.style.igap, pady=self.style.igap)

        CTkLabel(
            section,
            text="SUBMARINE SETTINGS",
            font=self.style.get_font()
        ).pack(anchor="w", padx=self.style.igap, pady=(self.style.igap, 8))

        slider_defs = [
            ("Sensor Noise Variance", 0.0, 20, 8.3, "sensor_noise_variance", 2),
            ("Kalman Expected Sensor Variance", 0.0, 20, 8.3, "kalman_expected_sensor_variance", 2),
            ("Rudder Error Threshold", 0.0, 10, 2.75, "rudder_error_threshold", 1),
            ("Speed Error Threshold", 0.0, 10, 2.0, "speed_error_threshold", 1),
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

                # Only POST when the USER moved the slider.
                if not self._syncing_sliders:
                    self._post_slider_settings()
                
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

    def _post_slider_settings(self):
        payload = {
            "sensor_noise_variance": self.sensor_noise_variance,
            "kalman_expected_sensor_variance": self.kalman_expected_sensor_variance,
            "rudder_error_threshold": self.rudder_error_threshold,
            "speed_error_threshold": self.speed_error_threshold,
            "kalman_filter_enabled": self._submarine_kalman_filter_enabled,
        }

        def _request():
            try:
                resp = requests.post(
                    f"{self._get_url()}/set_settings",
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

    def _sync_submarine_sliders(self, data: dict):
        client_revision = int(
            data.get("client_settings_revision", 0)
        )

        server_revision = int(
            data.get("server_settings_revision", 0)
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
                data.get("sensor_noise_variance"),

            "Kalman Expected Sensor Variance":
                data.get("kalman_expected_sensor_variance"),

            "Rudder Error Threshold":
                data.get("rudder_error_threshold"),

            "Speed Error Threshold":
                data.get("speed_error_threshold"),
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
                slider.set(value)

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

                    label.configure(
                        text=f"{value:.{decimals}f}"
                    )

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

        # Prevent each slider.set() from generating its own POST
        self._syncing_sliders = True

        try:
            for title, (value, attr, decimals) in defaults.items():

                # Update Python variable
                setattr(self, attr, value)

                # Move slider
                self._sliders[title].set(value)

                # Update displayed number
                self._slider_value_labels[title].configure(
                    text=f"{value:.{decimals}f}"
                )

        finally:
            self._syncing_sliders = False

        self._post_slider_settings()

    # ════════════════════════════════════════════════════════════════════════
    #  Network actions
    # ════════════════════════════════════════════════════════════════════════

    def _get_url(self) -> str:
        return self._url_entry.get().strip().rstrip("/") or self._server_url

    def _toggle_encryption(self):
        new_state = not self._encryption_on
        enc_key   = self._enc_key_entry.get().strip()

        def _request():      
            try:
                resp = requests.post(
                    f"{self._get_url()}/set_encryption",
                    json={"encryption_status": new_state, "encryption_key": enc_key},
                    timeout=3,
                )
                if resp.ok:
                    self._encryption_on = new_state
                    self.after(0, self._refresh_encryption_ui)
            except Exception:
                pass

        threading.Thread(target=_request, daemon=True).start()

    def _toggle_AP_communication(self):
        new_state = not self._AP_communication_on

        def _request():
            try:
                resp = requests.post(
                    f"{self._get_url()}/set_AP_communication",
                    json={"AP_communication": new_state},
                    timeout=3,
                )
                if resp.ok:
                    self._AP_communication_on = new_state
                    self.after(0, self._refresh_AP_communication_ui)
            except Exception:
                pass

        threading.Thread(target=_request, daemon=True).start()

    def _refresh_AP_communication_ui(self):
        try:
            if self._AP_communication_on:
                self._filter_label.configure(text="Status: ON", text_color="green")
                self._filter_button.configure(text="Disable Communication Through AP")
            else:
                self._filter_label.configure(text="Status: OFF", text_color="gray")
                self._filter_button.configure(text="Enable Communication Through AP")
        except Exception as e:
            print("refresh_AP_communication_ui:", e)

    def _poll(self):
        '''
        Registers the AP polling tick with the shared animation_manager instead
        of a raw self-rescheduling self.after() chain, so a destroyed frame or a
        raising callback can't leave an un-stoppable loop running, and so it's
        cleaned up automatically on page exit/refresh. animation_manager ticks
        every callback at its own fixed (much faster) rate, so poll_tick
        throttles itself internally to still only actually poll every
        POLL_INTERVAL_MS - without this it would fire an HTTP request/thread on
        every animation tick instead of every 2 seconds.
        '''
        last_poll_time = 0.0

        def _request():
            try:
                resp = requests.get(f"{self._get_url()}/api/data", timeout=3)
                if resp.ok:
                    data = resp.json()
                    self.after(0, lambda: self._on_data(data))
                    self.after(0, self._set_connected)
                else:
                    self.after(0, self._set_disconnected)
            except Exception:
                self.after(0, self._set_disconnected)

        def poll_tick():
            nonlocal last_poll_time
            now = time.monotonic()
            if now - last_poll_time < self.POLL_INTERVAL_MS / 1000.0:
                return
            last_poll_time = now
            threading.Thread(target=_request, daemon=True).start()

        self.context.animation_manager.add_callback(f"DefenderPoll_{id(self)}", poll_tick)

    def _on_log_source_change(self, value: str):
        self._log_source = value.lower()
        active = self._last_points.get(self._log_source, [])
        self._update_log(list(reversed(active[-10:])))

    def _toggle_submarine_kalman_filter(self):
        self._submarine_kalman_filter_enabled = (
            not self._submarine_kalman_filter_enabled
        )

        if self._submarine_kalman_filter_enabled:
            self._submarine_kalman_label.configure(
                text="Kalman Filter Status: ON",
                text_color="green",
            )
        else:
            self._submarine_kalman_label.configure(
                text="Kalman Filter Status: OFF",
                text_color="gray",
            )

        self._post_slider_settings()

    # ════════════════════════════════════════════════════════════════════════
    #  UI update helpers
    # ════════════════════════════════════════════════════════════════════════

    def _on_data(self, data: dict):
        self._encryption_on = data.get("encryption_status", False)
        self._refresh_encryption_ui()

        incoming_mode = data.get("submarine_mode", True)
        
        if incoming_mode != self._submarine_mode:
            self._submarine_mode = incoming_mode
            self._refresh_mode_ui()

        if self._submarine_mode:
            self._sync_submarine_sliders(data)

        if not self._submarine_mode:
            # HVAC mode — Submarine widgets are hidden, only the HVAC view
            # needs this poll's data (current_temp / target_temp / heater_on)
            self._hvac_view.update(data)
            self._HVAC_flags["HVAC_filter_flag"] = self._hvac_view.get_hvac_anomaly()
            self._refresh_flags()
            return

        # Flask returns separate lists; fall back to combined "points" if the
        # server hasn't been updated yet (backwards compatible)
        client_points = data.get("client_points", data.get("points", []))
        server_points = data.get("server_points", [])
        self._last_points = {"client": client_points, "server": server_points}

        # Value cards
        self._update_value_card("client", client_points)
        self._update_value_card("server", server_points)

        # Packet log — whichever source the toggle is set to
        active = client_points if self._log_source == "client" else server_points
        self._update_log(list(reversed(active[-10:])))

        # Map — always driven by client positions
        if client_points:
            self._positions = [(float(p["x"]), float(p.get("y", 0.0))) for p in client_points]
            if len(self._positions) >= 2:
                dx = self._positions[-1][0] - self._positions[-2][0]
                dy = self._positions[-1][1] - self._positions[-2][1]
                self._last_bearing = math.atan2(dy, dx)
            else:
                self._last_bearing = None

        if server_points:
            latest_server = server_points[-1]
            self._submarine_flags["state_filter_flag"] = bool(latest_server.get("state_anomaly_detected", False))

        if client_points:
            latest_client = client_points[-1]
            self._submarine_flags["speed_filter_flag"] = bool(latest_client.get("speed_anomaly_detected", False))
            self._submarine_flags["rudder_filter_flag"] = bool(latest_client.get("rudder_anomaly_detected", False))

        self._refresh_flags()

    def _update_value_card(self, source: str, points: list):
        if not points:
            return
        latest = points[-1]
        for field in ["x", "y", "theta", "speed", "rudder"]:
            raw = latest.get(field, "—")
            try:
                text = f"{float(raw):.3f}"
            except (ValueError, TypeError):
                text = str(raw)
            self._val_labels[source][field].configure(text=text)

    def _update_log(self, rows: list):
        cols  = ["received_at", "x", "y", "theta", "speed", "rudder", "timestamp"]

        for widget in self._log_frame.winfo_children():
            widget.destroy()
        self._log_rows = []

        for r_idx, packet in enumerate(rows):
            row_labels = []
            bg = self.style.color("widget") if r_idx % 2 == 0 else self.style.color("panel")
            for c_idx, key in enumerate(cols):
                raw = packet.get(key, "—")
                if key == "received_at":
                    raw_str = str(raw)
                    # Handle both Flask datetime strings ("2024-01-01 12:34:56")
                    # and AP ESP32 uptime strings ("100", "3661")
                    if len(raw_str) > 10:
                        text = raw_str[11:19]   # Flask datetime format
                    else:
                        # Convert raw seconds to HH:MM:SS
                        secs = int(raw_str)
                        text = f"{secs//3600:02d}:{(secs%3600)//60:02d}:{secs%60:02d}"
                elif key == "timestamp":
                    text = str(raw)
                else:
                    try:
                        text = f"{float(raw):.4f}"
                    except (ValueError, TypeError):
                        text = str(raw)

                lbl = CTkLabel(self._log_frame, text=text,
                               font=self.style.get_font("small"),
                               fg_color=bg, anchor="w")
                lbl.grid(row=r_idx, column=c_idx, padx=4, pady=1, sticky="ew")
                row_labels.append(lbl)
            self._log_rows.append(row_labels)


    def _refresh_encryption_ui(self):
        try:
            if self._encryption_on:
                self._enc_label.configure(
                    text="Status: ON",
                    text_color="green"
                )
                self._enc_button.configure(
                    text="Disable Encryption"
                )
            else:
                self._enc_label.configure(
                    text="Status: OFF",
                    text_color="gray"
                )
                self._enc_button.configure(
                    text="Enable Encryption"
                )
        except Exception as e:
            print("refresh_encryption_ui:", e)

    def _refresh_flags(self):
        for labels, flags in (
            (getattr(self, "_submarine_flag_labels", {}), self._submarine_flags),
            (getattr(self, "_hvac_flag_labels", {}), self._HVAC_flags),
        ):
            for key, dot in labels.items():
                dot.configure(text_color="red" if flags.get(key, False) else "gray")

    def _set_connected(self):
        try:
            self._conn_status.configure(
                text="⬤  Connected",
                text_color="green"
            )
        except Exception as e:
            print("set_connected:", e)

    def _set_disconnected(self):
        try:
            self._conn_status.configure(
                text="⬤  Disconnected",
                text_color="red"
            )
        except Exception as e:
            print("set_disconnected:", e)