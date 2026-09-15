from .wifi import WifiBaseClass


class Wifi(WifiBaseClass):
    '''
    Windows Version - not yet implemented.
    '''
    def __init__(self, buffer, context):
        super().__init__(buffer, context)

    def start(self, match_name: str):
        pass

    def get_current_ssid(self) -> "str | None":
        pass

    def connect_to_saved_wifi(self, ssid: "str | None") -> bool:
        pass
