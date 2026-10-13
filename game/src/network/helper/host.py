'''
The GUI side of the privileged helper (see server.py for the other side).

PrivilegedHelper owns the helper's lifecycle: it launches the elevated
process, hands it a one-time key over a permission-restricted file, accepts
the connection it makes back, and from then on feeds everything the helper
reports into the real Buffer. A capability hosted by the helper is used
through proxy(name), which looks exactly like an in-process action to the
forms (start/stop/is_running) but forwards over the connection.

Enabled by a single preference ("network_helper"): on at startup starts the
helper straight away; the Performance settings tab toggles it live.

Imports only the standard library and launch.py - no scapy, no Qt - so the
GUI can hold one of these without pulling the capture stack into its process.
'''
import json
import os
import secrets
import stat
import threading

from multiprocessing.connection import Listener

from .launch import spawn

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...app_core import Context

import sys

ACCEPT_TIMEOUT = 30.0  # s to wait for the elevated helper to connect back


class _Proxy:
    '''An in-process stand-in for a capability the helper hosts - same contract the forms use for a real one.'''

    def __init__(self, helper: "PrivilegedHelper", name: str):
        self._helper = helper
        self._name = name

    def start(self, *args, **kwargs):
        self._helper._send({"op": "start", "name": self._name, "args": list(args), "kwargs": kwargs})

    def stop(self):
        self._helper._send({"op": "stop", "name": self._name})

    def is_running(self) -> bool:
        return self._helper._status.get(self._name, False)


class PrivilegedHelper:
    PREFERENCE = "network_helper"
    # Capabilities routed through the helper when it's on. Others keep
    # running in-process (see BaseForm.get_process); NFQ stays in-process -
    # its modbus-modify path needs the GUI's TransactionManager and settings.
    CAPABILITIES = {"sniff"}

    def __init__(self, context: "Context"):
        self.context = context
        self.buffer = context.buffer
        self._listener: Listener | None = None
        self._conn = None
        self._process = None
        self._status: dict[str, bool] = {}
        self._proxies: dict[str, _Proxy] = {}
        self._send_lock = threading.Lock()
        self._connected = False
        self._starting = False
        if self.enabled:
            self.start()

    @property
    def enabled(self) -> bool:
        return bool(self.context.preferences.get(self.PREFERENCE))

    @property
    def connected(self) -> bool:
        return self._connected

    def hosts(self, name: str) -> bool:
        '''Whether `name` should run in the helper right now (a known capability, and the helper is up).'''
        return name in self.CAPABILITIES and self._connected

    def proxy(self, name: str) -> _Proxy:
        if name not in self._proxies:
            self._proxies[name] = _Proxy(self, name)
        return self._proxies[name]

    # Lifecycle
    def set_enabled(self, on: bool):
        self.context.preferences.set(self.PREFERENCE, bool(on))
        if on:
            self.start()
        else:
            self.stop()

    def start(self):
        if self._connected or self._starting:
            return
        self._starting = True
        key = secrets.token_hex(32)
        try:
            # Same bytes the helper derives from the hex key (see server.run)
            self._listener = Listener(("127.0.0.1", 0), authkey=bytes.fromhex(key))
        except Exception as error:
            self._log(f"helper: could not open a local listener: {error}")
            self._starting = False
            return
        port = self._listener.address[1]
        handshake_path = self._write_handshake(port, key)
        try:
            self._process = spawn(self._argv(handshake_path))
        except Exception as error:
            self._log(f"helper: launch failed (elevation declined?): {error}")
            self._close_listener()
            self._cleanup_handshake(handshake_path)
            self._starting = False
            return
        threading.Thread(target=self._accept, args=(handshake_path,), daemon=True).start()

    def stop(self):
        self._send({"op": "shutdown"})
        conn, self._conn = self._conn, None
        self._connected = False
        self._status.clear()
        if conn is not None:
            try:
                conn.close()
            except Exception:
                pass
        self._close_listener()
        process, self._process = self._process, None
        if process is not None and process.poll() is None:
            process.terminate()

    # Connection
    def _accept(self, handshake_path: str):
        watchdog = threading.Timer(ACCEPT_TIMEOUT, self._close_listener)
        watchdog.start()
        try:
            conn = self._listener.accept()
        except Exception as error:
            self._log(f"helper: no connection from the helper process: {error}")
            self._cleanup_handshake(handshake_path)
            self._starting = False
            return
        finally:
            watchdog.cancel()
        self._conn = conn
        self._connected = True
        self._starting = False
        self._cleanup_handshake(handshake_path)
        self._log("Privileged helper connected.")
        threading.Thread(target=self._reader, daemon=True).start()

    def _reader(self):
        conn = self._conn
        while conn is not None:
            try:
                message = conn.recv()
            except (EOFError, OSError):
                break
            event = message.get("ev")
            if event == "buf":
                for kind, source, purpose, payload, direction in message["batch"]:
                    if kind == "pkt":
                        self.buffer.put_payload(source, purpose, payload, direction)
                    else:
                        self.buffer.put(source, purpose, None, direction)
            elif event == "status":
                self._status[message["name"]] = bool(message["running"])
            elif event == "log":
                self._log(message.get("text", ""))
        self._connected = False
        self._status.clear()

    def _send(self, message: dict):
        with self._send_lock:
            conn = self._conn
            if conn is None:
                return
            try:
                conn.send(message)
            except Exception as error:
                self._log(f"helper: lost connection: {error}")
                self._conn = None
                self._connected = False

    # Handshake file: port + one-time key, readable only by this user, read
    # and deleted by the helper (see server.run). The port isn't secret; the
    # key is what authenticates the connection, so it never goes on a command
    # line (visible to other processes) - only into this file.
    def _write_handshake(self, port: int, key: str) -> str:
        directory = self.context.paths.user_data
        os.makedirs(directory, exist_ok=True)
        path = os.path.join(directory, f"helper_handshake_{secrets.token_hex(8)}.json")
        descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, stat.S_IRUSR | stat.S_IWUSR)
        with os.fdopen(descriptor, "w", encoding="utf-8") as file:
            json.dump({"port": port, "key": key}, file)
        return path

    def _cleanup_handshake(self, path: str):
        try:
            if os.path.exists(path):
                os.unlink(path)
        except OSError:
            pass

    def _argv(self, handshake_path: str) -> list[str]:
        if getattr(sys, "frozen", False):
            return [sys.executable, "--helper", "--handshake", handshake_path]
        main_script = os.path.abspath(sys.argv[0])
        return [sys.executable, main_script, "--helper", "--handshake", handshake_path]

    def _close_listener(self):
        listener, self._listener = self._listener, None
        if listener is not None:
            try:
                listener.close()
            except Exception:
                pass

    def _log(self, text: str):
        if text:
            self.buffer.put("helper", text)
