import base64
import json
import os
import threading

from scapy.all import Ether, IP

from tkinter.filedialog import asksaveasfilename

from ..process import Process
from ..buffer.meta_packet import MetaPacket

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


    # ------------------------------------------------------------------
    # Loading
    # ------------------------------------------------------------------

    def load_json(self):
        """
        Button entry point for loading a replay file.

        Packets are streamed off disk one line at a time and replayed
        with the exact time spacing recorded in each packet's .time
        field - the whole file is never held in memory at once.
        """

        with self._lock:
            if self._is_loading:
                self.buffer.put(
                    "json",
                    "Refused to load another JSON file at the same time."
                )
                return

            self._is_loading = True

        self.abort_event.clear()

        try:
            file_path = self.select_json_file()

            if not file_path:
                with self._lock:
                    self._is_loading = False
                return

            self.stream_json_file(file_path)

        except Exception as e:
            with self._lock:
                self._is_loading = False

            self.buffer.put(
                "json",
                f"Error during JSON loading: {str(e)}"
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

    def parse_line(self, line: str):
        """
        Parse one replay record line into a (source, purpose, pkt,
        direction) tuple.

        Each line contains:
            {
                "packet": "<base64>",
                "purpose": "...",
                "producer": "...",
                "time": <float, optional>,
                "direction": "in" | "out" | "other" | null, optional
            }
        """

        data = json.loads(line)

        raw_packet = base64.b64decode(data["packet"])
        source = data["producer"]
        purpose = data["purpose"]
        direction = data.get("direction")

        if source == "nfq":
            pkt = IP(raw_packet)
        else:
            pkt = Ether(raw_packet)

        # Parsing a packet from raw bytes resets .time to "now".
        # Restore the originally recorded timestamp, if one was saved,
        # so playback can reproduce the real spacing.
        if "time" in data:
            pkt.time = data["time"]

        # Pass the originally resolved direction back in as an explicit
        # override so replay doesn't depend on MAC-based inference,
        # which breaks on a different device's local MAC address.
        return (source, purpose, pkt, direction)

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
            # Start with an empty buffer state.
            self.buffer.reset()

            with open(self.file_path, "r", encoding="utf-8") as file:
                for line_number, line in enumerate(file, start=1):

                    if self.abort_event.is_set():
                        aborted_prematurely = True
                        break

                    # Allow blank lines
                    if not line.strip():
                        continue

                    try:
                        source, purpose, pkt, direction = self.parse_line(line)
                    except Exception as e:
                        self.buffer.put(
                            "json",
                            f"Skipping invalid packet on line "
                            f"{line_number}: {e}"
                        )
                        continue

                    if previous_time is not None:
                        delay = max(0.001, pkt.time - previous_time)

                        # Wake up early if an abort is requested mid-wait.
                        if self.abort_event.wait(delay):
                            aborted_prematurely = True
                            break

                    self.buffer.put(source, purpose, pkt, direction)

                    previous_time = pkt.time
                    index += 1

            if aborted_prematurely:
                self.buffer.put(
                    "json",
                    f"JSON replay aborted. Processed {index} packets."
                )

            else:
                self.buffer.put(
                    "json",
                    f"Finished replaying {index} packets from {filename}"
                )
        except Exception as e:
            # Without this, an uncaught exception here would leave _is_loading
            # stuck True forever, permanently blocking future loads.
            self.buffer.put("json", f"Error during JSON replay: {e}")
        finally:
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

        file_path = asksaveasfilename(
            initialdir=directory,
            title="Save JSON replay",
            defaultextension=".jsonl",
            filetypes=[
                ("JSON Lines", "*.jsonl"),
                ("JSON", "*.json"),
                ("All files", "*.*"),
            ],
        )

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

        Only the original/replayable packet information is stored:
            - raw Scapy packet
            - purpose
            - producer
            - capture time
            - direction (in/out/other, as resolved when captured)

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

                    pkt = mpkt.get("pkt")

                    if pkt is None:
                        continue

                    data = {
                        "packet": base64.b64encode(
                            bytes(pkt)
                        ).decode("ascii"),

                        "purpose": mpkt.get("purpose"),

                        "producer": mpkt.get("hack"),

                        "time": pkt.time,

                        "direction": mpkt.get("direction"),
                    }

                    file.write(
                        json.dumps(
                            data,
                            separators=(",", ":")
                        )
                        + "\n"
                    )

                    saved += 1

            # The app typically runs under sudo for raw-socket access,
            # so the file above would otherwise come out root-owned and
            # off-limits to the user who actually ran it.
            self.context.paths.lower_permissions(file_path)

            self.buffer.put(
                "json",
                f"Saved {saved} packets to {file_path}"
            )

        except Exception as e:
            self.buffer.put(
                "json",
                f"Failed to save JSON replay: {str(e)}"
            )

    # ------------------------------------------------------------------
    # Cleanup
    # ------------------------------------------------------------------

    def reset_parameters(self):
        self.file_path = ""