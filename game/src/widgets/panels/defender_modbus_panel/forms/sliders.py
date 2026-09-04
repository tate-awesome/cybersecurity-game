import threading
import requests
from customtkinter import CTkFrame, CTkLabel, CTkSlider
from .....app_core import Context
from .....network.hardware import APPoller
from ...base_form import BaseForm

SUBMARINE_SLIDER_DEFS = [
    ("Sensor Noise Variance", 0.0, 20, 8.3, "sensor_noise_variance", 2),
    ("Kalman Expected Sensor Variance", 0.0, 20, 8.3, "kalman_expected_sensor_variance", 2),
    ("Rudder Error Threshold", 0.0, 10, 2.75, "rudder_error_threshold", 1),
    ("Speed Error Threshold", 0.0, 10, 2.0, "speed_error_threshold", 1),
]

HVAC_SLIDER_DEFS = [
    ("Sensor Noise Variance", 0.0, 1.0, 0.1, "sensor_noise_variance", 2),
    ("Kalman Expected Sensor Variance", 0.0, 1.0, 0.1, "kalman_expected_sensor_variance", 2),
    ("State Error Threshold", 0.0, 10.0, 5.0, "state_error_threshold", 1),
]

# HVAC's slider attrs are posted under different field names than they're
# read back under - same asymmetry as the old HVACView._sync_hvac_sliders.
HVAC_STATUS_KEYS = {
    "sensor_noise_variance": "hvac_sensor_noise_variance",
    "kalman_expected_sensor_variance": "hvac_kalman_expected_sensor_variance",
    "state_error_threshold": "hvac_state_error_threshold",
}


class SlidersForm(BaseForm):
    '''
    Submarine and HVAC filter-tuning sliders in one form, ported from
    DefenderV0's _build_slider_block/_post_slider_settings/
    _sync_submarine_sliders and HVACView's equivalents. Whichever group
    matches context.buffer.defender_status.submarine_mode is shown -
    checked every animation tick, not a static settings toggle.
    '''

    def __init__(self, master: CTkFrame, context: Context):
        super().__init__(master, context, attack_noun="Sliders")

        # Shares the AP Connect form's poller process rather than starting
        # its own - see EncryptionForm for why this isn't a
        # Process/get_process() case.
        self.process = self.context.process_manager.get_process("ap_connect")
        if self.process is None:
            self.process = APPoller(self.context.buffer, self.context)
            self.context.process_manager.add_process("ap_connect", self.process)

        self.add_header("Filter Settings")

        self._syncing = False
        self._pending_revision = 0
        self.submarine_values = {attr: default for _, _, _, default, attr, _ in SUBMARINE_SLIDER_DEFS}
        self.hvac_values = {attr: default for _, _, _, default, attr, _ in HVAC_SLIDER_DEFS}

        body = CTkFrame(self, fg_color="transparent")
        body.grid(row=self.current_row, column=0, columnspan=3, sticky="ew")
        self.current_row += 1

        self.submarine_frame, self.submarine_sliders, self.submarine_labels = self._build_group(
            body, SUBMARINE_SLIDER_DEFS, self.submarine_values, lambda: self._push_submarine())
        self.hvac_frame, self.hvac_sliders, self.hvac_labels = self._build_group(
            body, HVAC_SLIDER_DEFS, self.hvac_values, lambda: self._push_hvac())

        self._submarine_mode = True
        self.submarine_frame.pack(fill="x")

        self._push_submarine()
        self._push_hvac()

        self.context.animation_manager.add_callback(f"DefenderSlidersForm_{id(self)}", self.refresh)

    def _build_group(self, parent, defs, values: dict, push_func):
        frame = CTkFrame(parent, fg_color="transparent")
        sliders = {}
        value_labels = {}

        for title, min_val, max_val, default, attr, decimals in defs:
            header = CTkFrame(frame, fg_color="transparent")
            header.pack(fill="x", padx=self.style.igap)
            CTkLabel(header, text=title, font=self.style.get_font("small")).pack(side="left")
            value_label = CTkLabel(header, text=f"{default:.{decimals}f}",
                                    font=self.style.get_font("small"), text_color="gray")
            value_label.pack(side="right")

            def slider_callback(value, lbl=value_label, attr=attr, d=decimals):
                value = float(value)
                values[attr] = value
                lbl.configure(text=f"{value:.{d}f}")
                if not self._syncing:
                    push_func()

            slider = CTkSlider(frame, from_=min_val, to=max_val, command=slider_callback)
            slider.set(default)
            slider.pack(fill="x", padx=self.style.igap, pady=(0, 8))

            sliders[attr] = slider
            value_labels[attr] = value_label

        return frame, sliders, value_labels

    def _push_submarine(self):
        status = self.context.buffer.defender_status
        payload = dict(self.submarine_values)
        payload["kalman_filter_enabled"] = status.get("kalman_filter_enabled", True)

        def _request():
            try:
                resp = requests.post(f"{self.process.url}/set_settings", json=payload, timeout=3)
                if resp.ok:
                    body = resp.json()
                    self._pending_revision = int(body.get("settings_revision", 0))
                    self.context.buffer.put("kalman", f"Submarine settings posted, revision {self._pending_revision}")
            except Exception as e:
                self.context.buffer.put("kalman", f"Failed to post submarine settings: {e}")

        threading.Thread(target=_request, daemon=True).start()

    def _push_hvac(self):
        status = self.context.buffer.defender_status
        payload = {
            "encryption_status": status.get("encryption_status", False),
            "AP_communication": status.get("ap_communication", False),
            "hvac_sensor_noise_variance": self.hvac_values["sensor_noise_variance"],
            "hvac_kalman_expected_sensor_variance": self.hvac_values["kalman_expected_sensor_variance"],
            "hvac_state_error_threshold": self.hvac_values["state_error_threshold"],
            "hvac_kalman_filter_enabled": True,
        }

        def _request():
            try:
                resp = requests.post(f"{self.process.url}/set_hvac_settings", json=payload, timeout=3)
                if resp.ok:
                    self.context.buffer.put("kalman", "HVAC settings posted")
            except Exception as e:
                self.context.buffer.put("kalman", f"Failed to post HVAC settings: {e}")

        threading.Thread(target=_request, daemon=True).start()

    def refresh(self):
        status = self.context.buffer.defender_status
        submarine_mode = bool(status.get("submarine_mode", True))

        if submarine_mode != self._submarine_mode:
            self._submarine_mode = submarine_mode
            if submarine_mode:
                self.hvac_frame.pack_forget()
                self.submarine_frame.pack(fill="x")
            else:
                self.submarine_frame.pack_forget()
                self.hvac_frame.pack(fill="x")

        if submarine_mode:
            self._sync_submarine(status)
        else:
            self._sync_hvac(status)

    def _sync_submarine(self, status):
        client_revision = int(status.get("client_settings_revision", 0) or 0)
        server_revision = int(status.get("server_settings_revision", 0) or 0)

        if self._pending_revision > 0:
            if client_revision < self._pending_revision or server_revision < self._pending_revision:
                return
            self._pending_revision = 0

        self._syncing = True
        try:
            for _, _, _, _, attr, decimals in SUBMARINE_SLIDER_DEFS:
                value = status.get(attr)
                if value is None:
                    continue
                value = float(value)
                self.submarine_values[attr] = value
                self.submarine_sliders[attr].set(value)
                self.submarine_labels[attr].configure(text=f"{value:.{decimals}f}")
        finally:
            self._syncing = False

    def _sync_hvac(self, status):
        self._syncing = True
        try:
            for _, _, _, _, attr, decimals in HVAC_SLIDER_DEFS:
                value = status.get(HVAC_STATUS_KEYS[attr])
                if value is None:
                    continue
                value = float(value)
                self.hvac_values[attr] = value
                self.hvac_sliders[attr].set(value)
                self.hvac_labels[attr].configure(text=f"{value:.{decimals}f}")
        finally:
            self._syncing = False
