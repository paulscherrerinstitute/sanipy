import pandas as pd


def load_csv(fname):
    fname = fix_file_ext(fname, "csv")
    return pd.read_csv(fname, index_col=0, comment="#", float_precision="high")    

def store_csv(df, fname, meta=None):
    fname = fix_file_ext(fname, "csv")
    with open(fname, "w") as f:
        if meta is not None:
            f.write(f"# {meta}\n")
        df.to_csv(f)

def fix_file_ext(fn, ext):
    if not ext.startswith("."):
        ext = "." + ext
    if not fn.endswith(ext):
        fn += ext
    return fn


def load_config(fname):
    chans = set()
    for line in read_lines(fname):
        line = remove_comments(line).strip()
        if not line:
            continue
        chans.add(line)
    return sorted(chans)

def read_lines(fname):
    with open(fname, "r") as f:
        yield from f

def remove_comments(line, comment_char="#"):
    return line.split(comment_char)[0]



