import math


def is_num(x, include_str=True):
    if include_str and isinstance(x, str):
        return x.isnumeric()
    return isinstance(x, int) or isinstance(x, float)
