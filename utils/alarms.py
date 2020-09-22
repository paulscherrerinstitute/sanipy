
STATUS = {
    0:  "no alarm",
    1:  "read",
    2:  "write",
    3:  "hihi",
    4:  "high",
    5:  "lolo",
    6:  "low",
    7:  "state",
    8:  "cos",
    9:  "comm",
    10: "timeout",
    11: "hw limit",
    12: "calc",
    13: "scan",
    14: "link",
    15: "soft",
    16: "bad sub",
    17: "udf",
    18: "disable",
    19: "simm",
    20: "read access",
    21: "write access"
}

SEVERITY = {
    0: "no alarm",
    1: "minor",
    2: "major",
    3: "invalid"
}



def message(status_code, severity_code):
    status = STATUS.get(status_code, "unknown")
    if status_code == severity_code == 0:
        return status
    severity = SEVERITY.get(severity_code, "unknown")
    return f"{status} ({severity})"



