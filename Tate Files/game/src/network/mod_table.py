table = {}

for var in ["x", "y", "theta", "speed", "rudder"]:
    type = "mult"
    key = f"{var}_{type}"
    table[key] = 1.0
    type = "offset"
    key = f"{var}_{type}"
    table[key] = 0.0

factors = {}

factors["x"] = 100.0
factors["y"] = 100.0
factors["theta"] = 1000
factors["speed"] = 4095.0 / 5.0
factors["rudder"] = 4095.0 / 5.0

def reset_table():
    for var in ["x", "y", "theta", "speed", "rudder"]:
        type = "mult"
        key = f"{var}_{type}"
        table[key] = 1.0
        type = "offset"
        key = f"{var}_{type}"
        table[key] = 0.0

def set(var: str, type: str, value: float):
    key = f"{var}_{type}"
    if type == "offset":
        value = value * factors[var]
    table[key] = value