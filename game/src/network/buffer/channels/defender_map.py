'''
Composed (x, y) boat-path buffer for the defender page's AP-polled submarine
telemetry - analogous to MapBuffer, but keyed by the AP's own four
observation types instead of MetaPacket in/out. Bearing (theta) isn't a
position, so it stays in DefenderModbusBuffer - a widget wanting to draw a
boat reads its path here and its heading there, the same way WorldMap reads
paths from MapBuffer and bearing from ModbusBuffer (via MapBuffer).
'''

from threading import Lock
from collections import deque

class DefenderMapBuffer:

    PATHS = ("client_clean", "client_noisy", "server_clean", "server_noisy")

    def __init__(self, max_size: int = 5000):
        self.max_size = max_size
        self.lock = Lock()
        self.reset()

    def reset(self):
        with self.lock:
            self.paths: dict[str, deque] = {path: deque(maxlen=self.max_size) for path in self.PATHS}

    def put_point(self, path: str, x, y):
        if path not in self.PATHS or x is None or y is None:
            return
        with self.lock:
            self.paths[path].append((x, y))

    def get_path(self, path: str) -> list[tuple[float, float]]:
        with self.lock:
            return list(self.paths.get(path, ()))

    def get_latest(self, path: str) -> tuple[float, float] | None:
        with self.lock:
            points = self.paths.get(path)
            return points[-1] if points else None
