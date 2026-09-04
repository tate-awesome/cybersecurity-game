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

# customtkinter widgets
from customtkinter import (
    CTkLabel, CTkEntry, CTkButton, CTkFrame,
    CTkScrollableFrame, CTkSegmentedButton, CTkSlider
)

import threading
import requests
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

        self._hvac_view = HVACView(self.style, self._mode_content_left, right_p, context)

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
        # HVAC's own Kalman Filter block lives entirely inside HVACView now
        # (see hvac_view.py's _build_kalman_block) - it owns the button, the
        # label, and the toggle state, so there's no callback threaded back
        # into this page just to update a label this class doesn't build.

        self._build_mode_block(middle_p)       # mode-agnostic — always visible
        self._refresh_mode_ui()

        self._post_slider_settings()

        self._map_container = CTkFrame(right_p, fg_color="transparent")
        self._map_container.pack(fill="both", expand=True)

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
        #self._map.canvas.bind("<Button-1>", self._on_map_click)

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
            if not self.context.buffer.defender_status.get("encryption_status", False):
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
                self._hvac_middle.pack_forget()

                self._submarine_left.pack(fill="x")
                self._submarine_middle.pack(fill="both", expand=True)
                self._map_container.pack(fill="both", expand=True)
            else:
                self._mode_label.configure(text="Mode: HVAC", text_color="orange")
                self._submarine_left.pack_forget()
                self._submarine_middle.pack_forget()
                self._map_container.pack_forget()

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

        cols = ["Time", "X (m)", "Y (m)", "Theta", "Speed", "Rudder"]
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
        # Falls back to the poller's own last-known URL (which defaults to
        # 192.168.4.1 itself) rather than a second hardcoded default here.
        return self._url_entry.get().strip().rstrip("/") or self._ap_poller.url

    def _toggle_encryption(self):
        new_state = not self.context.buffer.defender_status.get("encryption_status", False)
        enc_key   = self._enc_key_entry.get().strip()

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
                self._filter_label.configure(text="Status: ON", text_color="green")
                self._filter_button.configure(text="Disable Communication Through AP")
            else:
                self._filter_label.configure(text="Status: OFF", text_color="gray")
                self._filter_button.configure(text="Enable Communication Through AP")
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
            self._conn_status.configure(text="⬤  Connected", text_color="green")
        else:
            self._conn_status.configure(text="⬤  Disconnected", text_color="red")

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
            self._val_labels[source][field].configure(text=text)

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

        for widget in self._log_frame.winfo_children():
            widget.destroy()
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

                lbl = CTkLabel(self._log_frame, text=text,
                               font=self.style.get_font("small"),
                               fg_color=bg, anchor="w")
                lbl.grid(row=r_idx, column=c_idx, padx=4, pady=1, sticky="ew")
                row_labels.append(lbl)
            self._log_rows.append(row_labels)


    def _refresh_encryption_ui(self):
        try:
            if self.context.buffer.defender_status.get("encryption_status", False):
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
                dot.configure(text_color="red" if flags.get(key, False) else "gray")