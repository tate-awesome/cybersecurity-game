from .wifi import WifiBaseClass

try:
    import gi
    gi.require_version("NM", "1.0")
    from gi.repository import GLib, NM
    _NM_IMPORT_ERROR = None
except (ImportError, ValueError) as e:
    NM = None
    GLib = None
    _NM_IMPORT_ERROR = e

# activate_connection_async can hang indefinitely if NetworkManager never
# calls back (e.g. the AP drops out of range mid-handshake), so give it a
# bound rather than freezing the caller's GLib.MainLoop forever.
CONNECT_TIMEOUT_SECONDS = 20

# Mirrors wifi_windows.py's SCAN_TIMEOUT_SECONDS: request_scan_async only
# confirms NetworkManager accepted the request, not that the scan actually
# finished - that's reported later via the device's "last-scan" property
# changing (or never, if the radio is busy/removed mid-scan), so bound the
# wait rather than blocking the caller forever.
SCAN_TIMEOUT_SECONDS = 10


class Wifi(WifiBaseClass):
    '''
    Linux Version - switches wifi via NetworkManager's libnm bindings.
    '''
    def __init__(self, buffer, context):
        super().__init__(buffer, context)
        self._client: "NM.Client | None" = None
        self._watched_connection = None
        self._watched_handler_id = None
        self._last_deactivation_reason = None

    def _watch_active_connection(self, active_connection):
        '''
        Keeps listening to the target connection's "state-changed" signal
        after connect_to_saved_wifi() returns, purely to capture *why* it
        eventually deactivates (NM reports this as an ActiveConnectionStateReason,
        e.g. USER_DISCONNECTED). is_running()'s polling only sees "the SSID
        changed" and can't otherwise tell a deliberate disconnect apart from
        the AP genuinely dropping out of range.
        '''
        self._unwatch_active_connection()
        self._watched_connection = active_connection
        self._last_deactivation_reason = None
        self._watched_handler_id = active_connection.connect("state-changed", self._on_watched_state_changed)

    def _unwatch_active_connection(self):
        if self._watched_connection is not None and self._watched_handler_id is not None:
            try:
                self._watched_connection.disconnect(self._watched_handler_id)
            except (GLib.Error, TypeError):
                pass
        self._watched_connection = None
        self._watched_handler_id = None

    def _on_watched_state_changed(self, active_connection, state, reason):
        if state == NM.ActiveConnectionState.DEACTIVATED:
            self._last_deactivation_reason = reason

    def _describe_lost_connection(self) -> str:
        if self._last_deactivation_reason == NM.ActiveConnectionStateReason.USER_DISCONNECTED:
            # A real reason from NM, not a guess - the user (or some other
            # app) explicitly disconnected it, so say that plainly instead
            # of the misleading "may be out of range".
            return f"'{self.target_network}' was manually disconnected."
        return super()._describe_lost_connection()

    @staticmethod
    def _pump_pending_events():
        '''
        NM.Client's properties (active access point, device state, etc.)
        are only kept current by processing D-Bus signals on GLib's default
        main context - and nothing else in this Qt app drives that context.
        The only time it normally gets pumped is inside connect_to_saved_wifi's
        own short-lived GLib.MainLoop, so a signal that arrives right after
        that loop quits (e.g. "active access point changed", which can lag
        slightly behind activate_connection_finish succeeding) sits
        unprocessed - a poll immediately afterwards would see stale state.
        Draining whatever's already arrived (non-blocking) before every
        read is what lets get_current_ssid()/is_running() see fresh state.
        '''
        if GLib is None:
            return
        context = GLib.MainContext.default()
        while context.iteration(False):
            pass

    def _get_client(self):
        self._pump_pending_events()
        if _NM_IMPORT_ERROR is not None:
            self.buffer.put("wifi", f"python-gobject/libnm bindings not available: {_NM_IMPORT_ERROR}")
            return None
        if self._client is None:
            try:
                self._client = NM.Client.new(None)
            except GLib.Error as e:
                self.buffer.put("wifi", f"Failed to reach NetworkManager (is it running?): {e.message}")
                return None
        return self._client

    def _wifi_device(self, client):
        for device in client.get_devices():
            if device.get_device_type() == NM.DeviceType.WIFI:
                return device
        return None

    @staticmethod
    def _ssid_to_str(ssid) -> "str | None":
        return NM.utils_ssid_to_utf8(ssid.get_data()) if ssid is not None else None

    @staticmethod
    def _connection_ssid(connection) -> "str | None":
        '''
        The SSID a wireless connection profile is actually configured to
        associate with. NM auto-names profiles it creates itself as
        "Auto <SSID>" (get_id() then differs from the real SSID), so this
        must be read from the profile's own wireless setting rather than
        assumed from its id/name.
        '''
        wireless_setting = connection.get_setting_wireless()
        if wireless_setting is None or wireless_setting.get_ssid() is None:
            return None
        return Wifi._ssid_to_str(wireless_setting.get_ssid())

    def _wifi_ready(self, client) -> "object | None":
        '''
        Common precondition checks shared by every action that needs to
        actually talk to a Wi-Fi radio (as opposed to just reading cached
        NetworkManager state). Returns the Wi-Fi device on success, or None
        after putting an explanatory status message.
        '''
        if not client.wireless_hardware_get_enabled():
            self.buffer.put("wifi", "Wi-Fi is disabled by a hardware switch/airplane mode.")
            return None
        if not client.wireless_get_enabled():
            self.buffer.put("wifi", "Wi-Fi is turned off. Turn it on and try again.")
            return None

        device = self._wifi_device(client)
        if device is None:
            self.buffer.put("wifi", "No Wi-Fi device found on this system.")
            return None
        if device.get_state() == NM.DeviceState.UNMANAGED:
            self.buffer.put("wifi", "Wi-Fi device is not managed by NetworkManager.")
            return None
        if device.get_state() == NM.DeviceState.UNAVAILABLE:
            self.buffer.put("wifi", "Wi-Fi device is unavailable.")
            return None
        return device

    def get_network_history(self) -> list[str]:
        client = self._get_client()
        if client is None:
            return []

        return [
            connection.get_id()
            for connection in client.get_connections()
            if connection.get_connection_type() == NM.SETTING_WIRELESS_SETTING_NAME
        ]

    def get_current_ssid(self) -> "str | None":
        '''
        Returns the SSID of the network currently connected to, or None if
        there isn't one (including "couldn't tell" cases - no client, no
        device, or nothing active) - callers only need to distinguish "there
        was a previous network" from "there wasn't", not why.
        '''
        client = self._get_client()
        if client is None:
            return None

        device = self._wifi_device(client)
        if device is None:
            return None

        access_point = device.get_active_access_point()
        return self._ssid_to_str(access_point.get_ssid()) if access_point else None

    def _scan_for_networks(self, device):
        '''
        Requests a fresh scan and waits (up to SCAN_TIMEOUT_SECONDS) for NM
        to report it done via the "last-scan" property changing, mirroring
        the WLAN_NOTIFICATION_ACM_SCAN_COMPLETE wait on Windows. Best-effort:
        if the request itself fails, this gives up quietly and
        get_available_networks() falls back to whatever's already cached,
        same as if this method didn't exist.
        '''
        loop = GLib.MainLoop()
        done = {"flag": False}

        def finish():
            if done["flag"]:
                return
            done["flag"] = True
            loop.quit()

        def on_last_scan_changed(_device, _pspec):
            finish()

        def on_scanned(_device, async_result, _user_data):
            try:
                device.request_scan_finish(async_result)
            except GLib.Error:
                # Request itself was rejected (e.g. scanning too frequently)
                # - nothing more to wait for.
                finish()

        def on_timeout():
            finish()
            return GLib.SOURCE_REMOVE

        handler_id = device.connect("notify::last-scan", on_last_scan_changed)
        timeout_id = GLib.timeout_add_seconds(SCAN_TIMEOUT_SECONDS, on_timeout)
        try:
            device.request_scan_async(None, on_scanned, None)
            loop.run()
        finally:
            device.disconnect(handler_id)
            GLib.source_remove(timeout_id)

    def get_available_networks(self, match_name: "str | None" = None) -> list[str]:
        '''
        match_name, when given, is checked against the already-cached access
        points before doing anything else - if the target is already known
        to be nearby, an explicit request_scan_async and its up-to-
        SCAN_TIMEOUT_SECONDS wait would be pure dead time on top of an answer
        this call already has.
        '''
        client = self._get_client()
        if client is None:
            return []

        device = self._wifi_device(client)
        if device is None:
            return []

        def cached() -> list[str]:
            networks = {self._ssid_to_str(ap.get_ssid()) for ap in device.get_access_points()}
            return [ssid for ssid in networks if ssid]

        networks = cached()
        if match_name is None or not any(self._matches(ssid, match_name) for ssid in networks):
            self._scan_for_networks(device)
            networks = cached()

        return networks

    @staticmethod
    def _describe_activation_error(e: "GLib.Error") -> str:
        '''
        libnm's own error messages are accurate but terse/technical - add a
        plain-language gloss in front of common failure modes while keeping
        the original message so nothing is lost.
        '''
        lowered = e.message.lower()
        if "secret" in lowered:
            return f"a password/secret was missing or rejected ({e.message})"
        if "busy" in lowered:
            return f"the Wi-Fi device is busy with another operation ({e.message})"
        if "no suitable" in lowered or "not visible" in lowered or "no network with ssid" in lowered:
            return f"the network is not currently in range ({e.message})"
        if "insufficient" in lowered or "not authorized" in lowered or "permission" in lowered:
            return f"permission was denied ({e.message})"
        return e.message

    def connect_to_saved_wifi(self, ssid: "str | None") -> bool:
        if not ssid:
            self.buffer.put("wifi", "No target network was specified to connect to.")
            return False

        client = self._get_client()
        if client is None:
            return False

        device = self._wifi_ready(client)
        if device is None:
            return False

        connection = next(
            (
                c for c in client.get_connections()
                if c.get_connection_type() == NM.SETTING_WIRELESS_SETTING_NAME and c.get_id() == ssid
            ),
            None,
        )
        if connection is None:
            self.buffer.put("wifi", f"'{ssid}' is not a saved (historical) connection.")
            return False

        configured_ssid = self._connection_ssid(connection)
        in_range = configured_ssid is not None and any(
            self._ssid_to_str(ap.get_ssid()) == configured_ssid for ap in device.get_access_points()
        )
        if not in_range:
            self.buffer.put("wifi", f"'{ssid}' is not currently in range.")
            return False

        loop = GLib.MainLoop()
        outcome = {"ok": False, "message": None, "done": False, "timed_out": False}
        state_handler: "list[tuple] | None" = []

        def finish(message: "str | None", ok: bool = False):
            if outcome["done"]:
                return
            outcome["done"] = True
            outcome["ok"] = ok
            outcome["message"] = message
            loop.quit()

        def on_state_changed(active_connection, state, reason, _loop):
            # activate_connection_finish only confirms NetworkManager accepted
            # the request, not that the device has actually finished
            # switching over (auth/DHCP take a moment) - waiting for this
            # signal to report ACTIVATED is what makes "connected" here mean
            # the same thing get_current_ssid() will report a moment later.
            if state == NM.ActiveConnectionState.ACTIVATED:
                finish(None, ok=True)
            elif state == NM.ActiveConnectionState.DEACTIVATED:
                finish("connection failed or was deactivated before completing")

        def on_activated(client, async_result, _loop):
            try:
                active_connection = client.activate_connection_finish(async_result)
            except GLib.Error as e:
                finish(self._describe_activation_error(e))
                return
            except Exception as e:
                finish(f"unexpected error ({e})")
                return

            self._watch_active_connection(active_connection)
            state = active_connection.get_state()
            if state == NM.ActiveConnectionState.ACTIVATED:
                finish(None, ok=True)
            elif state == NM.ActiveConnectionState.DEACTIVATED:
                finish("connection failed or was deactivated before completing")
            else:
                state_handler.append((active_connection, active_connection.connect("state-changed", on_state_changed, _loop)))

        def on_timeout():
            outcome["timed_out"] = True
            finish(f"timed out after {CONNECT_TIMEOUT_SECONDS}s waiting to finish connecting")
            return GLib.SOURCE_REMOVE

        timeout_id = GLib.timeout_add_seconds(CONNECT_TIMEOUT_SECONDS, on_timeout)
        try:
            client.activate_connection_async(connection, device, None, None, on_activated, loop)
            loop.run()
        finally:
            if not outcome["timed_out"]:
                GLib.source_remove(timeout_id)
            for active_connection, handler_id in state_handler:
                active_connection.disconnect(handler_id)

        if outcome["ok"]:
            self.buffer.put("wifi", f"Connected to '{ssid}'.")
        else:
            self.buffer.put("wifi", f"Failed to connect to '{ssid}': {outcome['message']}")
        return outcome["ok"]

    def disconnect_current(self):
        '''
        Drops whatever the device is currently connected to, without
        switching to anything else - used by stop() when no previous_network
        was ever recorded, so Stop still means "not connected" even with
        nowhere to fall back to.
        '''
        client = self._get_client()
        if client is None:
            return

        device = self._wifi_device(client)
        if device is None:
            self.buffer.put("wifi", "No Wi-Fi device found on this system.")
            return

        loop = GLib.MainLoop()
        outcome = {"ok": False, "message": None}

        def on_disconnected(dev, async_result, _loop):
            try:
                dev.disconnect_finish(async_result)
                outcome["ok"] = True
            except GLib.Error as e:
                outcome["message"] = e.message
            loop.quit()

        device.disconnect_async(None, on_disconnected, loop)
        loop.run()

        if outcome["ok"]:
            self.buffer.put("wifi", "Disconnected.")
        else:
            self.buffer.put("wifi", f"Failed to disconnect: {outcome['message']}")

    def _start_impl(self, match_name: str):
        '''
        The actual scan/match/connect flow, run on a background thread by
        WifiBaseClass.start() - see its docstring for why. is_running()/the
        empty-field and already-running checks are handled there before this
        is even called.
        '''
        client = self._get_client()
        if client is None or self._wifi_ready(client) is None:
            return

        if self.previous_network is None:
            current = self.get_current_ssid()
            if self._matches(current, match_name):
                # Already sitting on a network matching the target pattern -
                # there's nothing to fall back to, and saving it as
                # previous_network would make stop() "restore" the very
                # connection it just tore down.
                self.buffer.put("wifi", f"Already connected to a matching network: {current}")
            elif current is not None:
                self.previous_network = current
                self.buffer.put("wifi", f"Saved current connection: {self.previous_network}")
            else:
                self.buffer.put("wifi", "Not currently connected to any network; nothing to restore later.")
        else:
            self.buffer.put("wifi", f"Using saved connection: {self.previous_network}")

        available = self.get_available_networks(match_name)
        self.buffer.put("wifi", "Available Networks:")
        target_available = None
        for network in available:
            self.buffer.put("wifi", f"      {network}")
            if self._matches(network, match_name):
                target_available = network

        if target_available is None:
            self.buffer.put("wifi", f"No matching available or historical network was found for '{match_name}'.")
            return
        self.buffer.put("wifi", f"Found matching available connection: {target_available}")

        history = self.get_network_history()
        self.buffer.put("wifi", "Historical Connections:")
        target_history = None
        for network in history:
            self.buffer.put("wifi", f"      {network}")
            if self._matches(network, target_available):
                target_history = network

        if target_history is None:
            self.buffer.put(
                "wifi",
                f"No matching available or historical network was found for '{match_name}' "
                f"('{target_available}' is nearby but has no saved connection profile; connect to it manually once first).",
            )
            return
        self.buffer.put("wifi", f"Found matching historical connection: {target_history}")

        self.buffer.put("wifi", f"Connecting to: {target_history}")
        # Flip to "running" now, before the connection attempt actually
        # finishes, so the GUI doesn't sit showing "disconnected" for the
        # whole (sometimes multi-second) auth/DHCP handshake between this
        # message and the "Connected to ..." one below. self._connecting is
        # already True the whole time this method runs (WifiBaseClass.start()
        # claims it before spawning this thread), which is what tells
        # is_running() to skip its live-mismatch check meanwhile, since the
        # device is still legitimately mid-switch and won't match
        # target_network yet - that's not a dropped connection.
        self.is_connected = True
        # target_available, not target_history: get_current_ssid() reports
        # the bare over-the-air SSID, while target_history is the NM
        # connection profile's id/name (e.g. "Auto AP-Config" for the
        # SSID "AP-Config") - comparing against the wrong one would never
        # match and made is_running() think the connection had dropped
        # the instant it succeeded.
        self.target_network = target_available
        self.match_name = match_name
        if not self.connect_to_saved_wifi(target_history):
            self.is_connected = False
            self.target_network = None
