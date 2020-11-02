import numpy as np

from .alarms import message
from .colors import colored
from .consts import COL_NOT_CONNECTED, COL_SUCCESS, COL_ALARM
from .consts import MSG_NOT_CONNECTED, MSG_SUCCESS


class DataGetter:

    def __init__(self, timeout, quiet):
        self.timeout = timeout
        self.quiet = quiet


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

        if not self.quiet:
            msg = colored(col, msg)
            print(pv.pvname, msg)

        return data



class DataPutter:

    def __init__(self, timeout, quiet):
        self.timeout = timeout
        self.quiet = quiet


    def __call__(self, pv, value):
        connected = pv.wait_for_connection(self.timeout)

        if not connected:
            status = False
            msg = MSG_NOT_CONNECTED
            col = COL_NOT_CONNECTED
        else:
            status = pv_put_waiting(pv, value, self.timeout) #TODO: use same timeout twice?
            msg = f"put {value} "
            if status:
                msg += "successful"
                col = COL_SUCCESS
            else:
                msg += "timed out"
                col = COL_ALARM

        if not self.quiet:
            msg = colored(col, msg)
            print(pv.pvname, msg)

        return status



def pv_put_waiting(pv, value, timeout):
    """wraps waiting PV.put and returns completion status"""
    pv.put(value, wait=True, timeout=timeout, use_complete=True)
    return pv.put_complete



