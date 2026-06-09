from ...app_core.context import Context

# Widgets
from ...widgets.style import Style
from ...widgets import common, popup
from ...widgets.menu_bar import MenuBar
from ...widgets.map import Map
from ...drawing.viewport import ViewPort

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


class DefenderV0:

    POLL_INTERVAL_MS = 2000

    # Flag definitions — (key, display label).
    # Set the corresponding key to True in self._flags to light it up.
    FLAG_DEFS = [
        ("unexpected_movement",       "Unexpected movement"),
    ]

    def __init__(self, context: Context):
        root  = context.root
        style = Style(context)
        net   = context.refresh_net(HardwareDefender)

        # ── Internal state FIRST (map callback fires immediately) ────────────
        self._server_url    = "http://localhost:5000"
        self._positions     = []
        self._last_bearing  = None
        self._encryption_on = False
        self._last_seq      = -1
        self._log_source    = "client"   # "client" or "server"
        self._root          = root
        self._style         = style
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

        # Anomaly GUI variables
        self._anomaly_speed_expected = 0.0
        self._anomaly_speed_measured = 0.0
        self._anomaly_rudder_expected = 0.0
        self._anomaly_rudder_measured = 0.0

        # Flag state — all False until logic sets them
        self._flags = {key: False for key, _ in self.FLAG_DEFS}

        # ── Menu bar ─────────────────────────────────────────────────────────
        MenuBar(style, root, "Defender V0", context)

        # ── Three-pane layout ────────────────────────────────────────────────
        left, middle_p, right_p = common.trifold(style, root)
        left_p = common.scrollable(style, left)

        # ── Left pane ────────────────────────────────────────────────────────
        self._build_connection_block(style, left_p)
        self._build_encryption_block(style, left_p)
        self._build_target_block(style, left_p)
        self._build_values_block(style, left_p)
        common.scroll_deadspace(style, left_p)

        # ── Middle pane ──────────────────────────────────────────────────────
        self._build_packet_log(style, middle_p)
        self._build_flags_block(style, middle_p)

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

        self._map = Map(style, right_p, draw_defender_map,
                        framerate_ms=self.POLL_INTERVAL_MS, padding=20)
        #self._map.canvas.bind("<Button-1>", self._on_map_click)

        # ── Start polling ────────────────────────────────────────────────────
        self._poll()

    # ════════════════════════════════════════════════════════════════════════
    #  UI builder helpers
    # ════════════════════════════════════════════════════════════════════════

    def _build_connection_block(self, style, parent):
        section = CTkFrame(parent, fg_color=style.color("widget"))
        section.pack(fill="x", padx=style.igap, pady=style.igap)

        CTkLabel(section, text="SERVER URL", font=style.get_font()).pack(
            anchor="w", padx=style.igap, pady=(style.igap, 0)
        )
        self._url_entry = CTkEntry(section, font=style.get_font(),
                                   placeholder_text="http://localhost:5000")
        self._url_entry.pack(fill="x", padx=style.igap, pady=(style.igap, 4))
        self._url_entry.insert(0, "http://localhost:5000")

        CTkButton(section, text="Connect", font=style.get_font(),
                  command=self._poll).pack(fill="x", padx=style.igap, pady=(0, 4))

        self._conn_status = CTkLabel(section, text="⬤  Not connected",
                                     font=style.get_font(), text_color="gray")
        self._conn_status.pack(anchor="w", padx=style.igap, pady=(0, style.igap))

    def _build_encryption_block(self, style, parent):
        section = CTkFrame(parent, fg_color=style.color("widget"))
        section.pack(fill="x", padx=style.igap, pady=style.igap)

        CTkLabel(section, text="ENCRYPTION", font=style.get_font()).pack(
            anchor="w", padx=style.igap, pady=(style.igap, 0)
        )
        self._enc_label = CTkLabel(section, text="Status: OFF",
                                   font=style.get_font(), text_color="gray")
        self._enc_label.pack(anchor="w", padx=style.igap)

        # Key entry
        CTkLabel(section, text="Encryption Key", font=style.get_font("small"),
                 text_color="gray").pack(anchor="w", padx=style.igap, pady=(style.igap, 0))
        self._enc_key_entry = CTkEntry(section, font=style.get_font(),
                                       placeholder_text="Enter key…")
        self._enc_key_entry.pack(fill="x", padx=style.igap, pady=(2, 4))

        self._enc_button = CTkButton(section, text="Enable Encryption",
                                     font=style.get_font(),
                                     command=self._toggle_encryption)
        self._enc_button.pack(fill="x", padx=style.igap, pady=(0, style.igap))

    def _build_target_block(self, style, parent):
        section = CTkFrame(parent, fg_color=style.color("widget"))
        section.pack(fill="x", padx=style.igap, pady=style.igap)

        CTkLabel(section, text="TARGET POSITION", font=style.get_font()).pack(
            anchor="w", padx=style.igap, pady=(style.igap, 0)
        )
        self._target_status = CTkLabel(section, text="Status: Not set",
                                       font=style.get_font(), text_color="gray")
        self._target_status.pack(anchor="w", padx=style.igap)

        # X entry
        CTkLabel(section, text="X Target", font=style.get_font("small"),
                 text_color="gray").pack(anchor="w", padx=style.igap, pady=(style.igap, 0))
        self._target_x_entry = CTkEntry(section, font=style.get_font(),
                                        placeholder_text="Enter X…")
        self._target_x_entry.pack(fill="x", padx=style.igap, pady=(2, 4))

        # Y entry
        CTkLabel(section, text="Y Target", font=style.get_font("small"),
                 text_color="gray").pack(anchor="w", padx=style.igap, pady=(0, 0))
        self._target_y_entry = CTkEntry(section, font=style.get_font(),
                                        placeholder_text="Enter Y…")
        self._target_y_entry.pack(fill="x", padx=style.igap, pady=(2, 4))

        CTkButton(section, text="Set Target Position", font=style.get_font(),
                  command=self._send_target).pack(
            fill="x", padx=style.igap, pady=(0, style.igap)
        )

    def _build_values_block(self, style, parent):
        """Client values card and Server values card, side by side."""
        outer = CTkFrame(parent, fg_color="transparent")
        outer.pack(fill="x", padx=style.igap, pady=style.igap)
        outer.grid_columnconfigure(0, weight=1)
        outer.grid_columnconfigure(1, weight=1)

        fields = ["x", "y", "theta", "speed", "rudder"]
        self._val_labels = {"client": {}, "server": {}}

        for col, source in enumerate(["client", "server"]):
            card = CTkFrame(outer, fg_color=style.color("widget"))
            card.grid(row=0, column=col, padx=4, sticky="nsew")

            CTkLabel(card, text=f"{source.capitalize()} Values",
                     font=style.get_font()).pack(
                anchor="w", padx=style.igap, pady=(style.igap, 4)
            )

            for field in fields:
                row_frame = CTkFrame(card, fg_color="transparent")
                row_frame.pack(fill="x", padx=style.igap, pady=1)

                CTkLabel(row_frame, text=f"{field} =",
                         font=style.get_font("small"), text_color="gray",
                         width=60, anchor="w").pack(side="left")

                lbl = CTkLabel(row_frame, text="—",
                               font=style.get_font("small"), anchor="w")
                lbl.pack(side="left", fill="x", expand=True)
                self._val_labels[source][field] = lbl

            CTkFrame(card, fg_color="transparent", height=style.igap).pack()

    def _build_packet_log(self, style, parent):
        """Header with CLIENT | SERVER segmented toggle, then scrollable rows."""
        header_frame = CTkFrame(parent, fg_color=style.color("widget"))
        header_frame.pack(fill="x", padx=style.igap, pady=(style.igap, 0))

        title_row = CTkFrame(header_frame, fg_color="transparent")
        title_row.pack(fill="x", padx=style.igap, pady=style.igap)

        CTkLabel(title_row, text="PACKET LOG  (last 10)",
                 font=style.get_font()).pack(side="left")

        self._log_toggle = CTkSegmentedButton(
            title_row,
            values=["CLIENT", "SERVER"],
            command=self._on_log_source_change,
            font=style.get_font("small"),
        )
        self._log_toggle.set("CLIENT")
        self._log_toggle.pack(side="right")

        cols = ["Time", "X (m)", "Y (m)", "Theta", "Speed", "Rudder", "Uptime (s)"]
        col_frame = CTkFrame(parent, fg_color=style.color("panel"))
        col_frame.pack(fill="x", padx=style.igap)
        for i, col in enumerate(cols):
            CTkLabel(col_frame, text=col, font=style.get_font("small"),
                     text_color="gray").grid(row=0, column=i, padx=6, pady=4, sticky="w")
            col_frame.grid_columnconfigure(i, weight=1)

        self._log_frame = CTkScrollableFrame(parent, fg_color=style.color("panel"), height=240)
        self._log_frame.pack(fill="x", padx=style.igap, pady=(0, style.igap))
        common.bind_scroll(self._log_frame)
        for i in range(len(cols)):
            self._log_frame.grid_columnconfigure(i, weight=1)

        self._log_rows = []

    def _build_flags_block(self, style, parent):
        """Flags panel — dots light red when a flag is set."""
        section = CTkFrame(parent, fg_color=style.color("widget"))
        section.pack(fill="x", padx=style.igap, pady=(0, style.igap))

        CTkLabel(section, text="FLAGS", font=style.get_font()).pack(
            anchor="w", padx=style.igap, pady=(style.igap, 4)
        )

        self._flag_labels = {}
        for key, label_text in self.FLAG_DEFS:
            row = CTkFrame(section, fg_color="transparent")
            row.pack(fill="x", padx=style.igap, pady=2)

            dot = CTkLabel(row, text="●", font=style.get_font("small"),
                           text_color="gray", width=20)
            dot.pack(side="left")

            CTkLabel(row, text=label_text,
                     font=style.get_font("small"), anchor="w").pack(
                side="left", fill="x", expand=True
            )
            self._flag_labels[key] = dot

            if key == "unexpected_movement":
                self._speed_expected_lbl = CTkLabel(
                    section,
                    text="Expected Speed: --",
                    font=style.get_font("small"),
                    anchor="w"
                )
                self._speed_expected_lbl.pack(fill="x", padx=style.igap)

                self._speed_measured_lbl = CTkLabel(
                    section,
                    text="Measured Speed: --",
                    font=style.get_font("small"),
                    anchor="w"
                )
                self._speed_measured_lbl.pack(fill="x", padx=style.igap)

                self._rudder_expected_lbl = CTkLabel(
                    section,
                    text="Expected Rudder: --",
                    font=style.get_font("small"),
                    anchor="w"
                )
                self._rudder_expected_lbl.pack(fill="x", padx=style.igap)

                self._rudder_measured_lbl = CTkLabel(
                    section,
                    text="Measured Rudder: --",
                    font=style.get_font("small"),
                    anchor="w"
                )
                self._rudder_measured_lbl.pack(fill="x", padx=style.igap)

        CTkFrame(section, fg_color="transparent", height=style.igap).pack()

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
                    self._root.after(0, self._refresh_encryption_ui)
            except Exception:
                pass

        threading.Thread(target=_request, daemon=True).start()

    def _send_target(self):
        raw_x = self._target_x_entry.get().strip()
        raw_y = self._target_y_entry.get().strip()

        try:
            target_x = float(raw_x)
            target_y = float(raw_y)
        except ValueError:
            self._root.after(0, lambda: self._target_status.configure(
                text="Status: Invalid input", text_color="red"
            ))
            return

        def _request():
            try:
                resp = requests.post(
                    f"{self._get_url()}/set_target",
                    json={"target_x": target_x, "target_y": target_y},
                    timeout=3,
                )
                if resp.ok:
                    self._root.after(0, lambda: self._target_status.configure(
                        text=f"Status: Set to ({target_x:.1f}, {target_y:.1f})",
                        text_color="green"
                    ))
                else:
                    self._root.after(0, lambda: self._target_status.configure(
                        text=f"Status: Server error {resp.status_code}",
                        text_color="red"
                    ))
            except Exception:
                self._root.after(0, lambda: self._target_status.configure(
                    text="Status: Connection failed", text_color="red"
                ))

        threading.Thread(target=_request, daemon=True).start()

    def _poll(self):
        def _request():
            try:
                resp = requests.get(f"{self._get_url()}/api/data", timeout=3)
                if resp.ok:
                    data = resp.json()
                    self._root.after(0, lambda: self._on_data(data))
                    self._root.after(0, self._set_connected)
                else:
                    self._root.after(0, self._set_disconnected)
            except Exception:
                self._root.after(0, self._set_disconnected)

        threading.Thread(target=_request, daemon=True).start()
        self._root.after(self.POLL_INTERVAL_MS, self._poll)

    def _on_log_source_change(self, value: str):
        self._log_source = value.lower()
        active = self._last_points.get(self._log_source, [])
        self._update_log(list(reversed(active[-10:])))

    def _kalman_update(self, measured_speed, measured_rudder):

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
            try:
                measured_speed = float(measured_speed)
                measured_rudder = float(measured_rudder)
            except (ValueError, TypeError):
                measured_speed = 0.0
                measured_rudder = 0.0

            filtered_speed, filtered_rudder, flag = self._kalman_update(
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

            if latest.get("seq", -1) != self._last_seq:
                self._last_seq  = latest.get("seq", -1)
                self._positions = [(p["x"], p.get("y", 0.0)) for p in client_points]
                if len(self._positions) >= 2:
                    dx = self._positions[-1][0] - self._positions[-2][0]
                    dy = self._positions[-1][1] - self._positions[-2][1]
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
        style = self._style
        cols  = ["received_at", "x", "y", "theta", "speed", "rudder", "timestamp"]

        for widget in self._log_frame.winfo_children():
            widget.destroy()
        self._log_rows = []

        for r_idx, packet in enumerate(rows):
            row_labels = []
            bg = style.color("widget") if r_idx % 2 == 0 else style.color("panel")
            for c_idx, key in enumerate(cols):
                raw = packet.get(key, "—")
                if key == "received_at":
                    text = str(raw)[11:19]
                elif key == "timestamp":
                    text = str(raw)
                else:
                    try:
                        text = f"{float(raw):.4f}"
                    except (ValueError, TypeError):
                        text = str(raw)

                lbl = CTkLabel(self._log_frame, text=text,
                               font=style.get_font("small"),
                               fg_color=bg, anchor="w")
                lbl.grid(row=r_idx, column=c_idx, padx=4, pady=1, sticky="ew")
                row_labels.append(lbl)
            self._log_rows.append(row_labels)


    def _refresh_encryption_ui(self):
        if self._encryption_on:
            self._enc_label.configure(text="Status: ON", text_color="green")
            self._enc_button.configure(text="Disable Encryption")
        else:
            self._enc_label.configure(text="Status: OFF", text_color="gray")
            self._enc_button.configure(text="Enable Encryption")

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

    def _set_connected(self):
        self._conn_status.configure(text="⬤  Connected", text_color="green")

    def _set_disconnected(self):
        self._conn_status.configure(text="⬤  Disconnected", text_color="red")

    # def _on_map_click(self, event):
    #         if self._map_scale is None or self._map_offset is None:
    #             return

    #         if not (0.0 <= world_x <= 200.0 and 0.0 <= world_y <= 200.0):
    #             return
    #         world_x = (event.x - self._map_offset[0]) / self._map_scale
    #         world_y = (event.y - self._map_offset[1]) / self._map_scale

    #         # Clamp to valid map range
    #         world_x = max(0.0, min(200.0, world_x))
    #         world_y = max(0.0, min(200.0, world_y))

    #         self._map_click_xy = (world_x, world_y)

    #         self._target_x_entry.delete(0, "end")
    #         self._target_x_entry.insert(0, f"{world_x:.1f}")
    #         self._target_y_entry.delete(0, "end")
    #         self._target_y_entry.insert(0, f"{world_y:.1f}")