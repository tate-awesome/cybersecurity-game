'''
The privileged helper process (the "--helper" side).

Runs elevated, started by the GUI (see host.PrivilegedHelper and launch.spawn).
It reads the one-time handshake file the GUI wrote (port + key), deletes it,
connects back to the GUI over a localhost socket with HMAC auth
(multiprocessing.connection), and then:

  - hosts the privileged capabilities (see registry) the GUI asks it to
    start/stop, each running here with its own GIL, so packet dissection no
    longer competes with the GUI thread;
  - forwards everything those capabilities report - packets as compact
    MetaPacket payloads, status lines as text - back to the GUI in batches;
  - on the GUI going away (connection closed, GUI crashed) or a shutdown
    command, stops every capability before exiting, so nothing privileged is
    left running and no system state (once arp/nfq move here) is left changed.

Imports scapy and the hardware modules; never imports Qt.
'''
import json
import os
import threading
import time

from multiprocessing.connection import Client
from scapy.all import Ether, Packet

from ..buffer.meta_packet import MetaPacket
from .registry import build_capability

FLUSH_INTERVAL = 0.06   # s between batches sent to the GUI
STATUS_INTERVAL = 0.5   # s between status heartbeats (so self-finishing actions report back)


class _BufferShim:
    '''
    Stands in for the real Buffer where a capability expects one. Instead of
    distributing packets into channel buffers, it turns each put() into a
    picklable item and batches it for the GUI, which feeds its own real
    Buffer (see host.PrivilegedHelper._reader). A live scapy packet becomes a
    MetaPacket.to_payload() snapshot - built here, on the helper's GIL;
    a status (no packet) becomes a plain text item.
    '''

    def __init__(self):
        self._batch: list[tuple] = []
        self._lock = threading.Lock()

    def put(self, source: str, purpose: str, data: Packet | None = None, direction: str | None = None):
        if isinstance(data, Packet):
            link = "ether" if data.haslayer(Ether) else "ip"
            payload = MetaPacket(data, 0.0, 0, source, purpose, direction).to_payload(link=link)
            item = ("pkt", source, purpose, payload, direction)
        else:
            item = ("status", source, purpose, None, direction)
        with self._lock:
            self._batch.append(item)
        return None  # the GUI assigns packet numbers and builds transactions

    def drain(self) -> list[tuple]:
        with self._lock:
            batch, self._batch = self._batch, []
        return batch


class _ContextStub:
    '''A placeholder context for capabilities that don't need the GUI's real one (the sniffer doesn't).'''


def run(handshake_path: str):
    with open(handshake_path, encoding="utf-8") as file:
        handshake = json.load(file)
    try:
        os.unlink(handshake_path)  # one-time use - don't leave the key on disk
    except OSError:
        pass

    conn = Client(("127.0.0.1", handshake["port"]), authkey=bytes.fromhex(handshake["key"]))
    shim = _BufferShim()
    context = _ContextStub()
    capabilities: dict[str, object] = {}
    stop = threading.Event()
    send_lock = threading.Lock()

    def send(message: dict) -> bool:
        with send_lock:
            try:
                conn.send(message)
                return True
            except Exception:
                stop.set()
                return False

    def flusher():
        while not stop.is_set():
            batch = shim.drain()
            if batch:
                send({"ev": "buf", "batch": batch})
            time.sleep(FLUSH_INTERVAL)

    def status_heartbeat():
        while not stop.is_set():
            for name, capability in list(capabilities.items()):
                send({"ev": "status", "name": name, "running": bool(capability.is_running())})
            time.sleep(STATUS_INTERVAL)

    threading.Thread(target=flusher, daemon=True).start()
    threading.Thread(target=status_heartbeat, daemon=True).start()

    try:
        while not stop.is_set():
            try:
                message = conn.recv()
            except (EOFError, OSError):
                break  # GUI closed the connection or went away
            if _dispatch(message, capabilities, shim, context, send):
                break  # shutdown
    finally:
        stop.set()
        for capability in capabilities.values():
            try:
                capability.stop()
            except Exception:
                pass
        remaining = shim.drain()
        if remaining:
            try:
                conn.send({"ev": "buf", "batch": remaining})
            except Exception:
                pass
        try:
            conn.close()
        except Exception:
            pass


def _dispatch(message: dict, capabilities, shim, context, send) -> bool:
    '''Handles one GUI command. Returns True to shut the helper down.'''
    operation = message.get("op")
    if operation == "shutdown":
        return True
    name = message.get("name")
    if operation == "start":
        capability = capabilities.get(name)
        if capability is None:
            try:
                capability = build_capability(name, shim, context)
            except Exception as error:
                send({"ev": "log", "source": name, "text": f"helper has no capability {name!r}: {error}"})
                return False
            capabilities[name] = capability
        try:
            capability.start(*message.get("args", []), **message.get("kwargs", {}))
        except Exception as error:
            send({"ev": "log", "source": name, "text": f"helper failed to start {name}: {error}"})
        send({"ev": "status", "name": name, "running": bool(capability.is_running())})
    elif operation == "stop":
        capability = capabilities.get(name)
        if capability is not None:
            try:
                capability.stop()
            except Exception as error:
                send({"ev": "log", "source": name, "text": f"helper failed to stop {name}: {error}"})
            send({"ev": "status", "name": name, "running": bool(capability.is_running())})
    return False


def run_from_argv(argv: list[str]):
    '''Entry point for `main.py --helper --handshake <path>`.'''
    path = None
    for index, argument in enumerate(argv):
        if argument == "--handshake" and index + 1 < len(argv):
            path = argv[index + 1]
    if not path:
        print("helper: missing --handshake <path>")
        return
    try:
        run(path)
    except Exception as error:
        print(f"helper: fatal error: {error}")
