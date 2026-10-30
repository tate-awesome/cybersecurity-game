import os
import threading

from ..buffer.link import dissect
from ..buffer.notice import Notice


from ..process import Process
from . import record_schema as schema

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...app_core import Context
    from ..buffer import Buffer


class Replay(Process):

    def __init__(self, buffer: "Buffer", context: "Context"):
        super().__init__(buffer, context)

        self._is_loading = False
        self._lock = threading.Lock()

        self.abort_event = threading.Event()

        self.file_path = ""
        self.realtime = True
        self.record_filter = schema.RecordFilter()


    # ------------------------------------------------------------------
    # Loading
    # ------------------------------------------------------------------

    def load_json(self, realtime: bool = True, record_filter: schema.RecordFilter | None = None,
                  file_path: str | None = None):
        """
        Button entry point for loading a replay file.

        A file can hold every record kind (see record_schema); record_filter
        picks which parts this button replays - e.g. RecordFilter(kinds={"pkt"})
        for just the capture, {"poll"} for just the defender view, or
        {"act", "mark", "status"} for an instructor's tutorial steps.
        file_path skips the dialog (e.g. a clip that was just made).

        Packets are streamed off disk one line at a time and replayed
        with the exact time spacing recorded in each packet's .time
        field - or with realtime=False, as fast as the buffer takes them.
        The whole file is never held in memory at once.
        """

        with self._lock:
            if self._is_loading:
                self.buffer.put(
                    "json",
                    "Refused to load another JSON file at the same time."
                )
                return

            self._is_loading = True

        self.realtime = realtime
        self.record_filter = record_filter or schema.RecordFilter()
        self.abort_event.clear()

        try:
            file_path = file_path or self.select_json_file()

            if not file_path:
                with self._lock:
                    self._is_loading = False
                return

            self.stream_json_file(file_path)

        except Exception as e:
            with self._lock:
                self._is_loading = False

            self.buffer.put_error(
                "json",
                f"Error during JSON loading: {e!s}",
                "capture_file_failed",
            )

    def select_json_file(self):
        """Ask the user to select a replay JSONL file."""

        self.buffer.put("json", "Opening JSON file dialog...")

        directory = self.context.paths.mcaptures

        file_path = self.context.paths.select_path(
            directory,
            "Select a JSON replay file",
            [("jsonl", "*.jsonl")]
        )

        if file_path is None:
            self.buffer.put("json", "No file selected")
            return ""

        self.buffer.put(
            "json",
            f"Selected file: {file_path}"
        )

        return file_path

    def stream_json_file(self, file_path):
        """Start streaming a replay file off disk on a worker thread."""

        self.file_path = file_path

        self.buffer.put(
            "json",
            f"Streaming replay packets from {file_path}..."
        )

        worker_thread = threading.Thread(
            target=self.worker,
            daemon=True
        )

        worker_thread.start()

    def build_packet(self, record: dict):
        """Rebuild the scapy packet from a pkt record (see record_schema)."""

        raw_packet = schema.raw_bytes(record)

        pkt = dissect(raw_packet, record.get("link") or "ether")

        # Parsing a packet from raw bytes resets .time to "now".
        # Restore the originally recorded timestamp, if one was saved,
        # so playback can reproduce the real spacing.
        if record.get("t") is not None:
            pkt.time = record["t"]

        return pkt

    def post_record(self, record: dict):
        """
        Feed one record back into the buffer the way it first arrived.

        Packets pass their originally resolved direction back in as an
        explicit override so replay doesn't depend on MAC-based inference,
        which breaks on a different device's local MAC address.
        """

        kind = record["k"]

        if kind == "pkt":
            self.buffer.put(record["src"], record["purpose"], self.build_packet(record), record.get("dir"))
        elif kind == "poll":
            self.buffer.put_poll(record["data"])
        elif kind == "status":
            notice = Notice.from_dict(record["msg"], record)
            if notice is not None:
                self.buffer.put_notice(record["src"], notice)
            else:
                self.buffer.put(record["src"], record["msg"])
        elif kind == "act":
            self.buffer.put("replay", f"[{record.get('actor', '?')}] {record['name']} {record.get('args') or ''}")
        elif kind == "mark":
            self.buffer.put("replay", f"[{record.get('actor', '?')} mark] {record['label']}")

    # ------------------------------------------------------------------
    # Playback
    # ------------------------------------------------------------------

    def stop(self):
        """Request that the current replay be stopped."""

        with self._lock:
            if not self._is_loading:
                self.buffer.put(
                    "json",
                    "No active JSON loading process to abort."
                )
                return

            self.abort_event.set()

            self.buffer.put(
                "json",
                "Abort requested. Stopping replay thread..."
            )

    def worker(self):
        """
        Stream replay packets off disk one line at a time and feed
        them into the normal packet buffer, waiting between each one
        for the exact gap between the recorded .time values of
        consecutive packets.

        Packets are always posted in file order, never sorted or
        reordered by .time - NFQ pre/post-modification pairs routinely
        share the exact same recorded timestamp, and the file's own
        line order is the only thing that disambiguates which one
        happened first.
        """

        if not self.file_path:
            with self._lock:
                self._is_loading = False
            return

        filename = os.path.basename(self.file_path)

        index = 0
        aborted_prematurely = False
        previous_time = None

        try:
            # Start with an empty buffer state, and keep the replay out of
            # the session log - it's already on disk.
            self.buffer.reset()
            self.buffer.recorder.paused = True

            with open(self.file_path, encoding="utf-8") as file:
                for line_number, line in enumerate(file, start=1):

                    if self.abort_event.is_set():
                        aborted_prematurely = True
                        break

                    try:
                        record = schema.decode(line)
                    except Exception as e:
                        self.buffer.put(
                            "json",
                            f"Skipping invalid record on line "
                            f"{line_number}: {e}"
                        )
                        continue

                    # Blank lines, headers, and parts this button doesn't load
                    if record is None or record["k"] == "hdr" or not self.record_filter.keeps(record):
                        continue

                    record_time = record.get("t")

                    if self.realtime and previous_time is not None and record_time is not None:
                        delay = max(0.001, record_time - previous_time)

                        # Wake up early if an abort is requested mid-wait.
                        if self.abort_event.wait(delay):
                            aborted_prematurely = True
                            break

                    # Not real-time: as fast as the buffer takes them -
                    # wait while its put queue is nearly full
                    while not self.realtime and self.buffer.capacity() > 0.9:
                        if self.abort_event.wait(0.01):
                            aborted_prematurely = True
                            break
                    if aborted_prematurely:
                        break

                    try:
                        self.post_record(record)
                    except Exception as e:
                        self.buffer.put("json", f"Skipping invalid record on line {line_number}: {e}")
                        continue

                    if record_time is not None:
                        previous_time = record_time
                    index += 1

            if aborted_prematurely:
                self.buffer.put(
                    "json",
                    f"JSON replay aborted. Processed {index} records."
                )

            else:
                self.buffer.put(
                    "json",
                    f"Finished replaying {index} records from {filename}"
                )
        except Exception as e:
            # Without this, an uncaught exception here would leave _is_loading
            # stuck True forever, permanently blocking future loads.
            self.buffer.put_error("json", f"Error during JSON replay: {e}", "capture_file_failed")
        finally:
            self.buffer.recorder.paused = False
            self.reset_parameters()

            with self._lock:
                self._is_loading = False

    # ------------------------------------------------------------------
    # Saving
    # ------------------------------------------------------------------

    def save_json(self):
        """Button entry point for saving the current packet buffer."""

        with self._lock:
            if self._is_loading:
                self.buffer.put(
                    "json",
                    "Cannot save while a replay is loading."
                )
                return

        file_path = self.select_save_path()

        if not file_path:
            return

        self.write_json_file(file_path)

    def select_save_path(self):
        """Ask the user where to save the replay file."""

        self.buffer.put(
            "json",
            "Opening save dialog..."
        )

        directory = self.context.paths.mcaptures

        from ...app_core.context.paths import file_dialog  # here - app_core imports the network package
        file_path = file_dialog("Save JSON replay", directory,
                                "JSON Lines (*.jsonl);;JSON (*.json);;All files (*.*)", save=True) or ""

        # Qt doesn't auto-append the filter's extension the way tkinter's
        # defaultextension did, so add it back when the user typed a bare
        # filename.
        if file_path and not os.path.splitext(file_path)[1]:
            file_path += ".jsonl"

        if not file_path:
            self.buffer.put(
                "json",
                "Save cancelled"
            )
            return ""

        self.buffer.put(
            "json",
            f"Saving replay to {file_path}"
        )

        return file_path

    def write_json_file(self, file_path):
        """
        Write the current buffer to a JSON Lines replay file.

        Only the original/replayable packet information is stored, as v1
        pkt records (see record_schema): raw bytes, purpose, producer,
        capture time, and direction as resolved when captured.

        Derived/enriched information is intentionally not saved.
        """

        try:
            meta_packets = list(self.buffer.packets.buffer)

            saved = 0

            with open(
                file_path,
                "w",
                encoding="utf-8"
            ) as file:

                for mpkt in meta_packets:

                    record = schema.packet_from_meta(mpkt)

                    if record is None:
                        continue

                    saved += 1
                    record["v"] = schema.SCHEMA_VERSION
                    record["seq"] = saved
                    file.write(schema.dumps(record))

            # The app typically runs under sudo for raw-socket access,
            # so the file above would otherwise come out root-owned and
            # off-limits to the user who actually ran it.
            self.context.paths.lower_permissions(file_path)

            self.buffer.put(
                "json",
                f"Saved {saved} packets to {file_path}"
            )

        except Exception as e:
            self.buffer.put_error(
                "json",
                f"Failed to save JSON replay: {e!s}",
                "capture_file_failed",
            )

    # ------------------------------------------------------------------
    # Cleanup
    # ------------------------------------------------------------------

    def reset_parameters(self):
        self.file_path = ""