import threading
import requests
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget
from .....app_core import Context
from .....network.hardware import APPoller
from ....frame_widgets.shift_wheel_slider import ShiftWheelSlider
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

# QSlider only steps through integers - each slider's own float min/max is
# mapped onto this many integer positions (see _to_slider_pos/_from_slider_pos).
SLIDER_RESOLUTION = 1000


class SlidersForm(BaseForm):
    '''
    Submarine and HVAC filter-tuning sliders in one form, ported from
    DefenderV0's _build_slider_block/_post_slider_settings/
    _sync_submarine_sliders and HVACView's equivalents. Whichever group
    matches context.buffer.defender_status.submarine_mode is shown -
    checked every animation tick, not a static settings toggle.
    '''

    def __init__(self, master: QWidget, context: Context):
        super().__init__(master, context, process_noun="Sliders")

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

        body = QWidget()
        body.setLayout(QVBoxLayout())
        body.layout().setContentsMargins(0, 0, 0, 0)
        self.grid_layout.addWidget(body, self.current_row, 0, 1, 3)
        self.current_row += 1

        self.submarine_frame, self.submarine_sliders, self.submarine_labels = self._build_group(
            body, SUBMARINE_SLIDER_DEFS, self.submarine_values, lambda: self._push_submarine())
        self.hvac_frame, self.hvac_sliders, self.hvac_labels = self._build_group(
            body, HVAC_SLIDER_DEFS, self.hvac_values, lambda: self._push_hvac())

        self._submarine_mode = True
        self.hvac_frame.hide()

        self._push_submarine()
        self._push_hvac()

        self.context.animation_manager.add_callback(f"DefenderSlidersForm_{id(self)}", self.refresh)

    def _to_slider_pos(self, value: float, lo: float, hi: float) -> int:
        if hi == lo:
            return 0
        return int(round((value - lo) / (hi - lo) * SLIDER_RESOLUTION))

    def _from_slider_pos(self, pos: int, lo: float, hi: float) -> float:
        return lo + (pos / SLIDER_RESOLUTION) * (hi - lo)

    def _build_group(self, parent: QWidget, defs, values: dict, push_func):
        frame = QWidget()
        frame.setLayout(QVBoxLayout())
        frame.layout().setContentsMargins(0, 0, 0, 0)
        parent.layout().addWidget(frame)
        sliders = {}
        value_labels = {}

        for title, min_val, max_val, default, attr, decimals in defs:
            header = QWidget()
            header_layout = QHBoxLayout(header)
            header_layout.setContentsMargins(self.style.igap, 0, self.style.igap, 0)
            frame.layout().addWidget(header)

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

            def slider_callback(pos, lbl=value_label, attr=attr, d=decimals, lo=min_val, hi=max_val):
                value = self._from_slider_pos(pos, lo, hi)
                values[attr] = value
                lbl.setText(f"{value:.{d}f}")
                if not self._syncing:
                    push_func()

            slider.valueChanged.connect(slider_callback)
            frame.layout().addWidget(slider)

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
                self.hvac_frame.hide()
                self.submarine_frame.show()
            else:
                self.submarine_frame.hide()
                self.hvac_frame.show()

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
            for _, lo, hi, _, attr, decimals in SUBMARINE_SLIDER_DEFS:
                value = status.get(attr)
                if value is None:
                    continue
                value = float(value)
                self.submarine_values[attr] = value
                self.submarine_sliders[attr].setValue(self._to_slider_pos(value, lo, hi))
                self.submarine_labels[attr].setText(f"{value:.{decimals}f}")
        finally:
            self._syncing = False

    def _sync_hvac(self, status):
        self._syncing = True
        try:
            for _, lo, hi, _, attr, decimals in HVAC_SLIDER_DEFS:
                value = status.get(HVAC_STATUS_KEYS[attr])
                if value is None:
                    continue
                value = float(value)
                self.hvac_values[attr] = value
                self.hvac_sliders[attr].setValue(self._to_slider_pos(value, lo, hi))
                self.hvac_labels[attr].setText(f"{value:.{decimals}f}")
        finally:
            self._syncing = False
