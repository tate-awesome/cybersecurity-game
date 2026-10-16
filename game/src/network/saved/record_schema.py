'''
The session record schema (v1): one JSON object per line, shared by the
rolling session recorder, clips, the file stream, and replay saves.

Every record carries:
    "v":   schema version (1)
    "seq": per-session sequence number - the order things happened in.
           Replay always follows file order, never re-sorts by "t" (NFQ
           pre/post pairs share a timestamp; only order disambiguates).
    "t":   absolute wall-clock time (packets: the capture time)
    "k":   the record kind, one of KINDS

Kinds and their own fields:
    hdr     first line of every segment and clip, so any file stands alone
            session, role ("student" | "instructor"), mode ("attacker" |
            "defender" | "dual" | ...), segment, filter, started
    pkt     a captured packet
            src (producer: "sniff", "nfq", "arp", ...), purpose,
            dir ("in" | "out" | "other" | null), link ("ether" | "ip"),
            raw (base64 bytes), len (original length - raw may be cut to
            a snaplen), modbus (bool, so clips can filter without dissecting)
    poll    one defender-side /api/data poll blob (see Buffer.put_poll)
            data
    status  a status-log line
            src, msg
    act     something the user did - started/stopped a network action,
            changed a form value, switched a page
            actor ("student" | "instructor"), name, args
    mark    a bookmark/annotation - an instructor's tutorial step, or a
            "clip from here" marker
            label, actor

Files saved before v1 (no "v": {"packet","purpose","producer","time",
"direction"}) still load - see decode().

Deliberately free of scapy and Qt imports, so the privileged helper can
write records itself (see network/helper).
'''
import base64
import json
import time

SCHEMA_VERSION = 1

KINDS = ("hdr", "pkt", "poll", "status", "act", "mark")


def dumps(record: dict) -> str:
    return json.dumps(record, separators=(",", ":"), default=str) + "\n"


def header(session: str, role: str, mode: str, segment: int = 0, record_filter: dict | None = None) -> dict:
    return {
        "v": SCHEMA_VERSION, "k": "hdr", "t": time.time(),
        "session": session, "role": role, "mode": mode,
        "segment": segment, "filter": record_filter or {},
    }


def packet(raw: bytes, t: float, src: str, purpose: str, direction: str | None,
           link: str = "ether", modbus: bool = False, snaplen: int | None = None) -> dict:
    kept = raw[:snaplen] if snaplen else raw
    return {
        "k": "pkt", "t": float(t), "src": src, "purpose": purpose, "dir": direction,
        "link": link, "raw": base64.b64encode(kept).decode("ascii"),
        "len": len(raw), "modbus": bool(modbus),
    }


def packet_from_meta(mpkt, snaplen: int | None = None) -> dict | None:
    '''
    A pkt record from a MetaPacket - live (scapy packet inside) or rebuilt
    from a helper payload (raw bytes inside, see MetaPacket.from_payload).
    '''
    raw = getattr(mpkt, "_raw", None)
    link = getattr(mpkt, "_link", None)
    t = getattr(mpkt, "_abs_time", None)
    if raw is None:
        pkt = mpkt.get("pkt")
        if pkt is None:
            return None
        raw = bytes(pkt)
        t = float(pkt.time)
        # IP-only packets come from the NFQ queue; everything else is Ethernet
        link = "ip" if mpkt.get("hack") == "nfq" else "ether"
    return packet(raw, t, mpkt.get("hack"), mpkt.get("purpose"), mpkt.get("direction"),
                  link or "ether", bool(mpkt.get("is_modbus")), snaplen)


def poll(data: dict, t: float | None = None) -> dict:
    return {"k": "poll", "t": t or time.time(), "data": data}


def status(src: str, msg: str, t: float | None = None) -> dict:
    return {"k": "status", "t": t or time.time(), "src": src, "msg": msg}


def action(name: str, args: dict | None = None, actor: str = "student", t: float | None = None) -> dict:
    return {"k": "act", "t": t or time.time(), "actor": actor, "name": name, "args": args or {}}


def mark(label: str, actor: str = "student", t: float | None = None) -> dict:
    return {"k": "mark", "t": t or time.time(), "actor": actor, "label": label}


def decode(line: str) -> dict | None:
    '''
    Parses one line into a v1 record, upgrading pre-v1 packet lines.
    Returns None for blank lines; raises on malformed ones.
    '''
    if not line.strip():
        return None
    data = json.loads(line)
    if "v" in data:
        return data
    # Pre-v1 packet line
    return {
        "v": 0, "k": "pkt", "t": data.get("time"), "src": data["producer"],
        "purpose": data["purpose"], "dir": data.get("direction"),
        "link": "ip" if data["producer"] == "nfq" else "ether",
        "raw": data["packet"], "modbus": False,
    }


def raw_bytes(record: dict) -> bytes:
    return base64.b64decode(record["raw"])


class RecordFilter:
    '''
    Decides which records are kept. Used twice: at record time, to keep the
    rolling log small, and at clip time, to cut a narrower export out of
    what was kept. Anything left as None lets everything through.

    kinds:       record kinds to keep, e.g. {"pkt", "act", "mark"}
    sources:     packet/status producers to keep, e.g. {"sniff", "nfq"}
    directions:  packet directions to keep, e.g. {"in", "out"}
    modbus_only: drop non-Modbus packets
    snaplen:     cut stored packet bytes to this many (record time only)
    '''

    def __init__(self, kinds=None, sources=None, directions=None, modbus_only: bool = False,
                 snaplen: int | None = None):
        self.kinds = set(kinds) if kinds else None
        self.sources = set(sources) if sources else None
        self.directions = set(directions) if directions else None
        self.modbus_only = modbus_only
        self.snaplen = snaplen

    def keeps(self, record: dict) -> bool:
        kind = record.get("k")
        if kind == "hdr":
            return True
        if self.kinds is not None and kind not in self.kinds:
            return False
        if kind in ("pkt", "status") and self.sources is not None and record.get("src") not in self.sources:
            return False
        if kind == "pkt":
            if self.directions is not None and record.get("dir") not in self.directions:
                return False
            if self.modbus_only and not record.get("modbus"):
                return False
        return True

    def to_dict(self) -> dict:
        return {
            "kinds": sorted(self.kinds) if self.kinds else None,
            "sources": sorted(self.sources) if self.sources else None,
            "directions": sorted(self.directions) if self.directions else None,
            "modbus_only": self.modbus_only, "snaplen": self.snaplen,
        }

    @classmethod
    def from_dict(cls, data: dict | None) -> "RecordFilter":
        return cls(**(data or {}))
