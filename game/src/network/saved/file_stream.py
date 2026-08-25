import base64
import json
import os
import queue
import threading

from tkinter.filedialog import asksaveasfilename

from ..buffer.meta_packet import MetaPacket

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...app_core import Context
    from ..buffer import Buffer


class FileStream:
    '''
    Streams MetaPackets to a JSON Lines file as they're produced, instead
    of snapshotting the packet buffer at save time. Records use the same
    line format as Replay's save/load format, so a streamed file can be
    reloaded with Replay.load_json.
    '''

    def __init__(self, buffer: "Buffer", context: "Context"):
        self.buffer = buffer
        self.context = context

        self._lock = threading.Lock()
        self._queue: queue.Queue = queue.Queue()
        self._worker_thread: threading.Thread | None = None

        self.is_streaming = False
        self.file_path = ""
        self._file = None

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def start(self):
        '''Button entry point: prompt for a file and start streaming.'''

        with self._lock:
            if self.is_streaming:
                self.buffer.put(
                    "json",
                    "A file stream is already running."
                )
                return

        file_path = self.select_save_path()

        if not file_path:
            return

        try:
            file = open(file_path, "w", encoding="utf-8")
        except Exception as e:
            self.buffer.put(
                "json",
                f"Failed to open stream file: {str(e)}"
            )
            return

        with self._lock:
            self.is_streaming = True
            self.file_path = file_path
            self._file = file
            self._queue = queue.Queue()
            self._worker_thread = threading.Thread(
                target=self.worker,
                daemon=True
            )
            self._worker_thread.start()

        self.buffer.put(
            "json",
            f"Streaming packets to {file_path}"
        )

    def stop(self):
        '''Button entry point: stop streaming and close the file.'''

        with self._lock:
            if not self.is_streaming:
                self.buffer.put(
                    "json",
                    "No active file stream to stop."
                )
                return

            self.is_streaming = False
            worker_thread = self._worker_thread
            filename = os.path.basename(self.file_path)
            self.file_path = ""

        # Wake the worker with a sentinel so it flushes the rest of the
        # queue and closes the file, instead of dropping queued packets.
        self._queue.put(None)

        if worker_thread is not None:
            worker_thread.join(timeout=2)

        self.buffer.put(
            "json",
            f"Stopped streaming to {filename}"
        )

    def select_save_path(self):
        '''Ask the user where to stream replay data.'''

        self.buffer.put("json", "Opening save dialog...")

        directory = self.context.paths.mcaptures

        file_path = asksaveasfilename(
            initialdir=directory,
            title="Choose where to stream JSON replay data",
            defaultextension=".jsonl",
            filetypes=[
                ("JSON Lines", "*.jsonl"),
                ("JSON", "*.json"),
                ("All files", "*.*"),
            ],
        )

        if not file_path:
            self.buffer.put("json", "Stream start cancelled")
            return ""

        return file_path

    # ------------------------------------------------------------------
    # Streaming
    # ------------------------------------------------------------------

    def put(self, mpkt: MetaPacket):
        '''Queue a MetaPacket to be written to the stream, if one is active.'''

        with self._lock:
            if not self.is_streaming:
                return
            self._queue.put(mpkt)

    def worker(self):
        '''Writes queued MetaPackets to disk until the stream is stopped.'''

        file = self._file

        while True:
            item = self._queue.get()

            if item is None:
                break

            self.write_record(file, item)

        try:
            file.close()
        except Exception as e:
            self.buffer.put(
                "json",
                f"Failed to close stream file: {str(e)}"
            )

        self._file = None

    def write_record(self, file, mpkt: MetaPacket):
        '''
        Append one MetaPacket to the stream file, in the same record
        format as Replay.write_json_file.
        '''

        pkt = mpkt.get("pkt")

        if pkt is None:
            return

        data = {
            "packet": base64.b64encode(
                bytes(pkt)
            ).decode("ascii"),

            "purpose": mpkt.get("purpose"),

            "producer": mpkt.get("hack"),

            "time": pkt.time,

            "direction": mpkt.get("direction"),
        }

        try:
            file.write(
                json.dumps(
                    data,
                    separators=(",", ":")
                )
                + "\n"
            )
            file.flush()
        except Exception as e:
            self.buffer.put(
                "json",
                f"Failed to write streamed packet: {str(e)}"
            )
