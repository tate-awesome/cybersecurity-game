'''
Flat table of the defender AP-poll's non-history fields: boolean flags
(anomaly detections, submarine_mode, encryption_status, ...) and the scalar
settings/revision numbers the sliders sync against. Everything here is
"latest value only" - unlike DefenderModbusBuffer, nothing is kept as a
history, since these are statuses rather than a numeric series to chart.
'''

from threading import Lock

class DefenderStatusBuffer:

    def __init__(self):
        self.lock = Lock()
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
