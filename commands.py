from datetime import datetime
import numpy as np
import pandas as pd
import epics

from utils.df import drop_col, compare_dfs, count_true
from utils.epics import DataGetter, DataPutter
from utils.execute import parallel, serial
from utils.fileio import load_config, load_csv, store_csv
from utils.printing import print_good, print_bad, itemize
from utils.seq import is_empty


def run(clargs):
    commands = {
        "check": run_check,
        "compare": run_compare,
        "goto": run_goto
    }
    commands[clargs.command](clargs)


def run_check(clargs):
    filename = clargs.filename
    chans = load_config(filename)
    pvs = (epics.PV(ch) for ch in chans) # putting PV constructors into ThreadPoolExecutor has weird effects

    get_data = DataGetter(clargs.timeout, clargs.quiet)
    run = serial if clargs.serial else parallel
    data = run(get_data, pvs, names=chans)

    df = pd.DataFrame(data).T
    df = df.infer_objects() #TODO: why is this needed?
#    print(df)
#    print(df.dtypes)

    connected = df["connected"]
    if connected.all():
        print_good("all connections OK")
    else:
        ntotal = len(connected)
        ngood = count_true(connected)
        print_bad(f"only {ngood}/{ntotal} connections OK")

    output = clargs.output
    if not output:
        return

    timestamp = datetime.now()
    meta = f"{filename} / {timestamp}"
    store_csv(df, output, meta)


def run_compare(clargs):
    fn1, fn2 = clargs.filenames
    df1 = load_csv(fn1)
    df2 = load_csv(fn2)

    if clargs.ignore_values:
        drop_col(df1, "value")
        drop_col(df2, "value")

    diff = compare_dfs(df1, df2)
    if diff.empty:
        print_good(f'"{fn1}" and "{fn2}" are identical')
    else:
        print_bad(f'"{fn1}" and "{fn2}" differ:')
        print(diff)


def run_goto(clargs):
    fn = clargs.filename
    df = load_csv(fn)

    if clargs.ignore_alarm:
        which = (df["status"] == 0) & (df["severity"] == 0)
        if not clargs.quiet:
            all_names = df.index
            ignored = all_names[~which]
            if not is_empty(ignored):
                print("ignored due to alarm state:")
                print(itemize(ignored))
                print()
        df = df.loc[which]

    df = df["value"]

    if not clargs.quiet:
        which = df.notnull()
        all_names = df.index
        ignored = all_names[~which]
        if not is_empty(ignored):
            print("ignored due to NaN value:")
            print(itemize(ignored))
            print()
    df.dropna(inplace=True) #TODO: can NaN be a valid value?

    values = df.values
    chans = df.index
    pvs = (epics.PV(ch) for ch in chans)

    put_data = DataPutter(clargs.timeout, clargs.quiet)
    run = serial if clargs.serial else parallel
    status = run(put_data, pvs, values)

    status = np.array(status)
    if status.all():
        print_good("all puts successful")
    else:
        ntotal = len(status)
        ngood = count_true(status)
        print_bad(f"only {ngood}/{ntotal} puts successful")



