# -*- coding: utf-8 -*-

from time import time

from functools import wraps
def timeit(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print('%2.4f sec used by func:%r args:[%r, %r]' % \
          (te-ts, f.__name__, args, kw))
        return result
    return wrap