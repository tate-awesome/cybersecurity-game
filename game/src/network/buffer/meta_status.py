from .notice import Notice


class MetaStatus:
    '''
    One status: a plain line (kind "status"), or an error or report (see
    notice.py) - status is what the toast says either way.
    '''
    def __init__(self, hack: str, status: "str | Notice", time: float, number: int):
        self.hack = hack
        self.notice = status if isinstance(status, Notice) else None
        self.status = status.text if isinstance(status, Notice) else status
        self.time = time
        self.number = number

    @property
    def kind(self) -> str:
        return self.notice.kind if self.notice is not None else "status"

    def get_line(self, max_length=80) -> str:
        from datetime import datetime

        # --- format time ---
        dt = datetime.fromtimestamp(self.time)
        time_str = dt.strftime("%S.%f")[:-3]  # HH:MM:SS.SSS

        # --- prefix ---
        prefix = f"{self.number} {time_str} [{self.hack}] "
        return f"{prefix}{self.status}"

    def __str__(self) -> str:
        return self.get_line()
