'''
Unpacks the defender page's AP-polled /api/data JSON blob into the buffer's
defender_modbus/defender_map/defender_status channels. Private to Buffer -
nothing outside buffer_manager.py should import _PollUnpacker; the only
public entry point is Buffer.put_poll(data).
'''

import time

from .channels.defender_modbus import DefenderModbusBuffer
from .channels.defender_map import DefenderMapBuffer
from .channels.defender_status import DefenderStatusBuffer

# Scalar fields copied straight across to defender_status under their own
# name - flags and the settings/revision numbers the sliders sync against.
# encryption_status is here; encryption_key is not - the AP happens to echo
# the key back in plaintext, but nothing needs to read it back out.
STATUS_FIELDS = [
    "encryption_status",
    "submarine_mode",
    "kalman_filter_enabled",
    "sensor_noise_variance",
    "rudder_error_threshold",
    "speed_error_threshold",
    "kalman_expected_sensor_variance",
    "hvac_sensor_noise_variance",
    "hvac_kalman_expected_sensor_variance",
    "hvac_state_error_threshold",
    "settings_revision",
    "client_settings_revision",
    "server_settings_revision",
]

# Submarine variables every client/server point carries.
SUBMARINE_VARIABLES = ["x", "y", "theta", "speed", "rudder"]
# Of those, only x/y/theta also carry a client-side noisy reading (noise_x, ...).
NOISY_VARIABLES = ["x", "y", "theta"]


class _PollUnpacker:

    def __init__(self, modbus: DefenderModbusBuffer, map: DefenderMapBuffer, status: DefenderStatusBuffer):
        self.modbus = modbus
        self.map = map
        self.status = status
        self.reset()

    def reset(self):
        # Rolling poll windows overlap between ticks - these track the last
        # received_at already unpacked per source, so a slid-forward window
        # only contributes its genuinely new points instead of re-appending
        # duplicates into the histories on every poll.
        self._last_client_received_at: float | None = None
        self._last_server_received_at: float | None = None

    def unpack(self, data: dict):
        poll_time = self._latest_received_at(data)
        self._unpack_status(data)
        self._unpack_client_points(data.get("client_points") or [])
        self._unpack_server_points(data.get("server_points") or [])
        self._unpack_hvac(data)
        self._unpack_target(data, poll_time)

    def _latest_received_at(self, data: dict) -> float:
        '''
        Only meaningful for submarine data (see _unpack_target's target_x/
        target_y) - client_points/server_points are the AP's submarine
        telemetry buffers, and the AP's /set_mode handler never clears them
        on a mode switch, so while it's sitting in HVAC mode they just go
        stale: still present and non-empty, but frozen at whatever
        received_at they last had in submarine mode. Deriving the *HVAC*
        fields' own timestamp from this would timestamp every HVAC poll
        identically for as long as the AP stays in HVAC mode, collapsing
        temperature/heater history into one x position instead of a real
        timeline - see _unpack_hvac, which uses its own wall clock instead.
        '''
        points = data.get("server_points") or data.get("client_points") or []
        if points:
            try:
                return float(points[-1].get("received_at"))
            except (TypeError, ValueError):
                pass
        return time.time()

    def _unpack_status(self, data: dict):
        for key in STATUS_FIELDS:
            if key in data:
                self.status.put(key, data[key])

    def _new_points(self, points: list, mark_attr: str) -> list:
        last = getattr(self, mark_attr)
        latest = last
        output = []
        for point in points:
            try:
                t = float(point.get("received_at"))
            except (TypeError, ValueError):
                continue
            if last is not None and t <= last:
                continue
            output.append((t, point))
            if latest is None or t > latest:
                latest = t
        setattr(self, mark_attr, latest)
        return output

    def _unpack_client_points(self, points: list):
        for t, point in self._new_points(points, "_last_client_received_at"):
            for variable in SUBMARINE_VARIABLES:
                value = point.get(variable)
                if value is not None:
                    self.modbus.put(variable, "client_clean", float(value), t)
            for variable in NOISY_VARIABLES:
                value = point.get(f"noise_{variable}")
                if value is not None:
                    self.modbus.put(variable, "client_noisy", float(value), t)

            x, y = point.get("x"), point.get("y")
            if x is not None and y is not None:
                self.map.put_point("client_clean", float(x), float(y))
            noise_x, noise_y = point.get("noise_x"), point.get("noise_y")
            if noise_x is not None and noise_y is not None:
                self.map.put_point("client_noisy", float(noise_x), float(noise_y))

            if (value := point.get("speed_anomaly_detected")) is not None:
                self.status.put("speed_anomaly", bool(value))
            if (value := point.get("rudder_anomaly_detected")) is not None:
                self.status.put("rudder_anomaly", bool(value))

    def _unpack_server_points(self, points: list):
        for t, point in self._new_points(points, "_last_server_received_at"):
            for variable in SUBMARINE_VARIABLES:
                value = point.get(variable)
                if value is not None:
                    self.modbus.put(variable, "server_clean", float(value), t)

            x, y = point.get("x"), point.get("y")
            if x is not None and y is not None:
                self.map.put_point("server_clean", float(x), float(y))

            if (value := point.get("state_anomaly_detected")) is not None:
                self.status.put("state_anomaly", bool(value))

    def _unpack_hvac(self, data: dict):
        # Flat, single-source fields with no per-point timestamp of their
        # own and no real relationship to client_points/server_points (see
        # _latest_received_at) - timestamped with the unpacker's own wall
        # clock instead. That's fine even though it's a different clock
        # than submarine data's AP-uptime one: HVAC history is only ever
        # plotted against itself (DefenderHVACChart/defender_stripchart_
        # panel never overlay it with submarine x/y/theta), so all that
        # matters is that current_temp/target_temp/heater stay internally
        # consistent and keep moving forward every poll - which client_
        # points/server_points can't guarantee while the AP sits in HVAC
        # mode, but time.time() always can.
        hvac_time = time.time()
        if (value := data.get("current_temp")) is not None:
            self.modbus.put("temperature", "client_clean", float(value), hvac_time)
        if (value := data.get("target_temp")) is not None:
            self.modbus.put("temperature", "target", float(value), hvac_time)
        if (value := data.get("heater_on")) is not None:
            heater_on = bool(value)
            # Kept as a status flag too (ModeForm/hvac_view read it for a
            # plain ON/OFF label), but also recorded as a 0.0/1.0 modbus
            # history so charts can plot it over time like temperature -
            # see DefenderHVACChart/defender_stripchart_panel.
            self.status.put("heater_on", heater_on)
            self.modbus.put("heater", "client_clean", 1.0 if heater_on else 0.0, hvac_time)
        if (value := data.get("HVAC_anomaly_detected")) is not None:
            self.status.put("hvac_anomaly", bool(value))

    def _unpack_target(self, data: dict, poll_time: float):
        # Submarine-only now - target_temp moved into _unpack_hvac above,
        # since it needs the HVAC wall clock, not this AP-uptime one.
        if (value := data.get("target_x")) is not None:
            self.modbus.put("x", "target", float(value), poll_time)
        if (value := data.get("target_y")) is not None:
            self.modbus.put("y", "target", float(value), poll_time)
