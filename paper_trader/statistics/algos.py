from collections.abc import Iterable


def mean(iter: Iterable):
    s = None
    count = 0
    for x in iter:
        if s is None:
            s = x
        else:
            s = s + x
        count += 1

    if s is None:
        return None
    return s / count
