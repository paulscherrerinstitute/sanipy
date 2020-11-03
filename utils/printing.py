from .consts import SYM_GOOD, SYM_BAD


def print_good(*args, **kwargs):
    return print(SYM_GOOD, *args, **kwargs)

def print_bad(*args, **kwargs):
    return print(SYM_BAD, *args, **kwargs)


def itemize(iterable, bullet="•"):
    if not bullet.endswith(" "):
        bullet += " "
    lines = (bullet + str(i) for i in iterable)
    return "\n".join(lines)



