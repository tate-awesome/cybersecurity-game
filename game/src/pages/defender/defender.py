from ...app_core.context import Context

# Widgets
from ...widgets import Trifold, MenuBar
from ...widgets import common, popup
from ...widgets.map import Map
from ...drawing.viewport import ViewPort
from ...app_core.context import Context
from ..page import Page

# Network
from ...network.network_controller import HardwareDefender

# customtkinter widgets
from customtkinter import (
    CTkLabel, CTkEntry, CTkButton, CTkFrame,
    CTkScrollableFrame, CTkSegmentedButton
)

import threading
import requests
import math


class DefenderV0(Page):
    '''
    Page constructor for defender/defenderv0. Inherits CTkFrame
    '''

    POLL_INTERVAL_MS = 2000

    # Flag definitions — (key, display label).
    # Set the corresponding key to True in self._flags to light it up.
    FLAG_DEFS = [
        ("unexpected_movement",       "Server Detects Irrational Movement"),
        ("bicycle_verification",      "Submarine Detects Irrational Movement")
    ]

    def __init__(self, context: Context):
        super().__init__(context)
        context.refresh_net(HardwareDefender)
        # TODO use net for lifetime management   = context.refresh_net(HardwareDefender)

        # ── Internal state FIRST (map callback fires immediately) ────────────
        self._server_url    = "http://192.168.8.141/api/data"
        self._positions     = []
        self._last_bearing  = None
        self._encryption_on = False
        self._last_seq      = -1
        self._log_source    = "client"   # "client" or "server"
        self._last_points   = {"client": [], "server": []}

        # Filtering State Variables
        self._last_theta = None
        self._last_speed = None
        self._speed_threshold = 3
        self._rudder_threshold = 15

        self._k_speed_estimate = 0
        self._k_speed_cov = 5
        self._k_speed_process_noise = 0.05
        self._k_speed_measurement_noise = 0.1

        self._k_rudder_estimate = 0
        self._k_rudder_cov = 5
        self._k_rudder_process_noise = 2
        self._k_rudder_measurement_noise = 1

        self._target_x = 100
        self._target_y = 100

        # Anomaly GUI variables
        self._anomaly_speed_expected = 0.0
        self._anomaly_speed_measured = 0.0
        self._anomaly_rudder_expected = 0.0
        self._anomaly_rudder_measured = 0.0

        # Bicycle verification GUI variables
        self._bicycle_speed_expected = 0.0
        self._bicycle_speed_measured = 0.0
        self._bicycle_rudder_expected = 0.0
        self._bicycle_rudder_measured = 0.0

        # Flag state — all False until logic sets them
        self._flags = {key: False for key, _ in self.FLAG_DEFS}

        # ── Menu bar ─────────────────────────────────────────────────────────
        menu_bar = MenuBar(self, context, "Defender V0")
        menu_bar.all_buttons()

        # ── Three-pane layout ────────────────────────────────────────────────
        trifold = Trifold(self, context)
        left_p = common.scrollable(trifold.left, context)
        middle_p = trifold.middle
        right_p = trifold.right

        # ── Left pane ────────────────────────────────────────────────────────
        self._build_connection_block(left_p)
        self._build_encryption_block(left_p)
        self._build_target_block(left_p)
        self._build_values_block(left_p)
        common.scroll_deadspace(left_p, context)

        # ── Middle pane ──────────────────────────────────────────────────────
        self._build_packet_log(middle_p)
        self._build_flags_block(middle_p)

        self._map_scale  = None
        self._map_offset = None
        self._map_click_xy = None

        # ── Right pane — live map ─────────────────────────────────────────────
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

        self._map = Map(right_p, context, draw_defender_map,
                        framerate_ms=self.POLL_INTERVAL_MS, padding=20)
        #self._map.canvas.bind("<Button-1>", self._on_map_click)

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
        self._url_entry.insert(0, "http://192.168.8.141")

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

    def _build_target_block(self, parent):
        section = CTkFrame(parent, fg_color=self.style.color("widget"))
        section.pack(fill="x", padx=self.style.igap, pady=self.style.igap)

        CTkLabel(section, text="TARGET POSITION", font=self.style.get_font()).pack(
            anchor="w", padx=self.style.igap, pady=self.style.gaptop
        )
        self._target_status = CTkLabel(section, text="Status: Not set",
                                       font=self.style.get_font(), text_color="gray")
        self._target_status.pack(anchor="w", padx=self.style.igap)

        # X entry
        CTkLabel(section, text="X Target", font=self.style.get_font("small"),
                 text_color="gray").pack(anchor="w", padx=self.style.igap, pady=self.style.gaptop)
        self._target_x_entry = CTkEntry(section, font=self.style.get_font(),
                                        placeholder_text="Enter X…")
        self._target_x_entry.pack(fill="x", padx=self.style.igap, pady=(2, 4))

        # Y entry
        CTkLabel(section, text="Y Target", font=self.style.get_font("small"),
                 text_color="gray").pack(anchor="w", padx=self.style.igap, pady=self.style.nogap)
        self._target_y_entry = CTkEntry(section, font=self.style.get_font(),
                                        placeholder_text="Enter Y…")
        self._target_y_entry.pack(fill="x", padx=self.style.igap, pady=(2, 4))

        CTkButton(section, text="Set Target Position", font=self.style.get_font(),
                  command=self._send_target).pack(
            fill="x", padx=self.style.igap, pady=self.style.gapbot
        )

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

        self._log_frame = CTkScrollableFrame(parent, fg_color=self.style.color("panel"), height=240)
        self._log_frame.pack(fill="x", padx=self.style.igap, pady=(0, self.style.igap))
        common.bind_scroll(self._log_frame)
        for i in range(len(cols)):
            self._log_frame.grid_columnconfigure(i, weight=1)

        self._log_rows = []

    def _build_flags_block(self, parent):
        """Flags panel — dots light red when a flag is set."""
        section = CTkFrame(parent, fg_color=self.style.color("widget"))
        section.pack(fill="x", padx=self.style.igap, pady=(0, self.style.igap))

        CTkLabel(section, text="FLAGS", font=self.style.get_font()).pack(
            anchor="w", padx=self.style.igap, pady=(self.style.igap, 4)
        )

        self._flag_labels = {}
        for key, label_text in self.FLAG_DEFS:
            row = CTkFrame(section, fg_color="transparent")
            row.pack(fill="x", padx=self.style.igap, pady=2)

            dot = CTkLabel(row, text="●", font=self.style.get_font("small"),
                           text_color="gray", width=20)
            dot.pack(side="left")

            CTkLabel(row, text=label_text,
                     font=self.style.get_font("small"), anchor="w").pack(
                side="left", fill="x", expand=True
            )
            self._flag_labels[key] = dot

            if key == "unexpected_movement":
                self._speed_expected_lbl = CTkLabel(
                    section,
                    text="Expected Speed: --",
                    font=self.style.get_font("small"),
                    anchor="w"
                )
                self._speed_expected_lbl.pack(fill="x", padx=self.style.igap)

                self._speed_measured_lbl = CTkLabel(
                    section,
                    text="Measured Speed: --",
                    font=self.style.get_font("small"),
                    anchor="w"
                )
                self._speed_measured_lbl.pack(fill="x", padx=self.style.igap)

                self._rudder_expected_lbl = CTkLabel(
                    section,
                    text="Expected Rudder: --",
                    font=self.style.get_font("small"),
                    anchor="w"
                )
                self._rudder_expected_lbl.pack(fill="x", padx=self.style.igap)

                self._rudder_measured_lbl = CTkLabel(
                    section,
                    text="Measured Rudder: --",
                    font=self.style.get_font("small"),
                    anchor="w"
                )
                self._rudder_measured_lbl.pack(fill="x", padx=self.style.igap)
            
            if key == "bicycle_verification":
                self._bicycle_speed_expected_lbl = CTkLabel(
                    section, text="Bicycle Expected Speed: --",
                    font=self.style.get_font("small"), anchor="w"
                )
                self._bicycle_speed_expected_lbl.pack(fill="x", padx=self.style.igap)

                self._bicycle_speed_measured_lbl = CTkLabel(
                    section, text="Bicycle Measured Speed: --",
                    font=self.style.get_font("small"), anchor="w"
                )
                self._bicycle_speed_measured_lbl.pack(fill="x", padx=self.style.igap)

                self._bicycle_rudder_expected_lbl = CTkLabel(
                    section, text="Bicycle Expected Rudder: --",
                    font=self.style.get_font("small"), anchor="w"
                )
                self._bicycle_rudder_expected_lbl.pack(fill="x", padx=self.style.igap)

                self._bicycle_rudder_measured_lbl = CTkLabel(
                    section, text="Bicycle Measured Rudder: --",
                    font=self.style.get_font("small"), anchor="w"
                )
                self._bicycle_rudder_measured_lbl.pack(fill="x", padx=self.style.igap)

        CTkFrame(section, fg_color="transparent", height=self.style.igap).pack()

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

    def _send_target(self):
        raw_x = self._target_x_entry.get().strip()
        raw_y = self._target_y_entry.get().strip()

        try:
            target_x = float(raw_x)
            target_y = float(raw_y)

            if not(0 <= target_x <= 200 and 0 <= target_y <= 200):
                self.after(0, lambda: self._target_status.configure(
                    text="Status: Invalid input", text_color="red"
                ))
                popup.message(self, self.context, "The target X and target Y field must both be filled with values between 0 and 200")
                return
        
            self._target_x = target_x
            self._target_y = target_y
        except ValueError:
            self.after(0, lambda: self._target_status.configure(
                text="Status: Invalid input", text_color="red"
            ))
            popup.message(self, self.context, "The target X and target Y field must both be filled with values between 0 and 200")
            return

        def _request():
            try:
                resp = requests.post(
                    f"{self._get_url()}/set_target",
                    json={"target_x": target_x, "target_y": target_y},
                    timeout=3,
                )
                if resp.ok:
                    self.after(0, lambda: self._target_status.configure(
                        text=f"Status: Set to ({target_x:.1f}, {target_y:.1f})",
                        text_color="green"
                    ))
                else:
                    self.after(0, lambda: self._target_status.configure(
                        text=f"Status: Server error {resp.status_code}",
                        text_color="red"
                    ))
            except Exception:
                self.after(0, lambda: self._target_status.configure(
                    text="Status: Connection failed", text_color="red"
                ))

        threading.Thread(target=_request, daemon=True).start()

    def _poll(self):
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

        threading.Thread(target=_request, daemon=True).start()
        self.after(self.POLL_INTERVAL_MS, self._poll)

    def _on_log_source_change(self, value: str):
        self._log_source = value.lower()
        active = self._last_points.get(self._log_source, [])
        self._update_log(list(reversed(active[-10:])))

    def _k_update(self, measured_speed, measured_rudder):

        anomaly = False

        # --- SPEED ---
        speed_pred = self._k_speed_estimate
        speed_cov_pred = self._k_speed_cov + self._k_speed_process_noise

        k_speed = speed_cov_pred / (speed_cov_pred + self._k_speed_measurement_noise)

        self._k_speed_estimate = speed_pred + k_speed * (measured_speed - speed_pred)
        self._k_speed_cov = (1 - k_speed) * speed_cov_pred

        # --- RUDDER ---
        rudder_pred = self._k_rudder_estimate
        rudder_cov_pred = self._k_rudder_cov + self._k_rudder_process_noise

        k_rudder = rudder_cov_pred / (rudder_cov_pred + self._k_rudder_measurement_noise)

        self._k_rudder_estimate = rudder_pred + k_rudder * (measured_rudder - rudder_pred)
        self._k_rudder_cov = (1 - k_rudder) * rudder_cov_pred

        if (abs(measured_speed - self._k_speed_estimate) > self._speed_threshold):
            anomaly = True
        
        if (abs(measured_rudder - self._k_rudder_estimate) > self._rudder_threshold):
            anomaly = True

        return self._k_speed_estimate, self._k_rudder_estimate, anomaly
    
    @staticmethod
    def wrap_to_pi(angle):
        while angle > math.pi:
            angle -= 2.0 * math.pi

        while angle < -math.pi:
            angle += 2.0 * math.pi

        return angle

    @staticmethod
    def clamp(value, min_val, max_val):
        return max(min_val, min(value, max_val))
    
    def _bicycle_verification (self, boat_x, boat_y, boat_theta, target_x, target_y, measured_speed, measured_rudder):
        heading_x = boat_x + (2*math.cos(boat_theta))
        heading_y = boat_y + (2*math.sin(boat_theta))
        error_x = target_x - heading_x
        error_y = target_y - heading_y

        destination_theta = math.atan2(error_y, error_x)
        
        heading_error = self.wrap_to_pi(destination_theta - boat_theta)
        bicycle_expected_rudder_rad = 0.1*heading_error

        magnitude = math.pi/3
        bicycle_expected_rudder_rad = self.clamp(bicycle_expected_rudder_rad, -magnitude, magnitude)

        center_distance = math.sqrt(error_x**2 + error_y**2)

        if center_distance < 5:
            bicycle_expected_speed = 0
            bicycle_expected_rudder_rad = 0
        else:
            bicycle_expected_speed = self.clamp(0.1*center_distance, 0, 50)

        anomaly = False
        bicycle_expected_rudder = math.degrees(bicycle_expected_rudder_rad)

        if(abs(measured_rudder - bicycle_expected_rudder) > self._rudder_threshold):
            anomaly = True
        if(abs(measured_speed - bicycle_expected_speed) > self._speed_threshold):
            anomaly = True

        return bicycle_expected_speed, bicycle_expected_rudder, anomaly

    # ════════════════════════════════════════════════════════════════════════
    #  UI update helpers
    # ════════════════════════════════════════════════════════════════════════

    def _on_data(self, data: dict):
        self._encryption_on = data.get("encryption_status", False)
        self._refresh_encryption_ui()

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
            latest = client_points[-1]

            measured_speed = latest.get("speed", 0.0)
            measured_rudder = latest.get("rudder", 0.0)
            boat_x = latest.get("x", 0.0)
            boat_y = latest.get("y", 0.0)
            boat_theta = latest.get("theta", 0.0)
            try:
                measured_speed = float(measured_speed)
                measured_rudder = float(measured_rudder)
                boat_x = float(boat_x)
                boat_y = float(boat_y)
                boat_theta = float(boat_theta)
            except (ValueError, TypeError):
                measured_speed = 0.0
                measured_rudder = 0.0
                boat_x = 0.0
                boat_y = 0.0
                boat_theta = 0.0

            filtered_speed, filtered_rudder, flag = self._k_update(
                measured_speed,
                measured_rudder
            )

            self._anomaly_speed_expected = filtered_speed
            self._anomaly_speed_measured = measured_speed

            self._anomaly_rudder_expected = filtered_rudder
            self._anomaly_rudder_measured = measured_rudder

            self._flags["unexpected_movement"] = flag
            
            # optionally overwrite latest values for UI consistency
            latest["speed_filtered"] = filtered_speed
            latest["rudder_filtered"] = filtered_rudder

            bicycle_expected_speed, bicycle_expected_rudder, bicycle_flag = self._bicycle_verification(boat_x, 
                                                                                                       boat_y, 
                                                                                                       boat_theta, 
                                                                                                       self._target_x,
                                                                                                       self._target_y, 
                                                                                                       measured_speed, 
                                                                                                       measured_rudder)
            
            self._flags["bicycle_verification"] = bicycle_flag
            self._bicycle_speed_expected = bicycle_expected_speed
            self._bicycle_speed_measured = measured_speed
            self._bicycle_rudder_expected = bicycle_expected_rudder
            self._bicycle_rudder_measured = measured_rudder

            # With this (no seq check):
            self._positions = [(float(p["x"]), float(p.get("y", 0.0))) for p in client_points]
            if len(self._positions) >= 2:
                dx = self._positions[-1][0] - self._positions[-2][0]
                dy = self._positions[-1][1] - self._positions[-2][1]
                speed = math.sqrt((dx*dx) + (dy*dy))
                self._flags["unexpected_movement"] = speed > 50
                self._last_bearing = math.atan2(dy, dx)
            else:
                self._last_bearing = None

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
        """Dots turn red when flag is True, gray when clear."""
        for key, dot in self._flag_labels.items():
            dot.configure(text_color="red" if self._flags.get(key) else "gray")
        
        self._speed_expected_lbl.configure(
            text=f"Expected Speed: {self._anomaly_speed_expected:.3f}"
        )
        self._speed_measured_lbl.configure(
            text=f"Measured Speed: {self._anomaly_speed_measured:.3f}"
        )

        self._rudder_expected_lbl.configure(
            text=f"Expected Rudder: {self._anomaly_rudder_expected:.3f}"
        )
        self._rudder_measured_lbl.configure(
            text=f"Measured Rudder: {self._anomaly_rudder_measured:.3f}"
        )

        self._bicycle_speed_expected_lbl.configure(
            text=f"Bicycle Expected Speed: {self._bicycle_speed_expected:.3f}"
        )
        self._bicycle_speed_measured_lbl.configure(
            text=f"Bicycle Measured Speed: {self._bicycle_speed_measured:.3f}"
        )
        self._bicycle_rudder_expected_lbl.configure(
            text=f"Bicycle Expected Rudder: {self._bicycle_rudder_expected:.3f}"
        )
        self._bicycle_rudder_measured_lbl.configure(
            text=f"Bicycle Measured Rudder: {self._bicycle_rudder_measured:.3f}"
        )

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

    # def _on_map_click(self, event):
    #         if self._map_scale is None or self._map_offset is None:
    #             return

    #         if not (0.0 <= world_x <= 200.0 and 0.0 <= world_y <= 200.0):
    #             return
    #         world_x = (event.x - self._map_offset[0]) / self._map_scale
    #         world_y = (event.y - self._map_offset[1]) / self._map_scale

            # Clamp to valid map range
            world_x = max(0.0, min(200.0, world_x))
            world_y = max(0.0, min(200.0, world_y))

    #         self._map_click_xy = (world_x, world_y)

    #         self._target_x_entry.delete(0, "end")
    #         self._target_x_entry.insert(0, f"{world_x:.1f}")
    #         self._target_y_entry.delete(0, "end")
    #         self._target_y_entry.insert(0, f"{world_y:.1f}")