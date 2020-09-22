
def load(fname):
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



