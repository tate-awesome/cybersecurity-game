'''
Wifi module. Shared state machine, with platform-specific network calls
(scanning, connecting, reading the current SSID) in wifi_linux.py /
wifi_windows.py - see net_filter_queue.py for the same split.
'''

from ..process import Process


class WifiBaseClass(Process):

    def __init__(self, buffer, context):
        super().__init__(buffer, context)
        self.is_connected = False
        self.previous_network = None
        self.target_network = None
        self._connecting = False

    def _unwatch_active_connection(self):
        '''
        No-op by default. Linux overrides this to release its NM signal
        watcher; a platform with nothing to release doesn't need to.
        '''
        pass

    def _describe_lost_connection(self) -> str:
        return f"Lost connection to '{self.target_network}'; it may no longer be in range."

    def is_running(self) -> bool:
        '''
        Polled every frame (see base_form.py's refresh_process_button) to
        reconcile the button/status with reality. self.is_connected is only
        ever set by start()/stop(), so on its own it can't notice the OS
        dropping the connection out from under us (e.g. the target AP is
        turned off) - that's checked here instead.

        No click of Stop is required to recognize this: once the target
        network is gone, this immediately reflects "not connected" so the
        button/status updates on its own. It deliberately doesn't try to
        force a reconnect to previous_network itself - virtually every OS's
        network stack already auto-reconnects to a previously known network
        on its own, so forcing it here would at best be redundant and at
        worst fight whatever the OS is already doing.
        '''
        if self.is_connected and self.target_network is not None and not self._connecting:
            current = self.get_current_ssid()
            if current is not None and current == self.target_network:
                return self.is_connected

            if current is not None and current == self.previous_network:
                self.buffer.put("wifi", f"Already reconnected to '{current}' on its own.")
            else:
                self.buffer.put("wifi", self._describe_lost_connection())

            self._unwatch_active_connection()
            self.is_connected = False
            self.target_network = None
        return self.is_connected

    def stop(self):
        if not self.is_running():
            self.buffer.put("wifi", "Wifi is already disconnected.")
            self.is_connected = False
            return

        # Unlike start(), flip to "not running" *before* the restore attempt
        # rather than after: stopping means the forced switch is over, so the
        # GUI should read as disconnected for the whole "Restoring..." ...
        # "Connected to ..." window below, not just once it finishes.
        self._unwatch_active_connection()
        self.is_connected = False
        self.target_network = None

        if self.previous_network:
            self.buffer.put("wifi", f"Restoring previous connection: {self.previous_network}")
            self.connect_to_saved_wifi(self.previous_network)
        else:
            self.buffer.put("wifi", "No previous network was recorded; leaving current connection as is.")
