import threading
import requests
from customtkinter import CTkFrame
from .....app_core import Context
from .....network.hardware import APPoller
from ...base_form import BaseForm


class KalmanForm(BaseForm):
    '''
    Toggles the submarine Kalman filter. Shares the AP Connect form's
    poller process - see EncryptionForm for why this isn't a
    Process/get_process() case. Posts the full /set_settings payload (not
    just kalman_filter_enabled) using whatever values defender_status
    currently holds, so toggling this doesn't clobber sliders set
    elsewhere with unknown/default values.
    '''

    def __init__(self, master: CTkFrame, context: Context):
        super().__init__(master, context, key="kalman")

        self.process = self.context.process_manager.get_process("ap_connect")
        if self.process is None:
            self.process = APPoller(self.context.buffer, self.context)
            self.context.process_manager.add_process("ap_connect", self.process)

        self.add_header()

        self.add_attack_button(
            lambda: self._post_kalman(True),
            lambda: self._post_kalman(False),
            lambda: bool(self.context.buffer.defender_status.get("kalman_filter_enabled", True)),
        )

        self.context.animation_manager.add_callback(f"KalmanForm_{id(self)}", self._refresh_status)

    def _post_kalman(self, enabled: bool):
        status = self.context.buffer.defender_status
        payload = {
            "sensor_noise_variance": status.get("sensor_noise_variance", 8.3),
            "kalman_expected_sensor_variance": status.get("kalman_expected_sensor_variance", 8.3),
            "rudder_error_threshold": status.get("rudder_error_threshold", 2.75),
            "speed_error_threshold": status.get("speed_error_threshold", 2.0),
            "kalman_filter_enabled": enabled,
        }

        self.context.buffer.put("kalman", "Enabling Kalman filter..." if enabled else "Disabling Kalman filter...")

        def _request():
            try:
                resp = requests.post(f"{self.process.url}/set_settings", json=payload, timeout=3)
                if resp.ok:
                    self.context.buffer.defender_status.put("kalman_filter_enabled", enabled)
                    self.context.buffer.put("kalman", "Kalman Filter is on" if enabled else "Kalman Filter is off")
                else:
                    self.context.buffer.put("kalman", f"AP rejected settings request (HTTP {resp.status_code})")
            except Exception as e:
                self.context.buffer.put("kalman", f"Failed to reach AP: {e}")

        threading.Thread(target=_request, daemon=True).start()

    def _refresh_status(self):
        if self.context.buffer.defender_status.get("kalman_filter_enabled", True):
            self.configure_on()
        else:
            self.configure_off()
