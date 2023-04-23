def tuple_to_string(tup):
    from functools import reduce
    from operator import add
    return reduce(add, tup)