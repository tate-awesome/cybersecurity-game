'''
Polls a defender AP's /api/data endpoint on a background thread and hands
each response straight to Buffer.put_poll(). Unlike the attacker-side
hardware Processes, this doesn't need scapy or raw sockets - it's a plain
HTTP GET loop - but it's exactly the same kind of thing: a widget starts it,
it has to keep running across a page refresh, and whatever widget gets
rebuilt has to be able to reclaim it through context.process_manager instead
of losing track of it.

It's also the only thing that ever POSTs to the AP: widgets queue commands
on buffer.defender_status (see DefenderStatusBuffer.send), and this sends
them from the same thread as the polls - so a command and the poll after
it can never race, and there's exactly one AP connection no matter how many
defender widgets are on screen.
'''

import threading
import time
import requests

from ..process import Process
from . import ap_commands

# The process_manager key every defender widget shares the one poller under.
AP_POLLER_KEY = "ap_connect"


class APPoller(Process):

    def __init__(self, buffer, context, url: str = "http://192.168.4.1", interval_ms: float = 2000):
        super().__init__(buffer, context)
        self.url = url
        self.interval_ms = interval_ms
        self.running = False
        self.connected = False
        self._stop_event: threading.Event | None = None
        self._thread: threading.Thread | None = None

    def is_running(self) -> bool:
        return self.running

    def start(self):
        if self.running:
            self.buffer.put("ap_connect", "AP polling is already running")
            return
        self.running = True
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._loop, daemon=True)
        # Learn HVAC's own encryption/AP tunnel/Kalman state up front.
        ap_commands.read_hvac_state(self.buffer)
        self._thread.start()
        self.buffer.put("ap_connect", f"Starting AP polling at {self.url}")

    def stop(self):
        if not self.running:
            self.buffer.put("ap_connect", "AP polling is not running")
            return
        self.running = False
        if self._stop_event is not None:
            self._stop_event.set()
        self.buffer.defender_status.wake()
        if self._thread is not None:
            # A poll or command in flight can take up to its 3s request timeout.
            self._thread.join(timeout=max(self.interval_ms / 1000.0, 3) + 1)
        self._stop_event = None
        self._thread = None
        self.connected = False
        # Nothing is left to send these - fail them now, rather than having
        # their buttons keep showing a state the AP never got asked for.
        for command in self.buffer.defender_status.drop_commands():
            self.buffer.put(command.log_key, f"Not sent to AP ({command.endpoint}): AP polling stopped")
        self.buffer.put("ap_connect", "Stopped AP polling")

    def _loop(self):
        stop_event = self._stop_event
        status = self.buffer.defender_status
        next_poll = 0.0
        while not stop_event.is_set():
            while not stop_event.is_set() and (command := status.next_command()) is not None:
                self._send_command(command)
            if stop_event.is_set():
                break
            if time.monotonic() >= next_poll:
                self._poll_once()
                next_poll = time.monotonic() + self.interval_ms / 1000.0
            # Wakes early for a newly queued command (or stop()), so commands
            # go out immediately instead of waiting for the next poll.
            status.wait_for_command(max(0.0, next_poll - time.monotonic()))

    def _send_command(self, command):
        status = self.buffer.defender_status
        response = None
        try:
            resp = requests.post(f"{self.url}{command.endpoint}", json=command.payload, timeout=3)
            if resp.ok:
                try:
                    response = resp.json()
                except ValueError:
                    response = {}
            else:
                self.buffer.put(command.log_key, f"AP rejected {command.endpoint} (HTTP {resp.status_code})")
        except Exception as e:
            self.buffer.put(command.log_key, f"Failed to reach AP: {e}")
        status.finish_command(command, response)
        if response is not None and command.success_message:
            self.buffer.put(command.log_key, command.success_message)

    def _poll_once(self):
        was_connected = self.connected
        try:
            resp = requests.get(f"{self.url}/api/data", timeout=3)
            if resp.ok:
                self.buffer.put_poll(resp.json())
                self.connected = True
            else:
                self.connected = False
        except Exception:
            self.connected = False

        # Only log on a change of state - every poll succeeding/failing the
        # same way every 2s would otherwise spam the status console.
        if self.connected and not was_connected:
            self.buffer.put("ap_connect", f"Connected to {self.url}")
        elif was_connected and not self.connected:
            self.buffer.put("ap_connect", f"Lost connection to {self.url}")
