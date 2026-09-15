'''
Analogue of ModbusBuffer for the defender page's AP-polled telemetry.

The AP reports already-decoded values directly over HTTP - there's no wire
packet to sniff, so this channel is fed straight by the (private) poll
unpacker instead of by MetaPacket. Values are split by named variable
("x", "theta", "temperature", ...) and one of five attributes, matching
what the AP's /api/data payload actually distinguishes:

    client_clean  - the client's own filtered reading
    client_noisy  - the client's raw pre-filter sensor reading
    server_clean  - the server's independently reported/estimated reading
    server_noisy  - reserved; the server never reports a noisy reading today
    target        - a fixed setpoint (target_x/target_y/target_temp)

Not every variable has every attribute (speed/rudder have no noisy reading,
HVAC's "temperature" has no server/noisy reading at all) - an attribute
that's never put() simply reads back as an empty history / None single.

Every put() call is given an absolute timestamp (AP-uptime clock for
submarine data, wall clock for HVAC's flat fields - see poll_unpacker),
but what actually gets stored is relative to that variable's own first
sample - the defender-page analogue of PacketBuffer.first_packet_time -
so a history always starts at (approximately) 0 instead of some huge
absolute clock value.
'''

from threading import Lock
from collections import deque
from time import time as wall_time

# HVAC's flat fields (see poll_unpacker._unpack_hvac) are the only ones
# whose relative-time advancement is gated by pause_hvac()/resume_hvac() -
# tied to whether DefenderHVACChart is actually the model on screen (see
# its start_animation/stop_animation). Submarine variables have no such
# gate: DefenderWorldMap doesn't pause them, so they always advance.
HVAC_VARIABLES = {"temperature", "heater"}


class DefenderModbusBuffer:

    def __init__(self, max_size: int = 5000):
        self.max_size = max_size
        self.lock = Lock()
        self.reset()

    def reset(self):
        with self.lock:
            self.histories: dict[str, dict[str, deque]] = {}
            self.singles: dict[str, dict[str, float | bool | None]] = {}

            # First-sample offset per variable (shared by all of that
            # variable's attributes, e.g. temperature's client_clean and
            # target both zero against the same reference) - only ever
            # latched by a put() that's actually allowed to advance the
            # clock (see _relative_time).
            self._first_time: dict[str, float] = {}

            # HVAC pause tracking. Starts paused: nothing should count as
            # elapsed HVAC history before the HVAC model has ever actually
            # been shown once (see resume_hvac) - paused_at starts at None
            # rather than "now" so that first resume_hvac() doesn't count
            # startup time (before the model was ever built) as a paused
            # gap to excise, which would otherwise nudge the first sample
            # a few microseconds negative instead of landing on exactly 0.
            # paused_at is a wall-clock moment (not the AP/HVAC clock
            # domain put() uses), since pause/resume happen from the UI
            # thread independent of polls.
            self._hvac_active = False
            self._hvac_paused_at: float | None = None
            self._hvac_paused_elapsed = 0.0
            self._hvac_frozen_time = 0.0

    def pause_hvac(self):
        '''
        Called when DefenderHVACChart stops animating - a different model
        is now on screen (or the panel's gone). Freezes "temperature"/
        "heater" history's relative-time advancement so an idle stretch
        with the HVAC model swapped out doesn't stretch a long gap across
        the chart once it's swapped back in; values keep getting recorded
        (a live readout table elsewhere still wants the latest reading),
        they just all land at the same frozen relative time until resumed.
        '''
        with self.lock:
            if self._hvac_active:
                self._hvac_active = False
                self._hvac_paused_at = wall_time()

    def resume_hvac(self):
        '''Called when DefenderHVACChart starts animating - see pause_hvac.'''
        with self.lock:
            if not self._hvac_active:
                self._hvac_active = True
                if self._hvac_paused_at is not None:
                    self._hvac_paused_elapsed += wall_time() - self._hvac_paused_at
                self._hvac_paused_at = None

    def _relative_time(self, variable: str, raw_time: float) -> float:
        '''Caller must hold self.lock.'''
        if variable in HVAC_VARIABLES and not self._hvac_active:
            return self._hvac_frozen_time

        if variable not in self._first_time:
            self._first_time[variable] = raw_time

        relative = raw_time - self._first_time[variable]
        if variable in HVAC_VARIABLES:
            relative -= self._hvac_paused_elapsed
            self._hvac_frozen_time = relative
        return relative

    def _slot(self, variable: str, attribute: str):
        '''Caller must hold self.lock.'''
        if variable not in self.histories:
            self.histories[variable] = {}
            self.singles[variable] = {}
        if attribute not in self.histories[variable]:
            self.histories[variable][attribute] = deque(maxlen=self.max_size)
            self.singles[variable][attribute] = None

    def put(self, variable: str, attribute: str, value, time: float):
        '''
        Records one sample, e.g. put("x", "client_clean", 101.15, 13303.0).
        time is an absolute clock reading (see module docstring) - stored
        relative to this variable's own first sample instead, and for HVAC
        variables, only advances while the HVAC model is actually active
        (see _relative_time/pause_hvac).

        Samples only arrive once per poll (every couple seconds), so a
        strip chart connecting them directly would draw a diagonal
        interpolating a change that never actually happened gradually -
        the value really just held steady until the new reading landed.
        Same fix as ModbusBuffer.put: re-stamp the previous value an
        instant before this one, so the line holds flat and then steps,
        staircase-style, instead of slanting.
        '''
        with self.lock:
            self._slot(variable, attribute)
            relative_time = self._relative_time(variable, time)
            history = self.histories[variable][attribute]
            if history:
                previous_value = history[-1][1]
                history.append((relative_time - 0.0000001, previous_value))
            history.append((relative_time, value))
            self.singles[variable][attribute] = value

    def get_single(self, variable: str, attribute: str):
        '''Returns the latest value for (variable, attribute), or None if there is no data.'''
        with self.lock:
            return self.singles.get(variable, {}).get(attribute)

    def get_history(self, variable: str, attribute: str) -> list[tuple[float, float]]:
        with self.lock:
            return list(self.histories.get(variable, {}).get(attribute, ()))

    def get_all_histories_and_legends(self, variable: str) -> dict[str, list[tuple[float, float]]]:
        '''
        Returns every attribute's history for one variable, keyed by attribute
        name - the key doubles as a strip chart's legend name, mirroring
        ModbusBuffer.get_all_histories_and_legends.
        '''
        with self.lock:
            return {attribute: list(history) for attribute, history in self.histories.get(variable, {}).items()}

    def variables(self) -> list[str]:
        with self.lock:
            return list(self.histories.keys())
