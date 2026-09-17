'''
Wifi module. Shared state machine, with platform-specific network calls
(scanning, connecting, reading the current SSID) in wifi_linux.py /
wifi_windows.py - see net_filter_queue.py for the same split.
'''

import threading
import time

from ..process import Process

# A manual network switch (or a brief AP hiccup) doesn't jump cleanly from
# the old SSID to the new one - there's normally a gap of a second or two
# where get_current_ssid() reports nothing while the OS disassociates from
# the old network and associates with the new one. is_running() is polled
# every 100ms (see base_form.py's refresh_process_button), so without a
# grace period the very first poll during that gap would immediately declare
# the connection lost, before the OS even finishes reconnecting - see
# is_running() below.
RECONNECT_GRACE_SECONDS = 5


class WifiBaseClass(Process):

    def __init__(self, buffer, context):
        super().__init__(buffer, context)
        self.is_connected = False
        self.previous_network = None
        self.target_network = None
        self.match_name: "str | None" = None
        self._connecting = False
        self._mismatch_since: "float | None" = None

    def _unwatch_active_connection(self):
        '''
        No-op by default. Linux overrides this to release its NM signal
        watcher; a platform with nothing to release doesn't need to.
        '''
        pass

    def _describe_lost_connection(self) -> str:
        return f"Lost connection to '{self.target_network}'; it may no longer be in range."

    @staticmethod
    def _matches(text: "str | None", pattern: "str | None") -> bool:
        '''Case-insensitive substring check: does pattern appear anywhere in text?'''
        return text is not None and pattern is not None and pattern.lower() in text.lower()

    @staticmethod
    def _equal_ci(a: "str | None", b: "str | None") -> bool:
        return a is not None and b is not None and a.lower() == b.lower()

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
        can_sense = self.match_name is not None and not self._connecting
        current = self.get_current_ssid() if can_sense else None

        if can_sense and current is not None and not self._matches(current, self.match_name):
            # previous_network is always "whatever non-matching network was
            # last seen", kept live here rather than only captured once at
            # start() - so if the user hops through a string of unrelated
            # networks before finally landing on one that matches, the
            # fallback stop() restores is the last one they were actually on,
            # not whatever they happened to be on the moment Start was
            # clicked.
            self.previous_network = current

        if self.is_connected and self.target_network is not None and not self._connecting:
            if current is not None and current == self.target_network:
                self._mismatch_since = None
                return self.is_connected

            # The OS switched us to a different network than the one we were
            # tracking - but if it still matches the original search pattern
            # (e.g. the AP handed off between two SSIDs matching the same
            # Device Name filter), that's not a lost connection: keep
            # previous_network as-is for stop() to restore later, just start
            # tracking the new SSID so future polls don't keep re-triggering
            # this branch.
            if self._matches(current, self.match_name):
                self.buffer.put("wifi", f"Reconnected to a different matching network: '{current}'.")
                self.target_network = current
                self._mismatch_since = None
                return self.is_connected

            # Not (yet) a match either way - give it RECONNECT_GRACE_SECONDS
            # before treating it as lost, in case this is a transient gap
            # partway through a manual switch that's about to land on
            # target_network or a match_name-matching network above.
            now = time.monotonic()
            if self._mismatch_since is None:
                self._mismatch_since = now
            if now - self._mismatch_since < RECONNECT_GRACE_SECONDS:
                return self.is_connected

            if current is not None and current == self.previous_network:
                self.buffer.put("wifi", f"Already reconnected to '{current}' on its own.")
            else:
                self.buffer.put("wifi", self._describe_lost_connection())

            self._unwatch_active_connection()
            self.is_connected = False
            self.target_network = None
            self._mismatch_since = None

        elif not self.is_connected and self._matches(current, self.match_name):
            # Even while "off" (never started, or a previously detected
            # loss), keep watching for the OS landing on a network matching
            # the last Device Name filter used - e.g. the user reconnects
            # manually before ever clicking Start again. previous_network was
            # already kept current by the bookkeeping above (whatever
            # non-matching network, if any, was seen right before this one).
            self.buffer.put("wifi", f"Detected an existing matching connection: '{current}'.")
            self.is_connected = True
            self.target_network = current

        return self.is_connected

    def start(self, match_name: str):
        '''
        Scanning and connecting can take real, human-noticeable time - a
        connect attempt alone can run up to CONNECT_TIMEOUT_SECONDS. Doing
        that on the calling (GUI) thread would freeze the app for the whole
        stretch, so the actual work (_start_impl, platform-specific) runs on
        a background thread instead; this just validates the input and
        claims _connecting synchronously, so a rapid double-click can't slip
        a second attempt in before the thread has even started.

        _connecting also doubles as "don't touch the OS Wi-Fi APIs from the
        polling thread right now" for is_running() (see can_sense there) -
        on Linux in particular, NM's default GLib main context isn't safe to
        iterate from two threads paying attention to it at once, so the
        poller has to sit out entirely while a background thread is mid
        scan/connect/disconnect.
        '''
        if not match_name.strip():
            self.buffer.put("wifi", "Device Name field is empty; enter a network name to search for.")
            return

        if self.is_running() or self._connecting:
            self.buffer.put("wifi", "A Wi-Fi connection change is already in progress.")
            return

        self._connecting = True
        threading.Thread(target=self._run_start, args=(match_name,), daemon=True).start()

    def _run_start(self, match_name: str):
        try:
            self._start_impl(match_name)
        finally:
            self._connecting = False

    def stop(self):
        if not self.is_running():
            self.buffer.put("wifi", "Wifi is already disconnected.")
            self.is_connected = False
            return

        if self._connecting:
            self.buffer.put("wifi", "A Wi-Fi connection change is already in progress.")
            return

        # Unlike start(), flip to "not running" *before* the restore attempt
        # rather than after: stopping means the forced switch is over, so the
        # GUI should read as disconnected for the whole "Restoring..." ...
        # "Connected to ..." window below, not just once it finishes. The
        # restore/disconnect itself can block for real time (same reasoning
        # as start()), so it runs on a background thread too, with
        # _connecting claimed for the same reason.
        self._unwatch_active_connection()
        self.is_connected = False
        self.target_network = None
        self._connecting = True
        threading.Thread(target=self._run_stop, daemon=True).start()

    def _run_stop(self):
        try:
            if self.previous_network:
                self.buffer.put("wifi", f"Restoring previous connection: {self.previous_network}")
                # Scan for it first, same as start() does for its target -
                # connect_to_saved_wifi()'s own in-range check only reads
                # whatever's already cached, which by now could easily be
                # stale (e.g. left over from scanning for a completely
                # different match_name back when this run started).
                self.get_available_networks(self.previous_network)
                self.connect_to_saved_wifi(self.previous_network)
            else:
                # No fallback was ever recorded - e.g. the target network was
                # already the active connection when this was started, so
                # there's nothing non-matching to restore. Still disconnect
                # rather than leaving the target connection active: Stop
                # should always mean "not connected through this process" -
                # it just has nowhere else to switch to.
                self.buffer.put("wifi", "No previous network was recorded; disconnecting.")
                self.disconnect_current()
        finally:
            self._connecting = False
