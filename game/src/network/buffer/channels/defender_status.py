'''
Flat table of the defender AP-poll's non-history fields: boolean flags
(anomaly detections, submarine_mode, encryption_status, ...) and the scalar
settings/revision numbers the sliders sync against. Everything here is
"latest value only" - unlike DefenderModbusBuffer, nothing is kept as a
history, since these are statuses rather than a numeric series to chart.

Also the one way *into* the AP: widgets queue commands here with send(),
and the shared APPoller (the only thing that ever talks to the AP) sends
them from its own thread, serialized with its polls, then writes whatever
the AP confirmed back into this same table. So every defender widget - no
matter which panel or page it lives on - issues commands through here and
reads status from here, and never needs a handle on the poller or its URL.
'''

from collections import deque
from dataclasses import dataclass, field
from threading import Event, Lock


@dataclass
class APCommand:
    '''
    One queued POST to the AP.

    confirm: {status_key: value} written into this table once the AP accepts
             the command. While it's queued/in flight, expected(status_key)
             already reports that value - so a button can show the state the
             user just asked for instead of flicking back to the old one
             until the AP answers.
    echo:    {response_field: status_key} copied out of the AP's JSON reply
             (e.g. /set_settings' settings_revision).
    log_key: status-console source the success/failure messages go under.
    '''
    endpoint: str
    payload: dict
    confirm: dict = field(default_factory=dict)
    echo: dict = field(default_factory=dict)
    log_key: str = "ap_connect"
    success_message: str | None = None

    def keys(self) -> set[str]:
        return set(self.confirm) | set(self.echo.values())


class DefenderStatusBuffer:

    def __init__(self):
        self.lock = Lock()
        # Commands deliberately survive reset() - a page rebuild resets the
        # buffer, and its widgets queue their initial settings pushes while
        # rebuilding; those still have to reach the AP.
        self._commands: deque[APCommand] = deque()
        self._current: APCommand | None = None
        self._command_event = Event()
        self.reset()

    def reset(self):
        with self.lock:
            self.values: dict[str, object] = {}

    def put(self, name: str, value):
        with self.lock:
            self.values[name] = value

    def get(self, name: str, default=None):
        with self.lock:
            return self.values.get(name, default)

    # ── Commands (widget side) ──────────────────────────────────────────

    def send(self, endpoint: str, payload: dict, confirm: dict | None = None, echo: dict | None = None,
             log_key: str = "ap_connect", success_message: str | None = None):
        '''
        Queues a POST for the AP poller to send. Consecutive commands to the
        same endpoint from the same source merge into one (every AP settings
        endpoint only applies the fields it's given, so a merged payload
        means the same thing) - otherwise dragging a slider would queue one
        round-trip per pixel.
        '''
        command = APCommand(endpoint, dict(payload), dict(confirm or {}), dict(echo or {}), log_key, success_message)
        with self.lock:
            last = self._commands[-1] if self._commands else None
            if last is not None and last.endpoint == endpoint and last.log_key == log_key:
                last.payload.update(command.payload)
                last.confirm.update(command.confirm)
                last.echo.update(command.echo)
                last.success_message = command.success_message
            else:
                self._commands.append(command)
        self._command_event.set()

    def expected(self, name: str, default=None):
        '''
        get(), except a value that a queued/in-flight command is about to
        confirm wins over the last confirmed one.
        '''
        with self.lock:
            for command in reversed(self._commands):
                if name in command.confirm:
                    return command.confirm[name]
            if self._current is not None and name in self._current.confirm:
                return self._current.confirm[name]
            return self.values.get(name, default)

    def in_flight(self, name: str) -> bool:
        '''True while any queued/in-flight command will write `name` on completion.'''
        with self.lock:
            if self._current is not None and name in self._current.keys():
                return True
            return any(name in command.keys() for command in self._commands)

    # ── Commands (APPoller side) ────────────────────────────────────────

    def next_command(self) -> APCommand | None:
        with self.lock:
            if not self._commands:
                return None
            self._current = self._commands.popleft()
            return self._current

    def finish_command(self, command: APCommand, response: dict | None):
        '''response is the AP's parsed JSON reply on success, None on failure.'''
        with self.lock:
            if response is not None:
                self.values.update(command.confirm)
                for response_field, status_key in command.echo.items():
                    if response_field in response:
                        self.values[status_key] = response[response_field]
            if self._current is command:
                self._current = None

    def drop_commands(self) -> list[APCommand]:
        with self.lock:
            dropped = list(self._commands)
            self._commands.clear()
            self._current = None
        return dropped

    def wait_for_command(self, timeout: float):
        '''Blocks up to `timeout` seconds, returning early when a command is queued (or wake() is called).'''
        self._command_event.wait(timeout)
        self._command_event.clear()

    def wake(self):
        self._command_event.set()
