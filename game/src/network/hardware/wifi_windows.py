import ctypes
import html
import re
import threading
from ctypes import wintypes

from .wifi import WifiBaseClass

try:
    _wlanapi = ctypes.WinDLL("wlanapi.dll")
    _WLANAPI_IMPORT_ERROR = None
except OSError as e:
    _wlanapi = None
    _WLANAPI_IMPORT_ERROR = e

# WlanConnect only confirms Windows accepted the request; the actual
# association/auth/DHCP handshake is reported later through a WLAN_NOTIFICATION_ACM
# callback (or never, if the AP drops out of range mid-handshake), so give it a
# bound rather than blocking the caller forever.
CONNECT_TIMEOUT_SECONDS = 20

WLAN_MAX_NAME_LENGTH = 256
DOT11_SSID_MAX_LENGTH = 32

WLAN_INTF_OPCODE_RADIO_STATE = 4
WLAN_INTF_OPCODE_CURRENT_CONNECTION = 7

DOT11_RADIO_STATE_OFF = 2

WLAN_CONNECTION_MODE_PROFILE = 0
DOT11_BSS_TYPE_ANY = 3

WLAN_INTERFACE_STATE_CONNECTED = 1

WLAN_NOTIFICATION_SOURCE_NONE = 0
WLAN_NOTIFICATION_SOURCE_ACM = 0x00000008

WLAN_NOTIFICATION_ACM_CONNECTION_COMPLETE = 10
WLAN_NOTIFICATION_ACM_CONNECTION_ATTEMPT_FAIL = 11

# A saved profile's actual SSID lives in its XML under <SSIDConfig><SSID><name>,
# same as _connection_ssid on Linux reads the real SSID from the connection's
# wireless setting rather than assuming it from the profile's display name.
_SSID_NAME_RE = re.compile(r"<SSIDConfig>.*?<SSID>.*?<name>(.*?)</name>", re.DOTALL)


class GUID(ctypes.Structure):
    _fields_ = [
        ("Data1", wintypes.DWORD),
        ("Data2", wintypes.WORD),
        ("Data3", wintypes.WORD),
        ("Data4", ctypes.c_ubyte * 8),
    ]


class DOT11_SSID(ctypes.Structure):
    _fields_ = [
        ("uSSIDLength", wintypes.ULONG),
        ("ucSSID", ctypes.c_ubyte * DOT11_SSID_MAX_LENGTH),
    ]


class WLAN_INTERFACE_INFO(ctypes.Structure):
    _fields_ = [
        ("InterfaceGuid", GUID),
        ("strInterfaceDescription", ctypes.c_wchar * WLAN_MAX_NAME_LENGTH),
        ("isState", wintypes.DWORD),
    ]


class WLAN_INTERFACE_INFO_LIST(ctypes.Structure):
    _fields_ = [
        ("dwNumberOfItems", wintypes.DWORD),
        ("dwIndex", wintypes.DWORD),
        ("InterfaceInfo", WLAN_INTERFACE_INFO * 1),
    ]


class WLAN_AVAILABLE_NETWORK(ctypes.Structure):
    _fields_ = [
        ("strProfileName", ctypes.c_wchar * WLAN_MAX_NAME_LENGTH),
        ("dot11Ssid", DOT11_SSID),
        ("dot11BssType", wintypes.DWORD),
        ("uNumberOfBssids", wintypes.ULONG),
        ("bNetworkConnectable", wintypes.BOOL),
        ("wlanNotConnectableReason", wintypes.DWORD),
        ("uNumberOfPhyTypes", wintypes.ULONG),
        ("dot11PhyTypes", wintypes.DWORD * 8),
        ("bMorePhyTypes", wintypes.BOOL),
        ("wlanSignalQuality", wintypes.ULONG),
        ("bSecurityEnabled", wintypes.BOOL),
        ("dot11DefaultAuthAlgorithm", wintypes.DWORD),
        ("dot11DefaultCipherAlgorithm", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("dwReserved", wintypes.DWORD),
    ]


class WLAN_AVAILABLE_NETWORK_LIST(ctypes.Structure):
    _fields_ = [
        ("dwNumberOfItems", wintypes.DWORD),
        ("dwIndex", wintypes.DWORD),
        ("Network", WLAN_AVAILABLE_NETWORK * 1),
    ]


class WLAN_PROFILE_INFO(ctypes.Structure):
    _fields_ = [
        ("strProfileName", ctypes.c_wchar * WLAN_MAX_NAME_LENGTH),
        ("dwFlags", wintypes.DWORD),
    ]


class WLAN_PROFILE_INFO_LIST(ctypes.Structure):
    _fields_ = [
        ("dwNumberOfItems", wintypes.DWORD),
        ("dwIndex", wintypes.DWORD),
        ("ProfileInfo", WLAN_PROFILE_INFO * 1),
    ]


class WLAN_CONNECTION_PARAMETERS(ctypes.Structure):
    _fields_ = [
        ("wlanConnectionMode", wintypes.DWORD),
        ("strProfile", wintypes.LPCWSTR),
        ("pDot11Ssid", ctypes.POINTER(DOT11_SSID)),
        ("pDesiredBssidList", ctypes.c_void_p),
        ("dot11BssType", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
    ]


class WLAN_ASSOCIATION_ATTRIBUTES(ctypes.Structure):
    _fields_ = [
        ("dot11Ssid", DOT11_SSID),
        ("dot11BssType", wintypes.DWORD),
        ("dot11Bssid", ctypes.c_ubyte * 6),
        ("dot11PhyType", wintypes.DWORD),
        ("uDot11PhyIndex", wintypes.ULONG),
        ("wlanSignalQuality", wintypes.ULONG),
        ("ulRxRate", wintypes.ULONG),
        ("ulTxRate", wintypes.ULONG),
    ]


class WLAN_SECURITY_ATTRIBUTES(ctypes.Structure):
    _fields_ = [
        ("bSecurityEnabled", wintypes.BOOL),
        ("bOneXEnabled", wintypes.BOOL),
        ("dot11AuthAlgorithm", wintypes.DWORD),
        ("dot11CipherAlgorithm", wintypes.DWORD),
    ]


class WLAN_CONNECTION_ATTRIBUTES(ctypes.Structure):
    _fields_ = [
        ("isState", wintypes.DWORD),
        ("wlanConnectionMode", wintypes.DWORD),
        ("strProfileName", ctypes.c_wchar * WLAN_MAX_NAME_LENGTH),
        ("wlanAssociationAttributes", WLAN_ASSOCIATION_ATTRIBUTES),
        ("wlanSecurityAttributes", WLAN_SECURITY_ATTRIBUTES),
    ]


class WLAN_PHY_RADIO_STATE(ctypes.Structure):
    _fields_ = [
        ("dwPhyIndex", wintypes.DWORD),
        ("dot11SoftwareRadioState", wintypes.DWORD),
        ("dot11HardwareRadioState", wintypes.DWORD),
    ]


class WLAN_RADIO_STATE(ctypes.Structure):
    _fields_ = [
        ("dwNumberOfPhys", wintypes.DWORD),
        ("PhyRadioState", WLAN_PHY_RADIO_STATE * 64),
    ]


class WLAN_CONNECTION_NOTIFICATION_DATA(ctypes.Structure):
    _fields_ = [
        ("wlanConnectionMode", wintypes.DWORD),
        ("strProfileName", ctypes.c_wchar * WLAN_MAX_NAME_LENGTH),
        ("dot11Ssid", DOT11_SSID),
        ("dot11BssType", wintypes.DWORD),
        ("bSecurityEnabled", wintypes.BOOL),
        ("wlanReasonCode", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
    ]


class WLAN_NOTIFICATION_DATA(ctypes.Structure):
    _fields_ = [
        ("NotificationSource", wintypes.DWORD),
        ("NotificationCode", wintypes.DWORD),
        ("InterfaceGuid", GUID),
        ("dwDataSize", wintypes.DWORD),
        ("pData", ctypes.c_void_p),
    ]


WLAN_NOTIFICATION_CALLBACK = ctypes.WINFUNCTYPE(None, ctypes.POINTER(WLAN_NOTIFICATION_DATA), ctypes.c_void_p)

if _wlanapi is not None:
    _wlanapi.WlanOpenHandle.argtypes = [wintypes.DWORD, ctypes.c_void_p, ctypes.POINTER(wintypes.DWORD), ctypes.POINTER(wintypes.HANDLE)]
    _wlanapi.WlanOpenHandle.restype = wintypes.DWORD

    _wlanapi.WlanEnumInterfaces.argtypes = [wintypes.HANDLE, ctypes.c_void_p, ctypes.POINTER(ctypes.POINTER(WLAN_INTERFACE_INFO_LIST))]
    _wlanapi.WlanEnumInterfaces.restype = wintypes.DWORD

    _wlanapi.WlanGetAvailableNetworkList.argtypes = [
        wintypes.HANDLE, ctypes.POINTER(GUID), wintypes.DWORD, ctypes.c_void_p,
        ctypes.POINTER(ctypes.POINTER(WLAN_AVAILABLE_NETWORK_LIST)),
    ]
    _wlanapi.WlanGetAvailableNetworkList.restype = wintypes.DWORD

    _wlanapi.WlanGetProfileList.argtypes = [
        wintypes.HANDLE, ctypes.POINTER(GUID), ctypes.c_void_p, ctypes.POINTER(ctypes.POINTER(WLAN_PROFILE_INFO_LIST)),
    ]
    _wlanapi.WlanGetProfileList.restype = wintypes.DWORD

    _wlanapi.WlanGetProfile.argtypes = [
        wintypes.HANDLE, ctypes.POINTER(GUID), wintypes.LPCWSTR, ctypes.c_void_p,
        ctypes.POINTER(ctypes.c_wchar_p), ctypes.POINTER(wintypes.DWORD), ctypes.POINTER(wintypes.DWORD),
    ]
    _wlanapi.WlanGetProfile.restype = wintypes.DWORD

    _wlanapi.WlanQueryInterface.argtypes = [
        wintypes.HANDLE, ctypes.POINTER(GUID), wintypes.DWORD, ctypes.c_void_p,
        ctypes.POINTER(wintypes.DWORD), ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(wintypes.DWORD),
    ]
    _wlanapi.WlanQueryInterface.restype = wintypes.DWORD

    _wlanapi.WlanConnect.argtypes = [wintypes.HANDLE, ctypes.POINTER(GUID), ctypes.POINTER(WLAN_CONNECTION_PARAMETERS), ctypes.c_void_p]
    _wlanapi.WlanConnect.restype = wintypes.DWORD

    _wlanapi.WlanDisconnect.argtypes = [wintypes.HANDLE, ctypes.POINTER(GUID), ctypes.c_void_p]
    _wlanapi.WlanDisconnect.restype = wintypes.DWORD

    _wlanapi.WlanRegisterNotification.argtypes = [
        wintypes.HANDLE, wintypes.DWORD, wintypes.BOOL, WLAN_NOTIFICATION_CALLBACK,
        ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(wintypes.DWORD),
    ]
    _wlanapi.WlanRegisterNotification.restype = wintypes.DWORD

    _wlanapi.WlanReasonCodeToString.argtypes = [wintypes.DWORD, wintypes.DWORD, wintypes.LPWSTR, ctypes.c_void_p]
    _wlanapi.WlanReasonCodeToString.restype = wintypes.DWORD

    _wlanapi.WlanFreeMemory.argtypes = [ctypes.c_void_p]
    _wlanapi.WlanFreeMemory.restype = None


def _list_item(list_struct, field_name: str, item_type, index: int):
    '''
    WLAN_*_LIST structs declare their trailing array with a single element
    (e.g. "Network[1]") even though the OS allocation actually holds
    dwNumberOfItems of them - the classic C variable-length-array pattern.
    ctypes enforces the declared length on normal indexing, so elements past
    index 0 have to be reached with manual pointer arithmetic instead.
    '''
    field = getattr(type(list_struct), field_name)
    address = ctypes.addressof(list_struct) + field.offset + index * ctypes.sizeof(item_type)
    return ctypes.cast(address, ctypes.POINTER(item_type)).contents


def _guid_bytes(guid: GUID) -> bytes:
    return ctypes.string_at(ctypes.byref(guid), ctypes.sizeof(GUID))


class Wifi(WifiBaseClass):
    '''
    Windows Version - switches wifi via the Native Wifi API (wlanapi.dll),
    the same OS-level role libnm/NetworkManager plays on Linux.
    '''
    def __init__(self, buffer, context):
        super().__init__(buffer, context)
        self._handle: "wintypes.HANDLE | None" = None

    def _get_client(self):
        if _WLANAPI_IMPORT_ERROR is not None:
            self.buffer.put("wifi", f"wlanapi.dll not available: {_WLANAPI_IMPORT_ERROR}")
            return None
        if self._handle is None:
            negotiated_version = wintypes.DWORD()
            handle = wintypes.HANDLE()
            result = _wlanapi.WlanOpenHandle(2, None, ctypes.byref(negotiated_version), ctypes.byref(handle))
            if result != 0:
                self.buffer.put("wifi", f"Failed to reach the WLAN AutoConfig service (is it running?): {ctypes.FormatError(result)}")
                return None
            self._handle = handle
        return self._handle

    def _wifi_interface(self, client) -> "GUID | None":
        list_ptr = ctypes.POINTER(WLAN_INTERFACE_INFO_LIST)()
        result = _wlanapi.WlanEnumInterfaces(client, None, ctypes.byref(list_ptr))
        if result != 0:
            return None
        try:
            interface_list = list_ptr.contents
            if interface_list.dwNumberOfItems == 0:
                return None
            info = _list_item(interface_list, "InterfaceInfo", WLAN_INTERFACE_INFO, 0)
            # A copy, not a view - info's memory belongs to the OS allocation
            # that WlanFreeMemory releases below.
            return GUID.from_buffer_copy(info.InterfaceGuid)
        finally:
            _wlanapi.WlanFreeMemory(list_ptr)

    @staticmethod
    def _ssid_to_str(ssid: "DOT11_SSID | None") -> "str | None":
        if ssid is None or ssid.uSSIDLength == 0:
            return None
        return bytes(ssid.ucSSID[:ssid.uSSIDLength]).decode("utf-8", errors="replace")

    def _get_profile_xml(self, client, interface_guid, profile_name) -> "str | None":
        xml_ptr = ctypes.c_wchar_p()
        flags = wintypes.DWORD(0)
        granted_access = wintypes.DWORD(0)
        result = _wlanapi.WlanGetProfile(
            client, ctypes.byref(interface_guid), profile_name, None,
            ctypes.byref(xml_ptr), ctypes.byref(flags), ctypes.byref(granted_access),
        )
        if result != 0:
            return None
        try:
            return xml_ptr.value
        finally:
            _wlanapi.WlanFreeMemory(ctypes.cast(xml_ptr, ctypes.c_void_p))

    def _profile_ssid(self, client, interface_guid, profile_name) -> "str | None":
        '''
        The SSID a saved profile is actually configured to associate with,
        read from the profile's own XML. Unlike NetworkManager (which
        auto-names profiles "Auto <SSID>"), Windows normally names a profile
        after the SSID verbatim - but a profile can be renamed to anything,
        so that can't be assumed here either.
        '''
        xml = self._get_profile_xml(client, interface_guid, profile_name)
        if xml is None:
            return None
        match = _SSID_NAME_RE.search(xml)
        return html.unescape(match.group(1)) if match else None

    def _query_radio_state(self, client, interface_guid) -> "tuple[bool, bool] | None":
        data_size = wintypes.DWORD()
        data_ptr = ctypes.c_void_p()
        result = _wlanapi.WlanQueryInterface(
            client, ctypes.byref(interface_guid), WLAN_INTF_OPCODE_RADIO_STATE, None,
            ctypes.byref(data_size), ctypes.byref(data_ptr), None,
        )
        if result != 0:
            return None
        try:
            radio_state = ctypes.cast(data_ptr, ctypes.POINTER(WLAN_RADIO_STATE)).contents
            if radio_state.dwNumberOfPhys == 0:
                return True, True
            phy = radio_state.PhyRadioState[0]
            hardware_on = phy.dot11HardwareRadioState != DOT11_RADIO_STATE_OFF
            software_on = phy.dot11SoftwareRadioState != DOT11_RADIO_STATE_OFF
            return hardware_on, software_on
        finally:
            _wlanapi.WlanFreeMemory(data_ptr)

    def _wifi_ready(self, client) -> "GUID | None":
        '''
        Common precondition checks shared by every action that needs to
        actually talk to a Wi-Fi radio (as opposed to just reading cached
        state). Returns the interface GUID on success, or None after putting
        an explanatory status message - mirrors Linux's _wifi_ready.
        '''
        interface_guid = self._wifi_interface(client)
        if interface_guid is None:
            self.buffer.put("wifi", "No Wi-Fi device found on this system.")
            return None

        radio_state = self._query_radio_state(client, interface_guid)
        if radio_state is None:
            self.buffer.put("wifi", "Could not read the Wi-Fi radio state.")
            return None
        hardware_on, software_on = radio_state
        if not hardware_on:
            self.buffer.put("wifi", "Wi-Fi is disabled by a hardware switch/airplane mode.")
            return None
        if not software_on:
            self.buffer.put("wifi", "Wi-Fi is turned off. Turn it on and try again.")
            return None
        return interface_guid

    def _get_profile_names(self, client, interface_guid) -> "list[str]":
        list_ptr = ctypes.POINTER(WLAN_PROFILE_INFO_LIST)()
        result = _wlanapi.WlanGetProfileList(client, ctypes.byref(interface_guid), None, ctypes.byref(list_ptr))
        if result != 0:
            return []
        try:
            profile_list = list_ptr.contents
            return [
                _list_item(profile_list, "ProfileInfo", WLAN_PROFILE_INFO, i).strProfileName
                for i in range(profile_list.dwNumberOfItems)
            ]
        finally:
            _wlanapi.WlanFreeMemory(list_ptr)

    def get_network_history(self) -> "list[str]":
        client = self._get_client()
        if client is None:
            return []

        interface_guid = self._wifi_interface(client)
        if interface_guid is None:
            return []

        return self._get_profile_names(client, interface_guid)

    def _query_current_ssid(self, client, interface_guid) -> "str | None":
        data_size = wintypes.DWORD()
        data_ptr = ctypes.c_void_p()
        result = _wlanapi.WlanQueryInterface(
            client, ctypes.byref(interface_guid), WLAN_INTF_OPCODE_CURRENT_CONNECTION, None,
            ctypes.byref(data_size), ctypes.byref(data_ptr), None,
        )
        if result != 0:
            # Most commonly ERROR_INVALID_STATE (not connected) - either way
            # there's no current SSID to report.
            return None
        try:
            attrs = ctypes.cast(data_ptr, ctypes.POINTER(WLAN_CONNECTION_ATTRIBUTES)).contents
            if attrs.isState != WLAN_INTERFACE_STATE_CONNECTED:
                return None
            return self._ssid_to_str(attrs.wlanAssociationAttributes.dot11Ssid)
        finally:
            _wlanapi.WlanFreeMemory(data_ptr)

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

        interface_guid = self._wifi_interface(client)
        if interface_guid is None:
            return None

        return self._query_current_ssid(client, interface_guid)

    def _get_available_networks(self, client, interface_guid) -> "list[str | None]":
        list_ptr = ctypes.POINTER(WLAN_AVAILABLE_NETWORK_LIST)()
        result = _wlanapi.WlanGetAvailableNetworkList(client, ctypes.byref(interface_guid), 0, None, ctypes.byref(list_ptr))
        if result != 0:
            return []
        try:
            network_list = list_ptr.contents
            return [
                self._ssid_to_str(_list_item(network_list, "Network", WLAN_AVAILABLE_NETWORK, i).dot11Ssid)
                for i in range(network_list.dwNumberOfItems)
            ]
        finally:
            _wlanapi.WlanFreeMemory(list_ptr)

    def get_available_networks(self) -> "list[str]":
        client = self._get_client()
        if client is None:
            return []

        interface_guid = self._wifi_interface(client)
        if interface_guid is None:
            return []

        networks = set(self._get_available_networks(client, interface_guid))
        return [ssid for ssid in networks if ssid]

    @staticmethod
    def _reason_code_to_string(reason_code: int) -> str:
        message_buffer = ctypes.create_unicode_buffer(1024)
        result = _wlanapi.WlanReasonCodeToString(reason_code, len(message_buffer), message_buffer, None)
        return message_buffer.value if result == 0 else f"reason code {reason_code}"

    @staticmethod
    def _describe_activation_error(reason_code: int) -> str:
        '''
        wlanapi's own reason-code strings are accurate but terse/technical -
        add a plain-language gloss in front of common failure modes while
        keeping the original message so nothing is lost.
        '''
        message = Wifi._reason_code_to_string(reason_code)
        lowered = message.lower()
        if "password" in lowered or "key" in lowered or "credential" in lowered:
            return f"a password/secret was missing or rejected ({message})"
        if "busy" in lowered:
            return f"the Wi-Fi device is busy with another operation ({message})"
        if "not found" in lowered or "not visible" in lowered or "no network" in lowered or "range" in lowered:
            return f"the network is not currently in range ({message})"
        if "denied" in lowered or "not authorized" in lowered or "permission" in lowered:
            return f"permission was denied ({message})"
        return message

    def connect_to_saved_wifi(self, ssid: "str | None") -> bool:
        if not ssid:
            self.buffer.put("wifi", "No target network was specified to connect to.")
            return False

        client = self._get_client()
        if client is None:
            return False

        interface_guid = self._wifi_ready(client)
        if interface_guid is None:
            return False

        profile_name = next(
            (name for name in self._get_profile_names(client, interface_guid) if name == ssid),
            None,
        )
        if profile_name is None:
            self.buffer.put("wifi", f"'{ssid}' is not a saved (historical) connection.")
            return False

        configured_ssid = self._profile_ssid(client, interface_guid, profile_name)
        in_range = configured_ssid is not None and configured_ssid in self._get_available_networks(client, interface_guid)
        if not in_range:
            self.buffer.put("wifi", f"'{ssid}' is not currently in range.")
            return False

        outcome = {"ok": False, "message": None, "done": False}
        done_event = threading.Event()

        def finish(message: "str | None", ok: bool = False):
            if outcome["done"]:
                return
            outcome["done"] = True
            outcome["ok"] = ok
            outcome["message"] = message
            done_event.set()

        def on_notification(notification_ptr, _context):
            # WlanConnect only confirms Windows accepted the request, not that
            # the device finished switching over (auth/DHCP take a moment) -
            # waiting for this callback to report connection_complete is what
            # makes "connected" here mean the same thing get_current_ssid()
            # will report a moment later.
            data = notification_ptr.contents
            if _guid_bytes(data.InterfaceGuid) != _guid_bytes(interface_guid):
                return
            if data.NotificationCode not in (WLAN_NOTIFICATION_ACM_CONNECTION_COMPLETE, WLAN_NOTIFICATION_ACM_CONNECTION_ATTEMPT_FAIL):
                return
            try:
                conn_data = ctypes.cast(data.pData, ctypes.POINTER(WLAN_CONNECTION_NOTIFICATION_DATA)).contents
            except ValueError:
                return
            if conn_data.strProfileName != profile_name:
                return
            if data.NotificationCode == WLAN_NOTIFICATION_ACM_CONNECTION_COMPLETE:
                finish(None, ok=True)
            else:
                finish(self._describe_activation_error(conn_data.wlanReasonCode))

        callback = WLAN_NOTIFICATION_CALLBACK(on_notification)
        prev_source = wintypes.DWORD()
        register_result = _wlanapi.WlanRegisterNotification(
            client, WLAN_NOTIFICATION_SOURCE_ACM, True, callback, None, None, ctypes.byref(prev_source),
        )
        if register_result != 0:
            self.buffer.put(
                "wifi",
                f"Failed to connect to '{ssid}': could not register for WLAN notifications ({ctypes.FormatError(register_result)})",
            )
            return False

        try:
            params = WLAN_CONNECTION_PARAMETERS()
            params.wlanConnectionMode = WLAN_CONNECTION_MODE_PROFILE
            params.strProfile = profile_name
            params.pDot11Ssid = None
            params.pDesiredBssidList = None
            params.dot11BssType = DOT11_BSS_TYPE_ANY
            params.dwFlags = 0

            connect_result = _wlanapi.WlanConnect(client, ctypes.byref(interface_guid), ctypes.byref(params), None)
            if connect_result != 0:
                outcome["message"] = f"failed to start connection attempt ({ctypes.FormatError(connect_result)})"
            elif not done_event.wait(CONNECT_TIMEOUT_SECONDS):
                finish(f"timed out after {CONNECT_TIMEOUT_SECONDS}s waiting to finish connecting")
        finally:
            # ctypes rejects a bare None for a WINFUNCTYPE argtype (raises
            # ArgumentError) - it has to be an actual null function pointer
            # of that type instead.
            null_callback = ctypes.cast(None, WLAN_NOTIFICATION_CALLBACK)
            _wlanapi.WlanRegisterNotification(client, WLAN_NOTIFICATION_SOURCE_NONE, True, null_callback, None, None, None)

        if outcome["ok"]:
            self.buffer.put("wifi", f"Connected to '{ssid}'.")
        else:
            self.buffer.put("wifi", f"Failed to connect to '{ssid}': {outcome['message']}")
        return outcome["ok"]

    def disconnect_current(self):
        '''
        Drops whatever the interface is currently connected to, without
        switching to anything else - used by stop() when no previous_network
        was ever recorded, so Stop still means "not connected" even with
        nowhere to fall back to.
        '''
        client = self._get_client()
        if client is None:
            return

        interface_guid = self._wifi_interface(client)
        if interface_guid is None:
            self.buffer.put("wifi", "No Wi-Fi device found on this system.")
            return

        result = _wlanapi.WlanDisconnect(client, ctypes.byref(interface_guid), None)
        if result == 0:
            self.buffer.put("wifi", "Disconnected.")
        else:
            self.buffer.put("wifi", f"Failed to disconnect: {ctypes.FormatError(result)}")

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

        available = self.get_available_networks()
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
            # Exact match, not substring: unlike NetworkManager (which
            # auto-names profiles "Auto <SSID>"), Windows normally names a
            # saved profile after the SSID verbatim, so there's no prefix to
            # account for here.
            if self._equal_ci(target_available, network):
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
        self.target_network = target_available
        self.match_name = match_name
        if not self.connect_to_saved_wifi(target_history):
            self.is_connected = False
            self.target_network = None
