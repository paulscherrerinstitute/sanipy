#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(title="command", description="valid commands", dest="command", help="commands")

parser_check = subparsers.add_parser("check", help="check!", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser_check.add_argument("filename", help="name of input channel-list file")
parser_check.add_argument("-o", "--output", help="output CSV file", default=None)
parser_check.add_argument("-s", "--silent", help="do not show each channel's answer", action="store_true")
parser_check.add_argument("-t", "--timeout", help="connection timeout in seconds", type=float, default=1)

parser_compare = subparsers.add_parser("compare", help="compare!")
parser_compare.add_argument("filenames", metavar="filename", nargs=2, help="name of input CSV file, two are needed")
parser_compare.add_argument("-v", "--ignore-values", help="do not check values", action="store_true")

clargs = parser.parse_args()

if not clargs.command:
    parser.print_help()
    raise SystemExit



from datetime import datetime
import epics
import numpy as np
import pandas as pd
from colorama import Fore, Style

from alarms import message
from config import load
from execute import parallel
#from execute import serial as parallel


MSG_NOT_CONNECTED = "did not connect"
MSG_SUCCESS = "OK"

SYM_GOOD = "👍"
SYM_BAD = "💔"

COL_NOT_CONNECTED = Fore.RED
COL_SUCCESS = Fore.GREEN
COL_ALARM = Fore.YELLOW

#COL_COMP_LEFT = Fore.MAGENTA
#COL_COMP_LEFT = Fore.CYAN

COL_RESET = Fore.RESET



def get_data(pv):
    connected = pv.wait_for_connection(clargs.timeout)

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

    if not clargs.silent:
        msg = colored(col, msg)
        print(pv.pvname, msg)
    return data


def colored(color, msg):
    return color + str(msg) + COL_RESET



def run_check():
    filename = clargs.filename
    chans = load(filename)
    pvs = (epics.PV(ch) for ch in chans) # putting PV constructors into ThreadPoolExecutor has weird effects
    data = parallel(get_data, pvs, chans)

    df = pd.DataFrame(data).T
    df = df.infer_objects() #TODO: why is this needed?
#    print(df)
#    print(df.dtypes)

    connection_state = df["connected"]
    if connection_state.all():
        print(f"{SYM_GOOD} all connections OK")
    else:
        total = connection_state.index
        good = total[connection_state]

        ntotal = len(total)
        ngood = len(good)

        print(f"{SYM_BAD} only {ngood}/{ntotal} connections OK")


    output = clargs.output
    if not output:
        return

    timestamp = datetime.now()
    meta = f"{filename} / {timestamp}"
    store_csv(df, output, meta)


def run_compare():
    fn1, fn2 = clargs.filenames
    df1 = load_csv(fn1)
    df2 = load_csv(fn2)

    if clargs.ignore_values:
        df1.drop("value", axis="columns", inplace=True)
        df2.drop("value", axis="columns", inplace=True)

    def report_diff(x):
        return "" if equal(*x) else " {} | {}".format(*x)

    def equal(a, b):
        return a == b or (np.isnan(a) and np.isnan(b))

    df = pd.concat((df1, df2)) 
    changes = df.groupby(level=0).agg(report_diff)

    changes.replace("", np.nan, inplace=True)
    changes.dropna(axis="columns", how="all", inplace=True)
    changes.dropna(axis="index",   how="all", inplace=True)
    changes.replace(np.nan, "", inplace=True)

    if changes.empty:
        print(f'{SYM_GOOD} "{fn1}" and "{fn2}" are identical')
    else:
        print(f'{SYM_BAD} "{fn1}" and "{fn2}" differ:')
        print(changes)



def store_csv(df, fname, meta):
    fname = fix_file_ext(fname, "csv")
    with open(fname, "w") as f:
        f.write(f"# {meta}\n")
        df.to_csv(f)

def load_csv(fname):
    fname = fix_file_ext(fname, "csv")
    return pd.read_csv(fname, index_col=0, comment="#", float_precision="high")    



def fix_file_ext(fn, ext):
    if not ext.startswith("."):
        ext = "." + ext
    if not fn.endswith(ext):
        fn += ext
    return fn


if __name__ == "__main__":
    if clargs.command == "check":
        run_check()
    elif clargs.command == "compare":
        run_compare()



