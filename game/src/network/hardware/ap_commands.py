'''
The defender AP's commands and the statuses they confirm, in one place -
every defender widget (panels and the DefenderV0 page alike) issues its
commands and reads its toggles through these, so they all agree on which
endpoint, payload fields and status key each setting uses.

Everything goes through buffer.defender_status: send() queues the command
for the shared APPoller, and the readers below use expected() so a toggle
shows the state just asked for while the AP is still confirming it.

The AP keeps separate encryption/AP-tunnel/Kalman state for each mode
(g_encryption_status vs g_hvac_encryption_status, ...), set through
different endpoints - /set_encryption and friends in submarine mode, but
/set_hvac_settings in HVAC mode. /api/data only reports the submarine
ones, so the HVAC ones are tracked from what /set_hvac_settings echoes back
under their own hvac_* status keys instead of sharing (and being clobbered
by the poll's) submarine keys.
'''

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..buffer import Buffer

SUBMARINE_SLIDER_FIELDS = [
    "sensor_noise_variance",
    "kalman_expected_sensor_variance",
    "rudder_error_threshold",
    "speed_error_threshold",
]

# HVAC sliders' /set_hvac_settings field -> the /api/data field it's read
# back from. Noise variance is posted without the hvac_ prefix but reported
# with it - the AP firmware's own asymmetry.
HVAC_SLIDER_FIELDS = {
    "sensor_noise_variance": "hvac_sensor_noise_variance",
    "hvac_kalman_expected_sensor_variance": "hvac_kalman_expected_sensor_variance",
    "hvac_state_error_threshold": "hvac_state_error_threshold",
}

# Everything /set_hvac_settings echoes back that /api/data never reports.
HVAC_ECHO = {
    "encryption_status": "hvac_encryption_status",
    "AP_communication": "hvac_ap_communication",
    "hvac_kalman_filter_enabled": "hvac_kalman_filter_enabled",
}


def submarine_mode(buffer: "Buffer") -> bool:
    return bool(buffer.defender_status.get("submarine_mode", True))


def _hvac_send(buffer: "Buffer", payload: dict, confirm: dict, log_key: str, success_message: str | None):
    buffer.defender_status.send("/set_hvac_settings", payload, confirm=confirm, echo=HVAC_ECHO,
                                log_key=log_key, success_message=success_message)


# ── Encryption ──────────────────────────────────────────────────────────

def encryption_key(buffer: "Buffer") -> str:
    return "encryption_status" if submarine_mode(buffer) else "hvac_encryption_status"


def encryption_enabled(buffer: "Buffer") -> bool:
    return bool(buffer.defender_status.expected(encryption_key(buffer), False))


def set_encryption(buffer: "Buffer", enabled: bool, key: str):
    message = "Encryption is on" if enabled else "Encryption is off"
    payload = {"encryption_status": enabled, "encryption_key": key}
    confirm = {encryption_key(buffer): enabled}
    if submarine_mode(buffer):
        buffer.defender_status.send("/set_encryption", payload, confirm=confirm,
                                    log_key="encryption", success_message=message)
    else:
        _hvac_send(buffer, payload, confirm, "encryption", message)


# ── AP tunnel ───────────────────────────────────────────────────────────

def ap_tunnel_key(buffer: "Buffer") -> str:
    # The AP never reports the submarine value back on /api/data, so this
    # one is only ever what the last successful set confirmed.
    return "ap_communication" if submarine_mode(buffer) else "hvac_ap_communication"


def ap_tunnel_enabled(buffer: "Buffer") -> bool:
    return bool(buffer.defender_status.expected(ap_tunnel_key(buffer), False))


def set_ap_tunnel(buffer: "Buffer", enabled: bool):
    message = "AP Tunnel is on" if enabled else "AP Tunnel is off"
    payload = {"AP_communication": enabled}
    confirm = {ap_tunnel_key(buffer): enabled}
    if submarine_mode(buffer):
        buffer.defender_status.send("/set_AP_communication", payload, confirm=confirm,
                                    log_key="ap_tunnel", success_message=message)
    else:
        _hvac_send(buffer, payload, confirm, "ap_tunnel", message)


# ── Kalman filter ───────────────────────────────────────────────────────
# Unlike encryption/AP tunnel, these aren't mode-switched: the panels'
# Kalman widgets (and DefenderV0's middle-pane block) always mean the
# submarine filter and grey out in HVAC mode, while HVACView owns HVAC's
# separate filter through the hvac_ variants - so a toggle never silently
# changes which filter it's showing when the AP switches modes.

def kalman_enabled(buffer: "Buffer") -> bool:
    # Defaults on, like the AP firmware itself.
    return bool(buffer.defender_status.expected("kalman_filter_enabled", True))


def set_kalman(buffer: "Buffer", enabled: bool):
    # Only the one field - /set_settings applies just the fields it's
    # given, so this can't clobber the sliders with stale values.
    buffer.defender_status.send("/set_settings", {"kalman_filter_enabled": enabled},
                                confirm={"kalman_filter_enabled": enabled}, log_key="kalman",
                                success_message="Kalman Filter is on" if enabled else "Kalman Filter is off")


def hvac_kalman_enabled(buffer: "Buffer") -> bool:
    return bool(buffer.defender_status.expected("hvac_kalman_filter_enabled", True))


def set_hvac_kalman(buffer: "Buffer", enabled: bool):
    _hvac_send(buffer, {"hvac_kalman_filter_enabled": enabled}, {"hvac_kalman_filter_enabled": enabled}, "kalman",
               "HVAC Kalman Filter is on" if enabled else "HVAC Kalman Filter is off")


def read_hvac_state(buffer: "Buffer"):
    '''
    /api/data never reports HVAC's encryption/AP tunnel/Kalman state - only
    /set_hvac_settings echoes it. An empty one changes nothing on the AP
    (it only applies fields it's given) but still echoes all three, so this
    learns them without waiting for the user to toggle something.
    '''
    _hvac_send(buffer, {}, {}, "ap_connect", None)


# ── Filter sliders ──────────────────────────────────────────────────────

def push_submarine_settings(buffer: "Buffer", values: dict):
    '''
    values: {field: value} for any of SUBMARINE_SLIDER_FIELDS. The AP's
    reply carries the new settings_revision, recorded as
    pending_settings_revision - see submarine_settings_synced.
    '''
    payload = {name: float(values[name]) for name in SUBMARINE_SLIDER_FIELDS if name in values}
    buffer.defender_status.send("/set_settings", payload,
                                echo={"settings_revision": "pending_settings_revision"},
                                log_key="sliders", success_message="Submarine filter settings updated")


def submarine_settings_synced(buffer: "Buffer") -> bool:
    '''
    Whether /api/data's submarine slider values can be trusted yet. Those
    are the client/server's own reported values, which lag behind a
    /set_settings until both have picked up its revision - syncing the
    sliders any sooner would yank them back to the old values.
    '''
    status = buffer.defender_status
    if status.in_flight("pending_settings_revision"):
        return False
    pending = int(status.get("pending_settings_revision", 0) or 0)
    if pending <= 0:
        return True
    # The AP's own counter is behind what it told us - it rebooted since,
    # so nobody is ever going to catch up to the old revision.
    if int(status.get("settings_revision", pending) or 0) < pending:
        return True
    client_revision = int(status.get("client_settings_revision", 0) or 0)
    server_revision = int(status.get("server_settings_revision", 0) or 0)
    return client_revision >= pending and server_revision >= pending


def push_hvac_settings(buffer: "Buffer", values: dict):
    '''
    values: {field: value} for any of HVAC_SLIDER_FIELDS' keys (the POST
    names). Unlike submarine's, HVAC's reported slider values are the AP's
    own, current the moment it accepts them - so they're confirmed straight
    into their reported status keys, and expected() on those keys is always
    safe to sync the sliders from.
    '''
    payload = {name: float(values[name]) for name in HVAC_SLIDER_FIELDS if name in values}
    confirm = {HVAC_SLIDER_FIELDS[name]: value for name, value in payload.items()}
    _hvac_send(buffer, payload, confirm, "sliders", "HVAC filter settings updated")
