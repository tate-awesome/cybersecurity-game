factors = {
    "x": 100.0,
    "y": 100.0,
    "theta": 1000.0,
    "speed": 4095.0 / 5.0,
    "rudder": 4095.0 / 5.0
            }

class ModTable:
    def __init__(self):
        self.table = {}

        for var in ["x", "y", "theta", "speed", "rudder"]:
            type = "mult"
            key = f"{var}_{type}"
            self.table[key] = 1.0
            type = "offset"
            key = f"{var}_{type}"
            self.table[key] = 0.0

    def reset_table(self):
        for var in ["x", "y", "theta", "speed", "rudder"]:
            type = "mult"
            key = f"{var}_{type}"
            self.table[key] = 1.0
            type = "offset"
            key = f"{var}_{type}"
            self.table[key] = 0.0

    def set(self, var: str, type: str, value: float):
        '''
        var: ["x", "y", "theta", "speed", "rudder"]
        type: ["mult", "offset"]
        '''
        key = f"{var}_{type}"
        if type == "offset":
            value = value * factors[var]
        self.table[key] = value

    def get_raw(self, var: str, type: str):
        key = f"{var}_{type}"
        return self.table[key]

    def get_readable(self, var: str, type: str):
        key = f"{var}_{type}"
        value = self.table[key]
        if type == "offset":
            value = value / factors[var]
        return value