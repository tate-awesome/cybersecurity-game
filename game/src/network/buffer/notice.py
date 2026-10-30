'''
What a status can be besides a plain line of text - put by the network
actions through Buffer.put_error and Buffer.put_report, shown by the
status toasts (see widgets/frame_widgets/toasts.py):

    error  - one message, shown as written, with a fix to read (a key
             naming a file in assets/fixes - see FIXES)
    report - many lines an action gathered (an nmap scan's hosts, the
             Wi-Fi networks in range...), bundled into one Report by the
             action itself, shown as a one-line summary with the report
             behind it

The bundling is the producer's job, never the toasts': an action that
has a report builds one and puts it once, so nothing downstream has to
guess which lines belong together.

Plain python, no scapy or Qt - the privileged helper sends these too (see
helper/server.py's _BufferShim), as to_dict()'s plain dicts.
'''


# Every fix an error can name - a markdown file each, assets/fixes/<key>.md
FIXES = (
    "nmap_not_installed",
    "nmap_scan_failed",
    "no_network_connection",
    "ap_unreachable",
    "arp_host_not_found",
    "arp_spoof_failed",
    "ip_forwarding",
    "dos_failed",
    "nfq_failed",
    "windivert_failed",
    "sniffer_failed",
    "wifi_unavailable",
    "wifi_radio_off",
    "no_wifi_device",
    "wifi_network_not_found",
    "wifi_no_saved_profile",
    "wifi_connect_failed",
    "capture_file_failed",
)


class Report:
    '''
    A report's markdown, built up a block at a time - headings, text,
    lists and tables, in the order added. Put it with Buffer.put_report.
    '''

    def __init__(self, title: str):
        self.title = title
        self.blocks: list[str] = []

    def heading(self, text: str) -> "Report":
        self.blocks.append(f"### {self.escape(text)}")
        return self

    def text(self, text: str) -> "Report":
        self.blocks.append(self.escape(text))
        return self

    def facts(self, facts: dict[str, object]) -> "Report":
        '''Name: value lines - "Local IP: 192.168.1.15".'''
        self.blocks.append("\n".join(f"- **{self.escape(name)}:** {self.escape(str(value))}" for name, value in facts.items()))
        return self

    def bullets(self, items: list[str], empty: str = "None") -> "Report":
        self.blocks.append("\n".join(f"- {self.escape(str(item))}" for item in items) if items else f"*{self.escape(empty)}*")
        return self

    def table(self, headers: list[str], rows: list[list[object]], empty: str = "None") -> "Report":
        if not rows:
            self.blocks.append(f"*{self.escape(empty)}*")
            return self
        lines = ["| " + " | ".join(self.cell(header) for header in headers) + " |",
                 "|" + "---|" * len(headers)]
        lines += ["| " + " | ".join(self.cell(value) for value in row) + " |" for row in rows]
        self.blocks.append("\n".join(lines))
        return self

    def markdown(self) -> str:
        return "\n\n".join(self.blocks)

    @staticmethod
    def escape(text: str) -> str:
        '''Shown as typed - an SSID or hostname with * or _ in it isn't markup.'''
        for mark in ("\\", "*", "_", "`", "[", "]", "#", "|", "<"):
            text = text.replace(mark, "\\" + mark)
        return text

    @classmethod
    def cell(cls, value: object) -> str:
        return cls.escape(str(value)).replace("\n", " ")


class Notice:
    '''
    An error or a report, as the status buffer holds it (see
    StatusBuffer.put) - text is what the toast says, word for word.
    '''

    def __init__(self, kind: str, text: str, fix: str | None = None,
                 title: str | None = None, markdown: str | None = None):
        if kind == "error" and fix not in FIXES:
            raise ValueError(f"{fix!r} isn't one of notice.FIXES")
        self.kind = kind
        self.text = text
        self.fix = fix
        self.title = title
        self.markdown = markdown

    @classmethod
    def error(cls, text: str, fix: str) -> "Notice":
        return cls("error", text, fix=fix)

    @classmethod
    def report(cls, summary: str, report: Report) -> "Notice":
        return cls("report", summary, title=report.title, markdown=report.markdown())

    def to_dict(self) -> dict:
        '''Its fields as plain data - for the helper's pipe and the session recording.'''
        fields = {"kind": self.kind, "fix": self.fix, "title": self.title, "report": self.markdown}
        return {key: value for key, value in fields.items() if value is not None}

    @classmethod
    def from_dict(cls, text: str, fields: dict) -> "Notice | None":
        '''Back from to_dict - None for a plain status (or a fix this version doesn't have).'''
        kind = fields.get("kind")
        if kind == "report":
            return cls("report", text, title=fields.get("title"), markdown=fields.get("report", ""))
        if kind == "error" and fields.get("fix") in FIXES:
            return cls("error", text, fix=fields["fix"])
        return None
