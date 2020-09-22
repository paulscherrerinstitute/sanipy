#!/usr/bin/env python


import argparse

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("filename")

#parser.add_argument("-v", "--verbose", action="count", default=0)
parser.add_argument("-s", "--show", action="store_true")
parser.add_argument("-t", "--timeout", type=float, default=2)

clargs = parser.parse_args()








import enum

import epics
import pandas as pd

from pvcollection import PVCollection
from alarms import message
from config import load
from execute import parallel












MSG_NOT_CONNECTED = "did not connect"
MSG_SUCCESS = "OK"



def v1a():
    cs = load(clargs.filename)
    pvs = [epics.PV(c) for c in cs]
    for pv in pvs:
        c = pv.pvname
        connected = pv.wait_for_connection(clargs.timeout)
        if not connected:
            msg = MSG_NOT_CONNECTED
        elif pv.status != 0 or pv.severity != 0:
            msg = message(pv.status, pv.severity)
        else:
            if not clargs.show:
                continue
            msg = MSG_SUCCESS
#        print(c, msg)


def v1b():
    chans = load(clargs.filename)
    pvs = [epics.PV(ch) for ch in chans]
    connected = parallel(lambda pv: pv.wait_for_connection(clargs.timeout), pvs)

    for ch, pv, con in zip(chans, pvs, connected):
        if not con:
            msg = MSG_NOT_CONNECTED
        elif pv.status != 0 or pv.severity != 0:
            msg = message(pv.status, pv.severity)
        else:
            if not clargs.show:
                continue
            msg = MSG_SUCCESS
#        print(ch, msg)





def v1c():
    chans = load(clargs.filename)
    length = maxstrlen(chans)
    pvs = [epics.PV(ch) for ch in chans]
    connected = parallel(lambda pv: pv.wait_for_connection(clargs.timeout), pvs)

    data = {}
    for ch, pv, con in zip(chans, pvs, connected):
        if not con:
            status = severity = -1
            value = None
            msg = MSG_NOT_CONNECTED
        else:
            status = pv.status
            severity = pv.severity
            if status == 0 and severity == 0:
                if not clargs.show:
                    continue
                msg = MSG_SUCCESS
            else:
                msg = message(status, severity)
            value = pv.value

#        print(ch.ljust(length), msg)
        data[ch] = (con, status, severity, value)

    columns = ("connected", "status", "severity", "value")
    df = pd.DataFrame.from_dict(data, columns=columns, orient="index")
#    print()
#    print(df)
#    print()
#    print(df.dtypes)



def maxstrlen(seq):
    return max(strlen(i) for i in seq)

def strlen(val):
    return len(str(val))



#cs = load(clargs.filename)
#pvs = [epics.PV(c) for c in cs]
#data = []
#for pv in pvs:
#    c = pv.pvname
#    connected = pv.wait_for_connection(clargs.timeout)

#    if not connected:
#        print(c, "didn't connect")
#        data.append((connected, -1, -1, None))
#        continue
#    if pv.status != 0 or pv.severity != 0:
#        print(c, message(pv.status, pv.severity))

#    data.append((connected, pv.status, pv.severity, pv.value))

#df = pd.DataFrame(data, index=cs, columns=["connected", "status", "severity", "value"])

#print(df)
#print(df.dtypes)







def v2a():
    pvc = PVCollection.from_file(clargs.filename)

    data = {
        "connected": pvc.connected(),
        "status":    pvc.status(),
        "severity":  pvc.severity(),
        "value":     pvc.value()
    }

    df = pd.DataFrame(data, index=pvc.chans)

#    print(df)
#    print(df.dtypes)








def get_data(pv):
    connected = pv.wait_for_connection(clargs.timeout)

    if not connected:
        value = None
        status = severity = -1
        msg = MSG_NOT_CONNECTED
    else:
        value = pv.value #TODO: not needed if shot not ok
        status = pv.status
        severity = pv.severity
        if status == 0 and severity == 0:
            msg = MSG_SUCCESS
        else:
            msg = message(status, severity)

    data = {
        "connected": connected,
        "value": value,
        "status": status,
        "severity": severity
    }

    if clargs.show:
        print(pv.pvname, msg)
    return data#, msg





def v3():
    chans = load(clargs.filename)
    pvs = (epics.PV(ch) for ch in chans) # putting PV constructors into threads has weird effects
    data = parallel(get_data, pvs, chans)
    df = pd.DataFrame(data).T
    return df








res = v3()
print(res)
#for m in res:
#    print(m)















