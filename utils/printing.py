from .consts import SYM_NOTHING, SYM_GOOD, SYM_BAD
from .seq import is_empty


def print_outcome(state, units):
    if is_empty(state):
        print_nothing("nothing to do")
    elif all(state):
        print_good(f"all {units}")
    else:
        ntotal = len(state)
        ngood = count_true(state)
        print_bad(f"only {ngood}/{ntotal} {units}")

def print_nothing(*args, **kwargs):
    return print(SYM_NOTHING, *args, **kwargs)

def print_good(*args, **kwargs):
    return print(SYM_GOOD, *args, **kwargs)

def print_bad(*args, **kwargs):
    return print(SYM_BAD, *args, **kwargs)


def itemize(iterable, bullet="•"):
    if not bullet.endswith(" "):
        bullet += " "
    lines = (bullet + str(i) for i in iterable)
    return "\n".join(lines)



