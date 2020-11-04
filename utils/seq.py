import numpy as np


def count_true(seq):
    bools = np.asanyarray(seq, dtype=bool)
    return np.count_nonzero(bools)


def is_empty(seq):
    return len(seq) == 0



