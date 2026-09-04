'''
Polls a defender AP's /api/data endpoint on a background thread and hands
each response straight to Buffer.put_poll(). Unlike the attacker-side
hardware Processes, this doesn't need scapy or raw sockets - it's a plain
HTTP GET loop - but it's exactly the same kind of thing: a widget starts it,
it has to keep running across a page refresh, and whatever widget gets
rebuilt has to be able to reclaim it through context.process_manager instead
of losing track of it.
'''

import threading
import requests

from ..process import Process

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
            return
        self.running = True
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self):
        if not self.running:
            return
        self.running = False
        if self._stop_event is not None:
            self._stop_event.set()
        if self._thread is not None:
            self._thread.join(timeout=self.interval_ms / 1000.0 + 1)
        self._stop_event = None
        self._thread = None
        self.connected = False

    def _loop(self):
        stop_event = self._stop_event
        while not stop_event.is_set():
            self._poll_once()
            stop_event.wait(self.interval_ms / 1000.0)

    def _poll_once(self):
        try:
            resp = requests.get(f"{self.url}/api/data", timeout=3)
            if resp.ok:
                self.buffer.put_poll(resp.json())
                self.connected = True
            else:
                self.connected = False
        except Exception:
            self.connected = False
