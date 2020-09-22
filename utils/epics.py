import numpy as np

from .alarms import message
from .colors import colored
from .consts import COL_NOT_CONNECTED, COL_SUCCESS, COL_ALARM
from .consts import MSG_NOT_CONNECTED, MSG_SUCCESS


class DataGetter:

    def __init__(self, timeout, silent):
        self.timeout = timeout
        self.silent = silent

    def __call__(self, pv):
        connected = pv.wait_for_connection(self.timeout)

        if not connected:
            value = np.nan
            status = severity = -1
            msg = MSG_NOT_CONNECTED
            col = COL_NOT_CONNECTED
        else:
            value = pv.value
            status = pv.status
            severity = pv.severity
            if status == 0 and severity == 0:
                msg = MSG_SUCCESS
                col = COL_SUCCESS
            else:
                msg = message(status, severity)
                col = COL_ALARM

        data = {
            "connected": connected,
            "value": value,
            "status": status,
            "severity": severity
        }

        if not self.silent:
            msg = colored(col, msg)
            print(pv.pvname, msg)
        return data



