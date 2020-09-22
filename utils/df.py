import numpy as np
import pandas as pd


def compare_dfs(df1, df2):
    df = pd.concat((df1, df2)) 
    diff = df.groupby(level=0).agg(report_diff)
    drop_empty(diff)
    return diff

def report_diff(x):
    return "" if equal(*x) else " {} | {}".format(*x) #TODO: color left and right differently

def equal(a, b):
    return a == b or (np.isnan(a) and np.isnan(b))


def drop_empty(df):
    replace_empty_nan(df)
    drop_nan_cols(df)
    drop_nan_rows(df)
    replace_nan_empty(df)

def replace_empty_nan(df):
    df.replace("", np.nan, inplace=True)

def replace_nan_empty(df):
    df.replace(np.nan, "", inplace=True)

def drop_nan_cols(df):
    df.dropna(axis="columns", how="all", inplace=True)

def drop_nan_rows(df):
    df.dropna(axis="index", how="all", inplace=True)


def drop_col(df, name):
    df.drop(name, axis="columns", inplace=True)


def count_true(bdf):
    good = bdf[bdf]
    ngood = len(good)
    return ngood



