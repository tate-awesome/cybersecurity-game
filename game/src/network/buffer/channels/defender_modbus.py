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
'''

from threading import Lock
from collections import deque

class DefenderModbusBuffer:

    def __init__(self, max_size: int = 5000):
        self.max_size = max_size
        self.lock = Lock()
        self.reset()

    def reset(self):
        with self.lock:
            self.histories: dict[str, dict[str, deque]] = {}
            self.singles: dict[str, dict[str, float | bool | None]] = {}

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
        time is the AP's own received_at clock, not wall time, so history
        stays comparable across variables/attributes from the same poll.
        '''
        with self.lock:
            self._slot(variable, attribute)
            self.histories[variable][attribute].append((time, value))
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
