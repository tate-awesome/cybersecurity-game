'''
The rolling session log: a circular buffer on disk of everything a session
produced - packets, defender polls, status lines, user actions, and marks -
in the record_schema format.

On disk:
    <root>/<session id>/seg-000000.jsonl
                        seg-000001.jsonl ...

Each segment starts with a hdr record, so any segment (or clip) can be
replayed by itself. The writer rolls over to a new segment every
segment_seconds or segment_bytes, and drops whole segments, oldest first,
once they fall outside the forgetting window or the whole root grows past
max_bytes - including segments left behind by earlier sessions.

Callers only enqueue; JSON/base64 encoding and disk writes happen on the
writer thread. If the queue fills (disk slower than capture), records are
dropped and counted rather than stalling the capture thread.

Free of scapy and Qt imports, so the privileged helper can own one of these
for its own packets if the GUI-side writer can't keep up (see
network/helper/server.py).
'''
import os
import queue
import threading
import time
import uuid
from pathlib import Path

from . import record_schema as schema


class RetentionPolicy:
    '''
    window_seconds:  the forgetting window - segments whose newest record is
                     older than this are deleted (None: keep by age forever)
    max_bytes:       cap on the whole root, oldest segments go first
    segment_seconds: roll over to a new segment after this long
    segment_bytes:   ...or after this many bytes
    '''

    def __init__(self, window_seconds: float | None = 15 * 60, max_bytes: int = 256 * 1024 * 1024,
                 segment_seconds: float = 30, segment_bytes: int = 8 * 1024 * 1024):
        self.window_seconds = window_seconds
        self.max_bytes = max_bytes
        self.segment_seconds = segment_seconds
        self.segment_bytes = segment_bytes


class SessionRecorder:

    QUEUE_LIMIT = 50_000

    def __init__(self, root: Path, role: str = "student", mode: str = "attacker",
                 retention: RetentionPolicy | None = None, record_filter: schema.RecordFilter | None = None,
                 on_file_created=None):
        self.root = Path(root)
        self.role = role
        self.mode = mode
        self.retention = retention or RetentionPolicy()
        self.filter = record_filter or schema.RecordFilter()
        # Called with each new file/dir path - the GUI passes
        # paths.lower_permissions so sudo runs don't leave root-owned files
        self._on_file_created = on_file_created or (lambda path: None)

        self.session = ""
        self.paused = False
        self.dropped = 0

        self._queue: queue.Queue = queue.Queue(maxsize=self.QUEUE_LIMIT)
        self._write_lock = threading.Lock()  # held while writing/rotating, and while clipping
        self._thread: threading.Thread | None = None
        self._file = None
        self._segment = -1
        self._segment_started = 0.0
        self._segment_size = 0
        self._seq = 0
        self._last_poll: dict | None = None

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    @property
    def is_running(self) -> bool:
        return self._thread is not None and self._thread.is_alive()

    def start(self):
        if self.is_running:
            return
        self.session = time.strftime("%Y%m%d-%H%M%S-") + uuid.uuid4().hex[:6]
        self._segment = -1
        self._seq = 0
        self._last_poll = None
        self._queue = queue.Queue(maxsize=self.QUEUE_LIMIT)
        self._thread = threading.Thread(target=self._worker, daemon=True)
        self._thread.start()

    def stop(self):
        if not self.is_running:
            return
        self._queue.put(None)
        self._thread.join(timeout=2)
        self._thread = None

    def set_context(self, role: str | None = None, mode: str | None = None):
        '''Role/mode changes start a fresh segment so its header is accurate.'''
        self._enqueue(("ctx", role, mode))

    # ------------------------------------------------------------------
    # Recording - called from capture/worker threads; never blocks
    # ------------------------------------------------------------------

    def record(self, record: dict):
        self._enqueue(("rec", record))

    def record_meta(self, mpkt):
        '''A MetaPacket - encoded later, on the writer thread.'''
        self._enqueue(("meta", mpkt))

    def record_poll(self, data: dict):
        self.record(schema.poll(data))

    def record_status(self, src: str, msg: str):
        self.record(schema.status(src, msg))

    def record_action(self, name: str, args: dict | None = None, actor: str | None = None):
        self.record(schema.action(name, args, actor or self.role))

    def mark(self, label: str, actor: str | None = None):
        self.record(schema.mark(label, actor or self.role))

    def _enqueue(self, item):
        if self.paused or not self.is_running:
            return
        try:
            self._queue.put_nowait(item)
        except queue.Full:
            self.dropped += 1

    # ------------------------------------------------------------------
    # Writer thread
    # ------------------------------------------------------------------

    def _worker(self):
        while True:
            item = self._queue.get()
            if item is None:
                break
            try:
                with self._write_lock:
                    self._handle(item)
                    # Drain whatever else is waiting under the same lock
                    while True:
                        try:
                            item = self._queue.get_nowait()
                        except queue.Empty:
                            break
                        if item is None:
                            self._close_segment()
                            return
                        self._handle(item)
                    if self._file is not None:
                        self._file.flush()
            except Exception as error:
                print(f"Session recorder error: {error}")
        with self._write_lock:
            self._close_segment()

    def _handle(self, item):
        kind = item[0]
        if kind == "ctx":
            _, role, mode = item
            self.role = role or self.role
            self.mode = mode or self.mode
            self._close_segment()
            return
        if kind == "meta":
            record = schema.packet_from_meta(item[1], self.filter.snaplen)
            if record is None:
                return
        else:
            record = item[1]
        if not self.filter.keeps(record):
            return
        if record["k"] == "poll":
            self._last_poll = record
        self._write(record)

    def _write(self, record: dict):
        now = time.time()
        if (self._file is None
                or now - self._segment_started >= self.retention.segment_seconds
                or self._segment_size >= self.retention.segment_bytes):
            self._rotate(now)
        self._seq += 1
        record["v"] = schema.SCHEMA_VERSION
        record["seq"] = self._seq
        line = schema.dumps(record)
        self._file.write(line)
        self._segment_size += len(line)

    def _rotate(self, now: float):
        self._close_segment()
        session_dir = self.root / self.session
        if not session_dir.exists():
            session_dir.mkdir(parents=True, exist_ok=True)
            self._on_file_created(self.root)
            self._on_file_created(session_dir)
        self._segment += 1
        path = session_dir / f"seg-{self._segment:06d}.jsonl"
        self._file = open(path, "w", encoding="utf-8")
        self._on_file_created(path)
        self._segment_started = now
        line = schema.dumps(schema.header(self.session, self.role, self.mode, self._segment, self.filter.to_dict()))
        self._file.write(line)
        self._segment_size = len(line)
        # A segment that starts mid-session still needs the defender view's
        # current state to replay from - repeat the latest poll as a baseline
        if self._last_poll is not None:
            baseline = dict(self._last_poll, t=now)
            self._seq += 1
            line = schema.dumps(dict(baseline, v=schema.SCHEMA_VERSION, seq=self._seq, baseline=True))
            self._file.write(line)
            self._segment_size += len(line)
        self._prune(keep=path)

    def _close_segment(self):
        if self._file is not None:
            try:
                self._file.close()
            except Exception:
                pass
            self._file = None

    def _prune(self, keep: Path):
        '''Forget segments outside the window, then oldest-first down to max_bytes.'''
        segments = []
        for path in self.root.glob("*/seg-*.jsonl"):
            try:
                stat = path.stat()
            except OSError:
                continue
            segments.append((stat.st_mtime, stat.st_size, path))
        segments.sort()

        cutoff = time.time() - self.retention.window_seconds if self.retention.window_seconds else None
        total = sum(size for _, size, _ in segments)
        for mtime, size, path in segments:
            if path == keep:
                continue
            expired = cutoff is not None and mtime < cutoff
            if not expired and total <= self.retention.max_bytes:
                break
            try:
                path.unlink()
                total -= size
            except OSError:
                pass

        for session_dir in self.root.iterdir():
            if session_dir.is_dir() and session_dir.name != self.session and not any(session_dir.iterdir()):
                try:
                    session_dir.rmdir()
                except OSError:
                    pass

    # ------------------------------------------------------------------
    # Clips
    # ------------------------------------------------------------------

    def clip(self, out_path: Path, last_seconds: float | None = None, since: float | None = None,
             until: float | None = None, record_filter: schema.RecordFilter | None = None,
             session: str | None = None) -> int:
        '''
        Writes a standalone replay file of the records between since and
        until (or the last last_seconds), narrowed further by record_filter.
        Defaults to the current session. Returns the number of records kept.
        '''
        if last_seconds is not None:
            since = time.time() - last_seconds
        session = session or self.session
        export_filter = record_filter or schema.RecordFilter()
        segments = sorted((self.root / session).glob("seg-*.jsonl"))

        # Hold the write lock so the open segment is flushed and not mid-line
        with self._write_lock:
            if self._file is not None:
                self._file.flush()
            kept = 0
            baseline = None
            role, mode = self.role, self.mode
            with open(out_path, "w", encoding="utf-8") as out:
                header_written = False
                for segment in segments:
                    with open(segment, encoding="utf-8") as file:
                        for line in file:
                            try:
                                record = schema.decode(line)
                            except Exception:
                                continue  # a torn last line from a crash
                            if record is None:
                                continue
                            if record["k"] == "hdr":
                                role, mode = record.get("role", role), record.get("mode", mode)
                                continue
                            t = record.get("t") or 0
                            if since is not None and t < since:
                                if record["k"] == "poll":
                                    baseline = record
                                continue
                            if until is not None and t > until:
                                break
                            if not header_written:
                                clip_header = schema.header(session, role, mode, 0, export_filter.to_dict())
                                clip_header.update(clip=True, since=since, until=until)
                                out.write(schema.dumps(clip_header))
                                if baseline is not None and export_filter.keeps(baseline):
                                    out.write(schema.dumps(dict(baseline, t=t, baseline=True)))
                                header_written = True
                            if export_filter.keeps(record):
                                out.write(schema.dumps(record))
                                kept += 1
        self._on_file_created(Path(out_path))
        return kept

    def sessions(self) -> list[str]:
        '''Session ids still on disk, oldest first - for an instructor picking one to review.'''
        if not self.root.exists():
            return []
        return sorted(path.name for path in self.root.iterdir() if path.is_dir())

    def disk_usage(self) -> int:
        return sum(path.stat().st_size for path in self.root.glob("*/seg-*.jsonl") if path.exists())
