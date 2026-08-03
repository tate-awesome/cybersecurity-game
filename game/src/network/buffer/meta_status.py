class MetaStatus:
    def __init__(self, hack: str, status: str, time: float, number: int):
        self.hack = hack
        self.status = status
        self.time = time
        self.number = number
    
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
