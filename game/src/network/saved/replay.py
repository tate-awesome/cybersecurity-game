import base64
import json
import os
import threading
import time

from scapy.all import Ether, IP

from tkinter.filedialog import asksaveasfilename

from ..buffer import Buffer
from ..buffer.meta_packet import MetaPacket

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...app_core import Context


class Replay:

    def __init__(self, buffer: Buffer, context: "Context"):
        self.buffer = buffer
        self.context = context

        self._is_loading = False
        self._lock = threading.Lock()

        self.abort_event = threading.Event()

        self.file_path = ""
        self.ptuples = []
        self.timed_playback = False


    # ------------------------------------------------------------------
    # Loading
    # ------------------------------------------------------------------

    def load_json(self, timed_playback: bool = False):
        """
        Button entry point for loading a replay file.

        timed_playback: if True, replay packets with the exact time
        spacing recorded in each packet's .time field instead of
        bursting them into the buffer as fast as capacity allows.
        """

        self.timed_playback = timed_playback

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

            self.read_json_file(file_path)

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

    def read_json_file(self, file_path):
        """
        Read replay records from disk.

        Each line contains:
            {
                "packet": "<base64>",
                "purpose": "...",
                "producer": "..."
            }
        """

        self.file_path = file_path
        self.ptuples = []

        self.buffer.put(
            "json",
            f"Reading replay packets from {file_path}..."
        )

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                for line_number, line in enumerate(file, start=1):

                    # Allow blank lines
                    if not line.strip():
                        continue

                    try:
                        data = json.loads(line)

                        raw_packet = base64.b64decode(
                            data["packet"]
                        )
                        source = data["producer"]
                        purpose = data["purpose"]


                        if source == "nfq":
                            pkt = IP(raw_packet)
                        else:
                            pkt = Ether(raw_packet)

                        # Parsing a packet from raw bytes resets .time
                        # to "now". Restore the originally recorded
                        # timestamp, if one was saved, so timed
                        # playback can reproduce the real spacing.
                        if "time" in data:
                            pkt.time = data["time"]

                        ptuple = (source, purpose, pkt)

                        self.ptuples.append(ptuple)

                    except Exception as e:
                        self.buffer.put(
                            "json",
                            f"Skipping invalid packet on line "
                            f"{line_number}: {e}"
                        )

        except Exception as e:
            self.buffer.put(
                "json",
                f"Failed to read JSON replay: {str(e)}"
            )

            with self._lock:
                self._is_loading = False

            return

        self.buffer.put(
            "json",
            f"Loaded {len(self.ptuples)} packets into memory. "
            f"Starting rate-limiter..."
        )

        worker_thread = threading.Thread(
            target=self.worker,
            daemon=True
        )

        worker_thread.start()

    # ------------------------------------------------------------------
    # Playback
    # ------------------------------------------------------------------

    def abort(self):
        """Request that the current replay be stopped."""

        with self._lock:
            self.reset_parameters()
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
        """Feed replay packets into the normal packet buffer."""
        if not self.ptuples or not self.file_path:
            with self._lock:
                self._is_loading = False
            return

        filename = os.path.basename(self.file_path)

        # Start with an empty buffer state.
        self.buffer.reset()

        if self.timed_playback:
            index, aborted_prematurely = self.worker_timed()
        else:
            index, aborted_prematurely = self.worker_burst()

        total_packets = len(self.ptuples)

        if aborted_prematurely:
            self.buffer.put(
                "json",
                f"JSON replay aborted. "
                f"Processed {index}/{total_packets} packets."
            )

        else:
            self.buffer.put(
                "json",
                f"Finished replaying {total_packets} packets "
                f"from {filename}"
            )

        self.reset_parameters()

        with self._lock:
            self._is_loading = False

    def worker_burst(self) -> tuple[int, bool]:
        """
        Feed packets into the buffer as fast as its capacity allows,
        ignoring their recorded time spacing.

        Returns (packets_processed, aborted_prematurely).
        """

        index = 0
        total_packets = len(self.ptuples)

        aborted_prematurely = False

        while index < total_packets:

            if self.abort_event.is_set():
                aborted_prematurely = True
                break

            time.sleep(0.01)

            if self.buffer.capacity() < 0.1:

                while (
                    self.buffer.capacity() < 0.9
                    and index < total_packets
                ):

                    if self.abort_event.is_set():
                        aborted_prematurely = True
                        break

                    ptuple = self.ptuples[index]

                    # Feed the MetaPacket into the normal buffer.
                    self.buffer.put(ptuple[0], ptuple[1], ptuple[2])
                    index += 1
                    # minimum gap
                    time.sleep(0.001)

                if aborted_prematurely:
                    break

        return index, aborted_prematurely

    def worker_timed(self) -> tuple[int, bool]:
        """
        Feed packets into the buffer one at a time, waiting between
        each one for the exact gap between the recorded .time values
        of consecutive packets.

        Returns (packets_processed, aborted_prematurely).
        """

        index = 0
        total_packets = len(self.ptuples)

        aborted_prematurely = False
        previous_time = None

        while index < total_packets:

            if self.abort_event.is_set():
                aborted_prematurely = True
                break

            ptuple = self.ptuples[index]
            pkt = ptuple[2]

            if previous_time is not None:
                delay = max(0.0, pkt.time - previous_time)

                # Wake up early if an abort is requested mid-wait.
                if self.abort_event.wait(delay):
                    aborted_prematurely = True
                    break

            self.buffer.put(ptuple[0], ptuple[1], pkt)

            previous_time = pkt.time
            index += 1

        return index, aborted_prematurely

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
                    }

                    file.write(
                        json.dumps(
                            data,
                            separators=(",", ":")
                        )
                        + "\n"
                    )

                    saved += 1

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
        self.ptuples = []