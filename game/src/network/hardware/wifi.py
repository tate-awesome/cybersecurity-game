import platform
from ..process import Process

try:
    import gi
    gi.require_version("NM", "1.0")
    from gi.repository import GLib, NM
    _NM_IMPORT_ERROR = None
except (ImportError, ValueError) as e:
    NM = None
    GLib = None
    _NM_IMPORT_ERROR = e


class Wifi(Process):
    def __init__(self, buffer, context):
        super().__init__(buffer, context)
        self.is_connected = False
        self.previous_network = None
        self.os_name = platform.system()
        self._client: "NM.Client | None" = None

    def _get_client(self):
        if _NM_IMPORT_ERROR is not None:
            self.buffer.put("wifi", f"python-gobject/libnm bindings not available: {_NM_IMPORT_ERROR}")
            return None
        if self._client is None:
            try:
                self._client = NM.Client.new(None)
            except GLib.Error as e:
                self.buffer.put("wifi", f"Failed to connect to NetworkManager: {e}")
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

    def get_network_history(self) -> list[str]:
        client = self._get_client()
        if client is None:
            return []

        return [
            connection.get_id()
            for connection in client.get_connections()
            if connection.get_connection_type() == NM.SETTING_WIRELESS_SETTING_NAME
        ]

    def get_current_ssid(self) -> str:
        client = self._get_client()
        if client is None:
            return "Error: could not reach NetworkManager"

        device = self._wifi_device(client)
        if device is None:
            return "Error: no Wi-Fi device found"

        ssid = self._ssid_to_str(device.get_active_access_point().get_ssid()) if device.get_active_access_point() else None
        return ssid if ssid else "Not connected to Wi-Fi"

    def get_available_networks(self) -> list[str]:
        client = self._get_client()
        if client is None:
            return []

        device = self._wifi_device(client)
        if device is None:
            return []

        networks = {self._ssid_to_str(ap.get_ssid()) for ap in device.get_access_points()}
        return [ssid for ssid in networks if ssid]

    def connect_to_saved_wifi(self, ssid) -> bool:
        client = self._get_client()
        if client is None:
            return False

        connection = next(
            (
                c for c in client.get_connections()
                if c.get_connection_type() == NM.SETTING_WIRELESS_SETTING_NAME and c.get_id() == ssid
            ),
            None,
        )
        if connection is None:
            self.buffer.put("wifi", f"No saved connection profile named '{ssid}'")
            return False

        device = self._wifi_device(client)
        loop = GLib.MainLoop()
        outcome = {"ok": False}

        def on_activated(client, async_result, _loop):
            try:
                client.activate_connection_finish(async_result)
                outcome["ok"] = True
            except GLib.Error as e:
                self.buffer.put("wifi", f"Failed to connect: {e}")
            finally:
                _loop.quit()

        client.activate_connection_async(connection, device, None, None, on_activated, loop)
        loop.run()

        if outcome["ok"]:
            self.buffer.put("wifi", f"Success: connected to {ssid}")
        return outcome["ok"]

    def start(self, match_name: str):
        if self.os_name != "Linux":
            self.buffer.put("wifi", f"WiFi switching is only supported on Linux (NetworkManager/libnm), not {self.os_name}.")
            return
        if self.is_running():
            self.buffer.put("wifi", "WiFi is already connected")
        else:
            if self.previous_network is None:
                self.previous_network = self.get_current_ssid()
                self.buffer.put("wifi", f"Saved current connection: {self.previous_network}")
            else:
                self.buffer.put("wifi", f"Using saved connection: {self.previous_network}")

            available = self.get_available_networks()
            self.buffer.put("wifi", "Available Networks:")
            target_available = None
            for network in available:
                self.buffer.put("wifi", f"      {network}")
                if match_name in network:
                    target_available = network
            self.buffer.put("wifi", f"Found matching available connection: {target_available}")

            history = self.get_network_history()
            self.buffer.put("wifi", "Historical Connections:")
            target_history = None
            for network in history:
                self.buffer.put("wifi", f"      {network}")
                if target_available is not None and target_available in network:
                    target_history = network
            self.buffer.put("wifi", f"Found matching historical connection: {target_history}")

            self.buffer.put("wifi", f"Connecting to: {target_history}")
            self.connect_to_saved_wifi(target_history)
            self.is_connected = True

    def is_running(self):
        return self.is_connected

    def stop(self):
        if not self.is_running():
            self.buffer.put("wifi", f"Wifi is already disconnected.")
        else:
            if self.previous_network:
                self.buffer.put("wifi", f"Connecting to saved connection: {self.previous_network}")
                self.connect_to_saved_wifi(self.previous_network)
            self.is_connected = False
